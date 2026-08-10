---
company: Tidewater Logistics
period: 03/2019 – present
location: remote (company HQ Rotterdam)
what_it_is: freight-booking SaaS; mid-market shippers book and track container freight
scale:
  engineers: ~40 at hire, ~120 today
  team: Fulfilment Platform — 6 engineers, 1 EM, 1 PM
  reported_to: Engineering Manager
sources:
  - resume.md (vetted)
  - interview with Sam, 2026-02-14 (vetted)
  - interview with Sam, 2026-03-02 (vetted)
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented numbers. Shows the corpus format only.

Shared context for every Tidewater story. Story files assume this and never restate it.

## The role

Backend engineer on **Fulfilment Platform** — the services that turn a booked shipment into
dispatch instructions, and everything downstream of "customer clicked confirm". Promoted to
Senior in 2022.

**Not a manager, and the corpus should stop implying otherwise.** Sam has led projects, run
on-call, and mentored two juniors. They have never had reports.

⚠️ **Ceiling, theirs, 2026-03-02**, and they volunteered it unprompted: *"I keep seeing 'led
the team' in drafts. I led the work. There's a difference and an EM interviewer will find it in
about nine seconds."* Render as *"led the project"* / *"technical lead on"*, never *"led the
team"* or anything implying line management.

## Why the batch window mattered here

Tidewater's customers get dispatch instructions by 06:00 local. Everything in the nightly
pipeline is measured against that deadline, which is why `batch-window.md` is a story at all —
a slow job is an ops problem; a slow job with a contractual delivery time is a business one.

## Gaps

- [ ] **What did the Senior promotion actually require?** It's on the résumé as a date. If an
      interviewer asks "what changed when you were promoted", there's currently no answer.
