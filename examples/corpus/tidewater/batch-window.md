---
title: The nightly batch that kept missing its window
company: Tidewater Logistics
role: Software Engineer → Senior Software Engineer
period: 2021-09 – 2022-03 (~6 months, part-time alongside normal work)
status: drafted — good depth; one number still disputed
related:
  - oncall-rebuild.md (same team, a year later; the on-call pain here is what led to that)
facts_vetted:
  - the nightly dispatch job ran ~40 min in 2019 and ~3h10 by mid-2021
  - the 06:00 delivery deadline is contractual, not internal
  - the fix was incremental processing — only re-run partitions whose inputs changed
  - two other teams adopted the same pattern afterwards
  - the scheduler was owned by a different team (Platform Infra), not Sam's
facts_disputed:
  - "runtime after the fix: résumé says **'cut runtime 80%'**; interview 2026-03-02 says
    **'about half, honestly. Maybe a bit better on a good night.'** UNRESOLVED — LEANS HALF.
    Neither value renders on its own. Both sources do agree it came down by *at least* half,
    and Sam has settled that floor in the rendering decision below — that, and nothing above
    it, is what renders until a dashboard turns up."
facts_unvetted:
  - "'we were about six weeks from breaching an SLA' — Sam's recollection of what their EM
    said at the time. No document. Do not put a breach claim in writing."
sources:
  - resume.md (vetted)
  - interview with Sam, 2026-03-02 (vetted)
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented people, invented numbers and quotes.
> Shows the corpus format only — never a source.

## Setup

Tidewater's nightly pipeline turns the day's bookings into dispatch instructions, due to
customers by 06:00. When Sam joined it ran about 40 minutes. By mid-2021 it ran **three hours
ten**, and the failure mode had changed character: a job that overran used to be an annoyance,
and now it was a missed contractual delivery and a morning of phone calls.

Nobody owned "the batch is getting slower." It had degraded a few minutes a month for two
years, which is exactly the rate at which nothing triggers an alarm.

## Beat: the diagnosis nobody wanted to hear

The assumed cause was data volume — bookings had roughly tripled, so of course it was slower.

Sam profiled it instead and found the job re-processed **every** historical partition on every
run, not just the ones whose inputs had changed. Volume wasn't the cause; it was the multiplier
on a design that was wrong from the beginning and cheap enough not to notice at 40 minutes.

**The uncomfortable part, and Sam says it themselves:** *"I'd worked on that job twice before
and never looked at what it was actually doing. I optimised two queries inside a thing that
shouldn't have been running at all."*

## Beat: the fix, and who didn't want it

Incremental processing — track input watermarks per partition, re-run only what changed.

**Platform Infra owned the scheduler and pushed back.** Their objection was reasonable and Sam
still repeats it as reasonable: incremental state means *stale state* when the watermark logic
is wrong, and a silently-stale dispatch file is worse than a late one. A late file gets a phone
call. A wrong file gets a truck to the wrong depot.

What resolved it was not an argument. Sam ran both pipelines in parallel for **three weeks** and
diffed the output nightly — same inputs, both paths, byte-compare the result. Two mismatches
surfaced in week one, both real watermark bugs, both fixed before cutover.

> **Judgment, theirs, worth keeping:** *"They weren't blocking me, they were right. The
> difference between us was that I could prove it and they couldn't disprove it, so the parallel
> run was the only honest way through. I'd have argued for a month otherwise."*

## Outcome

Runtime came down — see `facts_disputed`, the size is unsettled. The pattern (watermark table,
parallel-run harness) was picked up by **two other teams** over the following year.

⚠️ **Ceiling, theirs, 2026-03-02:** *"Two teams took it. Not the org. There are still batch jobs
at Tidewater doing the exact same dumb thing today."* Never render as org-wide adoption.

## What it cost

Six months of evenings-and-edges work alongside a normal roadmap, and Sam is clear it was too
slow: *"if I'd asked for it as actual planned work in month one instead of being precious about
proving it first, it'd have been done in six weeks."*

## ❌ Rejected reading — do not resurrect

**Claude proposed, 2026-03-02, that this was Sam identifying and fixing an architectural flaw
the org had missed — "systems thinking, applied to a blind spot." Sam rejected it:**

> *"That's very flattering and it's backwards. I didn't spot a blind spot, I was handed a pager
> and got woken up by it four times. I fixed the thing that was hurting me. Call it what it is."*

Record it as the model's error. **The honest framing is stronger anyway** — "I fixed the thing
waking me up, then noticed it generalised" is a real engineer; "identified an architectural
flaw" is a LinkedIn post.

## 📌 RENDERING DECISION — 2026-03-02

**The résumé's "80%" comes down or gets sourced.** Sam's own recollection is "about half", and
their recollection is the only source either number has. Render **"roughly halved"** until a
dashboard screenshot turns up. The smaller number is also the safer one in the room: nobody
follows up on "halved a batch job", and "80%" invites "80% of what, measured how?"

## Gaps — the interview queue

- [ ] **Is there a dashboard, a PR description, or a ticket with the real before/after?** This
      is the only thing that settles `facts_disputed`, and it's a lookup, not a memory. Sam
      thinks the Grafana board still exists.
- [ ] **What did the two watermark bugs actually do?** A concrete near-miss caught by the
      parallel run is the best possible answer to "how do you de-risk a migration", and right
      now it's one clause.
