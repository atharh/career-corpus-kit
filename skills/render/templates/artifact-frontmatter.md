---
artifact: <resume | cover-letter | interview-prep | study-pack-section>
application: <company>-<role>   # optional — absent on a baseline, which belongs to no application
lifecycle: <baseline | in-flight | submitted>
generated: <YYYY-MM-DD>
corpus_pin: <the corpus commit this render read>
sources:                        # the files this drew on, repo-root-relative
  - corpus/<company>/<story>.md
  - applications/<company>-<role>/jd.md
submitted:                      # optional — present only once lifecycle is `submitted`
  date: <YYYY-MM-DD>
  as: <what actually went out — filename, format, or "pasted into the form">
  sha256: <only when the sent bytes are NOT in git — see apply's `[PIN-NOT-ARCHIVE]`>
---

<The frontmatter block above is the whole template. Every rendered artifact carries it —
`render`'s résumés and cover letters, `prep`'s pack files alike. The body below the block is
whatever [REFERENCE.md](../REFERENCE.md) says that artifact's shape is.>

<Each slot records something that cannot be reconstructed later: which corpus a render read,
which files it drew on, what actually went out. Nothing here is a rollup of state held
elsewhere. Lifecycle is the exception and it is not derived either — it is a property of this
file, and it decides what may be done to it (the interview skill's surface-the-change rule
`[MARK-DONT-FIX]`): a `submitted` artifact is frozen evidence of what a reader saw, an
`in-flight` one is re-rendered on request with the diff shown, a `baseline` one is refreshed as
its own deliberate act.>

<This block is repository-only, because raw Markdown is not a sending format: what goes out is
a PDF, a DOCX, or body text pasted into a form — never this file itself. When handing over
paste-ready text, hand over the body alone; the block above never reaches a reader.>

<`sha256` identifies the sent bytes; it does not keep them, and it is the fallback rather than
the default. Keeping them is `git add -f <what went out>` at the freeze, because a generated
artifact cannot be rebuilt — PDF and DOCX writers stamp a creation time, so the same Markdown
gives different bytes every run. Where the bytes are in git, `git show <commit>:<path>` answers
what the hash answered and answers what it never could, so the hash is left out rather than
duplicated. Write it only when the bytes genuinely cannot be tracked — sent from another
machine, a portal that kept no copy, a file the user declines to commit. See apply's
`[PIN-NOT-ARCHIVE]`, and `[PIN-NOT-SELF]` for the pasted-text case, where the hash must never
be taken over the file that holds it.>
