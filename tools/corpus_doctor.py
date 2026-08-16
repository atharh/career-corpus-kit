#!/usr/bin/env python3
"""Where an existing corpus does not yet match the kit's current guidance.

The kit can never see a private corpus, so it cannot migrate one. It can only
ship this: a checker the user runs locally, which reports and never edits. That
constraint is the whole shape of the tool, and every design call below follows
from it.

**Nothing records which guidance version a corpus has reached.** A `kit_version:`
marker would be a stored copy of derivable state — `[NO-ROLLUP]` — and it goes
stale the first time a file is hand-edited. Every rule is checked on every run,
which is cheap, and it is the same argument that made application status derived
rather than stored.

**Findings are ordered by what blocks what**, because a corpus several versions
behind otherwise gets a wall it cannot act on. Four classes, and they need
genuinely different treatment:

  BLOCKING    Nothing else about this thread is knowable until it is fixed.
  MECHANICAL  The fix exists and is unambiguous. Propose it; write nothing
              without confirmation.
  EDITORIAL   Detectable, but the fix is a judgement. Never auto-applied.
              Summarising provenance is a silent lossy edit, and what still
              binds is the user's call.
  ADDITIVE    Nothing is wrong. The report is the migration.

**It reports terms and locations, never verdicts** — `[SURFACE-DONT-DECIDE]`.
Several checks here cannot separate a real finding from an ordinary one: a role
called Inbound Marketing Lead trips the heading check and is fine. Naming what
was found and where costs the reader a glance; "may be non-compliant" costs them
a hunt.

    python3 "${CLAUDE_PLUGIN_ROOT}/tools/corpus_doctor.py" [corpus-repo-root]

**It is a report, not a gate, and its exit status says so**: 0 whenever it ran,
2 only when it could not. That is a deliberate split from
`application_status.py`, which exits 1 to mean *a rule this corpus already
follows is being broken*. **Your corpus predates this guidance is not the same
claim as your corpus violates it**, and a user who gets a failure on a corpus
they have not touched in six months will read it as the second. Nothing here is
urgent by construction; the status checker is where urgency lives.

Stdlib only.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import appthread as at  # noqa: E402
from application_status import (  # noqa: E402
    binary_findings, findings, read_thread, tracked_binaries,
)

# A log entry that has grown into session narration. The number is a heuristic
# for finding silt, not a rule about length — `[LENGTH-IS-THEIRS]` — so the
# report says so and the user judges.
LOG_ENTRY_LINES = 6

# Two markers, deliberately not the same one. `RENDERING DECISION` is the
# kit's explicit marker for a recorded constraint, so it is what the duplicate
# check greps for. A bare ⚠️ is used all over the kit for cautions and banners
# alike, and matching it as a constraint reports every file that carries a
# header — measured against the example corpus, which is why the split exists.
CONSTRAINT = re.compile(r"RENDERING DECISION")
CAUTION = re.compile(r"RENDERING DECISION|⚠️")
CAUTION_FILES = 3

# `examples/**/_inbox/` is committed on purpose and the exemption is written
# into the check rather than discovered by it: `examples/` is not a corpus, the
# skills never read it, and a fixture with no unvetted material in it cannot
# demonstrate the rule that unvetted material is never evidence. A doctor that
# "fixes" it deletes the only trap the trip-wires have.
INBOX_EXEMPT = re.compile(r"(^|/)examples/.*(^|/)_inbox/")


class Findings:
    def __init__(self) -> None:
        self.blocking: list[str] = []
        self.mechanical: list[str] = []
        self.editorial: list[str] = []
        self.additive: list[str] = []


def stage_terms(vocab) -> set[str]:
    """Each event plus its participle — a heading says INTERVIEWING where the
    vocabulary says `interviewed`. Not a prefix match: `open` and `sent` are
    ordinary words, and a company or role name is the one thing guaranteed to be
    in that heading."""
    return set(vocab) | {re.sub(r"(?:ed|d)$", "", w) + "ing" for w in vocab}


def body_of(text: str) -> str:
    parts = at.split_frontmatter(text)
    return parts[1] if parts else text


def check_thread_shape(f: Findings, name: str, text: str) -> None:
    """`[STATE-FIRST]` and `[LOG-APPEND-ONLY]`, on one application.md."""
    body = body_of(text)
    lines = body.split("\n")

    head = next((ln for ln in lines if ln.startswith("# ")), "")
    hits = sorted({t for t in stage_terms(at.EVENTS) if re.search(rf"\b{re.escape(t)}\b", head, re.I)})
    if re.search(r"\d{4}-\d{2}-\d{2}", head):
        hits.append("a date")
    if hits:
        f.mechanical.append(
            f"{name} — the heading contains {hits}: {head.strip()[:60]!r}. A stage there is "
            f"recomputable from events:, so it goes stale the next time the thread moves "
            f"(`[STATE-FIRST]`). If the term is part of the role's own name, ignore this."
        )

    # The state paragraph: prose between the `# ` heading and the first `## `.
    if head:
        after = lines[lines.index(head) + 1:]
        upto = after[: next((i for i, ln in enumerate(after) if ln.startswith("## ")), len(after))]
        if not any(ln.strip() and not ln.startswith(">") for ln in upto):
            f.editorial.append(
                f"{name} — no paragraph under the heading saying what the thread is waiting on "
                f"and whose move it is next (`[STATE-FIRST]`). Only the user knows that, so "
                f"nothing here can write it."
            )

    entry, count = None, 0

    def flush() -> None:
        # Flushed at every boundary, including a blank line. An earlier version
        # only flushed when the next entry began, so the longest entry in a log —
        # the last one before a blank line — was the one it could never report.
        if entry and count > LOG_ENTRY_LINES:
            f.editorial.append(
                f"{name} — a log entry runs {count} lines: {entry[:60]!r}…. One dated line "
                f"per event (`[LOG-APPEND-ONLY]`), and this compresses rather than being "
                f"deleted. The line count is a heuristic for finding silt, not a rule about "
                f"length; whether this entry still earns its space is a judgement."
            )

    for ln in body.split("\n"):
        if ln.startswith("- "):
            flush()
            entry, count = ln[2:], 1
        elif entry is not None and ln.strip():
            count += 1
        elif entry is not None:
            flush()
            entry, count = None, 0
    flush()


def check_constraints(f: Findings, root: Path) -> None:
    """`[CONSTRAINT-HAS-ONE-HOME]`, the operational half.

    A rule saying *don't duplicate* loses to a session that sincerely believes it
    is not duplicating, so this greps rather than trusting. Every constraint
    marker inside `applications/` is reported, because that folder is not where a
    constraint lives; whether a given line is really a constraint is left to the
    reader, and the corpus is searched for an echo so the common case answers
    itself.
    """
    corpus = root / "corpus"
    corpus_lines = []
    if corpus.is_dir():
        for p in sorted(corpus.rglob("*.md")):
            corpus_lines.extend(
                (p.relative_to(root), ln.strip()) for ln in p.read_text().split("\n")
                if CONSTRAINT.search(ln)
            )

    for p in sorted((root / "applications").rglob("*.md")):
        for ln in p.read_text().split("\n"):
            if not CONSTRAINT.search(ln):
                continue
            words = {w for w in re.findall(r"[a-z]{5,}", ln.lower())}
            echo = next(
                (src for src, other in corpus_lines
                 if words and len(words & set(re.findall(r"[a-z]{5,}", other.lower()))) >= 4),
                None,
            )
            where = f"also in {echo}" if echo else "no obvious echo in corpus/ — check by hand"
            f.editorial.append(
                f"{p.relative_to(root)} — constraint-marked line, {where} "
                f"(`[CONSTRAINT-HAS-ONE-HOME]`): {ln.strip()[:70]!r}"
            )


def check_caution(f: Findings, root: Path) -> None:
    """The countable half of `[NOT-EVERY-DOUBT-IS-A-BLOCKER]`.

    A weakness named once is preparation; the same one named across four files is
    accumulation, and the count is countable even though the judgement is not.
    This cannot tell a justified gate from an accumulated one and does not try —
    it names the files and stops.
    """
    for folder in sorted(p for p in (root / "applications").iterdir() if p.is_dir()):
        # Blockquoted lines are quoted material or a file header, not the file's
        # own caution about the candidate. Counting them makes every folder look
        # anxious and the check useless — measured, not assumed.
        marked = sorted(
            p.name for p in folder.glob("*.md")
            if any(CAUTION.search(ln) for ln in p.read_text().split("\n")
                   if not ln.lstrip().startswith(">"))
        )
        if len(marked) >= CAUTION_FILES:
            f.editorial.append(
                f"{folder.name} — caution markers in {len(marked)} files: {', '.join(marked)} "
                f"(`[NOT-EVERY-DOUBT-IS-A-BLOCKER]`). Nothing here can tell a justified gate "
                f"from an accumulated one; that read is the user's."
            )


def check_tracked_inbox(f: Findings, root: Path) -> None:
    """`_inbox/` is git-ignored by default; a tracked one is unvetted material in
    history in every clone, and deleting the file later does not take it back."""
    try:
        # --full-name so paths are relative to the repository root: the exemption
        # below is about where a file sits in the repo, and paths relative to
        # whatever directory this was pointed at would miss it.
        r = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--full-name", "*_inbox/*"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return
    if r.returncode != 0:
        return
    tracked = [p for p in r.stdout.split("\0") if p and not INBOX_EXEMPT.search("/" + p)]
    for p in sorted(tracked):
        f.mechanical.append(
            f"{p} — tracked, but `_inbox/` is unvetted material and is ignored by default. "
            f"It is in history in every clone; removing the file now does not take it back."
        )


def check_additive(f: Findings, root: Path) -> None:
    """Nothing is wrong here. The report is the migration."""
    if not (root / "corpus" / "directions.md").is_file():
        f.additive.append(
            "corpus/directions.md — absent, which is a fine state to be in. It holds role "
            "families the evidence could back, and an entry only goes in by citing its story "
            "files, naming its gap, and saying where it doesn't hold (`[DIRECTIONS-FILE]`). "
            "An empty one is an invitation to fill it, so it appears when the first entry passes."
        )

    families = sorted(
        re.sub(r"^cover-letter-|\.md$", "", p.name)
        for p in root.rglob("cover-letter-*.md")
        if "applications" not in p.parts
    )
    if families:
        f.additive.append(
            f"baseline families in this repo: {', '.join(families)}. Each maintained family "
            f"wants a résumé baseline as well as a letter; a family with a letter and no résumé "
            f"is the gap nothing else surfaces. Suggest a missing member and stop — a baseline "
            f"is upkeep, and creating one nobody asked for manufactures it (`[SUGGEST-DONT-SPAWN]`)."
        )


def main(argv: list[str]) -> int:
    if any(a in ("-h", "--help") for a in argv[1:]):
        print(__doc__)
        return 0
    args = [a for a in argv[1:] if not a.startswith("-")]
    root = Path(args[0]).resolve() if args else Path.cwd()
    if not (root / "corpus").is_dir() and not (root / "applications").is_dir():
        print(f"no corpus/ or applications/ under {root} — run this from the corpus repo "
              f"root, or pass the path to it.", file=sys.stderr)
        return 2

    f = Findings()
    if (root / "applications").is_dir():
        tracked = tracked_binaries(root)
        for folder in sorted(p for p in (root / "applications").iterdir() if p.is_dir()):
            thread = folder / "application.md"
            if not thread.is_file():
                f.blocking.append(f"{folder.name} — no application.md. There is no thread to read.")
                continue
            t = read_thread(folder)
            if t["error"] or t["unmigrated"]:
                f.blocking.extend(findings(t, folder))
                continue
            f.mechanical.extend(findings(t, folder))
            f.mechanical.extend(binary_findings(t, folder, tracked))
            check_thread_shape(f, folder.name, thread.read_text())
        check_constraints(f, root)
        check_caution(f, root)
    check_tracked_inbox(f, root)
    check_additive(f, root)

    blocks = [
        ("BLOCKING — nothing else about these can be checked until they are fixed", f.blocking),
        ("MECHANICAL — the fix is unambiguous; confirm before anything is written", f.mechanical),
        ("EDITORIAL — detectable, but the fix is a judgement and is not this tool's", f.editorial),
        ("ADDITIVE — nothing is wrong; this list is the whole migration", f.additive),
    ]
    print(f"corpus doctor — {root}\n")
    for title, items in blocks:
        if not items:
            continue
        print(title)
        for item in items:
            print(f"  {item}")
        print()
    if not any(items for _, items in blocks):
        print("Nothing to report against the current guidance.\n")

    print("Nothing was written, and no record of this run is kept: every rule is checked on "
          "every run rather than\nmarked off, because a stored migration marker is a copy of "
          "derivable state that goes stale on the first hand-edit.")
    print("This is a report and not a gate, so it does not fail. A corpus that predates a rule "
          "is not a corpus\nbreaking one — run application_status.py for the checks that are "
          "urgent.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
