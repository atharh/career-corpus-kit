# Promote passes

Maintainer state for the promote workflow — see `CLAUDE.md` for how a pass runs. Two things
live here and nothing else: the cursor the next pass diffs from, and the declines it must not
re-propose. Ported rules need no record — they're in the skills. Landed release notes don't
either — git keeps them.

## Cursor

**Reviewed up to corpus commit `81490e1` (2026-08-14), lesson log, repo instructions and work
backlog diffed from the prior cursor; the capability files' own design sections read as intake
because they were addressed to this pass.** Start the next pass from
`git log -p 81490e1..HEAD -- <intake paths>`. Advance this sha when a pass finishes, and don't
replace it with a date — a date can't be diffed, and it misses amendments to older entries.

**The cursor did not move on 2026-09-07.** That pass ported `[TEXT-LAYER]` from a brief a
corpus session sent directly; it read no intake file, so it attests to nothing about the lesson
log between `81490e1` and now. A pass that lands a rule without reading the intake must leave
this sha alone — advancing it would mark a range reviewed that no one has read, which is the
one failure this cursor exists to prevent.

## Declined — do not re-propose

A rule rejected on purpose leaves no trace in the skills, so without this list every pass
re-argues it — and the dangerous case is a deliberate divergence quietly reverted to match
the corpus that suggested it.

- **`display: inline-block` on a bullet's `::before` silently reverts the glyph to vector
  paths** (declined 2026-09-07). Offered as a warning to carry alongside `[TEXT-LAYER]`, and it
  did cost the reporting session real time. It **did not reproduce here**: a probe using
  `display: inline-block` with an explicit width still mapped U+2022 in its `ToUnicode` table.
  So the cause is something else in that build — a font, a version, another declaration — and a
  mechanism the kit cannot reproduce is not justifiable by reading the kit alone. **What was
  real in it shipped instead:** `[TEXT-LAYER]`'s "verify by reading the extracted text, never by
  eye," which is the durable half and covers this case and every sibling of it. Don't re-add the
  specific claim without a reproduction.

- **"One structural slot per company for the role itself."** The kit deliberately allows more
  than one: role and scope bullets are structural, don't compete for outcome slots, and a
  promotion or role change inside one company needs a second. The divergence is intentional.

- **A supersession trail — keeping the earlier answer when a later one replaces it** (declined
  2026-08-12). Proposed "because the shape of the drift is itself evidence"; it fails the
  kit's own leave test — drift evidence is calibration about one person, the canonical shape
  `CLAUDE.md` names as the thing not to port — and it earns nothing at the point of use: a
  render needs the current value, and the superseded one reaches no artifact ever. **What was
  real in it shipped instead:** the self-correction carve-out in `[MARK-DONT-FIX]` — a
  self-correction is not a conflict, and the tell is whether the user marks the change
  themselves. **Don't re-derive the trail** from `compact`'s keep-list: that rule preserves a
  supersession trail *if one exists*; it is not evidence that anything should write one.

- **The 350–450 word target for cover letters** (declined 2026-08-13). The corpus's "What a
  cover letter is for" section sets it as "a good target for these" — *these* being one
  person's letters, which is the tell: it is calibration, not method. The kit keeps the wide
  form range (~350–600, ceiling not target, shorter reads stronger) and leaves the tighter
  number where preferences live. The rest of that corpus section ported in the same pass —
  the Wednesday test, don't-restate-the-résumé, practical facts in the close — so a future
  pass seeing the kit diverge only on the number is seeing a decision, not an omission.

- **Worktree-per-change git discipline** (declined 2026-08-13). The corpus's repo instructions
  grew a full concurrency protocol — one worktree per change, `--ff-only` merges, explicit-path
  staging — because several sessions commit to that repo at once. The kit's skills prescribe no
  git workflow at all, and the case for adding one rests entirely on one repo's collision
  pattern; a single-session corpus never hits it. Revisit only if concurrent-session collisions
  prove to be a class, not an incident.

- **The baseline-letter "general thesis" clause is resolved upstream, not open.** The corpus's
  work backlog still carries as *open* a proposed clause giving a baseline letter "the
  strongest general answer to why this role family" as its thesis. The kit answered the same
  gap differently in 1.16.10: a baseline letter is a summary-led scaffold — no why-them, no JD
  thesis, stories as one-clause flashes, flagged if about to be sent unedited. A future pass
  seeing the corpus clause unshipped is seeing a design superseded by a stronger one, not an
  omission.

- **A PDF rebuilt in the same commit as its Markdown** (declined 2026-08-14). The corpus's repo
  instructions require it, and the reasoning is sound *there* — a stale PDF beside updated
  Markdown is a wrong artifact looking finished. But the rule presumes a build script and a
  commit workflow, and the kit ships neither: render's workflow already says to rebuild when a
  PDF pipeline is present, which is all the kit can honestly promise about tooling it doesn't
  provide. Same family as the declined worktree discipline: the kit prescribes no git workflow.

- **"Check the shipped artifact before believing a status line in `tasks/`"** (declined
  2026-08-14). Real defect, wrong scope: it is hygiene for one repo's private work-tracking
  files, which a stranger's corpus won't have. The kit-side mirror of the same failure is
  already covered by its own `CLAUDE.md` — read the clone, not the cache, and pin a sha rather
  than trusting a note.

- **PyYAML as a dependency of a kit tool** (declined 2026-09-03, in the pass that ported
  `technologies:` / `covers:` and `tools/corpus_status.py`). The corpus's version of the tool
  imports it; the kit's reads the two list fields with the same one-token-per-item grammar
  `appthread.py` uses, because that file already states the decision — a kit cannot assume a
  library on a stranger's machine — and `./evals/run.sh` promises nothing but `python3`. The
  strict-YAML rule ported as template guidance plus a static check that runs when PyYAML is
  present and skips itself otherwise. A future pass seeing the corpus tool import `yaml` is
  seeing a decision, not an omission.

- **`background.md` as a story file for the status tool** (declined 2026-09-03). The corpus's
  tool counts every non-spine file; the kit's excludes background files. A background file holds
  a company's context, not an arc, and a stack listed there is a technology existing near the
  user — the exact thing `[CAPABILITY-FILE]` says is not evidence — so asking it for
  `technologies:` would invite the inventory the field exists to refuse.

- **The cursor was not advanced by the 2026-09-03 pass.** That pass was a brief-driven port of
  one design, not a diff of the three intake paths from `81490e1`; the next full pass still
  starts there.

- **The recurrence-gated version of *absent* vs. *unwritten* is still sitting in the corpus.**
  The kit shipped the ungated version in release B — `fit.md` records `no-corpus-evidence`,
  never `missing`, and asks — because the kit-internal argument stands on its own: the kit
  never takes a call that is the user's, and which of *absent* and *unwritten* applies is
  exactly such a call. A pass reading the corpus entry will see the kit apparently
  disagreeing; it is resolved, not divergent.
