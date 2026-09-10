---
# Strict YAML, read by tools as well as people. A prose value goes in a block scalar (`|`).
artifact: assessment
scope: <corpus/<company>, or the whole corpus, or one story file>
track: <ic | manager>
role_file: <roles/<file>.md, or "provisional" when no role file matched>
generated: <YYYY-MM-DD>
corpus_pin: <the corpus commit this assessment read — a date alone cannot be diffed against>
sources:                        # every story file the verdict cites, repo-root-relative
  - corpus/<company>/<story>.md
standing: |
  One session's read of the corpus at the pin above, on the date above. It says what a body
  of written work demonstrates, which is narrower than what the person is capable of, and it
  is not a rating of the person, a promotion decision, or anything to hand to a third party.
---

<The frontmatter block above is the whole template; the body is the report the ladder skill's
"The report" section describes, in this order, and the terminal version is the same body with
no frontmatter. It is written to disk only when the user asks, at
`benchmarks/<company>/assessment.md` — or `benchmarks/assessment.md` for the whole corpus —
and never under `corpus/`.>

## Verdict

<One sentence: the level range the vetted evidence supports, and any track caveat. Where the
evidence reads below the user's current title, this sentence and the next say so plainly —
`[CITE-THE-GRADE]`.>

## Pillars

<Floor first — the weakest row is the actionable one. Every grade cites the story and line that
carries it; a row with no citation is an impression and is marked as one. Only `facts_vetted`
lines score — `[VETTED-ONLY]`.>

| Pillar | Level the evidence supports | Carried by |
|---|---|---|
| <the floor> | <level> | `corpus/<company>/<story>.md:<line>` |
| <…> | <…> | <…> |

## Strongest evidence

<Two or three items, named as what an interviewer would find most convincing.>

## The floor

<What specifically is thin, and which bucket it fell in — missing from the file, missing from
the work, or not available in that role (`[CAPTURE-GAP-ISNT-A-GAP]`).>

## The delta

<Two or three concrete things that would move the verdict a level, each phrased as work or as
capture, never as a personal quality.>

## Interview queue

<The stories where the level is probably in the work but not in the file — every unvetted or
disputed claim the verdict could not count, with the story named. Routes to
`/career-corpus:interview`.>

- [ ] `corpus/<company>/<story>.md` — <the claim, and what it would carry if vetted>
