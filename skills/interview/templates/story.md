---
title: <the arc, not the project — "Breaking the docs-platform deadlock", not "DocsPlatform">
company: <folder name — or personal-projects, for an arc that belongs to no employer>
role: <the role they held DURING this arc — not their title at the company>
authorship:          # who produced the artifact itself — establish it before anything renders
                     # (`[WHO-OWNED-IT]`'s provenance tell). Authorship is not proficiency in
                     # the stack; record each claim separately. Required for personal projects.
  - <artifact> — <by hand | directed an agent that wrote it | one of N authors> (source, date)
period: <what's actually known. "?" is a legitimate value. Don't guess.>
status: <seed | drafted, partially fact-checked | drafted>
related:
  - <other-story.md (why they must be read together)>
# These three record PROVENANCE, not proof. Nothing here means "independently
# verified" — see "What 'vetted' means" in the interview skill.
facts_vetted:        # they assert it themselves, and this file records where and when.
  - <fact> (source, date confirmed)
facts_disputed:      # sources disagree about the size or shape of one claim.
  - <claim A> vs <claim B>. UNRESOLVED. Neither value renders. A floor both
    sources agree on may render once the user settles it in a RENDERING
    DECISION below — never chosen by the model on its own.
facts_unvetted:      # they said it, but their standing for it is weak: second-hand,
                     # another person's private state, or a precise number resting on
                     # an old memory with no artifact. Lower ceiling, not silence —
                     # say why it's weak AND what may still be said.
  - <fact> — <why the standing is weak>. <what may still be said, if anything.>
sources:
  - <resume-file>.md (vetted)
  - interview with <user>, YYYY-MM-DD (vetted)
  - <prior AI chat draft, pasted YYYY-MM-DD (unvetted prose, AI-written)>
overridden:          # only if the user overrode the corpus or a skill rule (render's
                     # [USER-OVERRIDES]) — dated, so a later session can tell a directed
                     # claim from a corpus-vouched one.
  - <date> — <what they directed>
---

<If the story describes real people who aren't public figures — especially anyone managed
out, put on a plan, or overruled — open with:>

**NO NAMES. Ever. Roles only.** <one line on who is described here and why it stays private.>

## Setup

<The stakes, written once. Every beat below hangs on this and never restates it.
Company-level context belongs in background.md, not here — this is what's specific to *this
arc*.>

<Where the résumé's phrasing is misleading, say so plainly and explain why. e.g. "two-year
deadlock" is true but implies a long project; the reality was a frozen product with activity
on top.>

## Beat: <the decision, stated as a decision>

<What they chose, what they chose against, who wanted the other thing, and the actual
argument — not the tidy retrospective one. The reasoning is corpus material; their opinions
are corpus material. The essay shape is not.>

## Outcome

<What happened. Numbers with sources. If a decision caused the outcome, say so explicitly —
they'll report both without connecting them, and the connection is usually the point.>

## What it cost

<Who lost. What broke. What the predicted disaster turned out to be. A story with no cost is
a case study.>

## What I'd do differently

<The real regret, at its real size. Keep the tension honest: "the decision was right, but one
of my reasons for it was wrong" is a better sentence than either half alone.>

## Judgment (theirs, worth keeping)

<Lines that are their philosophy rather than their history — the reusable convictions. These
are what renderings are built from.>

## Gaps — the interview queue

<Only questions whose answers would change a bullet, a letter, or a spoken answer — the
say-it-out-loud test `[SAY-ALOUD]`. Not everything you'd like to know. If it fails that test,
don't write it here; delete it. Lookups you can do yourself are never gaps.>

- [x] ~~<resolved question>~~ Resolved YYYY-MM-DD: <the answer, briefly>.
- [ ] **<the sharpest unanswered question, in bold>**
- [ ] <question>
- [ ] Verify: <every fact in facts_unvetted>
- [ ] <only if this arc landed vetted material about a technology with no capability file
      yet: `../capabilities/<technology>.md` — forward pointer, no file yet
      (`[CAPABILITY-HARVEST]`)>
