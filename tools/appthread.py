#!/usr/bin/env python3
"""Read an application thread's state out of `application.md` frontmatter.

The grammar is closed on purpose, and nothing here infers: anything outside it
raises. That is `apply`'s `[STATE-IS-DATA]` in code. A reader that recovers
state by grepping the log body cannot tell *this thread has no events* from
*this thread has events I could not read* — both present as an empty stage — so
one malformed line makes a sent application look like it is still being written
and silently disarms every check gated on having reached `sent`.

Stdlib only, and deliberately no YAML library: a kit cannot assume one is
installed on a stranger's machine, and the grammar is narrow enough that one
anchored expression per line is a complete and safe reader.
"""

from __future__ import annotations

import datetime as dt
import re

# The nine events `apply` defines. A file naming anything else is a file whose
# author meant something this vocabulary cannot express — worth a question, not
# a guess.
EVENTS = (
    "opened", "fit-checked", "rendered", "sent", "inbound",
    "scheduled", "interviewed", "outcome", "routed",
)

# `inbound` and `routed` are events but never stages: both land after
# `interviewed` all the time, and reading the last line written would pull a
# thread backwards. The stage is the furthest point reached.
PIPELINE = (
    "opened", "fit-checked", "rendered", "sent",
    "scheduled", "interviewed", "outcome",
)

LIFECYCLES = ("baseline", "in-flight", "submitted")

EVENT_LINE = re.compile(r"^  - (\d{4}-\d{2}-\d{2}) ([a-z][a-z-]*)$")
ITEM_LINE = re.compile(r"^    - (\S.*)$")
SENT_DATE = re.compile(r"^  date: (\d{4}-\d{2}-\d{2})$")
BASELINE_PIN = re.compile(r"^  baseline_pin: (\S+)$")
TOP_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:")
# Any non-space token, not `[a-z-]+`: a value like `Submitted` must come back
# and fail the LIFECYCLES comparison as *unknown*, not vanish into "this file
# has no lifecycle" — which reads as "no checks apply".
LIFECYCLE = re.compile(r"^lifecycle:\s*[\"']?([^\"'#\s]+)")


class ThreadFormatError(Exception):
    """The file's shape is not the declared grammar. Never guessed past."""


def split_frontmatter(text: str) -> tuple[list[str], str] | None:
    """-> (frontmatter lines, body), or None when there is no `---` block."""
    lines = text.replace("\r", "").split("\n")
    if not lines or lines[0].rstrip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].rstrip() in ("---", "..."):
            return lines[1:i], "\n".join(lines[i + 1:])
    return None


def strip_comment(line: str) -> str:
    """Drop a whole-line or trailing `# …`.

    Comments are for the reader and never change what the data says. A corpus
    annotates its frontmatter — why a date is an estimate, what a pin covers —
    and a grammar that calls that a syntax error pushes the annotation into
    some other file, away from the value it explains.
    """
    if line.lstrip().startswith("#"):
        return ""
    # One space is enough, as in YAML itself — the template promises a trailing
    # `# …` is stripped, and a stricter rule here turns that promise into a
    # ThreadFormatError.
    m = re.search(r"[ \t]#", line)
    return line[:m.start()].rstrip() if m else line.rstrip()


def real_date(iso: str) -> str:
    """The date, or a raised ThreadFormatError when the calendar disagrees.

    The digit-shape regexes accept `2026-06-31`; letting it through means the
    first consumer to do date arithmetic dies mid-report instead of this one
    thread reading as unreadable.
    """
    try:
        dt.date.fromisoformat(iso)
    except ValueError:
        raise ThreadFormatError(f"not a real calendar date: {iso!r}")
    return iso


def block(fm_lines: list[str], key: str) -> list[str] | None:
    """The lines under `key:`, up to the next top-level key. None if absent."""
    out: list[str] = []
    inside = False
    for raw in fm_lines:
        if inside:
            if TOP_KEY.match(raw):
                break
            line = strip_comment(raw)
            if line.strip():
                out.append(line)
        elif strip_comment(raw) == f"{key}:":
            inside = True
    return out if inside else None


def parse_events(fm_lines: list[str]) -> list[tuple[str, str]]:
    """-> [(date, event)]. Empty when the key is absent; raises when unreadable.

    Empty and absent are the same value here on purpose — the caller has to
    distinguish *no events yet* from *no `events:` key*, because only the
    second one means the thread is unmigrated.
    """
    lines = block(fm_lines, "events")
    if lines is None:
        return []
    events = []
    for line in lines:
        m = EVENT_LINE.match(line)
        if not m:
            raise ThreadFormatError(f"not an event line: {line!r}")
        if m.group(2) not in EVENTS:
            raise ThreadFormatError(f"not one of the nine events: {m.group(2)!r}")
        events.append((real_date(m.group(1)), m.group(2)))
    return events


def parse_sent(fm_lines: list[str]) -> dict | None:
    """-> {'date', 'artifacts', 'baselines', 'baseline_pin'}, or None if absent.

    `artifacts` are files in this thread's own folder, and each one is
    cross-checked against its `lifecycle:`. `baselines` are repo-relative paths
    to living baseline files that went out instead, and are deliberately NOT
    cross-checked: a baseline goes on being edited, so demanding it be frozen
    would be wrong rather than merely noisy. One `baseline_pin` covers all of
    them, because it pins a repo commit — `git show <pin>:<path>` recovers each
    listed file as it stood. See `apply`'s `[SENT-NAMES-WHAT-WENT]`.
    """
    lines = block(fm_lines, "sent")
    if lines is None:
        return None
    out: dict = {"date": None, "artifacts": [], "baselines": [], "baseline_pin": None}
    listing = None
    for line in lines:
        stripped = line.rstrip()
        m_date, m_pin, m_item = (
            SENT_DATE.match(line), BASELINE_PIN.match(line), ITEM_LINE.match(line)
        )
        if m_date:
            out["date"], listing = real_date(m_date.group(1)), None
        elif m_pin:
            out["baseline_pin"], listing = m_pin.group(1), None
        elif stripped in ("  artifacts: []", "  baselines: []"):
            listing = None
        elif stripped in ("  artifacts:", "  baselines:"):
            listing = stripped.strip().rstrip(":")
        elif listing and m_item:
            out[listing].append(m_item.group(1))
        else:
            raise ThreadFormatError(f"not a sent: line: {line!r}")
    if out["date"] is None:
        raise ThreadFormatError("sent: block has no date")
    return out


def stage(events: list[tuple[str, str]]) -> str | None:
    """The furthest event in pipeline order, not the last one written."""
    reached = {e for _, e in events}
    found = [e for e in PIPELINE if e in reached]
    return found[-1] if found else None


def lifecycle_of(text: str) -> str | None:
    """The `lifecycle:` value of a rendered artifact, or None if it has none."""
    parts = split_frontmatter(text)
    if parts is None:
        return None
    for line in parts[0]:
        m = LIFECYCLE.match(line)
        if m:
            return m.group(1)
    return None
