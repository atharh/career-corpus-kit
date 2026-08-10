> ⚠️ **FICTIONAL EXAMPLE.** Annotates `resume.md` against the fictional corpus in `../corpus/`.

# What the corpus refused to let the résumé say

This is the part that's hard to show any other way. A résumé rendered from a corpus doesn't
look special — it looks like a normal, slightly understated résumé. **The value is in what
isn't there**, and why.

Each row is a line the model would happily have written, and the specific corpus line that
stopped it.

| The tempting version | What shipped | What stopped it |
|---|---|---|
| "Cut pipeline runtime by 80%" | "roughly halving runtime" | `facts_disputed` in `batch-window.md` — the résumé said 80%, Sam said "about half", and Sam's own memory is the only source either number has. Neither value renders. What shipped is the floor both sources agree on, and only because Sam settled it in a `RENDERING DECISION` — the model doesn't get to pick which contested number to say. |
| "Drove org-wide adoption of incremental processing" | "Two other teams later adopted the same pattern" | A ceiling in Sam's words: *"Two teams took it. Not the org. There are still batch jobs doing the exact same dumb thing today."* |
| "Identified and resolved a critical architectural flaw" | "Diagnosed and fixed a nightly dispatch pipeline…" | A rejected reading, recorded as the model's error. Sam: *"I didn't spot a blind spot, I got woken up by it four times. I fixed the thing that was hurting me."* |
| "Led the team responsible for six services" | "Led a rebuild of the on-call rotation" | A ceiling in `tidewater/background.md`: Sam has never had reports. *"I led the work. There's a difference and an EM interviewer will find it in about nine seconds."* |
| "Reduced on-call load 70% through rotation redesign" | "pages fell from 31 in Q1 2023 to 9 in Q4" | Sam blocked the causal claim themselves: the alert cleanup did the work, and the rotation change was reversed. The number is real; the attribution wasn't. |
| "Architected a data platform for clinical analytics" | "Built and owned the nightly export and transform" | Two things at once — an `anachronisms_corrected` block (it was a cron job and a second Postgres; *data mesh* postdates the work by three years) and an attribution ceiling (the schema was a contractor's). |
| "Kubernetes expertise" | "deploys to Kubernetes" | A ceiling in `profile.md`: *"I use Kubernetes. I have never run a cluster."* |

## The point

Six of those seven rejected lines are things Sam **could** have gotten away with on paper. Every
one of them is a landmine in the room, because each invites a follow-up Sam can't answer:
*80% of what, measured how? Which teams? What did you architect about the schema?*

**The corpus isn't a modesty filter.** It's the record of which claims survive a follow-up
question, written down at a moment when Sam had the context to judge — instead of at 11pm the
night before an application, when they don't.

Worth noting what *did* survive: the 31→9 page reduction, the three-week parallel run, the
contractual 06:00 deadline, "19 of 31 required no human action." Specific, sourced, and
defensible. **The true version is usually the stronger one.** That's not a moral claim, it's a
practical one — vague inflation reads as filler, and precise detail reads as someone who was
actually there.

## What isn't on the résumé at all

**The reversal.** Sam cut the rotation from eight people to five, made the best responders'
lives worse, and reversed it after seven weeks. `oncall-rebuild.md` carries a rendering
decision saying it stays out of the résumé and goes to any interview that asks for a failure —
not because it's embarrassing, but because a bullet has no room to make it land, and half-told
it just looks like a mistake.

That's the corpus doing its actual job: **the strongest material in the whole record is
material a résumé can't hold.**
