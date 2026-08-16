---
artifact: resume
application: kestrel-freight-engineering-lead
lifecycle: submitted
generated: 2026-04-09
corpus_pin: a3f19c2
sources:
  - corpus/profile.md
  - corpus/tidewater/background.md
  - corpus/tidewater/batch-window.md
  - corpus/tidewater/oncall-rebuild.md
  - corpus/bellhaven/reporting-migration.md
  - applications/kestrel-freight-engineering-lead/jd.md
  - applications/kestrel-freight-engineering-lead/fit.md
submitted:
  date: 2026-04-09
  as: PDF uploaded to the Kestrel careers form
  # The fallback, not the default: this repo is documentation and holds no PDFs, so the
  # bytes are untracked and a hash is all there is. A real corpus force-adds the sent
  # file at the freeze and writes no sha256 at all — apply's `[PIN-NOT-ARCHIVE]`.
  sha256: 9f2b7c41d0a8e6535ab1c9f0742de83b6c1a5f92e4d70b83cc61a2f4d9e70b15
---

> ⚠️ **FICTIONAL EXAMPLE.** Rendered from the fictional corpus in `../../corpus/` against the
> fictional posting in `jd.md`. Never a source.

# SAM RIVERA

sam@example.com | Lisbon, Portugal | remote

Backend engineer, 11 years, mostly on overnight builds and the deadlines they have to hit.
Currently senior on a six-person platform team at a freight-booking company.

**Skills:** Python · Go · PostgreSQL · Airflow · AWS · Terraform · deploys to Kubernetes

---

## EXPERIENCE

### Senior Software Engineer
**Tidewater Logistics** | 03/2019 – present | Remote

- Diagnosed and fixed a nightly dispatch pipeline that had degraded from 40 minutes to over
  three hours against a contractual 06:00 delivery deadline. The cause was design, not volume:
  the job reprocessed every historical partition on every run. Moved it to incremental
  processing keyed on input watermarks, **roughly halving runtime**.
- Cut that pipeline over with no customer-visible break by running both versions in parallel
  for three weeks and diffing output nightly. Two watermark bugs surfaced in the first week and
  were fixed before cutover.
- Got that change accepted without owning the system it touched. The scheduler belonged to
  another team, whose objection — stale state is worse than late state — was correct; the
  parallel run is what settled it. Two other teams later adopted the same pattern.
- Led a rebuild of the on-call rotation covering six services. Categorised every page from a
  full quarter and found 19 of 31 required no human action at all; removed or thresholded those
  alerts. **Out-of-hours pages fell from 31 in Q1 2023 to 9 in Q4.**
- Mentored two junior engineers through their first year, both still on the team.

### Software Engineer
**Bellhaven Health** | 08/2015 – 02/2019 | Hybrid

- Built and owned the nightly export and transform that moved clinic-facing reporting off the
  production database, where one large customer's month-end report could hold locks for minutes
  and slow appointment booking for everyone. Maintained it for two years; it outlived my time
  on it.
- Argued against buying a BI tool pointed at production, on the grounds that the tool was not
  the problem and the coupling was.

### Junior Developer
**Small digital agency** | 07/2014 – 07/2015

Client web applications in Python and PHP.

## EDUCATION

- **B.Sc. Computer Science**, 2014
