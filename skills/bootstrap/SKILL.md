---
name: bootstrap
description: One-time onboarding for a new career corpus. Reads the user's existing résumé / LinkedIn / notes, sets up the corpus structure, writes profile.md, and generates a prioritized queue of stories worth extracting. Use when starting a career corpus from scratch, or when someone new is setting up the career-corpus kit.
---

# Career corpus — bootstrap

Run this once, when the corpus is empty. It turns "here's my résumé" into a set-up corpus and
a ranked queue of stories to extract, then hands off to the `interview` skill.

Goal: get from zero to "let's start with this one" in a single session — without inventing
anything.

## What it produces

```
corpus/
  profile.md         ← career spine, seeded from vetted résumé text
  through-lines.md   ← empty stub; fills in as stories accrete
  QUEUE.md           ← prioritized list of stories worth extracting
  LESSONS.md         ← empty; grows as you correct the skills (see any skill's Lessons note)
  _inbox/            ← drop raw material here (old drafts, docs, reviews)
```

Nothing else yet. `applications/` appears alongside `corpus/` the first time the user opens an
application with the `apply` skill — don't create it here.

## Steps

1. **Gather what exists.** Ask the user for their current résumé, LinkedIn text, an old CV,
   brag docs, past performance reviews — whatever they have. Anything they paste goes into
   `_inbox/` as raw material (never rendered from; see the interview skill's rules).
2. **Write `profile.md` from vetted text only.** The career spine: years, education, contact,
   the skills line, and a one-paragraph summary — taken from what they wrote, not invented.
   Mark anything uncertain as a gap.
3. **Build the extraction queue.** Read the résumé and list the stories worth extracting — one
   per real arc (a hard project, a conflict, a build, a turnaround). Rank by interview value:
   prefer arcs with a decision, opposition, and a number over accomplishments with none. Flag
   the user's headline claims — the things a JD will most often ask for. Write them to
   `QUEUE.md` as a checklist.
4. **Seed, don't fill.** Do NOT write story files yet. Bootstrap sets up the queue; the
   interview skill writes the stories, one at a time, with the user in the room.
5. **Create `LESSONS.md`** — an empty file with a one-line header explaining that the skills
   append corrections here to personalise over time.
6. **Hand off.** Point at the top of the queue: *"Your highest-value story looks like <X>. Run
   `/career-corpus:interview <X>` to start."*

## The one rule that matters here

**Bootstrap seeds; it never invents.** A résumé is a *biased index* — it contains what the
user already remembers, which is exactly the material that needs the least help. The queue's
job is to name the arcs; the interview's job is to find what's *not* on the résumé (the
forgotten work, the mistake nobody wrote down, the project that got cut to one line). Don't
let a tidy résumé convince you the corpus is nearly done — it has barely started.
