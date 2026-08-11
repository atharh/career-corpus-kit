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
  sha256: <hash of the bytes that went out>
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

<`sha256` identifies the sent bytes; it does not keep them. It settles whether a file still on
disk is the one that went out, and says nothing at all once that file is gone: rendered `*.pdf`
and `*.docx` are git-ignored by default, so keeping the bytes themselves is a separate,
deliberate `git add -f` — the user's privacy call, not this template's.>
