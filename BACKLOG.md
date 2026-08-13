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

## The examples are all engineering

**A positioning call, not a task — still undecided 2026-08-12**, and nothing downstream should
be planned until it is made. The metadata promises a general career tool — keywords name no
discipline, the description says "your work history" — and `examples/` delivers a backend
engineering one: one invented engineer, two invented backend companies, an application fixture
for a staff engineering role. The skills themselves are nearly clean (re-counted 2026-08-12:
about a dozen lines of engineering vocabulary, mostly illustrative — an afternoon to
neutralise, not a rewrite). The concentration is in `examples/`, which is also the first thing
a reader opens.

Two options, and they are different products:

- **Narrow the positioning.** Say in the README and the plugin description that this is built
  for technical careers. An afternoon of wording. Honest, and it stops disappointing people
  who don't fit; the cost is choosing a smaller audience deliberately.
- **Build one credible second-domain corpus.** One discipline, fabricated to the standard of
  the existing fixture, plus the vocabulary sweep above. **It has to be convincing or it is
  worse than the current state** — a thin example in a second discipline reads as a claim the
  kit can't back. Explicitly *not* a gallery of shallow examples across four fields.

**Why it can't be delegated:** it is a question about who this is for. Both answers are
defensible on the material, so nothing in the repo decides it. Decide when audience expansion
becomes real work.

---

## Port the corpus's `verify` skill, once it proves out

**Waiting on corpus-side evidence, noted 2026-08-13.** A live corpus built a repo-local
skill that reads story files like a technical interviewer and checks publicly checkable
technical claims against the public record, with citations — the batch counterpart of
`interview`'s `[CHECK-THE-CLAIM]`, which ported in the same pass. The skill itself was parked
by its author with explicit proof criteria (multiple company directories covered, each finding
class through an accept/amend/reject loop, no accepted correction reverted). Propose the port
when a later promote pass finds those criteria met; port the design, not the implementation's
paths.
