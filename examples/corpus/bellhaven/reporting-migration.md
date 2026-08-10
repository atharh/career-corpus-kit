---
title: Getting clinic reporting off the production database
company: Bellhaven Health
role: Software Engineer
period: 2016-05 – 2016-12
status: drafted — thin on outcome, strong on the anachronism lesson
facts_vetted:
  - clinic-facing reports ran directly against the production Postgres primary
  - a large customer's month-end report could lock tables for minutes during clinic hours
  - Sam built a nightly export into a separate reporting database
  - the schema for the reporting database was designed by a contractor, not by Sam
facts_unvetted:
  - "'it took the worst report from four minutes to under ten seconds' — Sam's memory, ten
    years old, no source. Plausible; unciteable. Render without the number."
anachronisms_corrected:
  - "Sam first described this as **'building a data platform'** and then as **'basically a data
    mesh'** (interview 2026-02-14). Both walked back in the same conversation once asked what it
    actually did. **It was a nightly `pg_dump`-and-transform into a second Postgres instance,
    with a cron job.** The term *data mesh* was coined in 2019, three years after this work, and
    it describes decentralised domain ownership — close to the opposite of what this was.
    **Never render either term for this work.**"
  - "**'ETL pipeline'** is fine and contemporaneous. **'Data engineering'** as a job description
    is a stretch for 2016 but defensible. **'Analytics platform'** is not — there was no
    platform, there was one database and four reports."
sources:
  - interview with Sam, 2026-02-14 (vetted)
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented people, invented numbers and quotes.
> Shows the corpus format only — never a source.

## Setup

Bellhaven's clinic-facing reports queried the production primary directly. For most customers,
fine. For the two largest, a month-end report could hold locks long enough that appointment
booking got slow — during clinic hours, for everyone, because one customer pressed a button.

Sam was the person who didn't mind database work, so it landed on them.

## Beat: the boring correct answer

A nightly export into a separate Postgres instance. Reports point at the replica-ish copy;
production never sees a reporting query again.

There is no clever decision here and the corpus should not manufacture one. **The interesting
part is what Sam argued *against*:** the VP Engineering wanted to buy a BI tool and point it at
production, which would have made the exact problem worse while making it look solved. Sam's
case was that the tool wasn't the problem, the *coupling* was, and a BI tool with production
credentials is the same outage with a nicer dashboard.

## Beat: the part that wasn't Sam's — and this had to be corrected

Sam initially described the work as *"we designed the reporting schema and built the
pipeline."* Asked what specifically they did, versus what "we" did:

> *"Right — no, the schema was a contractor. They were there about six weeks and they were good. I
> built the export and the transform and I maintained it for two years after he left, but I
> didn't design that schema and I shouldn't say I did."*

⚠️ **Attribution ceiling, theirs.** Render as *"built and owned the export pipeline"*. Never
*"designed the reporting schema"*, never *"architected"*.

## Outcome

The reports got fast and production stopped locking up at month end. **No number survives** —
see `facts_unvetted`. It ran for at least two more years after Sam stopped touching it.

## What it cost

Reports went stale by up to a day, and two customers complained. **Sam's read, unchanged ten
years later:** *"correct trade and I'd make it again, but I told the customers it was 'near
real-time' at the time, which was a weaselly thing to say about something that ran at 2am. I'd
just say 'it's from last night' now."*

## Gaps — the interview queue

- [ ] **What happened to it after Sam left?** They think it was still running at acquisition.
      If it ran five-plus years untouched, that's the outcome this story is missing — and it's
      the only claim here that would survive an interviewer pushing on results.
