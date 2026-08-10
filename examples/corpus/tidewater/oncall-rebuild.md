---
title: Rebuilding the on-call rotation, and the change I had to reverse
company: Tidewater Logistics
role: Senior Software Engineer
period: 2023-04 – 2023-11
status: drafted — this is the story with the mistake in it, and it's the strongest one
related:
  - batch-window.md (the pager pain that started this)
facts_vetted:
  - the rotation covered 6 services with 8 engineers on it, one week in eight
  - Q1 2023 had 31 out-of-hours pages across the rotation
  - by Q4 2023 that was 9
  - Sam proposed and ran the change; their EM sponsored it; nobody reported to Sam
  - Sam cut the rotation from 8 people to 5, then reversed it after ~7 weeks
facts_unvetted:
  - "'two people told me they were considering leaving over the pager' — Sam's account of
    private conversations. True as far as it goes; unverifiable, and not theirs to prove.
    Fine to say in an interview as a personal recollection. Never a résumé line."
sources:
  - interview with Sam, 2026-03-02 (vetted)
  - "internal incident review doc, shown 2026-03-02 — NOT stored, see note"
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented people, invented numbers and quotes.
> Shows the corpus format only — never a source.

**NO NAMES. Roles only.** Two colleagues' burnout and one person's near-resignation are
described here. This corpus stays private.

## Setup

31 out-of-hours pages in Q1 2023 across an eight-person rotation. Most were the same four
alerts. Nobody had touched the alerting rules in two years because everyone was too busy being
paged by them — the failure mode of every bad rotation.

Sam had no authority here. They had a pager, a sponsor in their EM, and the credibility from
`batch-window.md`.

## Beat: the boring part that worked

Three weeks of triage before changing anything: every page from Q1, categorised by whether a
human action was actually required.

**19 of 31 required no action.** They were alerts on symptoms that self-recovered inside the
window a human would take to open a laptop.

So the first change wasn't process, it was deletion — those alerts came out or got a
recovery-delay threshold. That alone took Q2 to 14 pages.

## Beat: the mistake

**Sam then cut the rotation from eight people to five.**

The reasoning was defensible and Sam still explains it without flinching: fewer people on the
rotation means each one sees it more often, builds real familiarity, stops treating every page
as a novel event. Context-switching costs are real. Depth over breadth.

**It was wrong, and the reason it was wrong is the useful part:**

> *"I optimised for the quality of the response and completely ignored the load on the
> responder. Eight people, one week in eight. Five people, one week in five — and I did that to
> the exact three people who'd been carrying the most already, because they were the ones who
> knew the systems. I made the good responders' lives worse as a direct consequence of them
> being good. One of them told me, fairly bluntly, about six weeks in."*

Reversed after seven weeks, back to eight, and Sam wrote up why in the team channel rather than
quietly rolling it back.

**What they'd do differently, at its real size:** not "consult more" — Sam is specific that they
*had* consulted, and everyone agreed in the room because the argument sounded good. *"The
mistake wasn't skipping a step. It was that I never asked what the change would feel like in
week five for the person with the most pages. That question doesn't come up in a design review.
I've asked it about every process change I've made since."*

## Outcome

Q4 2023: **9 out-of-hours pages**, down from 31. Rotation back at eight people.

⚠️ **The causal link is honest but partial**, and Sam flagged it: *"the alert cleanup did most
of that. The rotation stuff I got wrong and reversed. I don't want a bullet implying the
headcount change is why the number went down, because it isn't."*

## 📌 RENDERING DECISION — 2026-03-02

**This is the story to bring to any interview that asks for a failure, and the reversal stays
in.** A candidate who reversed their own change in seven weeks, in public, on the evidence of
one honest colleague, is describing judgment. The polished version — "cut pages 70%" with the
reversal filed off — is both weaker and checkable by anyone who worked there.

The résumé bullet carries the number. **The reversal is interview material, not résumé
material** — not because it's hidden, but because a bullet has no room to make it land, and
half-told it just looks like a mistake.

## Gaps — the interview queue

- [ ] **Did the alert cleanup hold after Sam stopped watching it?** Q4 2023 is the last number
      recorded and it's now 2026. If it crept back up, that's a more interesting answer than the
      original fix — and if it didn't, that's the real result.
