---
company: <Company, as the posting names it>
role: <Role, as the posting titles it>
opened: <YYYY-MM-DD>
found_via: <job board | referral | inbound | the company's own careers page>
# No status: field. The last event below is the status — see apply's no-rollup rule `[NO-ROLLUP]`.
events:              # the machine-readable thread. One line per event, oldest first, and the
  - <YYYY-MM-DD> opened          # only place anything reads state from — `[STATE-IS-DATA]`.
  - <YYYY-MM-DD> fit-checked     # `<YYYY-MM-DD> <event>`, one space, nothing else on the line.
  - <YYYY-MM-DD> sent            # A trailing `# …` note is fine and is stripped before parsing.
sent:                # optional — present once `events:` carries a `sent`. `[SENT-NAMES-WHAT-WENT]`
  date: <YYYY-MM-DD>
  artifacts:         # files in THIS folder the employer received. Each one is `lifecycle: submitted`,
    - resume.md      # and nothing outside this list is.
    - cover-letter.md
  baselines:         # optional — repo-relative files sent from outside this folder. Never frozen.
    - <the maintained résumé, or a cover letter kept per role family>
  baseline_pin: <the repo commit those baselines stood at — one pin covers all of them>
contacts:            # optional — roles, not names, unless the user wants them
  - <role>: <channel>
---

# <Company> — <Role>

<One or two lines: what this thread is waiting on and whose move it is next. Not the stage —
`events:` above already ends in that. This paragraph is the only part of the file that gets
rewritten rather than appended to, and it is what a reader sees first — see the state-first
rule `[STATE-FIRST]`.>

## Log

<Append-only, and one dated line per event. Never edit a line that is already here; add another
— see the apply skill's append-only-log rule `[LOG-APPEND-ONLY]`. This is the reader's surface:
it carries *why*, and nothing parses it.>

<Event vocabulary — these nine, and nothing else. Something that fits none of them is usually
two events:>

`opened` `fit-checked` `rendered` `sent` `inbound` `scheduled` `interviewed` `outcome` `routed`

- <YYYY-MM-DD> — **opened** — <where the posting came from>
- <YYYY-MM-DD> — **fit-checked** — <the one-line read, and what the user decided>
- <YYYY-MM-DD> — **sent** — <what actually went out, including anything the form asked for
  that this folder does not hold: a portfolio link, a salary expectation, a "why us" box>
- <YYYY-MM-DD> — **inbound** — <what arrived, and the `_inbox/` file it landed in>

<details>
<summary>Earlier entries</summary>

<Entries that no longer bear on the next decision, moved down here verbatim as the thread
grows. Folded, not deleted: this log is potentially evidence of what the user decided and
why.>

</details>

## Open questions

<Only what is genuinely unresolved about this thread — a form answer the user is unsure of, a
contact who has gone quiet, a date nobody has confirmed. Delete each one as it resolves; the
log already holds the history.>
