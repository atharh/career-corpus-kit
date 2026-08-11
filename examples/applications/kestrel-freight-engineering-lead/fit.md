---
jd: jd.md
checked: 2026-04-07
corpus_pin: a3f19c2
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented posting, invented candidate. Checked
> against the fictional corpus in `../../corpus/`. Never a source.

# Fit — Kestrel Freight Network, Engineering Lead, Dispatch Data

## Requirements

| Requirement | Evidence state | Corpus evidence | Their call |
|---|---|---|---|
| "Own the reliability of the overnight dispatch build against a contractual 05:00 hand-off" | backed | `corpus/tidewater/batch-window.md` — same shape, same stakes: a nightly pipeline against a contractual 06:00 delivery, degraded to 3h10, diagnosed as design rather than volume | lead with it |
| "Without a customer-visible break in service" | backed | `corpus/tidewater/batch-window.md` — three-week parallel run, nightly output diff, two watermark bugs caught before cutover | lead with it |
| "An on-call rotation the group currently dreads" | backed | `corpus/tidewater/oncall-rebuild.md` — 31 out-of-hours pages in Q1 2023 to 9 in Q4; 19 of 31 needed no human action | lead with it, reversal included |
| "Set technical direction with … groups you will not own" | backed | `corpus/tidewater/batch-window.md` — the scheduler belonged to Platform Infra, who objected and were right; agreement came from a parallel run, not from authority | lead with it |
| "Strong SQL and Postgres" | backed | `corpus/profile.md`; `corpus/bellhaven/reporting-migration.md` | — |
| "Hiring, growth" — as mentoring | thin | `corpus/tidewater/background.md` — mentored two juniors. Real, and it is mentoring. It is not owning anyone's growth, and it folds the moment somebody asks what happened at review time | answer it as mentoring; do not upgrade it |
| "Operate the group's Kubernetes footprint" | thin | `corpus/profile.md` ceiling, theirs: *"I use Kubernetes. I have never run a cluster."* Deploys to it; has never operated one | name the ceiling before they ask |
| "Line-manage a team of four to six engineers … performance and growth conversations you personally held" | no-corpus-evidence | none | **applying anyway, gap named** — 2026-04-08 |
| "Deep production Kafka experience — you have moved a real workload onto it" | no-corpus-evidence | none | **interview session booked** — 2026-04-08 |

## The two blanks are blank for opposite reasons, and that call is not this file's

`no-corpus-evidence` says what the corpus can see and stops there. It does not say the user has
never done the thing. Two rows above are both blank and they are not the same situation:

- **Line management.** The corpus does not merely fail to evidence it — it forecloses it.
  `corpus/tidewater/background.md` carries a ceiling in their own words: *"I keep seeing 'led
  the team' in drafts. I led the work."* `corpus/profile.md` records eleven years with no
  reports. This one reads as genuinely **absent**.
- **Kafka.** `corpus/through-lines.md` carries a withdrawn pattern, and inside the withdrawal is
  a sentence about four months of streaming work at a previous employer that was deleted and has
  never been extracted. So there may be material here and there is certainly no evidence. This
  one reads as plausibly **unwritten**, and the response to unwritten is an interview session,
  not a decision about whether to apply.

Which of those two each blank actually is, is a call about somebody's career. Both are put here
as questions.

## Discarded as boilerplate

- **"8+ years building and running production backend systems."** Met, and not a real filter.
- **"A degree in a technical field or equivalent experience."** Met.
- **"A genuine passion for logistics."** Not a requirement. Nobody is checking.
- **"Thrives in ambiguity and wears many hats."** Not a requirement either, though the second
  half is a mild signal about the size of the group.

Disagree with any of these and the row comes back.

## What these judgements rest on

Every `backed` row above was read off a story file, not off a résumé. **One row is weaker than
it looks:** the mentoring row rests on a baseline résumé bullet — *"mentored two junior
engineers through their first year"* — and no story file decompresses it. So "thin" here is a
statement about the corpus, not necessarily about what happened. If mentoring turns out to
matter, that bullet needs a session behind it before it is worth saying out loud.

## The read

The systems half of this posting is the closest match in the corpus to anything Sam has done —
same deadline shape, same overnight build, same migration-without-breakage problem, and the
direction-without-authority requirement is answered by a story where exactly that happened.

The people half is not there at all. This is a lead role and the posting is unambiguous about
what that means: performance and growth conversations, personally held. Nothing adjacent covers
that. The mentoring row is the obvious thing to reach for and it must not be stretched to cover
it — it survives one follow-up question and no more, and when it goes, the four strong rows
above it get discounted along with it.

**The read is: don't apply yet.** Two routes out of that, and both are the user's to pick. Book
an interview session on the streaming work first, which may turn the Kafka row from blank into
`backed` and is worth doing whatever happens here. And decide, deliberately, whether to go at a
lead posting with no line-management evidence — which is a fine thing to do with the gap named
and an answer prepared, and a bad thing to do by hoping it does not come up.
