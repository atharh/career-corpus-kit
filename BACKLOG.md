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
