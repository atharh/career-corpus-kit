---
name: compact
description: Prune accumulated history out of corpus story files without losing the rules that keep renders honest. Use when story files have become heavy with resolved gaps and dated back-and-forth, when a gap list is more history than queue, or after a long interview session.
---

# Career corpus — compact

Interview sessions leave sediment. Every resolved question, every rejected theory, every
superseded number stays in the file with a date on it, and after a few sessions the gap list
is more archive than queue. This skill removes the sediment and leaves the rock.

**It is a destructive skill.** Read the guard list before you touch anything.

## Why it exists, and why it is dangerous

The gap list is the interview's work queue, and a queue that is mostly struck-through is a queue
nobody can read: an open question buried under six resolved items gets missed, by the model and
by the user. But most of what *looks* like history is a **rule** — what was decided about how to
render something, and what was ruled out. Sweep those and the same wrong reading comes back next
session, and this time nobody catches it.

## The criterion

One question, applied line by line:

> **Does this line change what a future render does?**

- **Yes → it's a rule. It stays**, and it belongs in a labelled block, not in the gap list.
- **No → it's history. It goes.** Git has it.

Everything below is that criterion, applied.

## Guard list — never sweep these

Stop and leave the line alone if it carries any of:

1. **A ceiling** — the user's own limit on a claim. *"doubled, not tripled"*, *"two teams
   took it, not the org"*, *"roughly halved"*. These exist to stop a later
   session re-inflating a story that the user already shrank. They are the single most
   valuable lines in the corpus and the easiest to mistake for chatter.
2. **A rendering decision** — `RENDERING DECISION`, or any note saying how something must or
   must not be rendered. Including the negative ones: *"the reversal is interview material,
   not résumé material"*, *"do not put a breach claim in writing"*.
3. **A rejected reading** — a theory the model proposed and the user refuted, recorded as the
   model's error. Its whole function is recurrence prevention. Compress the prose if it's
   long; never remove the ruling.
4. **⚠️ markers**, and anything they're attached to.
5. **Provenance and vetting status** — `facts_unvetted`, `facts_disputed`, source lines,
   "their account only", "not independently sourced". A fact that loses its provenance becomes
   a fact that looks vetted.
6. **Anachronism corrections** — `anachronisms_corrected` blocks and any "they said X, the
   period term was Y" note. The wrong word creeps back the moment the correction is gone.
7. **Open gaps that would change a rendering** — however long open; age is not evidence a
   question is dead. The one kind that may go is the last item of the sweep list, and only
   with the user in the room.
8. **A supersession trail where the earlier version might return** — if the user gave two
   different numbers across sessions, keep both with dates. Drift is evidence.

When in doubt, keep. The skill's failure mode is over-sweeping, and it is not symmetric:
a kept line costs a few tokens, a swept rule costs a false claim in an interview.

## Sweep list — this is the sediment

- **Resolved gaps whose answer already appears in the body.** Pure duplication. The great
  majority of resolved items are this. Delete the checkbox line.
- **Resolved gaps whose answer exists *only* in the checkbox.** Do not delete these. **Promote
  first** — write the fact into the body or frontmatter where it belongs, *then* delete the
  line. Never delete an answer that has nowhere else to live.
- **Narration of the interview process** — "asked twice before they answered", "answered in
  the second session and split in two", "the model built this from an over-broad reading".
  Keep the *ruling*, drop the transcript around it. One clause, not a paragraph.
- **Stale cross-references** to files that have since been renamed, split, or merged.
- **Restated derived state** — counts of open gaps, "N seeds in the inbox", anything a status
  script computes. It rots silently.
