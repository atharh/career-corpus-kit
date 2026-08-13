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

## Declined — do not re-propose

A rule rejected on purpose leaves no trace in the skills, so without this list every pass
re-argues it — and the dangerous case is a deliberate divergence quietly reverted to match
the corpus that suggested it.

- **"One structural slot per company for the role itself."** The kit deliberately allows more
  than one: role and scope bullets are structural, don't compete for outcome slots, and a
  promotion or role change inside one company needs a second. The divergence is intentional.

- **A supersession trail — keeping the earlier answer when a later one replaces it** (declined
  2026-08-12). Proposed "because the shape of the drift is itself evidence"; it fails the
  kit's own leave test — drift evidence is calibration about one person, the canonical shape
  `CLAUDE.md` names as the thing not to port — and it earns nothing at the point of use: a
  render needs the current value, and the superseded one reaches no artifact ever. **What was
  real in it shipped instead:** the self-correction carve-out in `[MARK-DONT-FIX]` case a — a
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

- **The recurrence-gated version of *absent* vs. *unwritten* is still sitting in the corpus.**
  The kit shipped the ungated version in release B — `fit.md` records `no-corpus-evidence`,
  never `missing`, and asks — because the kit-internal argument stands on its own: the kit
  never takes a call that is the user's, and which of *absent* and *unwritten* applies is
  exactly such a call. A pass reading the corpus entry will see the kit apparently
  disagreeing; it is resolved, not divergent.
