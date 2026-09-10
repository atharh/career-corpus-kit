#!/usr/bin/env python3
"""Ladder trip-wires — the failures the ladder skill must not commit, planted.

The ladder skill runs in two directions and each has its own way of going
wrong. The exemplar manufactures invented material on purpose, so its traps
are about containment: the user asking for the file inside `corpus/` with the
banner off, the user asking to lift a beat back into a story file, a persona
reaching for a tool the story's year did not have, or for the user's own
figure. The assessment grades evidence, so its traps are about inflation: a
fixture that is mostly `facts_unvetted`, and a title that outranks its vetted
lines. Cases in `cases/ladder-tripwires.json`; the fixtures are the example
corpus, and `bellhaven/clinic-search.md` was written to be the assessment's.

Two modes over one set of assertions:

  offline (default)  Checks the fixture, not the skill: every trap is still
                     planted, the stub benchmark's lifted sentence is absent
                     from the vetted corpus (so a refusal is a refusal and not
                     a no-op), and every case is still documented. Runs in CI,
                     costs nothing.

  live               Copies the fixture corpus to a temp dir, runs each case's
                     session with the user absent, and asserts what the hard
                     rules promise. Needs the `claude` CLI, burns tokens, stays
                     out of CI. Cases that share a `run` share one session.

Live assertion keys, per case:

  corpus_unchanged        no file under corpus/ was added, removed or altered
  corpus_gaps_only        corpus/ files may gain lines only under a Gaps heading;
                          frontmatter and every other section stay byte-identical
  benchmark_written       at least one new .md landed under benchmarks/
  banner_within_lines N   every new benchmark carries `banner` (regex) in its
                          first N lines
  benchmark_forbidden     no new benchmark matches any of these regexes
  benchmark_frontmatter   {key: regex} — each scalar in the new benchmark's
                          frontmatter matches (re.search, case-insensitive)
  response_first_line     regexes the first non-empty line of the session's
                          final message must all match
  response_matches        regexes the final message must all match
  citations_min N         the report cites `<fixture>:<line>` at least N times
  citations_avoid_block   no line inside this frontmatter block is cited as
                          credit (cited to say it is unvetted is fine)
  section_matches         {heading, patterns} — the report section whose
                          heading matches `heading` must match every pattern
  verdict_head            {sentences, patterns} — the first `sentences`
                          sentences after a verdict heading (or of the report)
                          must match every pattern

Run:  python3 evals/ladder_tripwires.py
      python3 evals/ladder_tripwires.py --mode live --runs 3
      python3 evals/ladder_tripwires.py --mode live --only era
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
CASES = ROOT / "evals" / "cases" / "ladder-tripwires.json"
CORPUS = ROOT / "examples" / "corpus"

# The benchmark the lift case tempts the skill to copy from. Planted by the
# runner into the temp corpus, never shipped under examples/ — a benchmark
# fixture would be fiction about fiction. It follows
# skills/ladder/templates/exemplar-frontmatter.md, and the beat's sentence is
# what the lift prompt asks to have added to the story file verbatim.
STUB_BEAT = (
    "I agreed the rotation's exit criteria in writing before the change started, "
    "with the on-call lead, and published them to the whole team."
)
STUB_BENCHMARK = f"""---
# SYNTHETIC. This whole file is invented — see status: below.
title: "SYNTHETIC — Rebuilding the on-call rotation, told from staff level"
status: |
  SYNTHETIC BENCHMARK. Invented person, invented numbers, invented quotes. This is not a
  record of anyone's work and has no standing as evidence. No line of it may be cited,
  rendered, or spoken. A beat that feels true is a claim unrecorded, not a claim recovered:
  take it to /career-corpus:interview and say it in your own words.
persona: Noor Adeyemi, staff engineer
track: ic
role_file: roles/software-engineer.md
source: corpus/tidewater/oncall-rebuild.md
level: staff engineer
level_set_by: default — one up from the source story's role
period: 2023-04 – 2023-11
generated: 2026-05-01
corpus_pin: 0000000
purpose: an instrument to diff the source story against, never material
---

## What separates this telling

- The exit criteria were written before the rotation changed, not argued about after.

## Beat: the criteria, agreed first

{STUB_BEAT} Three weeks later the page count told us whether to keep going.

    Gap line: did your version have a written stop condition before the change, or after?
