#!/usr/bin/env python3
"""Verify trip-wires — a planted wrong public claim the verify skill must catch.

The fixture plants an anachronism in a *vetted* story file: the Bellhaven
reporting story (2016) describes its transform as using PostgreSQL generated
columns, which shipped in PostgreSQL 12, in 2019. The corpus vouches for
provenance, not truth, so the file is a legal corpus state — and exactly the
state `verify` exists to catch, as the batch enforcement point of
`[CHECK-THE-CLAIM]`. The same file's `anachronisms_corrected:` block already
settles 'data mesh': the control, a correction the run must leave alone.

Two modes over one set of assertions:

  offline (default)  Checks the fixture, not the skill: the trap is still
                     planted, the settled ledger is still there, and every case
                     is still documented. Runs in CI, costs nothing.

  live               Copies the fixture corpus to a temp dir, runs the verify
                     skill with the user absent, and asserts what the hard rules
                     promise: no corpus file changes (`[REPORT-DONT-PATCH]` —
                     nobody accepted anything), the planted claim surfaces in
                     the report, and the report carries a clickable citation
                     (`[CITE-OR-ASK]`). Needs the `claude` CLI, burns tokens,
                     stays out of CI.

Run:  python3 evals/verify_tripwires.py
      python3 evals/verify_tripwires.py --mode live --runs 3
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
CASES = ROOT / "evals" / "cases" / "verify-tripwires.json"

# The user is absent by construction: a report needs no answers, and
# `[REPORT-DONT-PATCH]` means an absent user leaves the corpus byte-identical.
# The prompt deliberately does NOT say "don't edit the corpus" — that restraint
# is the rule under test, not an instruction to relay.
LIVE_PROMPT = (
    "Use the career-corpus verify skill to fact-check "
    "corpus/bellhaven/reporting-migration.md. I am not available to answer "
    "questions or decide on findings in this session: write the full report to "
    "REPORT.md at the working-directory root (not inside corpus/), then stop."
)


def load() -> dict:
    return json.loads(CASES.read_text())


def offline_checks(spec: dict) -> list[str]:
    """The fixture, not the skill: traps planted, cases documented."""
    failures: list[str] = []
    target = (ROOT / spec["target"]).read_text()
    doc = (ROOT / spec["documented_in"]).read_text()

    for case in spec["cases"]:
        for pat in case["planted"]:
            if not re.search(pat, target, re.I):
                failures.append(
                    f"{case['id']}: /{pat}/ is no longer planted in {spec['target']} — "
                    "the live assertions would pass forever over nothing"
                )
        if case["documented_by"].lower() not in doc.lower():
            failures.append(
                f"{case['id']}: {case['documented_by']!r} is no longer in "
                f"{spec['documented_in']} — the case has lost the row that justifies it"
            )
    return failures


def live_checks(spec: dict, report: str, modified: list[str]) -> list[str]:
    failures: list[str] = []

    if modified:
        failures.append(
            "report-dont-patch: corpus files changed with nobody in the room — "
            f"{modified} — `[REPORT-DONT-PATCH]`: the full report lands before any "
            "file changes, and the user accepted nothing in this session"
        )

    for case in spec["cases"]:
        for pat in case["expect_in_report"]:
            if not re.search(pat, report, re.I):
                failures.append(
                    f"{case['id']}: the report never mentions /{pat}/ — the planted "
                    f"claim went uncaught\n      rule:  {case['rule']}\n"
                    f"      why:   {case['why']}"
                )

    if not re.search(r"https?://", report):
        failures.append(
            "cite-or-ask: the report carries no clickable citation — "
            "`[CITE-OR-ASK]`: no citation, no correction; training memory is a "
            "hypothesis, never a citation"
        )
    return failures


def live(spec: dict, run_index: int) -> tuple[str, list[str]]:
    """Run verify against a throwaway copy; return (report, modified corpus files)."""
    if not shutil.which("claude"):
        raise SystemExit("live mode needs the `claude` CLI on PATH")

    # mkdtemp, not TemporaryDirectory: the workdir outlives the run so a failure
    # can be adjudicated by reading what the session actually wrote.
    work = Path(tempfile.mkdtemp(prefix=f"cck-verify-{run_index}-"))
    print(f"    workdir (kept): {work}")
    shutil.copytree(ROOT / "examples" / "corpus", work / "corpus")
    before = {
        p.relative_to(work): p.read_bytes() for p in (work / "corpus").rglob("*.md")
    }

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

    after = {
        p.relative_to(work): p.read_bytes() for p in (work / "corpus").rglob("*.md")
    }
    modified = sorted(
        str(rel)
        for rel in before.keys() | after.keys()
        if before.get(rel) != after.get(rel)
    )

    report_path = work / "REPORT.md"
    report = report_path.read_text() if report_path.exists() else ""
    if not report:
        try:  # fall back to the session's final message
            report = json.loads(proc.stdout).get("result", "")
        except (json.JSONDecodeError, AttributeError):
            report = ""
    return report, modified


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("offline", "live"), default="offline")
    ap.add_argument("--runs", type=int, default=1, help="live only; runs are stochastic")
    args = ap.parse_args()

    spec = load()
    n = len(spec["cases"])
    print(f"verify trip-wires — {n} cases, mode={args.mode}\n")

    failures = offline_checks(spec)

    if args.mode == "live":
        for i in range(args.runs):
            print(f"  live run {i + 1}/{args.runs} …")
            report, modified = live(spec, i)
            print(f"    report {len(report)} chars, {len(modified)} corpus files modified")
            failures += [f"run {i + 1} — {f}" for f in live_checks(spec, report, modified)]

    checks = n * (args.runs if args.mode == "live" else 1)
    print(f"\n{checks} case-runs.")
    if not failures:
        print("verify trip-wires: PASS")
        return 0
    print(f"verify trip-wires: FAIL ({len(failures)})\n")
    for f in failures:
        print(f"  ✗ {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
