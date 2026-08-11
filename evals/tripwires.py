#!/usr/bin/env python3
"""Trip-wires — the claims examples/corpus/ tempts a render into making.

Two modes over one set of assertions:

  offline (default)  Assert against the committed examples/rendered/*.md. Runs in
                     CI, costs nothing. Catches the example drifting into a claim
                     its own corpus forbids — but it does NOT exercise the skills.

  live               Render fresh artifacts from the fixture corpus with a real
                     Claude Code session, then assert against those. This is the
                     one that tests the skill. Needs the `claude` CLI and burns
                     tokens, so it is opt-in and stays out of CI.

Run:  python3 evals/tripwires.py
      python3 evals/tripwires.py --mode live --runs 3

`forbidden` patterns are the trip-wire and run in both modes. `expected_in` pins
the wording the committed example shipped and runs offline only — a live render
may phrase the safe version differently and still be right.
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
CASES = ROOT / "evals" / "cases" / "render-tripwires.json"

# A true baseline: no JD, no target role. The earlier version of this prompt asked
# for a "baseline" and then described a role, which is a tailored render wearing the
# wrong name — it handed the model a target and then tested it for corpus discipline.
# Every trip-wire here is corpus-side, so it must hold with nothing to tailor to.
# Tailored selection belongs in an application fixture, which does not exist yet.
LIVE_PROMPT = (
    "Use the career-corpus render skill. Render a baseline resume.md and a baseline "
    "cover-letter.md — no job description and no target role, the general-purpose "
    "versions kept as a checkpoint. Source only from corpus/. Write both files to "
    "the working directory and apply them without asking me to confirm."
)


def load() -> dict:
    return json.loads(CASES.read_text())


def scan(text: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if re.search(p, text, re.I)]


# --------------------------------------------------------------------------- #


def assert_documented(spec: dict, failures: list[str]) -> None:
    """Each case must still be explained by a row in ANNOTATED.md.

    An assertion nobody can trace back to a documented rule is one nobody will
    maintain. This keeps the eval and the docs from drifting apart.
    """
    doc = (ROOT / spec["documented_in"]).read_text()
    for case in spec["cases"]:
        needle = case["documented_by"]
        if needle.lower() not in doc.lower():
            failures.append(
                f"{case['id']}: {needle!r} is no longer in {spec['documented_in']} — "
                "the case has lost the row that justifies it"
            )


def run_assertions(spec: dict, texts: dict[str, str], check_expected: bool) -> list[str]:
    failures: list[str] = []
    for case in spec["cases"]:
        for name, text in texts.items():
            hits = scan(text, case["forbidden"])
            for h in hits:
                failures.append(
                    f"{case['id']}: {name} matches forbidden /{h}/\n"
                    f"      rule:  {case['rule']}\n"
                    f"      why:   {case['why']}\n"
                    f"      source:{case['source']}"
                )
        if not check_expected:
            continue
        for target, pats in case.get("expected_in", {}).items():
            name = Path(target).name
            if name not in texts:
                failures.append(f"{case['id']}: expected target {target} was not rendered")
                continue
            if not scan(texts[name], pats):
                failures.append(
                    f"{case['id']}: {name} is missing the safe version — "
                    f"none of {pats} present"
                )
    return failures


# --------------------------------------------------------------------------- #


def offline(spec: dict) -> dict[str, str]:
    return {Path(t).name: (ROOT / t).read_text() for t in spec["targets"]}


def live(spec: dict, run_index: int) -> dict[str, str]:
    """Render into a throwaway copy of the fixture corpus, return what landed."""
    if not shutil.which("claude"):
        raise SystemExit("live mode needs the `claude` CLI on PATH")

    with tempfile.TemporaryDirectory(prefix=f"cck-eval-{run_index}-") as tmp:
        work = Path(tmp)
        shutil.copytree(ROOT / "examples" / "corpus", work / "corpus")
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

        out = {p.name: p.read_text() for p in work.glob("*.md")}
        if not out:
            raise SystemExit("live run produced no markdown in the working directory")
        return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("offline", "live"), default="offline")
    ap.add_argument("--runs", type=int, default=1, help="live only; renders are stochastic")
    args = ap.parse_args()

    spec = load()
    n_cases = len(spec["cases"])
    print(f"trip-wires — {n_cases} cases, mode={args.mode}\n")

    failures: list[str] = []
    assert_documented(spec, failures)

    if args.mode == "offline":
        texts = offline(spec)
        print(f"  targets: {', '.join(texts)}")
        failures += run_assertions(spec, texts, check_expected=True)
    else:
        for i in range(args.runs):
            print(f"  live run {i + 1}/{args.runs} …")
            texts = live(spec, i)
            print(f"    rendered: {', '.join(texts)}")
            failures += [f"run {i + 1} — {f}" for f in run_assertions(spec, texts, False)]

    checks = n_cases * (args.runs if args.mode == "live" else 1)
    print(f"\n{checks} case-runs.")
    if not failures:
        print("trip-wires: PASS")
        return 0
    print(f"trip-wires: FAIL ({len(failures)})\n")
    for f in failures:
        print(f"  ✗ {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
