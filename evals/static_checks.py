#!/usr/bin/env python3
"""Tier 1 — static checks. No model, no network, no dependencies.

These test the *kit*, not the model: manifest validity, skill frontmatter,
cross-references that silently rot when a file is edited, and the integrity of
the example corpus the trip-wires assert against.

Run:  python3 evals/static_checks.py [--base-ref <git ref>]

--base-ref enables the version-bump check by diffing against that ref. Omit it
locally; CI passes the merge base.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Paths whose contents users actually load. Changing one requires a version bump;
# see CLAUDE.md. Everything else (CI, .gitignore, this directory) is exempt.
USER_VISIBLE = ("skills/", "README.md", "examples/", ".claude-plugin/marketplace.json")

FICTIONAL = "FICTIONAL"


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks = 0

    def check(self, name: str, ok: bool, detail: str = "") -> bool:
        self.checks += 1
        if not ok:
            self.failures.append(f"{name}: {detail}" if detail else name)
        return ok

    def fail(self, name: str, detail: str) -> None:
        self.check(name, False, detail)

    def summary(self) -> int:
        print(f"\n{self.checks} checks run.")
        if not self.failures:
            print("static checks: PASS")
            return 0
        print(f"static checks: FAIL ({len(self.failures)})\n")
        for f in self.failures:
            print(f"  ✗ {f}")
        return 1


def frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def scalar(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:[ \t]*(.+)$", fm, re.M)
    return m.group(1).strip() if m else None


def skill_dirs() -> list[Path]:
    return sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file())


# --------------------------------------------------------------------------- #


def check_manifests(r: Report) -> dict:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    market_path = ROOT / ".claude-plugin" / "marketplace.json"
    plugin: dict = {}

    try:
        plugin = json.loads(plugin_path.read_text())
        r.check("plugin.json parses", True)
    except Exception as e:  # noqa: BLE001
        r.fail("plugin.json parses", str(e))
        return {}

    for key in ("name", "version", "description"):
        r.check(f"plugin.json has {key}", key in plugin, "missing")

    version = plugin.get("version", "")
    r.check(
        "plugin.json version is semver",
        bool(re.fullmatch(r"\d+\.\d+\.\d+", version)),
        f"got {version!r}",
    )

    try:
        market = json.loads(market_path.read_text())
        r.check("marketplace.json parses", True)
    except Exception as e:  # noqa: BLE001
        r.fail("marketplace.json parses", str(e))
        return plugin

    names = [p.get("name") for p in market.get("plugins", [])]
    r.check(
        "marketplace.json references the plugin by name",
        plugin.get("name") in names,
        f"plugin.json name {plugin.get('name')!r} not in {names}",
    )
    return plugin


def check_skill_frontmatter(r: Report) -> list[str]:
    names: list[str] = []
    for d in skill_dirs():
        path = d / "SKILL.md"
        rel = path.relative_to(ROOT)
        fm = frontmatter(path.read_text())
        if not r.check(f"{rel} has frontmatter", fm is not None, "no --- block"):
            continue
        assert fm is not None

        name = scalar(fm, "name")
        desc = scalar(fm, "description")

        r.check(f"{rel} name matches directory", name == d.name, f"name={name!r} dir={d.name!r}")
        r.check(f"{rel} has a description", bool(desc), "missing or empty")
        # A description is how the model decides to load the skill. A short one
        # does not describe when to use it, and the skill goes uninvoked.
        if desc:
            r.check(
                f"{rel} description is substantive",
                len(desc) >= 80,
                f"{len(desc)} chars, want >= 80",
            )
        if name:
            names.append(name)

    r.check("skill names are unique", len(names) == len(set(names)), f"{names}")
    return names


def numbered_sections(text: str) -> dict[str, list[int]]:
    """Map section heading -> the **N.** list numbers found under it."""
    out: dict[str, list[int]] = {}
    parts = re.split(r"^(#{2,} .*)$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        head, body = parts[i].strip(), parts[i + 1]
        nums = [int(m) for m in re.findall(r"^\*\*(\d+)\. ", body, re.M)]
        if nums:
            out[head] = nums
    return out


def check_numbered_lists(r: Report) -> dict[str, set[int]]:
    """Numbered rule lists must run 1..N with no gaps or repeats.

    Editing a rule list by hand is how you get two rule 6s, and every later
    cross-reference then points at the wrong rule.
    """
    per_skill: dict[str, set[int]] = {}
    for d in skill_dirs():
        text = (d / "SKILL.md").read_text()
        rel = (d / "SKILL.md").relative_to(ROOT)
        seen: set[int] = set()
        for head, nums in numbered_sections(text).items():
            r.check(
                f"{rel} — {head!r} is numbered 1..{len(nums)}",
                nums == list(range(1, len(nums) + 1)),
                f"got {nums}",
            )
            seen.update(nums)
        per_skill[d.name] = seen
    return per_skill


def check_rule_references(r: Report, rules: dict[str, set[int]]) -> None:
    """Every "rule N" mention must point at a rule that exists.

    This is the check that catches a renumbering. `compact` cites the interview
    skill's rule 13; `render` cites its own rule 9. Insert a rule near the top of
    either list and those references silently start pointing somewhere else.
    """
    for path in sorted((ROOT / "skills").rglob("*.md")):
        rel = path.relative_to(ROOT)
        text = path.read_text()
        owner_default = path.parent.name if path.parent.name in rules else None
        for m in re.finditer(r"rule (\d+)", text):
            n = int(m.group(1))
            context = text[max(0, m.start() - 120) : m.start()]
            # "the interview skill's ... (rule 13)" — attribute to the named skill.
            named = [s for s in rules if re.search(rf"\b{s}\b skill", context)]
            owner = named[-1] if named else owner_default
            if owner is None:
                continue
            r.check(
                f"{rel} — 'rule {n}' resolves in {owner}",
                n in rules[owner],
                f"{owner} has rules {sorted(rules[owner])}",
            )


def check_skill_cross_references(r: Report, names: list[str]) -> None:
    """Every /career-corpus:<skill> mentioned anywhere must exist."""
    for path in sorted([*(ROOT / "skills").rglob("*.md"), ROOT / "README.md"]):
        rel = path.relative_to(ROOT)
        for m in re.finditer(r"/career-corpus:([a-z-]+)", path.read_text()):
            r.check(
                f"{rel} — /career-corpus:{m.group(1)} exists",
                m.group(1) in names,
                f"known skills: {names}",
            )


def check_relative_links(r: Report) -> None:
    """Markdown links to files in this repo must resolve."""
    for path in sorted([*(ROOT / "skills").rglob("*.md"), *(ROOT / "examples").rglob("*.md")]):
        rel = path.relative_to(ROOT)
        for m in re.finditer(r"\[[^\]]+\]\(([^)#]+?)(?:#[^)]*)?\)", path.read_text()):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            r.check(
                f"{rel} — link to {target} resolves",
                (path.parent / target).exists(),
                "no such file",
            )


def check_readme_lists_every_skill(r: Report, names: list[str]) -> None:
    readme = (ROOT / "README.md").read_text()
    for n in names:
        r.check(f"README documents /career-corpus:{n}", f"/career-corpus:{n}" in readme, "absent")


def check_example_corpus(r: Report) -> None:
    """The example corpus is documentation *and* the trip-wire fixture.

    If it drifts, the trip-wires below are asserting against something that no
    longer demonstrates the rules they cite.
    """
    example_files = sorted((ROOT / "examples").rglob("*.md"))
    r.check("examples/ is not empty", bool(example_files), "no markdown found")

    for path in example_files:
        rel = path.relative_to(ROOT)
        text = path.read_text()

        # Rule 10 in the interview skill: folder location is a truth claim.
        # Fabricated career content must announce itself on every single file.
        if rel.name != "README.md":
            r.check(f"{rel} carries a FICTIONAL banner", FICTIONAL in text, "no banner")

        fm = frontmatter(text)
        if not fm:
            continue

        # A file that asserts facts must say where they came from.
        if "facts_vetted:" in fm:
            r.check(f"{rel} has sources:", "sources:" in fm, "facts_vetted with no sources block")

        # related: entries are read together on purpose; a dangling one breaks that.
        rel_block = re.search(r"^related:\n((?:[ \t]+-.*\n)+)", fm, re.M)
        if rel_block:
            for line in rel_block.group(1).strip().splitlines():
                target = line.strip().lstrip("- ").split("(")[0].strip()
                r.check(
                    f"{rel} — related: {target} resolves",
                    (path.parent / target).exists(),
                    "no such file",
                )


def check_version_bump(r: Report, base_ref: str, plugin: dict) -> None:
    """User-visible change without a version bump = a silent update.

    Installs are cached per version; an unchanged version overwrites the cache
    dir in place, so users see nothing in /plugin. See CLAUDE.md.
    """
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout

    try:
        changed = [ln for ln in git("diff", "--name-only", f"{base_ref}...HEAD").splitlines() if ln]
        before = git("show", f"{base_ref}:.claude-plugin/plugin.json")
    except subprocess.CalledProcessError as e:
        print(f"  (skipping version-bump check: {e.stderr.strip() or e})")
        return

    touched = [c for c in changed if c.startswith(USER_VISIBLE)]
    if not touched:
        print(f"  (no user-visible changes vs {base_ref}; version bump not required)")
        return

    old = json.loads(before).get("version")
    new = plugin.get("version")
    r.check(
        "version bumped for user-visible change",
        old != new,
        f"{', '.join(touched[:4])}{'…' if len(touched) > 4 else ''} changed but version is still {old}",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-ref", help="git ref to diff against for the version-bump check")
    args = ap.parse_args()

    print(f"static checks — {ROOT}\n")
    r = Report()

    plugin = check_manifests(r)
    names = check_skill_frontmatter(r)
    rules = check_numbered_lists(r)
    check_rule_references(r, rules)
    check_skill_cross_references(r, names)
    check_relative_links(r)
    check_readme_lists_every_skill(r, names)
    check_example_corpus(r)

    base = args.base_ref or os.environ.get("EVAL_BASE_REF")
    if base and plugin:
        check_version_bump(r, base, plugin)

    return r.summary()


if __name__ == "__main__":
    sys.exit(main())
