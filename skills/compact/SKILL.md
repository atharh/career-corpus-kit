---
name: compact
description: Prune accumulated history out of corpus story files without losing the rules that keep renders honest. Use when story files have become heavy with resolved gaps and dated back-and-forth, when a gap list is more history than queue, or after a long interview session.
---

# Career corpus — compact

Interview sessions leave sediment. Every resolved question, every rejected theory, every
superseded number stays in the file with a date on it, and after a few sessions the gap list
is more archive than queue. This skill removes the sediment and leaves the rock.

**It is a destructive skill.** Read the guard list before you touch anything.

## Why not just leave it

Because the gap list is the interview's work queue, and a queue that is 40% struck-through
is a queue nobody can read. The cost isn't tokens — a whole corpus is small. The cost is
**attention**: an open 🔴 buried under six resolved items gets missed, by the model and by
the user.

## Why not just delete the old stuff

Because most of what *looks* like history is a **rule**. A corpus file records not only what
happened but what was decided about how to render it, and what was ruled out. Sweep those and
you lose the thing that makes the corpus safer than memory — the same wrong reading comes
back next session, and this time nobody catches it.

## The criterion

One question, applied line by line:

> **Does this line change what a future render does?**

- **Yes → it's a rule. It stays**, and it belongs in a labelled block, not in the gap list.
- **No → it's history. It goes.** Git has it.

Everything below is that criterion, applied.

## Guard list — never sweep these

Stop and leave the line alone if it carries any of:

1. **A ceiling** — the user's own limit on a claim. *"doubled, not tripled"*, *"I honestly
   didn't do much"*, *"in four months you can hardly do much"*. These exist to stop a later
   session re-inflating a story that the user already shrank. They are the single most
   valuable lines in the corpus and the easiest to mistake for chatter.
2. **A rendering decision** — `RENDERING DECISION`, or any note saying how something must or
   must not be rendered. Including the negative ones: *"renders without a result"*,
   *"never cite byline position as evidence"*.
3. **A rejected reading** — a theory the model proposed and the user refuted, recorded as the
   model's error. Its whole function is recurrence prevention. Compress the prose if it's
   long; never remove the ruling.
4. **⚠️ or 🔴 markers**, and anything they're attached to.
5. **Provenance and vetting status** — `facts_unvetted`, `facts_disputed`, source lines,
   "his account only", "not independently sourced". A fact that loses its provenance becomes
   a fact that looks vetted.
6. **Anachronism corrections** — `anachronisms_corrected` blocks and any "he said X, the
   period term was Y" note. The wrong word creeps back the moment the correction is gone.
7. **Open gaps that would change a rendering.** Including ones that have been open a long
   time — age is not evidence a question is dead. **The one exception, and it needs the user
   in the room:** a gap that fails the interview skill's say-it-out-loud test (rule 13) is
   sediment, not queue. Nobody will ever ask it, so no answer changes anything, and it sits
   there making the real queue unreadable. Sweeping those is a *separate, named pass* — propose
   the list, get agreement, then delete. Never fold it into a routine compaction, and never
   sweep a gap that merely looks tedious: *demand the mistake*, the cost, and the opposition
   all read as uncomfortable and all pass the test.
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
- **Narration of the interview process** — "asked on the third asking", "answered 16/07 and
  split in two", "Claude built this from an over-broad reading". Keep the *ruling*, drop the
  transcript around it. One clause, not a paragraph.
- **Stale cross-references** to files that have since been renamed, split, or merged.
- **Restated derived state** — counts of open gaps, "N seeds in the inbox", anything a status
  script computes. It rots silently.
- **Duplicated setup** that `background.md` already carries, restated inside a story file.

## Procedure

Work **one file at a time**, and show the user what changed before moving on.

1. **Check the tree is clean.** `git status`. If there are uncommitted changes, stop and say
   so — the user needs the diff to be reviewable and the history to be recoverable.
2. **Read the whole file.** Compaction without full context is how ceilings get swept.
3. **Classify every candidate line** against the guard list, then the sweep list.
4. **Promote before deleting.** Any answer living only in a resolved checkbox moves into the
   body or frontmatter first. Do this as a separate visible step.
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
  If an application's log has grown long, that's history worth keeping; the folder is closed
  when the thread closes, not pruned.
- **Never compact `LESSONS.md`.** It is append-only by construction and small by design. If it
  genuinely outgrows itself, that's a conversation with the user, not a sweep.
- **Never compact `through-lines.md`'s "where it doesn't hold" sections.** A through-line
  without its counter-examples is hagiography — the counter-example *is* the rule.
- **Never run unsupervised**, in a loop, or across the whole corpus in one pass. This is a
  reviewed operation.
- **Never sweep a line you don't understand.** Ask.

## What good looks like

A compacted story file reads as **the current truth about one arc**, with its rules visible
and its queue short. A reader who has never seen the file should not be able to tell how many
sessions it took to get there — except where the drift itself is evidence, and then it should
be stated once, deliberately, with dates.
