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
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases" / "application-lane.json"

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOG_LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) — \*\*([a-z-]+)\*\* — \S")
# One `events:` entry. Anchored and closed on purpose: the whole point of the
# format is that a reader without a YAML library is still correct about it.
EVENT = re.compile(r"(\d{4}-\d{2}-\d{2}) ([a-z-]+)")
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
    # `[ \t]*` so a nested key (`sent.artifacts`) is readable too. Trailing `# …`
    # is stripped below, because a corpus annotates its frontmatter and a grammar
    # that calls that a syntax error pushes the annotation out of the file.
    m = re.search(rf"^[ \t]*{key}:[^\n]*\n((?:[ \t]+-[^\n]*\n?)+)", fm, re.M)
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

    `apply`'s no-rollup rule `[NO-ROLLUP]`: state that can be recomputed from
    what is already on disk is not stored. A `status:` field beside an
    append-only log is the canonical instance — the last line of the log already
    is the status.
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
                f"apply `[NO-ROLLUP]` — {key} is recomputable from the log; a second copy drifts",
            )
        # A `lifecycle:` on a file whose template declares none is invisible
        # rather than wrong: the freeze guards only ever test for `submitted`, so
        # an invented value sits there indefinitely doing nothing and reads as
        # meaningful to every human who opens the file. `fit.md` is the one that
        # attracts it — it is derived, never sent, and never frozen.
        declared = top_level_keys(frontmatter((ROOT / tmpl_rel).read_text()) or "")
        if "lifecycle" not in declared:
            r.check(
                f"{name} has no lifecycle: field",
                "lifecycle" not in keys,
                f"{tmpl_rel} declares none, and nothing reads one here — an invented value is "
                "invisible to the freeze guards and legible to everyone else",
            )


def check_event_vocabulary(r: Report, spec: dict, fixture: Path) -> None:
    """Events are read as data, from `events:`, and never out of the log prose.

    `apply`'s `[STATE-IS-DATA]`. Parsing the body fails in the unsafe direction:
    nothing distinguishes a thread with no events from a thread whose events did
    not parse, so a malformed `sent` line silently disarms every check gated on
    having reached `sent`. The body stays — it carries *why* — but nothing here
    derives state from it.
    """
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

    text = (fixture / "application.md").read_text()
    fm = frontmatter(text) or ""

    # `[STATE-FIRST]`: the state is at the top because `events:` is at the top,
    # and no other surface restates it. The heading is the one that tempts — the
    # most visible line in the file, where a stage reads as a courtesy rather
    # than as a rollup. It is one, and a conspicuous one goes stale in public.
    # Each event plus its participle, because a heading says INTERVIEWING where
    # the vocabulary says `interviewed`. Deliberately not a prefix match: `open`
    # and `sent` are ordinary words, and a company or role name is the one thing
    # guaranteed to be in this heading.
    stages = {w for w in vocab} | {re.sub(r"(?:ed|d)$", "", w) + "ing" for w in vocab}
    body_text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    head = next((ln for ln in body_text.splitlines() if ln.startswith("# ")), "")
    strays = sorted({w for w in stages if re.search(rf"\b{re.escape(w)}\b", head, re.I)})
    if re.search(r"\d{4}-\d{2}-\d{2}", head):
        strays.append("a date")
    r.check(
        "the application.md heading does not restate the stage",
        not strays,
        f"{head[:72]!r} contains {strays} — a stage there is recomputable from events:, so it "
        "drifts silently the next time the thread moves. apply `[STATE-FIRST]`. Name the term "
        "and let the reader judge: a role genuinely called Inbound Marketing Lead trips this "
        "and is fine, and 'may restate the stage' would send them hunting for nothing",
    )

    entries = list_block(fm, "events")

    # An unmigrated thread must report as unmigrated. Reporting it as a thread
    # with no events is the failure this whole format exists to remove.
    if not r.check(
        "the fixture's application.md carries an events: block",
        bool(entries),
        "a thread with a log and no events: is UNMIGRATED, not eventless — apply `[STATE-IS-DATA]`",
    ):
        return

    seen_dates: list[str] = []
    used: set[str] = set()
    for entry in entries:
        m = EVENT.fullmatch(entry)
        if not r.check(
            f"events entry parses: {entry[:56]!r}",
            m is not None,
            "want `<YYYY-MM-DD> <event>` — one plain string, never a mapping",
        ):
            continue
        assert m is not None
        seen_dates.append(m.group(1))
        used.add(m.group(2))
        r.check(
            f"event {m.group(2)!r} is in the vocabulary",
            m.group(2) in vocab,
            f"vocabulary is {sorted(vocab)}",
        )
    r.check(
        "events are in date order",
        seen_dates == sorted(seen_dates),
        "an append-only thread that jumps backwards has been rewritten, not appended to",
    )
    r.check(
        "the fixture exercises most of the vocabulary",
        len(used) >= 5,
        f"only {sorted(used)} used — a fixture that never reaches an outcome teaches half the lane",
    )

    # The reader's surface still has to exist, and its lines still have to be
    # dated one-per-event. That is conformance to the template, not state: no
    # assertion above reads a single character of it.
    body = section(text, "## Log")
    lines = [ln for ln in body.splitlines() if ln.startswith("- ")]
    r.check("the fixture log has entries", bool(lines), "no `- ` lines under ## Log")
    for ln in lines:
        r.check(
            f"log line is a dated entry: {ln[:56]!r}…",
            LOG_LINE.match(ln) is not None,
            "want `- YYYY-MM-DD — **event** — text`; the body is the reader's, and stays legible",
        )


