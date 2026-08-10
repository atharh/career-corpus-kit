> ⚠️ **FICTIONAL EXAMPLE.** Rendered from the fictional corpus in `../corpus/`. Every claim here
> traces to a story file. See `ANNOTATED.md` for what the corpus *refused* to let this say.

# SAM RIVERA

sam@example.com | Lisbon, Portugal | remote

Backend engineer, 11 years, mostly on the unglamorous half of the system: batch pipelines,
databases, and the things that page you at 3am. Currently senior on a six-person platform team
at a freight-booking company.

**Skills:** Python · Go · PostgreSQL · Airflow · AWS · Terraform · deploys to Kubernetes

---

## EXPERIENCE

### Senior Software Engineer
**Tidewater Logistics** | 03/2019 – present | Remote

- Diagnosed and fixed a nightly dispatch pipeline that had degraded from 40 minutes to over
  three hours against a contractual 06:00 delivery deadline. The cause was design, not volume:
  the job reprocessed every historical partition on every run. Moved it to incremental
  processing keyed on input watermarks, **roughly halving runtime**. Two other teams later
  adopted the same pattern.
- De-risked that cutover by running both pipelines in parallel for three weeks and diffing
  output nightly, which surfaced two watermark bugs before they reached customers. The
  scheduler was owned by another team, so agreement came from evidence rather than authority.
- Led a rebuild of the on-call rotation covering six services. Categorised every page from a
  full quarter and found 19 of 31 required no human action at all; removed or thresholded those
  alerts. **Out-of-hours pages fell from 31 in Q1 2023 to 9 in Q4.**
- Mentored two junior engineers through their first year, both still on the team.

### Software Engineer
**Bellhaven Health** | 08/2015 – 02/2019 | Hybrid

- Moved clinic-facing reporting off the production database, where a single large customer's
  month-end report could hold locks for minutes and slow appointment booking for everyone.
  Built and owned the nightly export and transform into a separate reporting database; argued
  against buying a BI tool that would have pointed at production and made the coupling worse.
- Maintained that pipeline for two years, and it outlived my time on it.
- Generalist backend work at a company that grew from 9 engineers to about 25 while I was there.

### Junior Developer
**Small digital agency** | 07/2014 – 07/2015

Client web applications in Python and PHP.

## EDUCATION

- **B.Sc. Computer Science**, 2014
