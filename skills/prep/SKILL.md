---
name: prep
description: Build an interview prep pack for one scheduled interview — an opener, a story bank mapped to the employer's own hiring criteria, the probes they'll push on with defensible answers, and questions to ask them. Use when an interview or an interview loop is booked, when preparing for a specific round, or after an interview to capture what was asked.
---

# Career corpus — prep

`render` produces artifacts you **send**. This produces a directory you **study**, for one
scheduled interview, and then captures what happened afterwards.

It is the corpus pointed at a room you're about to walk into. Everything it writes is a
rendering, so **every hard rule in `render`'s SKILL.md applies here unchanged** — vetted facts
only, numbers carry their ceilings, no names of private people, obey recorded rendering
decisions, and make it sound like the user as the last step. Read that file; those rules are
not repeated here.

## When this fires, and what it needs

The trigger is *"I have an interview"*, not *"I'm applying"*. That means inputs `render`
doesn't have, and you should ask for them rather than guess:

- **The JD**, and the recruiter's email or scheduling note — those often name the format, the
  rounds, the interviewers' roles, and sometimes the assessment criteria outright.
- **The employer's published hiring criteria**, if any. Many companies publish competencies,
  focus areas, or levelling guides. **When they exist, they are the story bank's sections.**
- **The loop structure and the date.** How many rounds, with whom, over what period. The pack
  is a study plan as well as a document, and a plan needs a clock.

If a round is with a named individual, keep that name **out of filenames**. Roles in the
filename, names in the body if the user wants them. Filenames get shared, screenshotted, and
tab-completed in front of other people.

## The pack

One directory: `applications/<company>-<role>/`. Numbered so the reading order is the
preparation order.

| File | What it holds |
|---|---|
| `interview-prep.md` | The index. The frame — what this employer is actually buying. The loop, the dates, what to do on which day. |
| `01-about-me.md` | The opener. Two to three minutes, spoken, ending on why you're in this conversation. |
| `02-why-<company>.md` | The "why us" answer, built from their own material, not from adjectives. |
| `03-story-bank.md` | Stories mapped to **their** criteria — one section per criterion. |
| `04-probes-and-defences.md` | Where they'll push, and the answer. See below; this is the file that earns the pack. |
| `05-questions-to-ask.md` | What to ask them, and what not to. |

Skip files that don't apply. A 30-minute screen doesn't need six.

## `03` — map to their criteria, never to generic categories

If the employer publishes focus areas, competencies, or a levelling rubric, **the story bank's
sections are theirs, verbatim**, and each section names the corpus stories that serve it.

The value is in what this exposes. A criterion with three strong corpus stories behind it is
fine and needs no work. **A criterion with nothing behind it is the actual finding**, and it
should be stated plainly at the top of the file rather than papered over with the nearest
adjacent story. The user can then decide to prepare a thinner honest answer, or to go and
extract a story that fits, or to accept it as the weak spot and prepare for the question.

Where no criteria are published, derive sections from the JD's own emphasis — but say that's
what you did, so nobody mistakes your inference for their rubric.

## `04` — the probes file, and where probes come from

**This is `interview`'s "state the worst reading" technique, turned around and pointed at the
application instead of a memory.** It's the reason a corpus-backed pack beats generic prep: the
corpus has already written down where this candidate is weak, in the candidate's own words.

Source probes from, in order of yield:

1. **`facts_disputed` and `facts_unvetted`.** A number the corpus won't vouch for is a number
   an interviewer can push on. The defence is usually to volunteer the smaller sourced figure
   before being asked.
2. **Open gaps.** The interview skill logged them because an answer would change something —
   which is very close to why an interviewer would ask.
3. **⚠️ ceilings.** Every ceiling exists because a claim could be over-read. Assume it will be.
4. **Résumé claims with thin corpus backing.** Anything on the page that no story file
   decompresses is a bullet the candidate cannot currently defend for more than one follow-up.
5. **The shape of the career itself** — employment gaps, level changes, an IC↔manager move, a
   short tenure, a domain they haven't worked in. These are asked in almost every loop and they
   are not in the corpus, because the corpus stores stories and these are facts about the
   résumé's silhouette.
6. **What the JD wants that the corpus can't evidence.** The honest version of this answer is
   nearly always "no, and here's the closest thing I have" — which lands far better than a
   stretched analogy that collapses under one question.

**Write the defence at spoken length, and never invent a strength to cover a gap.** If the true
answer is "I haven't done that", the prep is *how to say that well and what to pivot to*, not a
way around it. An interviewer who catches one stretched claim discounts everything else.

Finish the file with a short **"things not to say"** list — the framings the corpus has already
ruled out, the codenames that stay internal, the numbers that were withdrawn. Under pressure
people reach for the version they've said most often, which is frequently the one the corpus
retired six months ago.

## Rules specific to prep

**1. Bullets and a first line, never a script.** Give the opening sentence and the beats. A
written-out answer gets memorised and then *sounds* memorised, and it collapses the moment the
question arrives in a slightly different shape.

**2. Spend the stories deliberately.** Track which story serves which criterion and which
question type. One anecdote reused across three answers in a single loop is a tell — it reads
as a candidate with one good year. Where a story must serve twice, note which *lens* each use
takes, and make sure they're genuinely different.

**3. Carry the mistake into the room.** The corpus keeps the failure in each story precisely so
this file can use it. Prep the mistake as an answer, not as damage control.

**4. Prep the follow-up, not just the answer.** For each story, the second and third questions
are usually already written down as that story's gaps. Answer down to depth three.

**5. The homework is part of the pack.** If there's a take-home, a presentation, or a
"prepare a case" instruction, it goes in `interview-prep.md` with the dates, not in a separate
mental note. It is the single most skippable and least skippable part of a loop.

**6. Say what you don't have.** A pack that reads as though the candidate is strong on
everything is a pack that hasn't been read against the criteria properly. Name the weak
sections at the top of `interview-prep.md`.

## After the interview — this is half the skill

Run this again the same day, while it's fresh. Two outputs:

- **Update the pack** with what was actually asked, which answers landed, and which didn't.
  A later round with the same company inherits it.
- **Feed the misses back into the corpus.** Anything the user fumbled, couldn't source, or
  got asked and hadn't considered becomes a queue for `/career-corpus:interview` — and it is
  the highest-quality queue the corpus will ever get, because it comes from a real interviewer
  rather than a model guessing what one might ask.

**Do this even when the outcome was bad, and especially then.** A question that landed badly is
a precisely targeted gap someone else handed you for free.

## What "good" looks like

The user can hold the whole pack in their head before walking in: one frame, one opener, a
story per criterion, an answer to each thing they're afraid of being asked, and three questions
worth asking. Nothing in it is a claim they can't defend at depth three, and the parts they're
weak on are named rather than hidden.

A pack that makes the user feel prepared but says something they'd have to walk back in the
room has failed, however good it reads.
