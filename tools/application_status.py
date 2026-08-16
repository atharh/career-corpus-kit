#!/usr/bin/env python3
"""What's live — every application thread, derived, so it cannot go stale.

`apply` already specifies this behaviour and, until this script, shipped no way
to do it: *read the events of each `applications/*/application.md`, report stage,
age and next action per thread, and name the ones that have gone quiet. Compute
it; never store it.* A rule with nothing enforcing it is a rule every session
hand-rolls differently — the relationship the kit's other rules had to `evals/`
before the eval suite existed.

So this is a conformance checker for the application lane, and its findings are
violations of stated rules rather than opinions: an artifact that went out but
was never frozen, one frozen that nobody sent, a `lifecycle:` outside the three
`interview`'s `[MARK-DONT-FIX]` defines, a thread whose events cannot be read, a
sent PDF that never entered git and so cannot be recovered. It is portable
because it parses nothing the kit did not define.

Nothing it prints is stored anywhere — `[NO-ROLLUP]`.

    python3 "${CLAUDE_PLUGIN_ROOT}/tools/application_status.py" [corpus-repo-root]

Stdlib only. Exit status is 1 when a conformance finding is reported, 0
otherwise, so it can gate a commit if the user wants it to.
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import appthread as at  # noqa: E402

QUIET_DAYS = 14


def artifact_files(folder: Path, patterns: tuple[str, ...] = ("*.md",)):
    """Every artifact in a thread folder, at any depth.

    Flat globbing is a scoping failure this codebase has made three times now,
    and it fails the same way every time: a folder that grew a subfolder is a
    folder with *more* in it, so the check reports least where there is most.
    `_inbox/` is excluded because inbound material is not a rendered artifact and
    carries no lifecycle of the user's.
    """
    for pattern in patterns:
        for path in sorted(folder.rglob(pattern)):
            if "_inbox" not in path.relative_to(folder).parts:
                yield path


def read_thread(folder: Path) -> dict:
    """Everything derivable about one thread, and an honest failure if not.

    `unmigrated` and `error` are separate from an empty stage on purpose. A
    thread whose events cannot be read must never render as a thread with no
    events, because that is exactly what a brand-new folder looks like.
    """
    t: dict = {
        "name": folder.name, "stage": None, "events": [], "sent": None,
        "unmigrated": False, "error": None,
    }
    parts = at.split_frontmatter((folder / "application.md").read_text())
    if parts is None:
        t["error"] = "application.md has no frontmatter block"
        return t
    try:
        t["events"] = at.parse_events(parts[0])
        t["sent"] = at.parse_sent(parts[0])
    except at.ThreadFormatError as e:
        t["error"] = str(e)
        return t
    if not t["events"]:
        t["unmigrated"] = True
        return t
    t["stage"] = at.stage(t["events"])
    return t


def tracked_binaries(root: Path) -> set[Path] | None:
    """Every *.pdf and *.docx git knows about, or None when this isn't a repo.

    None rather than an empty set, because the two mean opposite things: outside
    a repo nothing is tracked and nothing can be, so the checks below have no
    opinion rather than a bad one. Read once per run — `git ls-files` is one
    process where one call per artifact would be dozens.
    """
    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=30
        )

    try:
        if git("rev-parse", "--git-dir").returncode != 0:
            return None
        r = git("ls-files", "-z", "*.pdf", "*.docx")
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return {(root / p).resolve() for p in r.stdout.split("\0") if p}


def binary_findings(t: dict, folder: Path, tracked: set[Path] | None) -> list[str]:
    """The sent bytes have to survive, and a generated artifact cannot be rebuilt.

    `apply`'s `[PIN-NOT-ARCHIVE]`: PDF and DOCX writers stamp a creation time
    into the output, so a rebuild produces a different file rather than the same
    one. Once the untracked working copy is gone, what a reader saw is gone.

    Two cases, and the second is the one a list of filenames cannot see: a sent
    artifact's binary that never got `git add -f`, and a binary nothing accounts
    for at all. A binary whose Markdown sibling exists but is absent from
    `sent.artifacts` is a working copy of something deliberately not sent, and is
    left alone.
    """
    if tracked is None or t["sent"] is None:
        return []
    out = []
    listed = set(t["sent"]["artifacts"])
    for binary in artifact_files(folder, ("*.pdf", "*.docx")):
        if binary.resolve() in tracked:
            continue
        sibling = binary.with_suffix(".md")
        if sibling.name in listed:
            out.append(
                f"{t['name']} — {binary.name} went out but is not in git. It cannot be "
                f"rebuilt byte-for-byte, so those bytes are unrecoverable: `git add -f` it."
            )
        elif not sibling.exists():
            out.append(
                f"{t['name']} — {binary.name} is untracked and nothing accounts for it: no "
                f"Markdown sibling, and not in sent.artifacts. Either it went out, or it is cruft."
            )
    return out


def findings(t: dict, folder: Path) -> list[str]:
    """Rule violations only. A quiet thread is an observation, not a defect."""
    if t["error"]:
        return [f"{t['name']} — unreadable: {t['error']}. Stage unknown, checks not run."]
    if t["unmigrated"]:
        return [
            f"{t['name']} — unmigrated: no events: block. Stage unknown, checks not run. "
            f"apply's migration section covers this, and it is assisted, never automatic."
        ]

    out = []
    if any(e == "sent" for _, e in t["events"]) and t["sent"] is None:
        out.append(
            f"{t['name']} — a sent event but no sent: block. Which files the employer "
            f"received is recorded nowhere, and nothing else on disk knows it."
        )

    listed = set(t["sent"]["artifacts"]) if t["sent"] else set()
    for f in artifact_files(folder):
        if f == folder / "application.md":
            continue
        life = at.lifecycle_of(f.read_text())
        if life is None:
            continue
        if life not in at.LIFECYCLES:
            out.append(
                f"{t['name']} — {f.name} has unknown lifecycle {life!r}; expected one of "
                f"{', '.join(at.LIFECYCLES)}."
            )
        elif f.name in listed and life != "submitted":
            out.append(f"{t['name']} — {f.name} went out but is not lifecycle: submitted.")
        elif f.name not in listed and life == "submitted" and t["sent"]:
            out.append(
                f"{t['name']} — {f.name} is frozen but nobody sent it: it is not in "
                f"sent.artifacts."
            )
    return out


def days_since(iso: str, today: dt.date) -> int:
    return (today - dt.date.fromisoformat(iso)).days


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("-")]
    if any(a in ("-h", "--help") for a in argv[1:]):
        print(__doc__)
        return 0
    root = Path(args[0]).resolve() if args else Path.cwd()
    apps = root / "applications"
    if not apps.is_dir():
        print(f"no applications/ under {root} — run this from the corpus repo root, "
              f"or pass the path to it.", file=sys.stderr)
        return 2

    today = dt.date.today()
    tracked = tracked_binaries(root)
    sent_rows: list[str] = []
    prep_rows: list[str] = []
    problems: list[str] = []
    quiet: list[str] = []

    for folder in sorted(p for p in apps.iterdir() if p.is_dir()):
        if not (folder / "application.md").is_file():
            problems.append(f"{folder.name} — no application.md. The folder has no thread to read.")
            continue
        t = read_thread(folder)
        problems.extend(findings(t, folder))
        problems.extend(binary_findings(t, folder, tracked))

        dates = [d for d, _ in t["events"]]
        age = days_since(max(dates), today) if dates else None
        when = f"{max(dates)}  {age}d" if dates else "(undated)"
        shown = t["stage"] or ("unmigrated" if t["unmigrated"] else "unreadable")
        row = f"  {t['name']:<46} {shown:<14} {when}"
        reached_sent = (
            t["stage"] is not None
            and at.PIPELINE.index(t["stage"]) >= at.PIPELINE.index("sent")
        )
        (sent_rows if reached_sent else prep_rows).append(row)
        if age is not None and age >= QUIET_DAYS:
            quiet.append(f"{t['name']} — no activity in {age}d.")

    print("SENT — out the door")
    print("\n".join(sorted(sent_rows)) or "    (none)")
    print("\nIN PREPARATION — nothing sent yet")
    print("\n".join(sorted(prep_rows)) or "    (none)")
    if problems:
        print("\nNEEDS ATTENTION — each of these is a stated rule being broken")
        for p in problems:
            print(f"  {p}")
    if quiet:
        print("\nQUIET — an observation, not a defect. Whether one is dead is the user's call.")
        for q in quiet:
            print(f"  {q}")

    print("\nStage is the furthest event reached, read from each application.md frontmatter.")
    # `[SURFACE-DONT-DECIDE]`. Stage and age are derivations; what to do about a
    # thread that has gone quiet is a judgement about someone's career. A tool
    # that computes the next action is a tool that quietly takes it.
    print("Next action is deliberately not computed — it is a judgement, not a derivation.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
