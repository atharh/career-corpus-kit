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
.gitignore         ← keeps raw inbound and rendered output out of git history
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

1. **Set up storage before anything is pasted.** Write a `.gitignore` at the repo root — this
   has to exist *before* step 2, because that's when the first sensitive file lands. If one is
   already there, add only the missing lines and show the diff; never overwrite it.

   ```gitignore
   # Raw inbound — unvetted, and the most sensitive material here: an employer's
   # take-home brief, a recruiter thread with other people's names and contact
   # details, an old performance review. A queue to be drained into vetted story
   # files, not storage. Matches at any depth, so it covers corpus/_inbox/ and
   # every applications/<app>/_inbox/ alike.
   #
   # To keep one file deliberately:  git add -f <path>
   _inbox/

   # Rendered output. Rebuildable from the markdown, and carries contact details
   # in a form that's easy to mis-attach.
   *.pdf
   *.docx

   .DS_Store
   ```

   Say what it does in one line, and point at `PRIVACY.md` in the kit for the reasoning. If
   the directory isn't a git repo yet, write it anyway and tell them to `git init` — the file
   is worthless applied retroactively.
2. **Gather what exists.** Ask the user for their current résumé, LinkedIn text, an old CV,
   brag docs, past performance reviews — whatever they have. Anything they paste goes into
   `_inbox/` as raw material (never rendered from; see the interview skill's rules).

   **Say once, here, that a private repo is not a private computer.** Reading a corpus file
   sends it to the model provider — that's how any of this works, and repo permissions don't
   change it. It's the same exposure as pasting the same text into a chat window, which is the
   alternative; the point is that they decide it knowingly rather than infer "private repo"
   means "never leaves the machine". Anything too sensitive to send to a model doesn't go in
   the corpus.
3. **Write `profile.md` from vetted text only.** The career spine: years, education, contact,
   the skills line, and a one-paragraph summary — taken from what they wrote, not invented.
   Mark anything uncertain as a gap.
4. **Build the extraction queue.** Read the résumé and list the stories worth extracting — one
   per real arc (a hard project, a conflict, a build, a turnaround). Rank by interview value:
   prefer arcs with a decision, opposition, and a number over accomplishments with none. Flag
   the user's headline claims — the things a JD will most often ask for. Write them to
   `QUEUE.md` as a checklist.
5. **Seed, don't fill.** Do NOT write story files yet. Bootstrap sets up the queue; the
   interview skill writes the stories, one at a time, with the user in the room.
6. **Create `LESSONS.md`** — an empty file whose header says both what the skills do with it
   and what belongs in it: they append the user's corrections here to personalise over time,
   and a rule that would still hold if the corpus were about someone else is not one of them —
   that one belongs to the method, and stays out of this file. The header also states how a
   lesson leaves: one that proves wrong is retired on the user's say-so by marking it in place
   — `~~<the entry>~~ retired YYYY-MM-DD: <one clause of why>` — and a struck entry is no
   longer applied. Nothing in the file is ever deleted.
7. **Hand off.** Point at the top of the queue: *"Your highest-value story looks like <X>. Run
   `/career-corpus:interview <X>` to start."*

## The one rule that matters here

**Bootstrap seeds; it never invents.** A résumé is a *biased index* — it contains what the
user already remembers, which is exactly the material that needs the least help. The queue's
job is to name the arcs; the interview's job is to find what's *not* on the résumé (the
forgotten work, the mistake nobody wrote down, the project that got cut to one line). Don't
let a tidy résumé convince you the corpus is nearly done — it has barely started.
