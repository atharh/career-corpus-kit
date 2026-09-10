---
# SYNTHETIC. This whole file is invented — see status: below. Strict YAML, read by tools as
# well as people; a prose value goes in a block scalar (`|`), as status: shows.
title: "SYNTHETIC — <the arc, retold at the target level>"
status: |
  SYNTHETIC BENCHMARK. Invented person, invented numbers, invented quotes. This is not a
  record of anyone's work and has no standing as evidence. No line of it may be cited,
  rendered, or spoken. A beat that feels true is a claim unrecorded, not a claim recovered:
  take it to /career-corpus:interview and say it in your own words.
persona: <invented name>, <role, in industry terms — never a grade code>
track: <ic | manager>
role_file: <roles/<file>.md, or "provisional" when no role file matched>
source: corpus/<company>/<story>.md
level: <the target level, in industry terms>
level_set_by: <user | default — one up from the source story's role>
period: <inherited from the source story, unchanged>
generated: <YYYY-MM-DD>
corpus_pin: <the corpus commit this exemplar read>
purpose: <one line — what the reader is meant to diff their own file against>
level_gaps:          # only when the distance is large: beats that are a level problem for the
                     # source story's role, not a capture problem, so the file cannot be read
                     # as a list of things the user failed to do
  - <beat> — <why it is out of reach at the source story's level>
---

<The frontmatter block above is the whole template. `status:` is the banner, and it sits
inside the first ten lines of the file by construction — the containment the ladder skill's
`[FICTION-IS-QUARANTINED]` promises is this block plus the path under `benchmarks/`. The body
below is the shape "Running an exemplar" in the ladder skill gives: what separates this
telling, the beats with their gap lines, the bullets the story would yield, and the checklist
of questions it answers.>

<Every value here is either inherited unchanged from the source story (`period:`, the
situation the beats are set in — `[SAME-SITUATION]`) or invented and marked as such. Nothing
in it is a claim about the user. `level_set_by:` records whether the user named the level or
the skill defaulted to one up, because the first line of the response says the same thing and
the file has to still say it a month later.>