def lifecycle_of(path: Path) -> str | None:
    if not path.is_file():
        return None
    return scalar(frontmatter(path.read_text()) or "", "lifecycle")


def sent_violations(fm: str, lifecycles: dict[str, str | None]) -> list[str]:
    """What is wrong with a `sent:` block, given each candidate file's lifecycle.

    `apply`'s `[SENT-NAMES-WHAT-WENT]`, and the two invariants only work as a
    pair: everything named went out frozen, and nothing else is frozen. Taking
    `lifecycles` as an argument rather than a folder is what lets the exemption
    below be asserted rather than merely omitted.
    """
    out: list[str] = []
    if "sent:" not in fm:
        return out
    date = re.search(r"^sent:[^\n]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+date:[ \t]*(\S+)", fm, re.M)
    if not date or not DATE.match(date.group(1)):
        out.append("sent: has no `date:` in YYYY-MM-DD form")
    artifacts = list_block(fm, "artifacts")
    if not artifacts and "baselines:" not in fm:
        out.append("sent: names nothing — an empty list reads as `nothing was sent`, which is a claim")
    for name in artifacts:
        life = lifecycles.get(name)
        if life is None:
            out.append(f"sent.artifacts names {name}, which is not in the folder")
        elif life != "submitted":
            out.append(f"sent.artifacts names {name}, which is `lifecycle: {life}` — it went out unfrozen")
    # Baselines are deliberately absent from that loop; see check_sent_block.
    for name, life in sorted(lifecycles.items()):
        if life == "submitted" and name not in artifacts:
            out.append(f"{name} is `lifecycle: submitted` but nobody sent it")
    return out


def check_sent_block(r: Report, spec: dict, fixture: Path) -> None:
    """`sent:` names what the employer received, and the pair of checks it enables."""
    fm = frontmatter((fixture / "application.md").read_text()) or ""
    events = [e.split()[-1] for e in list_block(fm, "events") if EVENT.fullmatch(e)]

    r.check(
        "a thread that reached `sent` carries a sent: block",
        ("sent" in events) == ("sent:" in fm),
        "one without the other — apply `[SENT-NAMES-WHAT-WENT]`",
    )

    lifecycles = {n: lifecycle_of(fixture / n) for n in spec["artifacts"]}
    problems = sent_violations(fm, lifecycles)
    r.check("the fixture's sent: block is consistent", not problems, "; ".join(problems))

    # The exemption, pinned. `sent.baselines` entries are NOT held to
    # `lifecycle: submitted`, because a baseline goes on being edited and
    # freezing one would be wrong rather than noisy. A later reader will see the
    # asymmetry with `artifacts:` and be tempted to "fix" it; these two
    # assertions are what makes that a failing change rather than a tidy-up.
    unfrozen = {"resume.md": "baseline"}
    as_baseline = "sent:\n  date: 2026-04-09\n  artifacts: []\n  baselines:\n    - resume.md\n"
    as_artifact = "sent:\n  date: 2026-04-09\n  artifacts:\n    - resume.md\n"
    r.check(
        "sent.baselines does not require `lifecycle: submitted`",
        not sent_violations(as_baseline, unfrozen),
        f"got {sent_violations(as_baseline, unfrozen)} — a baseline is edited on, and freezing "
        "one is wrong rather than merely noisy",
    )
    r.check(
        "sent.artifacts does require it",
        bool(sent_violations(as_artifact, unfrozen)),
        "the exemption above only means something while the rule it exempts from still bites",
    )


