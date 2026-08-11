#!/usr/bin/env python3
"""Tier 3 — the application fixture. No model, no network, no dependencies.

`apply`, `render` and `prep` write a folder rather than a document, and most of
what they get wrong is a property of the folder: a recruiter's claim promoted
into a résumé, a gap papered over with an adjacent story, a rollup field beside
a log that already holds the answer, a posting quietly summarised into the file
that was supposed to hold it verbatim.

Everything here asserts against examples/applications/<app>/, offline. Cases in
evals/cases/application-lane.json.

Two kinds of assertion, and the split matters:

  conformance  The fixture matches the templates the skills ship. Required
               frontmatter keys are read out of the template files, so the
               templates are load-bearing rather than decorative — grow a slot
               and the fixture fails until it grows one too.

  trip-wire    A claim the fixture tempts an artifact into making. Each one
               asserts the temptation is really present as well as absent from
               the outputs; a trap that gets deleted must not leave an assertion
               passing forever over nothing.

Run:  python3 evals/application_checks.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases" / "application-lane.json"

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOG_LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) — \*\*([a-z-]+)\*\* — \S")
PLACEHOLDER = re.compile(r"^<.*>$")

BEGIN = "<!-- BEGIN VERBATIM POSTING -->"
END = "<!-- END VERBATIM POSTING -->"


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks = 0

    def check(self, name: str, ok: bool, detail: str = "") -> bool:
        self.checks += 1
        if not ok:
            self.failures.append(f"{name}: {detail}" if detail else name)
        return ok

    def summary(self) -> int:
        print(f"\n{self.checks} checks run.")
        if not self.failures:
            print("application fixture: PASS")
            return 0
        print(f"application fixture: FAIL ({len(self.failures)})\n")
        for f in self.failures:
            print(f"  ✗ {f}")
        return 1


# --------------------------------------------------------------------------- #


def frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def top_level_keys(fm: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*):", fm, re.M)]


def required_keys(template_text: str) -> list[str]:
    """Keys the template declares, minus the ones it marks `# optional`."""
    fm = frontmatter(template_text) or ""
    out = []
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", line)
        if not m or "# optional" in line:
            continue
        out.append(m.group(1))
    return out


def scalar(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:[ \t]*(.*)$", fm, re.M)
    return m.group(1).strip() if m else None


def list_block(fm: str, key: str) -> list[str]:
    m = re.search(rf"^{key}:[^\n]*\n((?:[ \t]+-[^\n]*\n?)+)", fm, re.M)
    if not m:
        return []
    return [ln.strip().lstrip("- ").split("#")[0].strip() for ln in m.group(1).splitlines() if ln.strip()]


def section(text: str, heading: str) -> str:
    """The body under a `## heading`, up to the next heading of the same depth."""
    m = re.search(rf"^{re.escape(heading)}[ \t]*$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def scan(text: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if re.search(p, text, re.I)]


# --------------------------------------------------------------------------- #


def check_templates_conform(r: Report, spec: dict, fixture: Path) -> None:
    """Every owned file carries the frontmatter its template declares, and no rollup.

    `apply` rule 6: state that can be recomputed from what is already on disk is
    not stored. A `status:` field beside an append-only log is the canonical
    instance — the last line of the log already is the status.
    """
    banned = spec["banned_frontmatter_keys"]
    for name, tmpl_rel in spec["templates"].items():
        path = fixture / name
        if not r.check(f"{name} exists in the fixture", path.is_file(), f"no {path}"):
            continue
        fm = frontmatter(path.read_text())
        if not r.check(f"{name} has frontmatter", fm is not None, "no --- block"):
            continue
        assert fm is not None
        keys = top_level_keys(fm)
        for key in required_keys((ROOT / tmpl_rel).read_text()):
            r.check(
                f"{name} has required frontmatter key {key!r}",
                key in keys,
                f"declared by {tmpl_rel}, absent here",
            )
        for key in banned:
            r.check(
                f"{name} has no {key!r} rollup field",
                key not in keys,
                f"apply rule 6 — {key} is recomputable from the log; a second copy drifts",
            )


def check_event_vocabulary(r: Report, spec: dict, fixture: Path) -> None:
    """The log is dated, append-only, and uses the named events and nothing else."""
    tmpl = (ROOT / spec["templates"]["application.md"]).read_text()
    vocab: set[str] = set()
    for line in tmpl.splitlines():
        stripped = line.strip()
        if stripped.startswith("`") and re.fullmatch(r"(`[a-z-]+`\s*)+", stripped):
            vocab.update(re.findall(r"`([a-z-]+)`", stripped))
    if not r.check(
        "the application.md template declares an event vocabulary",
        bool(vocab),
        "no backticked event list found in the template",
    ):
        return
    r.check("the event vocabulary is small", len(vocab) <= 12, f"{len(vocab)} events")

    body = section((fixture / "application.md").read_text(), "## Log")
    lines = [ln for ln in body.splitlines() if ln.startswith("- ")]
    r.check("the fixture log has entries", bool(lines), "no `- ` lines under ## Log")

    seen_dates: list[str] = []
    used: set[str] = set()
    for ln in lines:
        m = LOG_LINE.match(ln)
        if not r.check(
            f"log line parses: {ln[:56]!r}…",
            m is not None,
            "want `- YYYY-MM-DD — **event** — text`",
        ):
            continue
        assert m is not None
        date, event = m.group(1), m.group(2)
        seen_dates.append(date)
        used.add(event)
        r.check(
            f"log event {event!r} is in the vocabulary",
            event in vocab,
            f"vocabulary is {sorted(vocab)}",
        )
    r.check(
        "the log is in date order",
        seen_dates == sorted(seen_dates),
        "an append-only log that jumps backwards has been rewritten, not appended to",
    )
    r.check(
        "the fixture exercises most of the vocabulary",
        len(used) >= 5,
        f"only {sorted(used)} used — a fixture that never reaches an outcome teaches half the lane",
    )


def check_jd_boundary(r: Report, fixture: Path) -> None:
    """The verbatim boundary is what makes `apply` rule 1 checkable.

    Rule 1 forbids summarising into jd.md. Without a marked boundary that is an
    intention; with one, anything that drifts in around the posting is visible.
    """
    text = (fixture / "jd.md").read_text()
    nb, ne = text.count(BEGIN), text.count(END)
    r.check("jd.md has exactly one BEGIN marker", nb == 1, f"found {nb}")
    r.check("jd.md has exactly one END marker", ne == 1, f"found {ne}")
    if nb != 1 or ne != 1:
        return
    i, j = text.index(BEGIN), text.index(END)
    r.check("jd.md BEGIN precedes END", i < j, "markers are inverted")
    if i >= j:
        return
    r.check(
        "jd.md has posting text between the markers",
        len(text[i + len(BEGIN) : j].strip()) > 200,
        "the verbatim block is empty or a stub",
    )
    r.check(
        "jd.md ends at the END marker",
        text[j + len(END) :].strip() == "",
        "commentary after the boundary belongs in fit.md — rule 1",
    )


def check_fit_states(r: Report, spec: dict, fixture: Path) -> None:
    """Evidence state is one of three, and `missing` is not one of them.

    The corpus not backing a requirement may mean the user never did it, or did
    it and never wrote it down. Those need opposite responses, and choosing
    between them is the user's call, not this file's.
    """
    allowed = set(spec["evidence_states"])
    text = (fixture / "fit.md").read_text()
    rows = [
        [c.strip() for c in ln.strip().strip("|").split("|")]
        for ln in section(text, "## Requirements").splitlines()
        if ln.strip().startswith("|") and not re.fullmatch(r"\|[\s|:-]+\|", ln.strip())
    ]
    rows = [cells for cells in rows if len(cells) >= 3 and cells[1].lower() != "evidence state"]
    r.check("fit.md has a requirements table", len(rows) >= 3, f"{len(rows)} rows")

    used: set[str] = set()
    for cells in rows:
        state = cells[1]
        used.add(state)
        r.check(
            f"fit.md evidence state {state!r} is permitted",
            state in allowed,
            f"one of {sorted(allowed)}; `missing` is deliberately not among them",
        )
    for state in sorted(allowed):
        r.check(
            f"the fixture exercises evidence state {state!r}",
            state in used,
            "a fit check where everything lines up teaches the opposite of the point",
        )
    for pat in spec["banned_in_fit"]:
        r.check(
            f"fit.md avoids /{pat}/",
            not re.search(pat, text, re.I),
            "the corpus not backing something is not the same claim as the user not having done it",
        )


def check_artifact_frontmatter(r: Report, spec: dict, fixture: Path) -> None:
    """Every rendered artifact records what cannot be reconstructed later."""
    required = required_keys((ROOT / spec["artifact_template"]).read_text())
    lifecycles = set(spec["lifecycle_states"])
    source_root = ROOT / spec["source_root"]

    for name in spec["artifacts"]:
        path = fixture / name
        if not r.check(f"{name} exists in the fixture", path.is_file(), f"no {path}"):
            continue
        fm = frontmatter(path.read_text())
        if not r.check(f"{name} has frontmatter", fm is not None, "no --- block"):
            continue
        assert fm is not None
        keys = top_level_keys(fm)
        for key in required:
            r.check(f"{name} has artifact key {key!r}", key in keys, "declared by the template")
        for key in spec["banned_frontmatter_keys"]:
            r.check(f"{name} has no {key!r} rollup field", key not in keys, "apply rule 6")

        life = scalar(fm, "lifecycle")
        r.check(
            f"{name} lifecycle is one of {sorted(lifecycles)}",
            life in lifecycles,
            f"got {life!r} — the interview skill's rule 11b names exactly these three",
        )
        gen = scalar(fm, "generated") or ""
        r.check(f"{name} generated: is a date", bool(DATE.match(gen)), f"got {gen!r}")
        pin = scalar(fm, "corpus_pin") or ""
        r.check(
            f"{name} corpus_pin is filled in",
            bool(pin) and not PLACEHOLDER.match(pin),
            f"got {pin!r} — an unrecoverable input, so a placeholder is worse than an empty file",
        )
        srcs = list_block(fm, "sources")
        r.check(f"{name} names its sources", bool(srcs), "sources: is empty")
        for s in srcs:
            r.check(
                f"{name} source {s} resolves",
                (source_root / s).exists(),
                f"no such file under {spec['source_root']}/",
            )
        if life == "submitted":
            r.check(
                f"{name} records what was sent",
                "submitted:" in fm,
                "a submitted artifact is evidence of what a reader saw; record the send",
            )


def check_inbox_claims(r: Report, spec: dict, fixture: Path) -> None:
    """A recruiter's claims aim the prep. They never become facts in an output."""
    inbox = sorted((fixture / "_inbox").glob("*.md"))
    r.check("the fixture has inbound material", bool(inbox), "no _inbox/*.md")
    # Only the quoted inbound text counts as the temptation. A fixture file also
    # explains its own traps further down, and matching that would let the actual
    # recruiter claim be deleted while the assertion kept passing on the caption.
    inbox_text = "\n".join(
        ln for p in inbox for ln in p.read_text().splitlines() if ln.lstrip().startswith(">")
    )
    artifacts = {n: (fixture / n).read_text() for n in spec["artifacts"] if (fixture / n).is_file()}

    for case in spec["inbox_claims"]:
        for pat in case["must_appear"]:
            r.check(
                f"{case['id']}: the temptation is present in _inbox/",
                bool(re.search(pat, inbox_text, re.I)),
                f"/{pat}/ is gone — the assertion below now guards nothing",
            )
        for name, text in artifacts.items():
            hits = scan(text, case["forbidden"])
            r.check(
                f"{case['id']}: {name} does not repeat the claim",
                not hits,
                f"matched {hits}\n      rule: {case['rule']}\n      why:  {case['why']}",
            )