- **Duplicated setup** that `background.md` already carries, restated inside a story file.
- **Open gaps whose answer the user would never say out loud — in a bullet, a letter, or an
  interview answer** (the interview skill's `[SAY-ALOUD]`). Nobody will ask, so no answer
  changes anything, and they make the real queue unreadable. A *separate, named pass* with the
  user in the room: propose the list, get agreement, then delete. Never part of a routine
  compaction, and never a gap that merely looks uncomfortable — the mistake, the cost and the
  opposition all pass the test.

## Procedure

Work **one file at a time**, and show the user what changed before moving on.

1. **Check the tree is clean.** `git status`. If there are uncommitted changes, stop and say
   so — the user needs the diff to be reviewable and the history to be recoverable.
2. **Read the whole file.** Compaction without full context is how ceilings get swept.
3. **Classify every candidate line** against the guard list, then the sweep list.
4. **Promote before deleting** — the sweep list's second item — as a separate visible step.
5. **Consolidate the rules into blocks.** A file after compaction should have its ceilings in
   one place, its rendering decisions in one place, and its rejected readings in one short
   section — not scattered through a gap list where the next sweep will mistake them for
   history.
6. **Rewrite the gap list as a pure queue.** Open items only. Sharpest first.
7. **Report the numbers**: lines before and after, how many resolved gaps were removed, how
   many facts were promoted, and anything you deliberately kept that looked like history.
8. **Commit per file or per company**, with a message naming what was compacted. One
   reviewable commit beats one big one.

## Never

- **Never compact `_inbox/`.** Raw material is pristine by design; extraction may need redoing.
- **Never compact `applications/`.** This skill works on `corpus/` only. An application folder
  is a dated record of what was actually claimed, sent and asked, and the dates *are* the
  value — a rendered artifact tidied after the fact stops matching what the employer received.
- **Never compact `LESSONS.md`.** An entry leaves it only by the two exits in the Lessons
  section below, never by a sweep. If it genuinely outgrows itself, that's a conversation with
  the user.
- **Never compact `through-lines.md`'s "where it doesn't hold" sections.** A through-line
  without its counter-examples is hagiography — the counter-example *is* the rule.
- **Never compact a capability file's depth ceilings or its noes.** Same defect, same reason:
  the noes are what make the yeses credible, and an entry swept of its ceiling reads as
  uniform confidence — see the interview skill's `[DEPTH-CEILING]`.
- **Never run unsupervised**, in a loop, or across the whole corpus in one pass. This is a
  reviewed operation.
- **Never sweep a line you don't understand.** Ask.

## Lessons — how this skill personalises to you

This skill ships generic and sharpens by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit. Never edit this
SKILL.md to record a lesson: the method stays stable and shareable; the scar tissue stays
private and personal.

A compaction session is where sweep-or-keep calls get corrected — "that line was a ceiling",
"never sweep X-shaped notes" — and those corrections are lessons like any other. Carrying this
block does not loosen the Never list above: reading and appending to `LESSONS.md` is not
compacting it.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After a correction that generalises, append one dated line**: the mistake, and the rule to
  apply next time. Route it first — a rule that would still hold if the corpus were about
  someone else belongs to the method, not this file. Either way the rule lives in a *file*: a
  rule nobody can diff is a rule nobody can review, port, or undo.
- **A lesson leaves this file two ways, each on the user's explicit say-so, entry by entry.**
  One that proves *wrong* is retired in the session where it misfired, struck in place —
  `~~<the entry>~~ retired YYYY-MM-DD: <one clause of why>` — and never applied again; the
  strike records wrongness, which lives nowhere else. One the method has since *absorbed* is
  deleted outright, no strike left behind — a shipped rule's duplicate here can only drift —
  once nothing local remains (no calibration about this user, no number they set, no recorded
  divergence; trim the entry to that residue if any does) and no session still loads a skill
  version without the rule.

## What good looks like

A compacted story file reads as **the current truth about one arc**, with its rules visible
and its queue short. A reader who has never seen the file should not be able to tell how many
sessions it took to get there — except where the drift itself is evidence, and then it should
be stated once, deliberately, with dates.