def check_jd_boundary(r: Report, fixture: Path) -> None:
    """The verbatim boundary is what makes `[CAPTURE-POSTING]` checkable.

    That rule forbids summarising into jd.md. Without a marked boundary that is
    an intention; with one, anything that drifts in around the posting is
    visible.
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
        "commentary after the boundary belongs in fit.md — apply `[CAPTURE-POSTING]`",
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
            r.check(f"{name} has no {key!r} rollup field", key not in keys, "apply `[NO-ROLLUP]`")

        life = scalar(fm, "lifecycle")
        r.check(
            f"{name} lifecycle is one of {sorted(lifecycles)}",
            life in lifecycles,
            f"got {life!r} — interview `[MARK-DONT-FIX]` names exactly these three",
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


STATUS_TOOL = ROOT / "tools" / "application_status.py"

# One synthetic thread per row of the tool's conformance table, and the needle
# that row must produce. Written to a temp dir rather than into examples/: these
# are broken on purpose, and a fixture that ships broken threads teaches the
# broken shape to every reader of the example corpus.
FM = "---\ncompany: C\nrole: R\n{}---\n\n# C — R\n\n## Log\n\n- 2026-01-01 — **opened** — x\n"
SENT_OK = "events:\n  - 2026-01-01 opened\n  - 2026-01-02 sent\nsent:\n  date: 2026-01-02\n  artifacts:\n    - resume.md\n"
ART = "---\nartifact: resume\nlifecycle: {}\ngenerated: 2026-01-02\n---\n\nbody\n"

BROKEN_THREADS = {
    "no-application-md": (None, "no application.md"),
    "unmigrated": (FM.format(""), "unmigrated: no events: block"),
    "unreadable": (FM.format("events:\n  - the sixth of January, opened\n"), "unreadable"),
    "sent-no-block": (
        FM.format("events:\n  - 2026-01-01 opened\n  - 2026-01-02 sent\n"),
        "a sent event but no sent: block",
    ),
    "went-out-unfrozen": (FM.format(SENT_OK), "went out but is not lifecycle: submitted"),
    "frozen-unsent": (FM.format(SENT_OK), "is frozen but nobody sent it"),
    "bad-lifecycle": (FM.format(SENT_OK), "unknown lifecycle"),
    "sent-pdf-untracked": (FM.format(SENT_OK), "went out but is not in git"),
    "orphan-binary": (FM.format(SENT_OK), "nothing accounts for it"),
}


def check_status_tool(r: Report, spec: dict) -> None:
    """The shipped checker agrees with the fixture, and each rule it states bites.

    `apply` specifies "asked what's live, compute it" and shipped no way to do
    it, so every session hand-rolled the computation and no two had a reason to
    agree. The tool closes that; these assertions are what stop it from
    reporting a clean corpus because it silently stopped checking.
    """
    if not r.check("the status tool ships", STATUS_TOOL.is_file(), f"no {STATUS_TOOL}"):
        return

    def run(root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(STATUS_TOOL), str(root)],
            capture_output=True, text=True, timeout=60,
        )

    clean = run(ROOT / spec["source_root"])
    r.check(
        "the tool reports the example corpus as conformant",
        clean.returncode == 0 and "NEEDS ATTENTION" not in clean.stdout,
        f"exit {clean.returncode}\n{clean.stdout}{clean.stderr}",
    )
    r.check(
        "the tool reads the fixture's stage as the furthest event reached",
        re.search(r"kestrel\S*\s+outcome\b", clean.stdout) is not None,
        "`outcome` is the furthest point in the pipeline this thread reached; the last event "
        f"written is a `routed`, and reading that instead pulls the thread backwards\n{clean.stdout}",
    )

    with tempfile.TemporaryDirectory() as tmp:
        apps = Path(tmp) / "applications"
        for name, (text, _) in BROKEN_THREADS.items():
            (apps / name).mkdir(parents=True)
            if text is None:
                continue
            (apps / name / "application.md").write_text(text)
            life = "in-flight" if name == "went-out-unfrozen" else "submitted"
            (apps / name / "resume.md").write_text(ART.format(life))
        (apps / "frozen-unsent" / "cover-letter.md").write_text(ART.format("submitted"))
        (apps / "bad-lifecycle" / "cover-letter.md").write_text(ART.format("archived"))
        # `[PIN-NOT-ARCHIVE]`: one sent PDF nobody force-added, and one binary with
        # no Markdown sibling at all. A real repo, because outside one the tool has
        # no opinion about what is tracked rather than a wrong one.
        (apps / "sent-pdf-untracked" / "resume.pdf").write_bytes(b"%PDF-1.4 fake\n")
        (apps / "orphan-binary" / "mystery.pdf").write_bytes(b"%PDF-1.4 fake\n")
        # The exemption, pinned the same way the baselines one is: a binary whose
        # Markdown sibling exists but is absent from sent.artifacts is a working
        # copy of something deliberately not sent, and reporting it would fire on
        # every folder holding a draft.
        clean_thread = apps / "prepared-not-sent"
        clean_thread.mkdir()
        (clean_thread / "application.md").write_text(FM.format(SENT_OK))
        (clean_thread / "resume.md").write_text(ART.format("submitted"))
        (clean_thread / "cover-letter.md").write_text(ART.format("in-flight"))
        (clean_thread / "cover-letter.pdf").write_bytes(b"%PDF-1.4 fake\n")
        subprocess.run(["git", "init", "-q", tmp], check=True, capture_output=True)

        got = run(Path(tmp))
        r.check(
            "an unsent artifact's binary is left alone",
            "cover-letter.pdf" not in got.stdout,
            "a working copy of something deliberately not sent is not a finding, or the check "
            f"fires on every folder holding a draft\n{got.stdout}",
        )
        r.check(
            "the tool exits non-zero when it has findings",
            got.returncode == 1,
            f"exit {got.returncode} — a checker whose exit status ignores its own findings "
            "cannot gate anything",
        )
        for name, (_, needle) in BROKEN_THREADS.items():
            r.check(
                f"the tool reports {name}",
                needle in got.stdout,
                f"expected {needle!r} in the output\n{got.stdout}{got.stderr}",
            )
        r.check(
            "an unmigrated thread is not reported as having no events",
            "unmigrated" in got.stdout and re.search(r"unmigrated\s+\(undated\)", got.stdout),
            "the whole reason the format changed: `no events` and `events I could not read` "
            f"must never be the same observation\n{got.stdout}",
        )


DOCTOR = ROOT / "tools" / "corpus_doctor.py"

# One deliberately broken corpus, one expectation per class. The doctor's four
# classes are its whole design — they exist because the four need genuinely
# different treatment — so the assertion is that a finding lands in the right
# class, not merely that it is found.
DOCTOR_CASES = [
    ("BLOCKING", "unmigrated: no events: block"),
    ("MECHANICAL", "the heading contains"),
    ("EDITORIAL", "tracked, but `_inbox/` is unvetted"),
    ("EDITORIAL", "no paragraph under the heading"),
    ("EDITORIAL", "a log entry runs"),
    ("EDITORIAL", "constraint-marked, and"),
    ("EDITORIAL", "caution markers in"),
    ("ADDITIVE", "corpus/directions.md — absent"),
]


def check_doctor(r: Report, spec: dict) -> None:
    """The conformance checker sorts findings into the class that fits them.

    A corpus several versions behind otherwise gets a wall it cannot act on, so
    ordering by what blocks what is the feature rather than the formatting. And
    the classes are not interchangeable: a mechanical fix may be proposed, an
    editorial one must never be applied, and an additive finding means nothing is
    wrong at all.
    """
    if not r.check("the corpus doctor ships", DOCTOR.is_file(), f"no {DOCTOR}"):
        return

    def run(root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(DOCTOR), str(root)], capture_output=True, text=True, timeout=60
        )

    clean = run(ROOT / spec["source_root"])
    r.check(
        "the doctor finds nothing blocking or mechanical in the example corpus",
        "BLOCKING" not in clean.stdout and "MECHANICAL" not in clean.stdout,
        f"{clean.stdout}{clean.stderr}",
    )
    r.check(
        "the doctor exempts examples/**/_inbox/ by path",
        "kafka-draft.md" not in clean.stdout,
        "the fixture inbox is committed on purpose — a doctor that reports it teaches the next "
        f"reader to delete the only trap the trip-wires have\n{clean.stdout}",
    )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "corpus").mkdir()
        (root / "corpus" / "story.md").write_text(
            "# Story\n\nRENDERING DECISION 2026-01-01: the team size stays out of the résumé.\n"
        )
        (root / "corpus" / "_inbox").mkdir()
        (root / "corpus" / "_inbox" / "raw.md").write_text("unvetted\n")
        # Inbound material in the corpus inbox, twice over: a pasted note that
        # echoes a thread constraint word for word, and a stray copy sharing a
        # basename with a real corpus file. Neither may surface — `_inbox/` is
        # never a constraint's home (`[INBOX-NOT-EVIDENCE]`), and a basename
        # collision there must not hide the one real match.
        (root / "corpus" / "_inbox" / "pasted.md").write_text(
            "RENDERING DECISION 2026-01-07: the demo cluster stays described as shared "
            "hardware borrowed between teams.\n"
        )
        (root / "corpus" / "_inbox" / "handle.md").write_text("unvetted copy\n")
        apps = root / "applications"
        (apps / "unmigrated").mkdir(parents=True)
        # An unmigrated thread with silt in it. Both are true of the same thread
        # in real life — a log predating the format is the one that has been
        # growing unchecked longest — and blocking the body checks behind the
        # stage reported least silt exactly where there was most.
        (apps / "unmigrated" / "application.md").write_text(
            FM.format("") + "- 2026-01-02 — **sent** — narration\n" + "  and more\n" * 8
        )

        # A second corpus constraint, so the echo test has to pick between two.
        (root / "corpus" / "craft.md").write_text(
            "# Craft\n\nRENDERING DECISION 2026-01-02: the support work is described as craft "
            "and never as a support role.\n"
        )
        # A decoy: a generic sentence *about* recorded rendering decisions rather
        # than any particular one. It shares exactly `rendering`, `decision`,
        # `recorded` and `without` with the constraint below — four words, of
        # which the marker guarantees two and collocation supplies a third.
        (root / "corpus" / "LESSONS.md").write_text(
            "# Lessons\n\n- 2026-01-05: a recorded RENDERING DECISION must be obeyed without "
            "relitigating.\n"
        )
        (root / "corpus" / "projects").mkdir()
        (root / "corpus" / "projects" / "handle.md").write_text(
            "# Handle\n\nRENDERING DECISION 2026-01-04: the account handle stays unlinked.\n"
        )

        bad = apps / "silted"
        bad.mkdir()
        (bad / "application.md").write_text(
            "---\ncompany: C\nrole: R\nevents:\n  - 2026-01-01 opened\n"
            "  - 2026-01-02 interviewed\n"
            # A marker inside dense frontmatter: no blank line anywhere in the
            # block, so treating the block as one paragraph quotes the whole
            # header and buries the marker.
            "note: RENDERING DECISION 2026-01-03: the salary box takes a range.\n---\n\n"
            "# C — R — INTERVIEWING\n\n## Log\n\n"
            "- 2026-01-01 — **opened** — a line\n"
            + "  more narration\n" * 8
            # A long log outgrows one heading. Matching `## Log` exactly hides
            # everything after the continuation, and the threads that need a
            # second heading are the ones with the most silt under it.
            + "\n## Log (continued)\n\n- 2026-01-03 — **inbound** — the long one\n"
            + "  and more\n" * 9
            # Two bullets, no blank line between them: two constraints echoing
            # two different corpus files. One unit would attribute the first
            # bullet's echo to both.
            + "\n## Constraints\n\n"
            "- RENDERING DECISION 2026-01-01: the team size stays out of the résumé.\n"
            "- RENDERING DECISION 2026-01-02: the support work is described as craft "
            "and never as a support role.\n"
            # Shares four words with the decoy, three of them free.
            "- RENDERING DECISION 2026-01-06: the box answer is recorded here and reused "
            "without change.\n"
            # Names its own home, which is stronger evidence than any overlap.
            "- RENDERING DECISION 2026-01-04: identity handling is settled in "
            "`corpus/projects/handle.md` and is not repeated here.\n"
            # Echoed only by corpus/_inbox/pasted.md, which is not an echo.
            "- RENDERING DECISION 2026-01-07: the demo cluster stays described as shared "
            "hardware borrowed between teams.\n"
            # Cites a bare basename that corpus/_inbox/handle.md also carries.
            "- RENDERING DECISION 2026-01-05: the account biography follows handle.md "
            "and stays unlinked.\n"
        )
        # A recruiter's inbound file quoting a decision back at the candidate.
        (bad / "_inbox").mkdir()
        (bad / "_inbox" / "recruiter.md").write_text(
            "RENDERING DECISION 2026-01-01: the team size stays out of the résumé.\n"
        )
        # A pack that grew a subfolder — the caution count must see into it.
        (bad / "rounds").mkdir()
        (bad / "rounds" / "02-probes.md").write_text("# Probes\n\n🔴 unresolved.\n")
        for name in ("resume.md", "cover-letter.md"):
            (bad / name).write_text(f"# {name}\n\n⚠️ something unresolved here.\n")
        # A frozen artifact carrying a duplicated constraint. Reporting it is
        # right; advising deletion is not, because the freeze forbids exactly
        # that. The freeze is easy to overlook — it is in the frontmatter of the
        # file being checked rather than anywhere in the check.
        (bad / "form-answers.md").write_text(
            "---\nartifact: form-answers\nlifecycle: submitted\n---\n\n# Answers\n\n"
            "RENDERING DECISION 2026-01-02: the support work is described as craft and never "
            "as a support role.\n"
        )
        # A conscientious fit check: it cites a ceiling and names where it came
        # from, which is the exception `[CONSTRAINT-HAS-ONE-HOME]` states rather
        # than a violation of it. Reporting this trains the reader to skim.
        (bad / "fit.md").write_text(
            "# fit\n\n⚠️ something unresolved here.\n\n"
            "- RENDERING DECISION 2026-01-04: ceiling per `corpus/projects/handle.md`.\n"
        )

        subprocess.run(["git", "init", "-q", tmp], check=True, capture_output=True)
        subprocess.run(["git", "-C", tmp, "add", "-A"], check=True, capture_output=True)

        got = run(root)
        r.check(
            "the doctor is a report and does not fail",
            got.returncode == 0,
            f"exit {got.returncode} — 'your corpus predates this guidance' is not the same claim "
            "as 'your corpus violates it', and an exit code cannot say both",
        )
        r.check(
            "a blocking thread still gets the checks that do not need a stage",
            "unmigrated — a log entry runs" in got.stdout,
            "the heading and log checks read the body, so blocking them behind the format "
            "reports least silt on the corpus that has the most of it, and the count rises as "
            f"the corpus gets cleaner\n{got.stdout}",
        )
        r.check(
            "the log check survives a continuation heading",
            "the long one" in got.stdout,
            "matching `## Log` exactly hides everything after `## Log (continued)`, and a log "
            "that outgrew one heading is the one with the most silt under it — the same "
            f"least-where-there-is-most failure one level down\n{got.stdout}",
        )
        r.check(
            "a marker in dense frontmatter is quoted as its own line",
            "'note: RENDERING DECISION" in got.stdout,
            "YAML has no blank line in it, so treating the block as one paragraph quotes the "
            f"whole header and buries the marker forty lines down\n{got.stdout}",
        )
        r.check(
            "each item in a list gets its own echo",
            "corpus/story.md" in got.stdout and "corpus/craft.md" in got.stdout,
            "a bullet list has no blank lines between items, so several constraints read as one "
            f"and an echo found for the first is reported for all of them\n{got.stdout}",
        )
        r.check(
            "the marker's own words do not count toward an echo",
            "LESSONS.md" not in got.stdout,
            "every candidate carries the marker on both sides by construction, so `rendering` "
            "and `decision` were half the required four for free — which matched a generic "
            f"sentence about recorded rendering decisions to a specific one\n{got.stdout}",
        )
        frozen_line = next(
            (ln for ln in got.stdout.split("\n") if "form-answers.md — constraint-marked" in ln),
            "",
        )
        r.check(
            "a finding on a frozen artifact does not advise editing it",
            "lifecycle: submitted` and frozen" in frozen_line and "before deleting" not in frozen_line,
            "a `submitted` artifact is frozen evidence and deletion is the one thing nobody may "
            "do to it, so advice to delete reads as a chore that cannot be done — and the freeze "
            f"is in the frontmatter of the file being checked, not in the check\n{frozen_line!r}",
        )
        r.check(
            "a fit check citing a ceiling with its source is not reported",
            "fit.md — constraint-marked" not in got.stdout,
            "`[CONSTRAINT-HAS-ONE-HOME]` states fit.md as the exception, and the rule's own test "
            "for it is whether the citation names its source. Reporting the convention working "
            f"teaches the reader to skim the class\n{got.stdout}",
        )
        r.check(
            "a constraint naming its own corpus file is reported as naming it",
            "it names corpus/projects/handle.md" in got.stdout,
            "a constraint that cites a path is naming its home, which is not a heuristic at all "
            f"and beats any word overlap\n{got.stdout}",
        )
        r.check(
            "a constraint in an application _inbox/ is not reported",
            "_inbox/recruiter.md — constraint-marked" not in got.stdout,
            "inbound material is somebody else's words (`[INBOX-NOT-EVIDENCE]`), so a "
            "recruiter quoting a decision back is not the user duplicating one — the same "
            f"exclusion the caution count already makes\n{got.stdout}",
        )
        demo_line = next(
            (ln for ln in got.stdout.split("\n") if "demo cluster" in ln), ""
        )
        r.check(
            "corpus/_inbox/ is never named as a constraint's home",
            "no echo found" in demo_line and "_inbox" not in demo_line,
            "an echo living only in corpus/_inbox/ is not an echo — reporting it asserts a "
            f"home that is never a valid home\n{demo_line!r}\n{got.stdout}",
        )
        biography_line = next(
            (ln for ln in got.stdout.split("\n") if "account biography" in ln), ""
        )
        r.check(
            "an _inbox/ basename collision does not hide the one real match",
            "it names corpus/projects/handle.md" in biography_line,
            "a stray copy in corpus/_inbox/ made the basename ambiguous, so the exactly-one "
            f"rule dropped the real match — the filter has to run before the count\n"
            f"{biography_line!r}\n{got.stdout}",
        )
        r.check(
            "the caution count sees into a subfolder",
            "rounds/02-probes.md" in got.stdout,
            "a flat glob is the same scoping failure a third time: a pack that grew a subfolder "
            f"is a pack with more in it\n{got.stdout}",
        )
        r.check(
            "the constraint echo test survives a hard-wrapped marker",
            "the same decision looks to be in" in got.stdout,
            "matching the line rather than the paragraph quotes a fragment starting mid-sentence "
            "and then reports no echo for a constraint that has one — the annotation sends a "
            f"reader to hand-check what the tool could have named\n{got.stdout}",
        )
        for cls, needle in DOCTOR_CASES:
            block = re.search(rf"^{cls}[^\n]*\n(.*?)(?=^[A-Z]{{4,}} —|\Z)", got.stdout, re.M | re.S)
            r.check(
                f"the doctor reports {needle!r} under {cls}",
                block is not None and needle in block.group(1),
                f"absent, or sorted into another class\n{got.stdout}{got.stderr}",
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
    check_status_tool(r, spec)
    check_doctor(r, spec)
    check_templates_conform(r, spec, fixture)
    check_event_vocabulary(r, spec, fixture)
    check_sent_block(r, spec, fixture)
    check_jd_boundary(r, fixture)
    check_fit_states(r, spec, fixture)
    check_artifact_frontmatter(r, spec, fixture)
    check_inbox_claims(r, spec, fixture)
    check_gap_not_covered(r, spec, fixture)
    return r.summary()


if __name__ == "__main__":
    sys.exit(main())
