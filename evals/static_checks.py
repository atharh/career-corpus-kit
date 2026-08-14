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
USER_VISIBLE = (
    "skills/",
    "README.md",
    "PRIVACY.md",
    "examples/",
    ".claude-plugin/marketplace.json",
)

# Docs at the repo root that skills link to and users read.
ROOT_DOCS = ("README.md", "PRIVACY.md")

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


def citing_files_outside_skills() -> list[Path]:
    """The files outside `skills/` that cite skill rules.

    Two places. `examples/` documents the rules to a reader, and the eval case
    tables in `evals/cases/` name the rule each assertion is testing. Both cite
    rules from about as far away as it is possible to get, and neither was
    scanned until a renumbering made the gap obvious.
    """
    return sorted([*(ROOT / "examples").rglob("*.md"), *(ROOT / "evals" / "cases").glob("*.json")])


def check_numbered_citations(r: Report) -> None:
    """A rule is addressed by its id. There are no numbers left to cite.

    Rule lists carry no numbers, so "rule 9" resolves against nothing at all —
    and the failure it used to cause was silent: a within-file citation pointed
    at whatever rule currently held that position, so inserting one rule above it
    retargeted the citation with every check still green. One addressing scheme
    removes the class.

    Scanned wherever a rule can be cited: `skills/`, the docs and fixtures under
    `examples/`, and the eval case tables. Fixture files are exempt, and the
    `FICTIONAL` banner is the line: a file under `examples/` that carries one is
    an invented artifact whose prose is its own rather than documentation of this
    kit — a story that mentions rule 4 of some invented policy is not making a
    claim about `skills/`. `check_example_corpus` requires that banner on every
    fixture file, so the two checks meet with nothing uncovered between them.

    Plain-numbered lists stay legal, and so do references to them: their numbers
    are execution order, not addresses — "step 2" of a workflow means the second
    thing you do, and it stays true however the rule lists are edited.
    """
    for path in [*sorted((ROOT / "skills").rglob("*.md")), *citing_files_outside_skills()]:
        text = path.read_text()
        if path.suffix == ".md" and FICTIONAL in text:
            continue
        hits = [m.group(0) for m in re.finditer(r"\b(rules?|playbooks?) (\d+[a-z]?)\b", text, re.I)]
        r.check(
            f"{path.relative_to(ROOT)} — cites rules by id, not by number",
            not hits,
            f"found {hits} — cite by name and id instead, `[LIKE-THIS]`; see check_rule_ids",
        )


RULE_ID = re.compile(r"`\[([A-Z][A-Z0-9-]+)\]`")

# A rule heading, matched against a whole paragraph and anchored to its start,
# so a bold phrase mid-sentence can never read as one — `**pristine**` opens a
# line whenever the paragraph happens to wrap that way, and opening a paragraph
# is the bar. The heading may carry single `*` emphasis and may wrap over lines,
# but never over a blank one.
RULE_HEAD = re.compile(r"\A\*\*((?:(?!\n\n)[^*]|\*(?!\*))+?)\*\*")

# Sections whose paragraphs are rules. Everything else in a skill is prose.
RULE_SECTION = re.compile(r"hard rules|rules specific to|playbook", re.I)


def rule_paragraphs(text: str) -> list[tuple[int, str, str]]:
    """Every rule in the file: (offset, section heading, paragraph).

    A **rule** is a paragraph inside a rule section — `## Hard rules`, `## Rules
    specific to …`, `## The question playbook` — that opens with a bold heading
    at the left margin. That is the whole detection rule, and it is what makes
    "every rule carries an id" checkable now that the numbers are gone.

    One exception: a lettered sub-case (`**a. …**`) is a branch of the rule above
    it rather than a rule of its own, and shares that rule's id. Bullets,
    blockquotes and indented prose are not paragraphs at the left margin, so they
    never qualify either.
    """
    out: list[tuple[int, str, str]] = []
    parts = re.split(r"^(#{2,} .*)$", text, flags=re.M)
    pos = len(parts[0])
    for i in range(1, len(parts), 2):
        head, body = parts[i], parts[i + 1]
        pos += len(head)
        if RULE_SECTION.search(head):
            at = pos
            for para in re.split(r"(\n[ \t]*\n)", body):
                if not para.startswith("\n"):
                    m = RULE_HEAD.match(para)
                    if m and not re.match(r"[a-z]\. ", m.group(1)):
                        out.append((at, head.strip(), para))
                at += len(para)
        pos += len(body)
    return out


