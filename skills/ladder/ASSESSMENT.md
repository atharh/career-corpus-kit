# Ladder — assessment mode

Read after [SKILL.md](SKILL.md), which carries the two containment rules, the calibration table
and role resolution. This file is the rest of the mode: its rules, its procedure, its report.

*"Look at what I did at this company and tell me what level that reads as."* The ladder run
backwards: evidence in, level out. It is the mode the user will reach for most, and the one
where being agreeable does the most damage — an assessment that can only flatter is worth
nothing, and they can get that anywhere.

## Rules specific to an assessment

**The level comes from the evidence, never from the title.** `[LEVEL-FROM-EVIDENCE]` What the
user was called is an input to set aside, not a prior to confirm — a senior manager's title on
a body of work that demonstrates a manager's scope is exactly the finding worth having. Read
the stories for what was owned, who was influenced, over what horizon, and grade that. If the
verdict lands on the title anyway, say what carried it rather than letting the coincidence do
the arguing.

**A thin file is a capture gap, not a competence gap — and the two get different verdicts.**
`[CAPTURE-GAP-ISNT-A-GAP]` The corpus records what the user chose to write down, so absence of
evidence is genuinely ambiguous, and collapsing that ambiguity into a level is the single most
damaging thing this mode can do. Every shortfall gets sorted before it is scored: **missing
from the file** (→ name the story and send them to `/career-corpus:interview`), **missing from
the work** (→ a real gap, and the honest half of the assessment), or **not available in that
role** (→ excluded from scoring, not held against them). When you cannot tell which, say so
and ask — one question is cheaper than a wrong grade.

**Only vetted facts score.** `[VETTED-ONLY]` A story file sorts its claims, and the sort is
the evidence's own grade: `facts_vetted` counts, and nothing else does. An entry under
`facts_unvetted` or `facts_disputed` is not held against the user, but it is not credit either
— it is a capture gap, and goes in the interview queue with the story named. A claim the user
has struck or withdrawn in place is excluded outright: it records something that did not hold.
Grading the unvetted version of a file is the quiet way an assessment inflates: the user never
asserted those claims, and the verdict would rest on them anyway.

**The recorded ceilings bind the verdict.** `[CEILINGS-BIND-THE-VERDICT]` Score the claim as
the story's ceilings leave it, never as the unfenced version. Work the user disclaimed —
somebody else's decision, a team's build, a mandate executed rather than authored — counts at
the level of *their actual contribution*, and air cover for a report's programme is a
manager's evidence rather than a director's. This is the rule that makes the whole mode
trustworthy: a grade that quietly re-inflates what the user themselves fenced off is worse
than no grade, because they will take it into a room and defend it.

**The most recent role carries the verdict, and an old story is graded in its own year.**
`[RECENT-ROLE-CARRIES]` Stories combine by consistency, not by peak. Over a company or the
whole corpus, the level is what holds across the stories of the most recent role: each pillar
sits where its weakest recent story leaves it, and one story at a higher level is a spike to
name, not a verdict to award. Earlier roles can fill a pillar the recent role has no evidence
on, and never lower one it does. A story a decade old is graded on scope, reach and horizon
as they were in its period — the ladder's axes don't date — and is never docked for a craft
dimension, an artifact or a practice that did not exist in that year; that is the assessment's
counterpart of `[SAME-SITUATION]`, and the source story's `period:` and
`anachronisms_corrected:` block say what the year allowed.

**Report a range and name the floor, because the floor is what gates a promotion.**
`[RANGE-NOT-A-POINT]` Nobody sits at one level across every pillar. Give the honest spread —
where they are solid, where they spike, where they are absent — and state plainly which weak
pillar is holding the level down. Ladders promote on consistency, not on a peak, so a single
outstanding dimension does not lift a verdict and should be named as a spike rather than a
level. One story shows a level *in that instance* and never a career level: asked about one
file, grade the file and refuse the generalisation.

**Cite every grade, and say the uncomfortable one plainly.** `[CITE-THE-GRADE]` Each pillar's
verdict points at the story and line that carries it; a grade with no citation is an
impression and gets marked as one. Where the evidence reads *below* the user's current title,
say it in the first two sentences, without cushioning and without apology — then spend the
detail on what would move it. `[REACHABLE-NOT-HEROIC]` applies here too: the delta to the
next level is stated as two or three specific things, not as a verdict on them.

## The procedure

1. **Fix the target.** Which company, which period, or the whole corpus — and which track. Ask
   only if it is genuinely ambiguous.
2. **Read the stories in that scope**, including their ceilings, withdrawals and rendering
   decisions. Those are evidence about the *level*, not just about the claim: a user who fences
   their own attribution accurately is demonstrating something a ladder grades. Score from
   `facts_vetted` only (`[VETTED-ONLY]`); everything unvetted or disputed goes straight to the
   interview queue.
3. **Grade against the calibration table in `SKILL.md` first** — scope, reach, horizon — then against the
   resolved role file's dimensions, artifacts and blind spots. Scope and reach carry the
   verdict; the dimensions explain it; the artifacts turn a soft grade into a question with a
   name on it.
4. **Sort every shortfall** into the three buckets from `[CAPTURE-GAP-ISNT-A-GAP]` before
   writing anything.
5. **Deliver in the terminal.** An assessment is a report to the user, not an artifact —
   nothing is written to disk unless they ask. If they do want it kept, it goes to
   `benchmarks/<company>/assessment.md` (or `benchmarks/assessment.md` for the whole corpus)
   in the shape of [`templates/assessment.md`](templates/assessment.md), whose frontmatter
   carries `generated:` (the
   date) and `corpus_pin:` (the commit SHA of the corpus it read), plus a line saying it is
   one session's read of the corpus at that pin, not a rating of the person. A date alone is
   not a pin: nothing can be diffed against it, and the corpus moves under every saved
   verdict.

## The report

[`templates/assessment.md`](templates/assessment.md) carries this shape; the terminal version
has the same sections and no frontmatter.

- **The verdict, in one sentence**, with the range and any track caveat.
- **A pillar table**: dimension, the level the evidence supports, and the `file:line` that
  carries it. Sorted with the floor first — the weakest pillar is the actionable row, so it
  should not be buried under the flattering ones.
- **The strongest evidence**, two or three items, named as what an interviewer would find
  most convincing.
- **The floor**, with what specifically is thin and which bucket it fell in.
- **The delta**: two or three concrete things that would move the verdict a level, each
  phrased as work or as capture, not as a personal quality.
- **The interview queue**: the stories where the level is probably in the work but not in the
  file — the highest-value output of this mode, and the one that routes straight to
  `/career-corpus:interview`.
