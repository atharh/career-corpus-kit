# Backlog

Things worth building that aren't built. Not a roadmap — a place ideas stop rotting in a chat
log. Newest at the bottom; delete rather than mark done.

This file holds only work that would actually be picked up, plus decisions still open.
Settled calls and deliberate declines live in `DECISIONS.md`; promote-pass state in
`PROMOTE.md`.

---

## Live mode for the application-lane evals

**Deferred 2026-08-12**, when the application fixture and tier 3 shipped. Tier 3 is offline
only, and offline mode has the same limit the trip-wires already admit to: **it pins the
example, it does not test the skills.** Every tier-3 assertion would still pass if `apply`'s
inbox rule were deleted tomorrow, because the committed fixture would not change.

Tier 2 solved this with a live mode that renders fresh from `examples/corpus/` and asserts
over the output. The analogue here is harder in one specific way: a live application run has
to *write a folder*, across three skills and several turns, from a starting state that is a JD
and an inbox file rather than a one-line prompt. The interesting assertions — did `prep`
promote a recruiter's claim, did `fit.md` name the gap or paper over it — are exactly the ones
that need the live run.

**Shape of a fix:** seed a temp dir with `examples/corpus/`, the fictional `jd.md` and the
recruiter note, run `prep` against it, and reuse the tier-3 trip-wire patterns unchanged. The
conformance half stays offline; only the trip-wire half needs a model. Keep it disposable and
optional until it shows a stable signal distinct from the fixture.

**Why deferred:** the fixture had to exist first, and the offline half is what stops the
example itself rotting, which is the failure that has actually happened in this repo.

---

## Open: is a corpus's own tooling part of the promote intake?

**Raised 2026-08-17, no call made.** `CLAUDE.md` fixes the promote intake at three files — the
lesson log, the corpus repo's instructions, the work backlog. A script sitting at a corpus
repo's root is in none of them, so a pass can read a *rule* about a checker while the checker
itself stays invisible. That is not hypothetical: the checker `tools/application_status.py`
ports from was in exactly that position, and it reached the kit because someone raised it by
hand rather than because a pass found it.

Two readings, and they are genuinely different bets:

1. **Working as intended.** The intake is rules; tooling is a different artifact and gets
   raised deliberately, which is what happened here and it worked.
2. **A blind spot.** The application lane is where several of these rules actually get
   *enforced*, so a pass that never sees the enforcement keeps porting rules while the local
   implementation diverges underneath them.

Widening the intake is not free: a script is long, it drags the corpus's own paths and
vocabulary into the session transcript, and **scoping the read is the privacy control** —
which is the argument `CLAUDE.md` makes for keeping the intake narrow in the first place. Any
version of this needs an answer to that, not just an extra row in the table.

**Reopens on:** a second piece of corpus tooling that a pass should have seen and didn't.