def check_rule_ids(r: Report) -> None:
    """Every rule carries a stable id, defined once, and every citation resolves.

    Three bars, and they compose into one addressing scheme:

    - **Coverage.** Every rule — see `rule_paragraphs` for what counts as one —
      is tagged, whether or not anything cites it yet. Tagging only the cited
      ones means adding a citation edits the file being cited, which is how a
      rule ends up cited by position instead.
    - **Uniqueness.** An id is defined once kit-wide, so a citation is never
      ambiguous about which rule it names.
    - **Resolution.** Every `[ID]` written anywhere in `skills/`, in `examples/`,
      or in the eval case tables names a rule that still exists. Delete a rule
      and its citations fail loudly instead of pointing at nothing.

    A definition is the id tag immediately following a rule's bold heading. It is
    positional on purpose: an id written mid-sentence is a citation, and the two
    must not be confusable, or a citation of a deleted rule would define it.
    """
    defs: dict[str, tuple[Path, str]] = {}
    spans: dict[Path, list[tuple[int, int]]] = {}
    dupes: list[str] = []
    for path in sorted((ROOT / "skills").rglob("*.md")):
        rel = path.relative_to(ROOT)
        for at, _section, para in rule_paragraphs(path.read_text()):
            m = RULE_HEAD.match(para)
            assert m is not None
            label = squash(m.group(1))[:56]
            tag = re.match(r"\s*`\[([A-Z][A-Z0-9-]+)\]`", para[m.end() :])
            if not r.check(
                f"{rel} — rule {label!r} carries an id",
                tag is not None,
                "every rule in a rule list is tagged `[LIKE-THIS]`, cited or not",
            ):
                continue
            assert tag is not None
            rid = tag.group(1)
            if rid in defs:
                dupes.append(rid)
            defs[rid] = (path, label)
            spans.setdefault(path, []).append(
                (at + m.end() + tag.start(), at + m.end() + tag.end())
            )

    r.check(
        "rule ids are unique kit-wide",
        not dupes,
        f"defined more than once: {sorted(set(dupes))}",
    )

    for rid, (path, label) in sorted(defs.items()):
        r.check(
            f"rule id {rid} — defined once, at {path.relative_to(ROOT)} {label!r}",
            rid not in dupes,
            "a second definition makes every citation ambiguous",
        )

    # Citations: every other occurrence of an id, anywhere in the kit.
    for path in [*sorted((ROOT / "skills").rglob("*.md")), *citing_files_outside_skills()]:
        rel = path.relative_to(ROOT)
        text = path.read_text()
        defined = spans.get(path, [])
        for m in RULE_ID.finditer(text):
            if any(a <= m.start() < b for a, b in defined):
                continue
            rid = m.group(1)
            r.check(
                f"{rel} — rule id {rid} resolves",
                rid in defs,
                f"known: {sorted(defs)}",
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
    # A missing root doc is reported by check_root_docs, not crashed on here.
    roots = [
        *(ROOT / "skills").rglob("*.md"),
        *(ROOT / "examples").rglob("*.md"),
        *(p for d in ROOT_DOCS if (p := ROOT / d).is_file()),
    ]
    for path in sorted(roots):
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


def check_no_gendered_pronouns(r: Report) -> None:
    """Skills address a generic user as "they". A "he" or "she" is leaked autobiography.

    Every skill tells the model to keep the user's corrections in their private
    `corpus/LESSONS.md` and never in the kit. The way that rule gets broken is a
    session writing up its own incident as method, and incident prose carries the
    pronoun of the person it happened to. Nothing else here catches a leak, because
    the numbers and vocabulary it also drags in are impossible to match generically.
    This one marker is cheap and it is present nearly every time.
    """
    banned = re.compile(r"\b(he|him|his|she|her|hers)\b", re.I)
    for path in sorted((ROOT / "skills").rglob("*.md")):
        rel = path.relative_to(ROOT)
        hits = sorted({m.group(0).lower() for m in banned.finditer(path.read_text())})
        r.check(
            f"{rel} — no gendered singular pronouns",
            not hits,
            f"found {hits} — say 'they'; if it is a real incident, it belongs in corpus/LESSONS.md",
        )


def check_root_docs(r: Report) -> None:
    """The docs skills point users at must exist.

    `bootstrap` and `apply` both send the user to PRIVACY.md. A dead pointer in
    a prompt is worse than no pointer: the model cites a file that isn't there.
    """
    for d in ROOT_DOCS:
        r.check(f"{d} exists", (ROOT / d).is_file(), "referenced by skills and USER_VISIBLE")


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

        # `[INBOX-QUEUE]` in the interview skill: folder location is a truth
        # claim. Fabricated career content announces itself on every file.
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


def check_capability_pointers(r: Report) -> None:
    """Every `capabilities/<x>.md` reference in the example corpus resolves or is a
    marked forward pointer.

    `[CAPABILITY-HARVEST]` makes a dangling capability reference legal on purpose: a
    story session citing the would-be file marks a file worth opening. What keeps that
    from swallowing typos is the marking — an unresolved reference whose paragraph never
    says "forward pointer" is indistinguishable from a broken link, and fails here.
    """
    corpus = ROOT / "examples" / "corpus"
    ref = re.compile(r"[\w./-]*\bcapabilities/[a-z0-9-]+\.md")
    for path in sorted(corpus.rglob("*.md")):
        rel = path.relative_to(ROOT)
        for para in re.split(r"\n[ \t]*\n", path.read_text()):
            for m in ref.finditer(para):
                if (path.parent / m.group(0)).exists():
                    r.check(f"{rel} — capability reference {m.group(0)} resolves", True)
                    continue
                r.check(
                    f"{rel} — capability reference {m.group(0)} is a marked forward pointer",
                    "forward pointer" in para.lower(),
                    "unresolved and unmarked — a typo, or a forward pointer missing its marking",
                )


def squash(text: str) -> str:
    """Collapse whitespace so a hard-wrapped sentence matches its one-line form.

    The skills are wrapped at ~96 columns, so almost every invariant sentence
    spans a line break. Rewrapping a paragraph is not drift; rewording it is.
    """
    return re.sub(r"\s+", " ", text)


def check_policy_blocks(r: Report, names: list[str]) -> None:
    """Policy stated in more than one skill must be stated identically.

    A skill loads its own SKILL.md and nothing else, so shared policy is
    repeated on purpose — extracting it into a file the model may not read
    would turn a rule into a hope. What repetition costs is drift, and drift
    has already shipped: `apply` and `render` both stated the claim-sourcing
    rule, differently enough that render's copy barred reading the folder its
    own workflow was told to read.

    Table: evals/cases/policy-blocks.json.
    """
    path = ROOT / "evals" / "cases" / "policy-blocks.json"
    try:
        table = json.loads(path.read_text())
    except Exception as e:  # noqa: BLE001
        r.fail("policy-blocks.json parses", str(e))
        return

    skills = set(names)

    for block in table.get("blocks", []):
        bid = block["id"]
        required = block.get("required_in", [])
        exempt = block.get("exempt", {})

        # Every skill is either required to carry the block or exempt with a
        # reason. This is the half that catches a *new* skill: add one and it
        # can't quietly opt out of policy it should be repeating.
        classified = set(required) | set(exempt)
        r.check(
            f"policy {bid} — every skill is classified",
            classified == skills,
            f"unclassified: {sorted(skills - classified)}; unknown: {sorted(classified - skills)}",
        )
        r.check(
            f"policy {bid} — canonical skill carries it",
            block.get("canonical") in required,
            f"canonical={block.get('canonical')!r} not in required_in={required}",
        )
        r.check(
            f"policy {bid} — exempt skills give a reason",
            all(v.strip() for v in exempt.values()),
            "an empty reason is an undocumented exemption",
        )

        for skill in required:
            if skill not in skills:
                continue
            body = squash((ROOT / "skills" / skill / "SKILL.md").read_text())
            for inv in block["invariants"]:
                r.check(
                    f"policy {bid} — {skill} states {inv[:48]!r}…",
                    squash(inv) in body,
                    f"absent or reworded in skills/{skill}/SKILL.md",
                )

    # Wording that was wrong and got fixed. Left unguarded, the old phrasing
    # comes back the next time someone tightens a sentence from memory.
    targets = [*(ROOT / "skills").rglob("*.md"), ROOT / "README.md"]
    for entry in table.get("superseded", []):
        needle = squash(entry["text"])
        hits = [str(p.relative_to(ROOT)) for p in targets if needle in squash(p.read_text())]
        r.check(
            f"superseded wording is gone: {entry['text'][:48]!r}…",
            not hits,
            f"found in {hits} — {entry['why']}",
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
    check_numbered_citations(r)
    check_rule_ids(r)
    check_skill_cross_references(r, names)
    check_relative_links(r)
    check_no_gendered_pronouns(r)
    check_root_docs(r)
    check_readme_lists_every_skill(r, names)
    check_policy_blocks(r, names)
    check_example_corpus(r)
    check_capability_pointers(r)

    base = args.base_ref or os.environ.get("EVAL_BASE_REF")
    if base and plugin:
        check_version_bump(r, base, plugin)

    return r.summary()


if __name__ == "__main__":
    sys.exit(main())
