---
artifact: study-pack-section
application: kestrel-freight-engineering-lead
lifecycle: in-flight
generated: 2026-04-24
corpus_pin: a3f19c2
sources:
  - corpus/through-lines.md
  - corpus/tidewater/background.md
  - corpus/tidewater/batch-window.md
  - corpus/tidewater/oncall-rebuild.md
  - corpus/bellhaven/reporting-migration.md
  - applications/kestrel-freight-engineering-lead/fit.md
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented criteria, invented candidate. Never a
> source.

# Story bank — Kestrel's focus areas

Sections are Kestrel's four published focus areas, verbatim, in their order. Each section with a
story writes its answer out once, under **Spoken answer:**, to be read from `06` rather than
learned; the notes around it are bullets.

**One section has no story behind it.** That is section 3, and it is stated there rather than
filled.

---

## 1. Delivery under constraint

**Story:** the nightly dispatch build — `corpus/tidewater/batch-window.md`.

**Spoken answer:**

> A hard deadline is the right word for it: dispatch instructions were owed to customers by 06:00,
> and that time was in the contract. That is the job this posting describes, an overnight build
> with a hand-off nobody can miss. At Tidewater the build had drifted from 40 minutes to three
> hours ten because it reprocessed every historical partition on every run, and fixing that
> roughly halved the runtime. Ask me how we found it, because I'd looked straight past it twice.

- Open with the deadline, not the technology: dispatch instructions owed to customers by 06:00,
  contractually. A slow job is an ops problem; a slow job with a delivery time in a contract is
  a different conversation.
- 40 minutes when Sam joined, three hours ten by mid-2021. Degraded a few minutes a month for
  two years, which is exactly the rate at which nothing alerts.
- Everyone assumed volume. It was reprocessing every historical partition on every run.
- **Carry the mistake:** *"I'd worked on that job twice before and never looked at what it was
  actually doing. I optimised two queries inside a thing that shouldn't have been running at
  all."*
- Runtime **roughly halved**. Not a bigger number — see `04`.

## 2. Migration and reversibility

**Story:** the same one, different face — the parallel run.

**Spoken answer:**

> The migration I de-risked moved that nightly build onto incremental processing, and the team
> that owned the scheduler objected. They weren't blocking me, they were right: a silently stale
> dispatch file is worse than a late one. So we ran both pipelines for three weeks with a nightly
> byte-compare, and it caught two watermark bugs in week one, both fixed before cutover. I can
> take you through the parallel run, or through what it cost to do it on evenings first.

- The other team owned the scheduler and objected: incremental state means stale state when the
  watermark logic is wrong, and a silently stale dispatch file is worse than a late one.
- Sam's line, worth saying almost as-is: *"they weren't blocking me, they were right."*
- Three weeks, both pipelines, nightly byte-compare. Two watermark bugs in week one, both fixed
  before cutover.
- **Depth three** — what did the two bugs actually do? The corpus does not have that yet
  (`batch-window.md`, open gap). Say it is one clause in the notes and give the shape, not
  invented detail.
- Cost, volunteered before it is asked: six months of evenings. *"If I'd asked for it as planned
  work in month one instead of being precious about proving it first, it'd have been done in six
  weeks."*

## 3. Growing engineers

**Nothing in the corpus backs this section, and nothing adjacent is going to be stretched over
it.**

The closest material is two juniors mentored through their first year
(`corpus/tidewater/background.md`), and mentoring is not what this focus area is asking about.
Eleven years, no reports — see `corpus/profile.md`. `fit.md` recorded this on 7 April as
`no-corpus-evidence` and Sam applied with it named.

The prepared answer is in `04-probes-and-defences.md`. It is short, it is "no, and here is the
closest thing I have", and it does not go looking for a substitute.

## 4. Direction without ownership

**Story:** the batch window again, third face — and this is the one to lead with in the
director round.

**Spoken answer:**

> Changing course for a team I don't manage has always come down to evidence rather than
> argument. That is most of this role, because the systems either side of it belong to other
> teams. On the on-call rebuild at Tidewater I had a pager and a sponsor and no authority, so I
> categorised every page from a quarter before changing a single rule, and 19 of 31 needed no
> human action. Ask me what I got wrong there, because I reversed part of it in public.

- The system Sam changed belonged to another team, who disagreed, on good grounds.
- What resolved it was evidence rather than argument. *"The difference between us was that I
  could prove it and they couldn't disprove it, so the parallel run was the only honest way
  through. I'd have argued for a month otherwise."*
- **Second story, different lens:** the on-call rebuild — `corpus/tidewater/oncall-rebuild.md`.
  Sam had no authority there either: a pager, a sponsor, and credibility from the batch work.
  Categorised every page from a quarter before changing a single rule. 19 of 31 needed no human
  action. Pages went 31 → 9 across the year.
- **The reversal belongs here, not hidden.** Sam cut the rotation from eight to five, made the
  best responders' lives worse, and reversed it after seven weeks in public. This is the answer
  to any question about consequences, and it is the strongest thing in the pack.

**Spend note.** The batch-window story serves sections 1, 2 and 4, which is three uses in one
loop. The lenses are genuinely different — a deadline, a migration, a disagreement — but if two
of those rounds compare notes it will read thin. So: lead section 4 with the *on-call* material
and keep the batch window as the second example there.
