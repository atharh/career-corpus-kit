---
title: Rebuilding clinic search, under a title the work didn't match
company: Bellhaven Health
role: Tech Lead, Clinic Search (squad charter title from 2017-09; the HR title stayed Software Engineer)
period: 2017-09 – 2018-08
status: seed — one session, mostly memory. Thin on vetted material, and the title outranks the evidence; the file says so rather than fixing it
related:
  - reporting-migration.md (same database, a year earlier; the nightly export this search indexed from)
technologies: [postgresql]
facts_vetted:
  - Sam was named tech lead of the three-person clinic-search squad on its charter in 2017-09; the HR title never changed from Software Engineer, and nobody reported to Sam
  - Sam built and owned the indexing job that rebuilt the search index from the nightly reporting export
  - the search design — Postgres full-text search over a materialised table, not a separate search engine — was the principal engineer's call; Sam argued for a separate engine, lost, and built the chosen design
facts_unvetted:
  - "'we took the worst clinic search from about eight seconds to well under one' — Sam's memory,
    no dashboard, no ticket. Plausible; unciteable. Render without the number."
  - "'the squad was five by the end' — Sam thinks so, and can't name who the fourth and fifth
    were, which suggests it stayed at three. Not a scope claim."
  - "'the design was mostly my idea by the time it was written up' — Sam's view, unprompted. The
    principal was not asked and the design doc names one author, not Sam. What may be said: Sam
    argued the alternative, lost, and built the winning design well. Never design ownership."
  - "'at least one other product team reused the index' — Sam remembers one for sure and thinks
    two. Unverifiable since the acquisition. Carries no adoption claim."
sources:
  - interview with Sam, 2026-04-20 (vetted)
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented people, invented numbers and quotes.
> Shows the corpus format only — never a source.

## Setup

Bellhaven's clinic search was a `LIKE` query over patient-visit rows, and by 2017 the two
largest customers could feel it. A three-person squad got chartered to fix it, and the charter
named Sam **tech lead** — the first time the word appeared next to their name anywhere.

What the word meant there is the whole point of this file. Sam's own account, first round:

> *"Tech lead meant I ran the standup and I was the one the principal talked to. Nobody
> reported to me. I didn't pick the design. I'd have picked a different one."*

The résumé says *Software Engineer* for the whole Bellhaven stay, which is correct — HR never
changed it. This story carries the title so that an assessment has to decide what it's worth,
not so that a render can use it. ⚠️ **Ceiling, theirs, 2026-04-20:** *tech lead* may appear
only with its scope attached — *tech lead of a three-person squad, no reports* — and never as
*led the team*. See `LESSONS.md`.

## Beat: the argument Sam lost

Sam wanted a separate search engine. The principal engineer wanted Postgres full-text search
over a materialised table fed from the nightly export that `reporting-migration.md` already
describes, on the grounds that the squad was three people and an extra system was an extra
on-call rota nobody had. Sam argued it for a week and lost.

> *"The principal was right, and it took me about a year to say so out loud. Three people can't run a
> search cluster. I was arguing for the interesting thing."*

The design doc names the principal as its author. Sam's later feeling that *"it was mostly my
idea by the time it was written up"* is recorded above as unvetted and stays there.

## Beat: the indexer

What Sam did own, end to end: the job that rebuilt the search index from the nightly export,
its failure handling, and the two occasions it silently produced an empty index and search
returned nothing for a morning. Sam added the row-count check after the second one.

## Outcome

Clinic search got fast and the two large customers stopped raising it. **No number survives**
— see `facts_unvetted`. The index was still being rebuilt nightly when Sam left.

## What it cost

Search results were up to a day stale, by design, and the support team had to learn to say so.
Sam's read: *"same trade as the reporting one, same weaselly instinct to call it near-real-time,
and this time I didn't."*

## Gaps — the interview queue

- [ ] **What did the principal actually delegate to Sam, in words?** The charter says *tech
      lead*; the design doc says one author. What sat between those two is the level question.
- [ ] Did the row-count check outlive Sam? A colleague could confirm; Sam has not asked.
- [ ] Verify: every fact in `facts_unvetted`, starting with the latency figure — a support
      ticket from 2018 would settle it.
