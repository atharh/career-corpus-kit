> ⚠️ **FICTIONAL EXAMPLE.** Invented person, invented evidence. Shows the corpus format only.

# Through-lines — Sam Rivera

Patterns that span the career and belong to no single story. Every instance carries a file
citation. Every through-line carries a **where it doesn't hold** section — a pattern with no
counter-examples is hagiography, not evidence.

⚠️ **These are derived, and they are not a lens.** A through-line describes what already
happened; it never gets to pick how a story is framed. The job description does that.

---

## 1. Prove it in parallel before you cut over

**Whose claim:** Claude's, from two instances. **Sam's reaction, 2026-03-02:** *"I'll take that
one. Though it's mostly that I'm bad at arguing and good at waiting."*

- Ran the incremental pipeline **alongside** the old one for three weeks, diffing output nightly,
  rather than winning the design argument. Two real bugs surfaced before cutover.
  (`tidewater/batch-window.md`)
- Categorised **every page from a full quarter** before changing a single alert rule, instead of
  deleting the obviously-noisy ones on instinct. (`tidewater/oncall-rebuild.md`)

### Where it doesn't hold

**It failed exactly where it was most needed.** The on-call headcount cut — the one change with
consequences for people rather than systems — got no parallel run, no trial, no reversibility
plan. It shipped on the strength of a good argument in a room, and had to be reversed seven
weeks later. (`tidewater/oncall-rebuild.md`)

**That's the honest shape of this pattern: it's a habit about systems that Sam had not, at that
point, transferred to decisions about people.** They say they have now. There is exactly one
data point since, and it isn't extracted, so the corpus can't back that yet.

---

## 2. ~~Simplifier — always chooses the boring architecture~~ — WITHDRAWN 2026-03-02

Claude proposed this from the nightly-export decision and the incremental-processing decision.
**Sam declined it**, and the reasoning is worth more than the pattern was:

> *"Two examples where the boring thing was also the right thing isn't a philosophy, it's two
> examples. I've also spent four months on a Kafka thing at Bellhaven that we deleted, which
> you don't know about because I haven't told you about it yet. Ask me again after that one."*

**Kept visible so a future session doesn't rediscover it from the same two files.** The
Kafka story is in the backlog; if it lands and shows the same instinct, this can come back —
with the counter-example built in from the start.

---

## Gaps

- [ ] **Two companies, three stories. That is not enough for a third through-line** and any
      that appears now is pattern-matching on a small sample. Revisit after Bellhaven 2017–2018
      is extracted.
