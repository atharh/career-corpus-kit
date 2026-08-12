# Promote passes

Maintainer state for the promote workflow — see `CLAUDE.md` for how a pass runs. Two things
live here and nothing else: the cursor the next pass diffs from, and the declines it must not
re-propose. Ported rules need no record — they're in the skills. Landed release notes don't
either — git keeps them.

## Cursor

**Reviewed up to corpus commit `e2e2c91` (2026-08-11), lesson log and repo instructions read
in full.** Start the next pass from `git log -p e2e2c91..HEAD -- <intake paths>`. Advance this
sha when a pass finishes, and don't replace it with a date — a date can't be diffed, and it
misses amendments to older entries.

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

- **The recurrence-gated version of *absent* vs. *unwritten* is still sitting in the corpus.**
  The kit shipped the ungated version in release B — `fit.md` records `no-corpus-evidence`,
  never `missing`, and asks — because the kit-internal argument stands on its own: the kit
  never takes a call that is the user's, and which of *absent* and *unwritten* applies is
  exactly such a call. A pass reading the corpus entry will see the kit apparently
  disagreeing; it is resolved, not divergent.
