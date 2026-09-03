#!/usr/bin/env python3
"""What's outstanding in the corpus — every line derived, so it cannot go stale.

Sibling of `application_status.py`, for the corpus side: unextracted seeds in
`_inbox/`, open gaps per story, flagged gaps, capability files a story cites
before anyone wrote them, and the capability queue itself — every technology
some story declares and no capability file answers for.

That last section is the reason this tool exists, and its design is the whole
point. Coverage is read from frontmatter, never grepped from prose. A story
file declares what it evidences in `technologies:`; a capability file declares
what it answers for in `covers:`, aliases included. The universe is the union
of the first, coverage the union of the second, and what is uncovered is the
difference — with no lexicon in this file to fall behind, no family list to
curate, and no dismissal list to keep in step: a term the user would not claim
standalone is covered by the family file whose ceiling says so, and a recorded
clean no is coverage too. `[TECHNOLOGIES-DECLARED]` and `[COVERS]` in the
interview skill are the rules this reads; the last two sections — story files
with no `technologies:` key, capability files with no `covers:` — are how they
get checked.

Nothing here infers, for the reason `appthread.py` gives: a frontmatter block
that could not be read must never present as a block that declared nothing,
because the second silently empties every set below. A malformed list raises
with the path, and so does a block that opens and never closes. A capability
file with no `covers:` is the same hole from the other side — it covers
nothing and looks like coverage — so it gets a section of its own, the twin of
the one for story files with no `technologies:`.

    python3 "${CLAUDE_PLUGIN_ROOT}/tools/corpus_status.py" [corpus-repo-root]

Stdlib only, and the list grammar is one token per item — the same bet
`appthread.py` makes: a reader this narrow needs no YAML library, and anything
outside it is worth a question rather than a guess. Exit status is 0 whenever
it ran and 2 only when it could not: the same split `corpus_doctor.py` makes,
because a story file that predates `technologies:` is behind the guidance, not
breaking it, and this is a work list rather than a gate.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import appthread as at  # noqa: E402

# Everything under corpus/ is a story file except the queue, the derived
# indexes, and the spine: `_inbox/` is raw material and never a source;
# `capabilities/` files answer for stories rather than being one; the named
# files are ledgers and profile, not arcs; and `background.md` holds a
# company's context rather than an arc — a stack listed there is a technology
# existing near the user, which `[CAPABILITY-FILE]` says is not evidence of
# anything they did. `_inbox` is tested at any depth, as `corpus_doctor.py`
# tests it.
EXCLUDED_DIRS = ("_inbox", "capabilities")
EXCLUDED_NAMES = (
    "README.md", "LESSONS.md", "BACKLOG.md", "QUEUE.md", "profile.md",
    "through-lines.md", "directions.md", "background.md",
)

GAP = "- [ ]"
FLAG = "🔴"
FLAG_WIDTH = 96
# As wide as a filename `[COVERS]` could give: the example ships `pg_dump` as
# an alias, so an underscore is a slug shape a reader will copy.
CAPABILITY_REF = re.compile(r"capabilities/[A-Za-z0-9_.-]+\.md")

# One token, no YAML structure inside it. `- foo: bar` is a mapping and not a
# term; a quoted or multi-word item is a shape this grammar does not read. `#`
# is allowed mid-token (`c#`): a comment only starts after whitespace, which
# the token already excludes.
TERM = re.compile(r"^[^\s:\[\]{},\"']+$")
KEY_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):(.*)$")
INLINE_LIST = re.compile(r"^\[(.*)\]$")
BLOCK_ITEM = re.compile(r"^(\s*)-\s*(\S.*)$")


class CorpusFormatError(Exception):
    """A frontmatter block is not readable. Never guessed past."""


def corpus_files(corpus: Path) -> list[Path]:
    """Every *.md in the corpus, sorted."""
    return sorted(p for p in corpus.rglob("*.md") if p.is_file())


def vetted_files(corpus: Path) -> list[Path]:
    """Every corpus file outside `_inbox/` — the gap and flag universe.

    Wider than `story_files`: the spine files carry gaps too. Narrower than
    `corpus_files`: a pasted draft's checkboxes are somebody else's to-do
    list, and a flag in unvetted material is not a corpus flag.
    """
    return [p for p in corpus_files(corpus)
            if "_inbox" not in p.relative_to(corpus).parts]


def is_story_file(path: Path, corpus: Path) -> bool:
    rel = path.relative_to(corpus)
    if any(part in EXCLUDED_DIRS for part in rel.parts[:-1]):
        return False
    return path.name not in EXCLUDED_NAMES


def story_files(corpus: Path) -> list[Path]:
    return [p for p in corpus_files(corpus) if is_story_file(p, corpus)]


def frontmatter_lines(path: Path) -> list[str] | None:
    """The file's frontmatter lines, or None when it has no block.

    A block that opens and never closes is not "no block": it is one that
    could not be read, and it raises rather than reading as empty.
    """
    text = path.read_text()
    parts = at.split_frontmatter(text)
    if parts is None and text.replace("\r", "").split("\n")[0].rstrip() == "---":
        raise CorpusFormatError(f"{path}: frontmatter opens with --- and never closes")
    return None if parts is None else parts[0]


def _term(raw: str, key: str, path: Path) -> str:
    term = raw.strip().lower()
    if not TERM.match(term):
        raise CorpusFormatError(
            f"{path}: {key}: {raw.strip()!r} is not a term — one bare token per item, "
            "no colon, no quotes, no spaces")
    return term


def term_list(fm_lines: list[str], key: str, path: Path) -> list[str] | None:
    """The normalised term list under `key`, or None when the key is absent.

    Two shapes and nothing else: `key: [a, b]` on one line, or `key:` followed
    by `- term` items. Exact match after strip().lower() — aliases live in a
    capability file's `covers:` and nowhere else, so nothing here is fuzzy.
    """
    for raw in fm_lines:
        m = KEY_LINE.match(at.strip_comment(raw))
        if not m or m.group(1) != key:
            continue
        rest = m.group(2).strip()
        if not rest:
            break
        inline = INLINE_LIST.match(rest)
        if not inline:
            raise CorpusFormatError(
                f"{path}: {key}: {rest!r} is a scalar, not a list")
        items = [s for s in inline.group(1).split(",") if s.strip()]
        return _dedupe(_term(s, key, path) for s in items)
    lines = at.block(fm_lines, key)
    if lines is None:
        return None
    out = []
    indent = None
    for line in lines:
        m = BLOCK_ITEM.match(line)
        if not m:
            raise CorpusFormatError(
                f"{path}: {key}: {line.strip()!r} is not a list item")
        # One flat list. An item deeper than the first is a nested structure,
        # which is not a term.
        if indent is None:
            indent = m.group(1)
        elif m.group(1) != indent:
            raise CorpusFormatError(
                f"{path}: {key}: {line.strip()!r} is nested — one flat list of terms")
        out.append(_term(m.group(2), key, path))
    return _dedupe(out)


def _dedupe(terms) -> list[str]:
    out: list[str] = []
    for t in terms:
        if t not in out:
            out.append(t)
    return out


def universe(corpus: Path) -> dict[str, list[Path]]:
    """-> {term: [story files naming it]}, from every `technologies:`."""
    out: dict[str, list[Path]] = {}
    for path in story_files(corpus):
        fm = frontmatter_lines(path)
        if fm is None:
            continue
        for term in term_list(fm, "technologies", path) or []:
            out.setdefault(term, []).append(path)
    return out


def capability_files(corpus: Path) -> list[Path]:
    return sorted(p for p in (corpus / "capabilities").glob("*.md")
                  if p.name not in EXCLUDED_NAMES)


def coverage(corpus: Path) -> set[str]:
    """-> {term} answered for by some capability file, aliases included."""
    out: set[str] = set()
    for path in capability_files(corpus):
        fm = frontmatter_lines(path)
        if fm is None:
            continue
        out.update(term_list(fm, "covers", path) or [])
    return out


def uncovered(corpus: Path) -> list[tuple[int, str, list[Path]]]:
    """-> [(count, term, [paths])], most-named first, then alphabetical.

    No threshold. A grep over prose needs one, because a passing mention and a
    claim look identical there; a `technologies:` entry is a deliberate
    declaration, so every one of them is worth listing.
    """
    covered = coverage(corpus)
    rows = [(len(paths), term, paths)
            for term, paths in universe(corpus).items() if term not in covered]
    return sorted(rows, key=lambda r: (-r[0], r[1]))


def untagged(corpus: Path) -> list[Path]:
    """-> [story files with no `technologies:` key].

    `technologies: []` is a declaration — this arc evidences none — and is not
    listed. A file with no frontmatter block has no key either, and is.
    """
    return _without_key(story_files(corpus), "technologies")


def uncovering(corpus: Path) -> list[Path]:
    """-> [capability files with no `covers:` key].

    Such a file answers for nothing, so every term it was written for lands
    in the queue as uncovered — the twin of `untagged`, checking `[COVERS]`.
    """
    return _without_key(capability_files(corpus), "covers")


def _without_key(paths: list[Path], key: str) -> list[Path]:
    out = []
    for path in paths:
        fm = frontmatter_lines(path)
        if fm is None or term_list(fm, key, path) is None:
            out.append(path)
    return out


def seeds(corpus: Path) -> list[Path]:
    inbox = corpus / "_inbox"
    if not inbox.is_dir():
        return []
    return [p for p in sorted(inbox.glob("*.md")) if p.name != "README.md"]


def gaps(corpus: Path) -> list[tuple[int, Path]]:
    """-> [(open gap count, path)] over every vetted file, most first."""
    rows = []
    for path in vetted_files(corpus):
        n = sum(1 for line in path.read_text().split("\n") if line.startswith(GAP))
        if n:
            rows.append((n, path))
    return sorted(rows, key=lambda r: (-r[0], str(r[1])))


def flagged(corpus: Path) -> list[tuple[Path, int, str]]:
    """-> [(path, line number, text)] for every flagged open gap."""
    out = []
    for path in vetted_files(corpus):
        for i, line in enumerate(path.read_text().split("\n"), 1):
            if line.startswith(GAP) and FLAG in line:
                out.append((path, i, line))
    return out


def forward_pointers(corpus: Path) -> list[str]:
    """-> [cited capabilities/<slug>.md paths with no such file].

    A story citing a capability file that isn't written yet marks a file worth
    opening, not an error — `[CAPABILITY-HARVEST]`.
    """
    cited: set[str] = set()
    for path in story_files(corpus):
        cited.update(CAPABILITY_REF.findall(path.read_text()))
    return sorted(ref for ref in cited if not (corpus / ref).is_file())


def _rel(path: Path, corpus: Path) -> str:
    return str(path.relative_to(corpus))


def report(corpus: Path) -> str:
    out: list[str] = []
    say = out.append

    say("UNEXTRACTED SEEDS — corpus/_inbox/")
    unextracted = seeds(corpus)
    for path in unextracted:
        say(f"    {path.name}")
    if not unextracted:
        say("    (none)")

    say("\nOPEN GAPS PER STORY")
    total = 0
    for n, path in gaps(corpus):
        total += n
        say(f"  {n:3d}  {_rel(path, corpus)}")
    say(f"  {total:3d}  TOTAL")

    rows = flagged(corpus)
    if rows:
        say(f"\nFLAGGED {FLAG}")
        for path, i, line in rows:
            say(f"  {f'{_rel(path, corpus)}:{i}:{line}'[:FLAG_WIDTH]}")

    say("\nFORWARD CAPABILITY POINTERS — cited by a story, file not yet written")
    missing = forward_pointers(corpus)
    for ref in missing:
        say(f"    {ref}")
    if not missing:
        say("    (none — every cited capability file exists)")

    say("\nUNCOVERED TECHNOLOGIES — named in a story's technologies:, "
        "covered by no capability file")
    uncov = uncovered(corpus)
    for n, term, paths in uncov:
        say(f"  {n:3d}  {term}")
        for path in paths:
            say(f"         {_rel(path, corpus)}")
    if not uncov:
        say("    (none — every named technology is covered)")

    say("\nSTORY FILES WITHOUT technologies:")
    bare = untagged(corpus)
    for path in bare:
        say(f"    {_rel(path, corpus)}")
    if not bare:
        say("    (none — every story file names its technologies)")

    say("\nCAPABILITY FILES WITHOUT covers: — answering for nothing, so their terms sit above")
    blank = uncovering(corpus)
    for path in blank:
        say(f"    {_rel(path, corpus)}")
    if not blank:
        say("    (none — every capability file says what it covers)")

    say("\nCoverage is read from frontmatter: a story's technologies:, a "
        "capability file's covers:.")
    say("Aliases belong in covers: and nowhere else — matching is exact, "
        "lowercased and stripped.")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    corpus = root / "corpus"
    if not corpus.is_dir():
        print(f"no corpus/ under {root}", file=sys.stderr)
        return 2
    try:
        print(report(corpus))
    except CorpusFormatError as e:
        print(f"could not read the corpus: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
