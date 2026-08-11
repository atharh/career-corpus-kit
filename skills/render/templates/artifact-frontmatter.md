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
file, and it decides what may be done to it (the interview skill's rule 11b `[MARK-DONT-FIX]`): a `submitted` artifact is
frozen evidence of what a reader saw, an `in-flight` one is re-rendered on request with the
diff shown, a `baseline` one is refreshed as its own deliberate act.>
