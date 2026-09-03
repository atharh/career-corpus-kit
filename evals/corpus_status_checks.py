#!/usr/bin/env python3
"""Tier 3b — the corpus status tool. No model, no network, no dependencies.

`tools/corpus_status.py` is the derivation behind `[CAPABILITY-HARVEST]`: the
capability queue is the set of `technologies:` terms no `covers:` line accounts
for, and nothing else. These assertions are what stop the tool from reporting a
clean corpus because it silently stopped reading — each rule it states is
checked to bite on a temp corpus built to break it, and the example corpus is
pinned to what it demonstrates.

Run:  python3 evals/corpus_status_checks.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import corpus_status as cs  # noqa: E402

TOOL = ROOT / "tools" / "corpus_status.py"
EXAMPLE = ROOT / "examples"


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
            print("corpus status: PASS")
            return 0
        print(f"corpus status: FAIL ({len(self.failures)})\n")
        for f in self.failures:
            print(f"  ✗ {f}")
        return 1


# --------------------------------------------------------------------------- #


def story(fm: str, body: str = "\n## Setup\n\nfictional.\n") -> str:
    return f"---\n{fm}\n---\n{body}"


def build(tmp: Path, files: dict[str, str]) -> Path:
    """Write a corpus under tmp/corpus from {relative path: text}."""
    corpus = tmp / "corpus"
    for rel, text in files.items():
        path = corpus / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (corpus / "capabilities").mkdir(exist_ok=True)
    return corpus


def raises(fn, *args) -> str | None:
    try:
        fn(*args)
    except cs.CorpusFormatError as e:
        return str(e)
    return None


def run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), str(root)], capture_output=True, text=True, timeout=60,
    )


# --------------------------------------------------------------------------- #


def check_set_difference(r: Report) -> None:
    """uncovered = union(technologies) − union(covers), counted and attributed."""
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/one.md": story("title: one\ntechnologies: [kafka, kubernetes]"),
            "a/two.md": story("title: two\ntechnologies:\n  - kafka\n  - terraform"),
            "capabilities/kubernetes.md": story("title: k\ncovers: [kubernetes, k8s]"),
        })
        rows = cs.uncovered(corpus)
        r.check(
            "uncovered is the set difference, most-named first",
            [(n, t) for n, t, _ in rows] == [(2, "kafka"), (1, "terraform")],
            repr(rows),
        )
        r.check(
            "each uncovered term names the story files declaring it",
            rows and sorted(p.name for p in rows[0][2]) == ["one.md", "two.md"],
            repr(rows),
        )
        r.check(
            "a covered term is absent from the queue",
            "kubernetes" not in {t for _, t, _ in rows},
            repr(rows),
        )


def check_covers(r: Report) -> None:
    """Aliases and family files are `covers:` entries — nothing else defines them."""
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/one.md": story("title: one\ntechnologies: [k8s, redis, memcached]"),
            "capabilities/kubernetes.md": story("title: k\ncovers: [kubernetes, k8s]"),
            "capabilities/caches.md": story(
                "title: caches\ncovers:\n  - redis\n  - memcached",
                "\n## The noes\n\nnever ran one.\n"),
        })
        r.check(
            "an alias in covers: covers the term a story used",
            cs.uncovered(corpus) == [],
            repr(cs.uncovered(corpus)),
        )
        r.check(
            "coverage is the union of every covers: list",
            cs.coverage(corpus) == {"kubernetes", "k8s", "redis", "memcached"},
            repr(cs.coverage(corpus)),
        )


def check_normalisation(r: Report) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/one.md": story("title: one\ntechnologies: [ Kafka , kafka, KAFKA ]"),
            "capabilities/kafka.md": story("title: k\ncovers: [KAFKA]"),
        })
        fm = cs.frontmatter_lines(corpus / "a" / "one.md")
        r.check(
            "terms are lowercased, stripped and deduped in order",
            cs.term_list(fm, "technologies", corpus / "a" / "one.md") == ["kafka"],
            repr(cs.term_list(fm, "technologies", corpus / "a" / "one.md")),
        )
        r.check("matching is case-insensitive both sides", cs.uncovered(corpus) == [])
        r.check(
            "a trailing comment on the key line is ignored",
            cs.term_list(["technologies: [a, b]  # why"], "technologies", Path("x")) == ["a", "b"],
        )


def check_untagged(r: Report) -> None:
    """Absent key is untagged; an empty list is a declaration and is not."""
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/absent.md": story("title: absent"),
            "a/empty-inline.md": story("title: e\ntechnologies: []"),
            "a/empty-block.md": story("title: e\ntechnologies:\nstatus: drafted"),
            "a/no-frontmatter.md": "# a heading\n\nno block at all\n",
        })
        names = [p.name for p in cs.untagged(corpus)]
        r.check("a story file with no technologies: key is listed",
                names == ["absent.md", "no-frontmatter.md"], repr(names))


def check_uncovering(r: Report) -> None:
    """A capability file with no `covers:` covers nothing, and says so."""
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/one.md": story("title: one\ntechnologies: [postgresql, airflow]"),
            "capabilities/postgresql.md": story("title: pg\nstatus: opened"),
            "capabilities/legacy.md": "# no frontmatter at all\n",
            "capabilities/README.md": "# index, not a capability file\n",
        })
        names = [p.name for p in cs.uncovering(corpus)]
        r.check("a capability file with no covers: is listed",
                names == ["legacy.md", "postgresql.md"], repr(names))
        r.check("its terms stay uncovered — nothing is inferred from the filename",
                [t for _, t, _ in cs.uncovered(corpus)] == ["airflow", "postgresql"],
                repr(cs.uncovered(corpus)))
        out = run(Path(tmp)).stdout
        r.check("the report has a section for it", "CAPABILITY FILES WITHOUT covers:" in out
                and "capabilities/postgresql.md" in out, out)


def check_story_file_set(r: Report) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        spine = {n: story(f"title: {n}") for n in cs.EXCLUDED_NAMES}
        corpus = build(Path(tmp), {
            **spine,
            "a/background.md": story("title: bg\nscale:\n  engineers: 3"),
            "a/arc.md": story("title: arc"),
            "_inbox/seed.md": story("title: seed"),
            "a/_inbox/nested.md": story("title: nested"),
            "README.md": story("title: readme"),
            "a/README.md": story("title: readme"),
            "capabilities/x.md": story("title: x\ncovers: [x]"),
        })
        names = [str(p.relative_to(corpus)) for p in cs.story_files(corpus)]
        r.check(
            "story files exclude _inbox/ at any depth, capabilities/, README.md, the spine "
            "files and background.md",
            names == ["a/arc.md"],
            repr(names),
        )
        r.check(
            "so the spine and background never show as untagged",
            [p.name for p in cs.untagged(corpus)] == ["arc.md"],
        )


def check_unparsable(r: Report) -> None:
    """A block that cannot be read raises with the path — never reads as empty."""
    p = Path("story.md")
    cases = {
        "a mapping item (`- foo: bar`)": ["technologies:", "  - kafka: streaming"],
        "a scalar value": ["technologies: kafka"],
        "a quoted item": ["technologies:", '  - "kafka"'],
        "a multi-word item": ["technologies:", "  - apache kafka"],
        "a nested list": ["technologies:", "  - kafka", "    - streams"],
    }
    for name, fm in cases.items():
        msg = raises(cs.term_list, fm, "technologies", p)
        r.check(f"{name} raises", msg is not None and "story.md" in msg, repr(msg))
    r.check(
        "an absent key is None, not an error",
        cs.term_list(["title: x"], "technologies", p) is None,
    )
    r.check(
        "a # inside a token is part of the term, not a comment",
        cs.term_list(["technologies: [c#, .net]"], "technologies", p) == ["c#", ".net"],
        repr(cs.term_list(["technologies: [c#, .net]"], "technologies", p)),
    )
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/open.md": "---\ntitle: open\ntechnologies: [kafka]\n\n## never closed\n",
        })
        msg = raises(cs.universe, corpus)
        r.check("a block that opens and never closes raises with the path — it is not "
                "\"no block\"", msg is not None and "open.md" in msg, repr(msg))
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/bad.md": story("title: bad\ntechnologies:\n  - kafka: streaming"),
        })
        r.check(
            "universe() raises rather than skipping the file",
            raises(cs.universe, corpus) is not None,
        )
        proc = run(Path(tmp))
        r.check(
            "the tool exits 2 and names the file when it cannot read the corpus",
            proc.returncode == 2 and "bad.md" in proc.stderr,
            f"exit {proc.returncode}\n{proc.stdout}{proc.stderr}",
        )


def check_forward_pointers(r: Report) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/one.md": story("title: one\ntechnologies: []",
                              "\n- [ ] `../capabilities/airflow.md` — forward pointer\n"
                              "- [ ] `../capabilities/pg_dump.md` — forward pointer\n"
                              "- [ ] `../capabilities/kafka.md` — forward pointer\n"),
            "capabilities/kafka.md": story("title: k\ncovers: [kafka]"),
        })
        r.check(
            "a cited capability file that does not exist is a forward pointer, "
            "underscores included",
            cs.forward_pointers(corpus) == ["capabilities/airflow.md", "capabilities/pg_dump.md"],
            repr(cs.forward_pointers(corpus)),
        )


def check_gaps_and_flags(r: Report) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        corpus = build(Path(tmp), {
            "a/one.md": story("title: one\ntechnologies: []",
                              "\n- [ ] open\n- [x] closed\n- [ ] 🔴 flagged\n"),
            "profile.md": story("title: p", "\n- [ ] one here too\n"),
            "_inbox/draft.md": "# pasted\n\n- [ ] their todo\n- [ ] 🔴 their flag\n",
        })
        rows = cs.gaps(corpus)
        r.check("open gaps are counted per vetted file, most first — _inbox/ stays out",
                [(n, p.name) for n, p in rows] == [(2, "one.md"), (1, "profile.md")], repr(rows))
        flags = cs.flagged(corpus)
        r.check("a flagged open gap is listed with its line number — _inbox/ stays out",
                [(p.name, i) for p, i, _ in flags] == [("one.md", 8)], repr(flags))
        out = run(Path(tmp)).stdout
        r.check("FLAGGED sits between the gap count and the forward pointers",
                0 < out.find("OPEN GAPS") < out.find("FLAGGED 🔴") < out.find("FORWARD CAPABILITY"),
                out)
        r.check("the flagged line is printed with its path and line number",
                "a/one.md:8:- [ ] 🔴 flagged" in out, out)


def check_example_corpus(r: Report) -> None:
    """The example corpus is documentation *and* fixture; pin what it demonstrates."""
    proc = run(EXAMPLE)
    r.check("the tool runs clean over the example corpus", proc.returncode == 0,
            f"exit {proc.returncode}\n{proc.stdout}{proc.stderr}")
    out = proc.stdout
    order = [
        "UNEXTRACTED SEEDS", "OPEN GAPS PER STORY", "FORWARD CAPABILITY POINTERS",
        "UNCOVERED TECHNOLOGIES", "STORY FILES WITHOUT technologies:",
        "CAPABILITY FILES WITHOUT covers:",
    ]
    positions = [out.find(h) for h in order]
    r.check("sections appear in the documented order", all(p >= 0 for p in positions)
            and positions == sorted(positions), repr(list(zip(order, positions))))
    rows = {t: n for n, t, _ in cs.uncovered(EXAMPLE / "corpus")}
    r.check(
        "the example demonstrates an uncovered term beside its forward pointer",
        rows.get("airflow") == 1 and "capabilities/airflow.md" in out,
        repr(rows),
    )
    r.check("postgresql is covered by the example capability file", "postgresql" not in rows, repr(rows))
    r.check("every example story file declares technologies:",
            cs.untagged(EXAMPLE / "corpus") == [], repr(cs.untagged(EXAMPLE / "corpus")))
    r.check("the tool exits 2 with no corpus/ at the root", run(ROOT / "evals").returncode == 2)


def main() -> int:
    print(f"corpus status — {ROOT}\n")
    r = Report()
    check_set_difference(r)
    check_covers(r)
    check_normalisation(r)
    check_untagged(r)
    check_uncovering(r)
    check_story_file_set(r)
    check_unparsable(r)
    check_forward_pointers(r)
    check_gaps_and_flags(r)
    check_example_corpus(r)
    return r.summary()


if __name__ == "__main__":
    sys.exit(main())