def check_gap_not_covered(r: Report, spec: dict, fixture: Path) -> None:
    """The requirement with no corpus evidence stays uncovered, and stays named."""
    gap = spec["gap"]
    for name in gap["forbidden_in"]:
        text = (fixture / name).read_text()
        hits = scan(text, gap["forbidden"])
        r.check(
            f"{gap['id']}: {name} does not cover the gap",
            not hits,
            f"matched {hits}\n      rule: {gap['rule']}\n      why:  {gap['why']}",
        )
    for name, pats in gap["must_name_gap"].items():
        text = (fixture / name).read_text()
        for pat in pats:
            r.check(
                f"{gap['id']}: {name} names the gap (/{pat}/)",
                bool(re.search(pat, text, re.I)),
                "an uncovered gap that is also unnamed is just an omission",
            )


def check_documented(r: Report, spec: dict) -> None:
    """Each group is explained by a sentence in the example README.

    An assertion nobody can trace back to a documented rule is one nobody will
    maintain.
    """
    # Collapse whitespace: the README is hard-wrapped, so almost every sentence
    # worth pointing at spans a line break. Rewrapping is not drift.
    doc = re.sub(r"\s+", " ", (ROOT / spec["documented_in"]).read_text().lower())
    needles = dict(spec["documented_by"])
    for case in spec["inbox_claims"]:
        needles[case["id"]] = case["documented_by"]
    needles[spec["gap"]["id"]] = spec["gap"]["documented_by"]
    for key, needle in needles.items():
        r.check(
            f"{key} is documented in {spec['documented_in']}",
            re.sub(r"\s+", " ", needle.lower()) in doc,
            f"{needle!r} is gone — the group has lost the row that justifies it",
        )


def main() -> int:
    spec = json.loads(CASES.read_text())
    fixture = ROOT / spec["fixture"]
    print(f"application fixture — {spec['fixture']}\n")

    r = Report()
    if not fixture.is_dir():
        r.check("the fixture directory exists", False, str(fixture))
        return r.summary()

    check_documented(r, spec)
    check_templates_conform(r, spec, fixture)
    check_event_vocabulary(r, spec, fixture)
    check_jd_boundary(r, fixture)
    check_fit_states(r, spec, fixture)
    check_artifact_frontmatter(r, spec, fixture)
    check_inbox_claims(r, spec, fixture)
    check_gap_not_covered(r, spec, fixture)
    return r.summary()


if __name__ == "__main__":
    sys.exit(main())
