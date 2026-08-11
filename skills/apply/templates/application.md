---
company: <Company, as the posting names it>
role: <Role, as the posting titles it>
opened: <YYYY-MM-DD>
found_via: <job board | referral | inbound | the company's own careers page>
# No status: field. The last line of the log is the status — see apply's no-rollup rule `[NO-ROLLUP]`.
contacts:            # optional — roles, not names, unless the user wants them
  - <role>: <channel>
---

# <Company> — <Role>

## Log

<Append-only. One dated line per event, oldest at the top. Never edit a line that is already
here; add another — see the apply skill's append-only-log rule `[LOG-APPEND-ONLY]`.>

<Event vocabulary — these nine, and nothing else. Something that fits none of them is usually
two events:>

`opened` `fit-checked` `rendered` `sent` `inbound` `scheduled` `interviewed` `outcome` `routed`

- <YYYY-MM-DD> — **opened** — <where the posting came from>
- <YYYY-MM-DD> — **fit-checked** — <the one-line read, and what the user decided>
- <YYYY-MM-DD> — **sent** — <what actually went out, including anything the form asked for
  that this folder does not hold: a portfolio link, a salary expectation, a "why us" box>
- <YYYY-MM-DD> — **inbound** — <what arrived, and the `_inbox/` file it landed in>

## Open questions

<Only what is genuinely unresolved about this thread — a form answer the user is unsure of, a
contact who has gone quiet, a date nobody has confirmed. Delete each one as it resolves; the
log already holds the history.>
