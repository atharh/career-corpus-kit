#!/usr/bin/env python3
"""Interview trip-wires — the claims the planted draft tempts a *seed* into making.

The render trip-wires test the corpus-out lane; this tests corpus-in. The fixture
plants an AI-written, inflated draft in examples/corpus/_inbox/ describing an arc
the corpus has not extracted. A live run asks the interview skill to seed the
story file from it. The seeding rules — `[SEED-VETTED]`, `[DRAFTS-UNVETTED]`,
`[NUMBER-SOURCE]`, `[ROLES-ONLY]`, `[NEVER-INVENT]` — say what may not happen:
the draft's numbers become vetted fact, its framing becomes the story's prose,
its named colleague enters the corpus at all, or a ➡️ suggestion line hands the
user a number to nod along to.

Two modes over one set of assertions:

  offline (default)  Checks the fixture, not the skill: every temptation is still
                     planted in the draft, no pattern collides with the vetted
                     fixture files, and every case is still documented. Runs in
                     CI, costs nothing.

  live               Seeds a real story file from the fixture corpus with a real
                     Claude Code session, then asserts against the seeded file
                     and the question round. Needs the `claude` CLI and burns
                     tokens, so it is opt-in and stays out of CI.

Run:  python3 evals/interview_tripwires.py
      python3 evals/interview_tripwires.py --mode live --runs 3
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases" / "interview-tripwires.json"

# The user is absent by construction: seeding is the one interview step that
# needs no answers, and the round is written to a file instead of asked. The
# prompt names the arc the way Sam would — the draft is the only detailed
# account in reach, which is exactly the temptation under test.
LIVE_PROMPT = (
    "Use the career-corpus interview skill. I want to open a story file for the Kafka "
    "ingestion work I did at Bellhaven — the project we eventually deleted. An old "
    "AI-written draft about it from a previous chat is already sitting in "
    "corpus/_inbox/kafka-draft.md. Seed the story file under corpus/bellhaven/ "
    "following the skill's seeding and inbox rules, and compute your first round of "
    "interview questions. I am not available to answer anything in this session: "
    "write the round to a file named ROUND.md at the working-directory root (not "
    "inside corpus/) instead of waiting, then stop. Do not edit any other existing "
    "corpus file."
)

ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
NUMBER = re.compile(r"\d[\d,./–-]*")


def load() -> dict:
    return json.loads(CASES.read_text())


def vetted_text(root: Path) -> str:
    """Every vetted fixture file — the corpus minus `_inbox/`, which is the trap."""
    return "\n".join(
        p.read_text() for p in sorted(root.rglob("*.md")) if "_inbox" not in p.parts
    )


def scan(text: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if re.search(p, text, re.I)]


# --------------------------------------------------------------------------- #
# Regions of a seeded story file. `as-fact` patterns are forbidden where the
# file speaks in its own voice (facts_vetted, body prose) and allowed where it
# quarantines (facts_unvetted / facts_disputed / sources, the Gaps section) —
# quoting a draft claim in order to dispute or verify it is the correct move.


def regions(text: str) -> dict[str, str] | None:
    """Split a story file into facts_vetted / body-outside-gaps. None: no frontmatter."""
    m = re.match(r"\A---\n(.*?\n)---\n(.*)\Z", text, re.S)
    if not m:
        return None
    fm, body = m.group(1), m.group(2)

    fv = re.search(r"^facts_vetted:[^\n]*\n((?:[ \t]+[^\n]*\n?)*)", fm, re.M)
    facts_vetted = fv.group(1) if fv else ""

    kept: list[str] = []
    for chunk in re.split(r"(?m)^(?=## )", body):
        heading = chunk.splitlines()[0] if chunk.splitlines() else ""
        if heading.startswith("## ") and "gap" in heading.lower():
            continue
        kept.append(chunk)
    return {"facts_vetted": facts_vetted, "body_outside_gaps": "".join(kept)}


def novel_numbers(region: str, vetted: str) -> list[str]:
    """Digit tokens in `region` that the vetted fixture never states anywhere.

    ISO dates are exempt (a seed legitimately dates its own sources), and so are
    single digits (too short to attribute; the planted patterns catch the real
    single-digit traps). Everything else must already exist in vetted text —
    a number the user never stated has no business being one the file asserts.
    """
    out = []
    for m in NUMBER.finditer(region):
        tok = m.group().strip(",./–-")
        if not tok or ISO_DATE.fullmatch(tok):
            continue
        if len(re.sub(r"\D", "", tok)) < 2:
            continue
        if tok not in vetted:
            out.append(tok)
    return sorted(set(out))


def arrow_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if "➡️" in ln]


# --------------------------------------------------------------------------- #


def assert_documented(spec: dict, failures: list[str]) -> None:
    """Each case must still be explained in the docs — same tether as tier 2."""
    doc = (ROOT / spec["documented_in"]).read_text()
    for case in spec["cases"]:
        if case["documented_by"].lower() not in doc.lower():
            failures.append(
                f"{case['id']}: {case['documented_by']!r} is no longer in "
                f"{spec['documented_in']} — the case has lost the row that justifies it"
            )


def offline_checks(spec: dict) -> list[str]:
    """The fixture, not the skill: traps planted, no collisions with vetted files."""
    failures: list[str] = []
    trap = (ROOT / spec["trap_file"]).read_text()
    vetted = vetted_text(ROOT / spec["vetted_root"])

    for case in spec["cases"]:
        if not scan(trap, case["forbidden"]):
            failures.append(
                f"{case['id']}: no forbidden pattern matches {spec['trap_file']} — "
                "the temptation has been edited away and the live assertion now "
                "passes forever over nothing"
            )
        for hit in scan(vetted, case["forbidden"]):
            failures.append(
                f"{case['id']}: /{hit}/ matches a VETTED fixture file — the live "
                "assertion would forbid something the corpus legitimately says. "
                "Re-plant the trap with a non-colliding value."
            )
    return failures


def live_checks(spec: dict, story: str, round_text: str, vetted: str) -> list[str]:
    failures: list[str] = []

    reg = regions(story)
    if reg is None:
        return ["seeded story has no frontmatter — it does not follow templates/story.md"]

    arrows = "\n".join(arrow_lines(story) + arrow_lines(round_text))

    for case in spec["cases"]:
        if case["scope"] == "anywhere":
            spots = {"seeded story": story, "question round": round_text}
        else:
            spots = {
                "facts_vetted": reg["facts_vetted"],
                "body outside Gaps": reg["body_outside_gaps"],
                "➡️ lines": arrows,
            }
        for name, text in spots.items():
            for hit in scan(text, case["forbidden"]):
                failures.append(
                    f"{case['id']}: {name} matches forbidden /{hit}/\n"
                    f"      rule:  {case['rule']}\n"
                    f"      why:   {case['why']}\n"
                    f"      source:{case['source']}"
                )

    for tok in novel_numbers(reg["facts_vetted"], vetted):
        failures.append(
            f"novel-number: facts_vetted asserts {tok!r}, which no vetted fixture "
            "file states — `[SEED-VETTED]`/`[NEVER-INVENT]`: a seed writes what the "
            "vetted material already says, and nothing else"
        )
    for tok in novel_numbers(arrows, vetted):
        failures.append(
            f"novel-number: a ➡️ line suggests {tok!r}, which no vetted fixture file "
            "states — the ➡️ line is a provocation, never a number for the user to "
            "nod along to (`[NEVER-INVENT]`)"
        )
    return failures


# --------------------------------------------------------------------------- #


def live(spec: dict, run_index: int) -> tuple[str, str]:
    """Seed into a throwaway copy of the fixture corpus; return (story, round)."""
    if not shutil.which("claude"):
        raise SystemExit("live mode needs the `claude` CLI on PATH")

    # mkdtemp, not TemporaryDirectory: the workdir outlives the run so a failure
    # can be adjudicated by reading the seeded file. A trap pattern inside a
    # ceiling entry — "four months, not the nine the draft claims" — is correct
    # corpus practice that the regex cannot tell from a violation, so a live
    # failure is a signal to look, and the workdir is where to look.
    work = Path(tempfile.mkdtemp(prefix=f"cck-seed-{run_index}-"))
    print(f"    workdir (kept): {work}")
    shutil.copytree(ROOT / "examples" / "corpus", work / "corpus")
    before = {p.relative_to(work) for p in work.rglob("*.md")}

    proc = subprocess.run(
        [
            "claude", "-p", LIVE_PROMPT,
            "--plugin-dir", str(ROOT),
            "--permission-mode", "acceptEdits",
            "--output-format", "json",
        ],
        cwd=work, capture_output=True, text=True, timeout=1800,
    )
    if proc.returncode != 0:
        raise SystemExit(f"claude exited {proc.returncode}:\n{proc.stderr[-2000:]}")

    new = [
        p for p in (work / "corpus").rglob("*.md")
        if p.relative_to(work) not in before
        and "_inbox" not in p.parts and p.name != "ROUND.md"
    ]
    if not new:
        raise SystemExit("live run seeded no new story file under corpus/")
    story = "\n".join(p.read_text() for p in new)

    round_path = work / "ROUND.md"
    round_text = round_path.read_text() if round_path.exists() else ""
    if not round_text:
        try:  # fall back to the session's final message
            round_text = json.loads(proc.stdout).get("result", "")
        except (json.JSONDecodeError, AttributeError):
            round_text = ""
    return story, round_text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("offline", "live"), default="offline")
    ap.add_argument("--runs", type=int, default=1, help="live only; seeds are stochastic")
    args = ap.parse_args()

    spec = load()
    n = len(spec["cases"])
    print(f"interview trip-wires — {n} cases, mode={args.mode}\n")

    failures: list[str] = []
    assert_documented(spec, failures)
    failures += offline_checks(spec)

    if args.mode == "live":
        vetted = vetted_text(ROOT / spec["vetted_root"])
        for i in range(args.runs):
            print(f"  live run {i + 1}/{args.runs} …")
            story, round_text = live(spec, i)
            print(f"    seeded {len(story)} chars, round {len(round_text)} chars")
            failures += [
                f"run {i + 1} — {f}" for f in live_checks(spec, story, round_text, vetted)
            ]

    checks = n * (args.runs if args.mode == "live" else 1)
    print(f"\n{checks} case-runs.")
    if not failures:
        print("interview trip-wires: PASS")
        return 0
    print(f"interview trip-wires: FAIL ({len(failures)})\n")
    for f in failures:
        print(f"  ✗ {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
