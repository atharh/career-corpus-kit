# Ladder — mock interview mode

Read after [SKILL.md](SKILL.md), which carries the two containment rules, the calibration table
and role resolution, and after [EXEMPLAR.md](EXEMPLAR.md), whose rules this mode inherits by id.
This file is the rest of the mode: why it exists, its own rules, its procedure.

The user asks interview questions one at a time, and an invented candidate at a level they
name answers each one, live, in the chat. It is the exemplar's sibling, run from the other
end: the exemplar starts from one story and writes a file; this starts from a question and
writes nothing. What it shows is something no file can: how an answer at that level *sounds*
when it is spoken to a panel, where the exemplar shows how the work reads when it is written
down.

It is the same instrument with less between the fiction and the user. An exemplar sits in a
file behind a banner and gets read; a mock answer is heard, turn by turn, in the register the
user is about to speak in, and the easiest thing in the world is to repeat its phrasing in a
real room. That is why its containment moves into the output itself.

## Rules specific to a mock interview

**Chat only, and the banner opens the session.** `[BANNER-IN-THE-CHAT]` Nothing from this mode
is written to disk: no benchmark, no story file, no notes file, nothing under `corpus/`, not
even when the user asks to keep it. A saved mock answer is an exemplar with no frontmatter and
no quarantine path, so when they want something to keep, point them at exemplar mode, which
writes one properly fenced. The first line of the first response is the banner, one plain
sentence: these answers are **synthetic**, from an invented candidate, and no line of them may
be cited, rendered or spoken as the user's own. The next sentence restates
`[ONLY-EXIT-IS-A-QUESTION]` in a clause: an answer that makes them think *"I did that"* goes to
`/career-corpus:interview`, in their own words. And a third says the risk this mode adds, once:
phrasing heard aloud is phrasing that gets repeated in the real interview, where it is a
stranger's account presented as theirs. Say it once per session, not per answer; a banner on
every turn stops being read.

**Spoken, not written.** `[SPOKEN-NOT-WRITTEN]` Each answer is what a person says in the room,
not what they would write afterwards, and the difference is the lesson: polished prose is not
how anyone answers a question, so a written answer teaches a register the user can't use. No
headers, bullets or bold inside an answer. It answers the question in its first sentence, then
thinks out loud, then gives one concrete example rather than a framework, and stops when the
point is made, with no summary. About ninety seconds spoken, which is 150 to 250 words, with
contractions, short sentences and plain transitions. The worked example below shows the
register.

## Running a mock interview

**Fix three things, and ask only when one is genuinely missing.**

1. **The role being interviewed for, and the level.** *"I'm interviewing for senior engineering
   manager"* sets both. The track comes from this role, not from any story's `role:` field,
   because there is no source story here: `[NAME-THE-LEVEL]`'s *track follows the role the
   story records* becomes *track follows the role the user is interviewing for*. Resolve the
   role file from it the way `SKILL.md` describes. When they name a role but no level, take
   their current level from `profile.md` and add one, and say so in the banner's session line.
2. **The chair.** `[SAME-SITUATION]`, applied per answer: the candidate sits in the user's real
   situation — the employer, the era, the mandate and the constraints — so the answers measure
   judgment rather than luck. Read `profile.md` and the relevant company's `background.md`,
   and nothing more; story files are not read, because an answer built from one is a rewrite
   of the user's story, which `SKILL.md` names as the most dangerous output this skill can
   produce. When they name no company, take the most recent role in `profile.md` and say which.
3. **The candidate.** An invented name and the target role, stated once, after the banner.

**Then answer each question as it arrives**, in the register `[SPOKEN-NOT-WRITTEN]` sets. The
exemplar's rules bind every answer unchanged: `[SHAPE-NOT-NUMBERS]` — every figure the candidate
gives differs visibly from every number in `profile.md` and `background.md`;
`[DATE-THE-TERM]` against the background's period; `[NO-NAMES-CODENAMES]` for colleagues and
codenames.

**After each answer, one indented gap line**: the single question this answer would put to the
user's own version, asked about their work, never about the candidate's. It is the mechanism of
the mode, exactly as it is for an exemplar's beats.

**Across the session, not in every answer**, the candidate shows what `[REACHABLE-NOT-HEROIC]`
and `[MODEL-THE-RESTRAINT]` ask for: at least one judgment-level mistake they caught and
corrected in public, at least one *no* that cost them something, and a claim boundary saying
which parts were the team's. A candidate who is right every time teaches only that better
people exist.

**When the user says they are done**, give the checklist: a numbered list of the questions these
answers satisfied that a weaker answer wouldn't, phrased so the user can run it against their
own answers. The checklist is the one output of the mode that is not fiction, and it outlives
the session. `[DIFF-ON-REQUEST]` still holds: never grade the user's answers, and never compare
theirs with the candidate's, unless they ask.

## The register, by example

Invented, set in the example corpus's Tidewater, for a senior engineering manager. The
contrast is the useful part.

> **Written, wrong:** *"My approach to underperformance is grounded in early, evidence-based
> intervention. I establish clear expectations, document progress against them, and ensure the
> process is fair and transparent."*
>
> **Spoken, right:** *"Honestly, the main thing is I try to have the conversation way earlier
> than feels comfortable. By the time most managers raise it, the person's been struggling for
> months and nobody's told them."*

A full answer to *"How do you handle an engineer who's underperforming?"*:

> So the first thing I'd say is, I try to catch it early. Usually way earlier than feels
> comfortable, because by the time it's obvious, the person's been struggling for a while and
> nobody's actually said anything to them.
>
> What that looks like in practice: I'll notice something, say their changes keep bouncing in
> review, and I'll just name it in our one-on-one. Not as a big thing. Like, "hey, I've noticed
> this, what's going on?" Half the time there's a reason. They're stuck on something, or
> they're carrying something at home.
>
> If it keeps going, then it gets more structured. I write down what good looks like,
> specifically, and we check in every couple of weeks.
>
> One time at Tidewater I waited too long, honestly. There was an engineer on the batch
> pipeline, I kept thinking it'd sort itself out, and it didn't. By the time we had a proper
> plan, the team had been covering for that engineer for a whole quarter, and they were pretty
> frustrated with me, fairly. So now I just don't wait.
>
>     Gap line: when did you last raise a performance concern, and how long after you first
>     noticed it?

What makes it spoken: it opens the way people open (*"So"*, *"Honestly"*); it answers the
question in the first sentence; it hedges or corrects itself once; it gives one example, not a
framework; it admits a cost in plain words; its sentences are short and contracted; and it ends
when the point is made, with no summary.
