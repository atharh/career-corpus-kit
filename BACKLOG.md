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

