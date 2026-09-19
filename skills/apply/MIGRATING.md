# Apply — migrating a thread that has no `events:` block

A thread opened before the frontmatter existed still has all its events, in prose. Offer to
migrate it when you next touch the folder, and run the migration like this:

- **Find them with the checker first**, rather than one at a time as you happen to open a
  folder: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/corpus_doctor.py"` reports every thread that is
  behind the current guidance, sorted by what blocks what, and writes nothing.
- **Assisted, never automatic.** Propose the block, report what you could not resolve, and let
  the user confirm before writing — report-then-patch, the shape `verify` already uses.
- **The mechanical half only.** Lift the events into `events:` and fold the existing body into
  the collapsed block **verbatim**. Don't rewrite paragraphs into one-liners and don't decide
  what still binds: auto-summarising provenance is a silent lossy edit, and compression is a
  judgement the user makes thread by thread, possibly never for a closed one.
- **Ask for `sent.artifacts`.** Which files an employer received is not on disk anywhere, which
  is the whole reason the block exists. A plausible guess here is indistinguishable from a fact.
- **A log older than the vocabulary is expected to defeat you.** Say which lines you could not
  parse and leave them alone. A confident wrong answer here is worse than an unmigrated thread,
  because the unmigrated one reports itself as unmigrated and this one reports itself as done.
- **Touch `application.md` and nothing else**, so a migration can never collide with a frozen
  artifact, and run it twice safely.
