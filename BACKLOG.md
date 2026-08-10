# Backlog

Things worth building that aren't built. Not a roadmap — a place ideas stop rotting in a chat
log. Newest at the bottom; delete rather than mark done.

---

## Pack staleness detection

**Deferred 2026-08-10.** A rendered artifact is a snapshot of a corpus that keeps moving, and
nothing currently notices when the two diverge.

**The concrete case that raised it:** a résumé claim was withdrawn from a corpus during an
interview session, and an interview prep pack written weeks earlier still carried it. It was
caught by hand, because someone happened to be editing the file that day. Nothing would have
caught it otherwise.

**The shape of a fix**, roughly:

- Rendered packs record which corpus files and which specific claims each section drew on,
  probably in frontmatter.
- Re-running `prep` (or a `--check` mode) reports what changed underneath: withdrawn claims,
  numbers whose ceilings moved, stories that gained a `RENDERING DECISION` since.
- Loudest signal reserved for **withdrawn or shrunk** claims, since those are the ones that
  turn into a false statement in a room rather than merely a stale one.

**Why it's deferred rather than dropped:** regenerating a pack from scratch before each
interview is cheap and mostly solves it. The failure only bites when a pack is reused for a
later round, or when several applications are live at once and a correction lands in the
middle. That's a real scenario, just not the common one.

**Applies to `render` output too**, not only `prep` — a tailored résumé sitting in
`applications/` has exactly the same problem.

---

## Example application folder

**Deferred 2026-08-10**, when `apply` shipped. `examples/` shows corpus in and artifacts out,
but not the folder an application actually accumulates — the JD, the fit check, the dated log,
the inbound material. That folder is where most of the new skill's shape lives, and reading it
would teach it faster than the SKILL.md does.

**Why deferred:** it means fabricating a job posting *and* a recruiter email, in a repo whose
first rule is "never invent". The existing example corpus is bounded by a per-file FICTIONAL
banner and its own tree; a fake posting attributed to a fake company is a step further, and a
fake recruiter email is a step further again. Worth doing carefully, not quickly.

**If built:** the `fit.md` is the file to get right — specifically a requirement the example
corpus genuinely cannot back, ending in "don't apply yet". A fit check where everything lines
up teaches the opposite of the point.
