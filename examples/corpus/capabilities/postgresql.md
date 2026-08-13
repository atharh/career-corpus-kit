---
title: PostgreSQL — what Sam can actually be asked about
kind: capability file — one technology, whole career
status: opened 2026-03-02; renderable within its ceilings
answers_the_question: |
  "How deep is your Postgres?" — asked as a self-rating box on an application form, which is
  what prompted the file.
owns_no_facts: |
  Derived index (`[OWNS-NO-FACTS]`). Every fact below cites the story file that owns it;
  nothing is restated as this file's own. No homeless facts at present.
sources:
  - interview with Sam, 2026-03-02
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented person, invented companies, invented numbers, invented
> quotes. This shows the *shape* of a capability file — one technology across a whole career,
> per `[CAPABILITY-FILE]`. It is never a source.

## The answer, in the shape they'd say it

"I've run production systems on Postgres for a decade, and I've built around it — exports,
reporting copies, schema changes on live clinic data. I'm not a DBA: I've never tuned a query
planner under real load, and I'd say so before guessing."

## Beat: the reporting copy at Bellhaven — the strongest claim

Clinic-facing reports ran against the production primary and were taking it down; Sam built
the nightly export into a second Postgres instance that reports point at instead. Owned by
`../bellhaven/reporting-migration.md` — including the ceiling that it was a
`pg_dump`-and-transform, **not** a replica, and is never rendered as "built replication".
**Depth ceiling:** designed and operated the export; can defend the transform and the failure
modes of a nightly copy. Cannot defend replication internals — it wasn't one. And the
reporting schema is not claimable at all: that file assigns it to a contractor.

## The noes — what makes the rest credible

- Never administered a Postgres fleet; instances were managed by the platform team at
  Tidewater and by hand at Bellhaven.
- Never tuned a query planner under production load — has read `EXPLAIN` output, yes; changed
  an outcome with it under pressure, no.
- No stored-procedure codebase anywhere in the career; logic lived in the app layer.

## Gaps — the interview queue

- [ ] **Tidewater's Postgres never came up in an interview round.** Sam listed it; nobody has
      yet asked what actually ran on it (`[LIST-IS-A-QUEUE]`).