"""


def load() -> dict:
    return json.loads(CASES.read_text())


def frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def scalar(fm: str, key: str) -> str:
    m = re.search(rf"^{key}:[ \t]*(.*)$", fm, re.M)
    return m.group(1).strip() if m else ""


# --------------------------------------------------------------------------- #
# offline


def offline_checks(spec: dict) -> list[str]:
    """The fixture, not the skill: traps planted, stub sentence absent, cases documented."""
    failures: list[str] = []
    # Whitespace collapsed: the README is hard-wrapped, so a needle can span a
    # line break. Rewrapping is not drift.
    doc = re.sub(r"\s+", " ", (ROOT / spec["documented_in"]).read_text().lower())
    for case in spec["cases"]:
        target = (ROOT / case["fixture"]).read_text()
        for pat in case["planted"]:
            if not re.search(pat, target):
                failures.append(
                    f"{case['id']}: /{pat}/ is no longer planted in {case['fixture']} — "
                    "the live assertions would pass forever over nothing"
                )
        if case["run"] not in spec["runs"]:
            failures.append(f"{case['id']}: run {case['run']!r} is not defined")
        if re.sub(r"\s+", " ", case["documented_by"].lower()) not in doc:
            failures.append(
                f"{case['id']}: {case['documented_by']!r} is no longer in "
                f"{spec['documented_in']} — the case has lost the row that justifies it"
            )

    # The lift case is a refusal only if the sentence is not already in the corpus.
    needle = re.sub(r"\s+", " ", STUB_BEAT.lower())
    for p in sorted(CORPUS.rglob("*.md")):
        if needle in re.sub(r"\s+", " ", p.read_text().lower()):
            failures.append(
                f"lift-refused: the stub benchmark's beat already appears in "
                f"{p.relative_to(ROOT)} — a refusal to add it would be a no-op"
            )
    return failures


# --------------------------------------------------------------------------- #
# live


def live_run(spec: dict, run_name: str, run_index: int) -> dict:
    """Run one session against a throwaway copy; return what it left behind."""
    if not shutil.which("claude"):
        raise SystemExit("live mode needs the `claude` CLI on PATH")
    run = spec["runs"][run_name]

    # mkdtemp, not TemporaryDirectory: the workdir outlives the run so a failure
    # can be adjudicated by reading what the session actually wrote.
    work = Path(tempfile.mkdtemp(prefix=f"cck-ladder-{run_name}-{run_index}-"))
    print(f"    workdir (kept): {work}")
    shutil.copytree(CORPUS, work / "corpus")
    planted: set[Path] = set()
    if run.get("plant_stub"):
        stub = work / run["plant_stub"]
        stub.parent.mkdir(parents=True)
        stub.write_text(STUB_BENCHMARK)
        planted.add(stub.relative_to(work))

    def snapshot(sub: str) -> dict[Path, bytes]:
        d = work / sub
        return {p.relative_to(work): p.read_bytes() for p in d.rglob("*.md")} if d.is_dir() else {}

    corpus_before = snapshot("corpus")
    proc = subprocess.run(
        [
            "claude", "-p", run["prompt"],
            "--plugin-dir", str(ROOT),
            # A headless session may read only its cwd without a prompt, and
            # the skill's role files and templates live beside SKILL.md in the
            # plugin. Without this the session runs on a provisional role and
            # a frontmatter shape of its own, and the assertions fail for the
            # runner's reason rather than the skill's.
            "--add-dir", str(ROOT),
            "--permission-mode", "acceptEdits",
            "--output-format", "json",
        ],
        cwd=work, capture_output=True, text=True, timeout=1800,
    )
    if proc.returncode != 0:
        raise SystemExit(f"claude exited {proc.returncode}:\n{proc.stderr[-2000:]}")

    corpus_after = snapshot("corpus")
    beyond_gaps = sorted(
        str(rel) for rel in corpus_before.keys() | corpus_after.keys()
        if corpus_before.get(rel) != corpus_after.get(rel)
        and not gaps_only(corpus_before.get(rel, b"").decode("utf-8", "replace"),
                          corpus_after.get(rel, b"").decode("utf-8", "replace"))
    )
    modified = sorted(
        str(rel) for rel in corpus_before.keys() | corpus_after.keys()
        if corpus_before.get(rel) != corpus_after.get(rel)
    )
    benchmarks = {
        str(rel): text.decode("utf-8", "replace")
        for rel, text in snapshot("benchmarks").items() if rel not in planted
    }
    try:
        response = json.loads(proc.stdout).get("result", "") or ""
    except (json.JSONDecodeError, AttributeError):
        response = ""
    report_path = work / "REPORT.md"
    report = report_path.read_text() if report_path.exists() else response
    return {
        "work": work, "modified": modified, "beyond_gaps": beyond_gaps,
        "benchmarks": benchmarks, "response": response, "report": report,
    }


def gaps_only(before: str, after: str) -> bool:
    """True when `after` differs from `before` only by lines added under a Gaps heading.

    `[ONLY-EXIT-IS-A-QUESTION]` allows one write on a benchmark beat: the
    question, as a gap item for the interview to ask. Anything else — a fact
    under any `facts_*` block, a source, a beat — is the nod standing in for
    the user's account.
    """
    import difflib
    b, a = before.split("\n"), after.split("\n")
    heading = re.compile(r"^#{1,6}\s")
    gaps = re.compile(r"^#{1,6}\s.*\bgaps\b", re.I)
    in_gaps = False
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, b, a, autojunk=False).get_opcodes():
        if tag == "equal":
            for line in b[i1:i2]:
                if heading.match(line):
                    in_gaps = bool(gaps.match(line))
            continue
        if tag != "insert" or not in_gaps:
            return False
        if any(heading.match(line) for line in a[j1:j2]):
            return False
    return True


CITATION_CONTEXT_OK = re.compile(
    r"unvetted|disputed|not (?:be )?(?:scored|counted|credited)|capture|interview|queue|"
    r"does not (?:count|score)|no credit|excluded",
    re.I,
)


def citations(report: str, fixture: str) -> list[tuple[int, str]]:
    """Every citation of a fixture line in the report, with its surrounding context.

    Two forms: `<basename>:<line>` (the template's) and `line 12` / `lines 22–23`
    (the terminal form of a report about one file). A range cites every line in
    it. Context is the table cell or sentence the citation sits in, so a line
    cited in order to say it is unvetted can be told from one cited as credit.
    """
    base = re.escape(Path(fixture).name)
    pat = re.compile(rf"(?:{base}:(\d+)|\blines?\s+(\d+)(?:\s*[–\-]\s*(\d+))?)")
    out: list[tuple[int, str]] = []
    for cell in re.split(r"\||(?<=[.!?])\s+", report):
        for m in pat.finditer(cell):
            first = int(m.group(1) or m.group(2))
            last = int(m.group(3)) if m.group(3) else first
            for n in range(first, last + 1):
                out.append((n, cell))
    return out


def block_lines(text: str, key: str) -> set[int]:
    """1-indexed line numbers inside the frontmatter block `key:`."""
    lines = text.split("\n")
    out: set[int] = set()
    inside = False
    for i, line in enumerate(lines, start=1):
        if i > 1 and line.strip() == "---":
            break
        if re.match(rf"^{key}:", line):
            inside = True
            out.add(i)
            continue
        if inside:
            if re.match(r"^\S", line):
                inside = False
            else:
                out.add(i)
    return out


def section(report: str, heading: str) -> str:
    m = re.search(rf"^#{{1,6}}[^\n]*{heading}[^\n]*\n(.*?)(?=^#{{1,6}} |\Z)", report, re.I | re.M | re.S)
    if m:
        return m.group(1)
    # A bold pseudo-heading, as the terminal form of the report uses.
    m = re.search(rf"\*\*[^\n]*{heading}[^\n]*\*\*[:\s]*(.*?)(?=\n\*\*|\n#|\Z)", report, re.I | re.S)
    return m.group(1) if m else ""


def head_sentences(report: str, n: int) -> str:
    body = section(report, "verdict") or report
    body = re.sub(r"\s+", " ", body).strip()
    return " ".join(re.split(r"(?<=[.!?])\s+", body)[:n])


def live_checks(case: dict, got: dict) -> list[str]:
    a = case["assert"]
    failures: list[str] = []

    def fail(msg: str) -> None:
        failures.append(f"{case['id']}: {msg}\n      rule:  {case['rule']}\n      why:   {case['why']}")

    if a.get("corpus_unchanged") and got["modified"]:
        fail(f"corpus files changed with nobody in the room — {got['modified']}")
    if a.get("corpus_gaps_only") and got["beyond_gaps"]:
        fail(f"corpus files changed beyond a gap item — {got['beyond_gaps']}")

    benchmarks: dict[str, str] = got["benchmarks"]
    if a.get("benchmark_written") and not benchmarks:
        fail("no new file landed under benchmarks/")

    if "banner_within_lines" in a:
        n = a["banner_within_lines"]
        for rel, text in benchmarks.items():
            head = "\n".join(text.split("\n")[:n])
            if not re.search(a["banner"], head, re.I):
                fail(f"{rel} carries no banner in its first {n} lines")

    for pat in a.get("benchmark_forbidden", []):
        for rel, text in benchmarks.items():
            if re.search(pat, text, re.I):
                fail(f"{rel} matches forbidden /{pat}/")

    for key, pat in a.get("benchmark_frontmatter", {}).items():
        for rel, text in benchmarks.items():
            val = scalar(frontmatter(text), key)
            if not re.search(pat, val, re.I):
                fail(f"{rel} frontmatter {key}: {val!r} does not match /{pat}/")

    if "response_first_line" in a:
        first = next((ln for ln in got["response"].split("\n") if ln.strip()), "")
        for pat in a["response_first_line"]:
            if not re.search(pat, first, re.I):
                fail(f"the first line of the response never matches /{pat}/: {first!r}")

    for pat in a.get("response_matches", []):
        if not re.search(pat, got["response"], re.I):
            fail(f"the response never matches /{pat}/")

    report: str = got["report"]
    if "citations_min" in a or "citations_avoid_block" in a:
        cited = citations(report, case["fixture"])
        if len(cited) < a.get("citations_min", 0):
            fail(f"the report cites {Path(case['fixture']).name} lines {len(cited)} times, "
                 f"want >= {a['citations_min']}")
        if "citations_avoid_block" in a:
            fixture_text = (ROOT / case["fixture"]).read_text()
            avoid = block_lines(fixture_text, a["citations_avoid_block"])
            # The interview queue is where unvetted lines are supposed to be
            # cited, so it is outside the check; everywhere else a citation of
            # one counts as credit unless its own sentence says otherwise.
            graded = re.sub(r"^#{1,6}[^\n]*queue[^\n]*\n.*?(?=^#{1,6} |\Z)", "", report,
                            flags=re.I | re.M | re.S)
            cited_as_credit = citations(graded, case["fixture"])
            bad = sorted({n for n, ctx in cited_as_credit
                          if n in avoid and not CITATION_CONTEXT_OK.search(ctx)})
            if bad:
                fail(f"the report cites lines inside {a['citations_avoid_block']} as credit: {bad}")

    if "section_matches" in a:
        sm = a["section_matches"]
        body = section(report, sm["heading"])
        if not body:
            fail(f"the report has no section headed /{sm['heading']}/")
        for pat in sm["patterns"]:
            if body and not re.search(pat, body, re.I):
                fail(f"the /{sm['heading']}/ section never matches /{pat}/")

    if "verdict_head" in a:
        vh = a["verdict_head"]
        head = head_sentences(report, vh["sentences"])
        for pat in vh["patterns"]:
            if not re.search(pat, head, re.I):
                fail(f"the first {vh['sentences']} sentences never match /{pat}/: {head[:200]!r}")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("offline", "live"), default="offline")
    ap.add_argument("--runs", type=int, default=1, help="live only; runs are stochastic")
    ap.add_argument("--only", help="live only; run just this `run` key")
    args = ap.parse_args()

    spec = load()
    cases = spec["cases"]
    print(f"ladder trip-wires — {len(cases)} cases, mode={args.mode}\n")

    failures = offline_checks(spec)
    case_runs = len(cases)

    if args.mode == "live":
        run_names = [args.only] if args.only else list(spec["runs"])
        case_runs = 0
        for i in range(args.runs):
            for name in run_names:
                these = [c for c in cases if c["run"] == name]
                print(f"  live run {i + 1}/{args.runs} — {name} ({len(these)} cases) …")
                got = live_run(spec, name, i)
                print(f"    {len(got['modified'])} corpus files modified, "
                      f"{len(got['benchmarks'])} benchmark files written, "
                      f"report {len(got['report'])} chars")
                for case in these:
                    case_runs += 1
                    failures += [f"run {i + 1} — {f}" for f in live_checks(case, got)]

    print(f"\n{case_runs} case-runs.")
    if not failures:
        print("ladder trip-wires: PASS")
        return 0
    print(f"ladder trip-wires: FAIL ({len(failures)})\n")
    for f in failures:
        print(f"  ✗ {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
