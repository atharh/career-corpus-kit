---
name: ladder
description: Work the career ladder in either direction against the user's corpus. Assessment mode reads what the vetted corpus holds and says which level the evidence supports — a range with citations, an honest floor, and every shortfall sorted into missing-from-the-file versus missing-from-the-work. Exemplar mode runs the other way — it writes how one story's situation would be told by an invented stranger operating at a named level, as an instrument to compare against, never as material — the output is fiction, quarantined outside the corpus in benchmarks/, never cited, rendered or spoken. Use when the user asks what level their work reads as (senior, staff, principal, EM, director, or the equivalent rung in any role the corpus covers), asks to benchmark a story, wants a target to compare against, or is building a promotion case and needs the bar made concrete.
---

# Career corpus — ladder

**Two modes over one ladder.** *Assessment* reads what the corpus actually holds and says
which level the evidence supports. *Exemplar* runs it the other way: it takes a story and a
level and writes what that situation would look like told from that level — fiction, to
compare against. Same calibration table, same role files, opposite direction, which is why
they live in one skill rather than drifting apart in two.

They chain, and that is the point. Assessment says *this reads as a senior engineer, and the
floor is here*; the exemplar then shows what the floor would look like raised. Run either
alone; run assessment first when the user doesn't yet know which level to aim at.

Everything down to **Running an assessment** concerns the exemplar. That mode comes first
because it is the dangerous one.

Every other skill in this kit exists to keep invented detail out. The exemplar manufactures it
on purpose, which makes it the most dangerous thing in the kit and the reason its containment
rules come before its method.

The problem it solves is real and nothing else touches it. The corpus records what the user
did and how they told it. It has no way to show them **what they didn't do, didn't measure, or
never thought to ask** — a gap of that kind leaves no trace in the material. An interview can
only mine what happened. A verify pass only checks what is written. Neither can say: *the
strongest version of this story opens with a baseline you never took.*

So this skill writes that version. Same situation, same year, same constraints, a different
person in the chair — one operating at the level the user is reaching for. The user reads it
and does the comparison themselves, which is the only way the comparison carries any weight.

**It is an instrument, not an artifact.** It has no standing as evidence, its numbers are
invented, and it is worthless the moment anyone mistakes it for a record.

## Hard rules

These govern the exemplar. Assessment has its own set, further down; the calibration table and
the role files in between belong to both.

**Fiction lives outside the corpus, labelled, in `benchmarks/`.** `[FICTION-IS-QUARANTINED]`
Never write a benchmark into `corpus/`, and never into a story file. `benchmarks/` mirrors
`corpus/` exactly — `corpus/tidewater/batch-window.md` is shadowed by
`benchmarks/tidewater/batch-window.md`: one directory per company, same filename — so a
benchmark sits parallel to the story it shadows and the pairing needs no index to find. One
departure only: a second benchmark of the same story at a different level takes the level as a
suffix (`batch-window-staff.md`), because two of them side by side are a comparison worth
keeping and an overwrite would destroy it. This is structural containment, not a convention:
`render`, `apply` and `prep` read `corpus/` only, so a file outside it cannot reach a résumé
through any path the kit provides — and `verify` skips it too, which matters, because
fact-checking fiction would waste a run and lend it a provenance it must never have. The file
opens with the frontmatter in [`templates/exemplar-frontmatter.md`](templates/exemplar-frontmatter.md),
and the `status:` block
there is the banner: within the first ten lines, this is invented, it is not a record, no line
of it may be cited, rendered or spoken. `tools/corpus_doctor.py` reports any sentence a story
file shares with a benchmark, because that is the one leak the fences cannot see.

**The only exit is a question.** `[ONLY-EXIT-IS-A-QUESTION]` A benchmark beat that makes the
user think *"I actually did that"* is not a claim recovered — it is a claim **unrecorded**, and
the difference is the whole method. Route it to `/career-corpus:interview`, where they say it
in their own words and it gets vetted like anything else. Never lift a sentence from the
exemplar into a story file, never soften one into a prompt that supplies its own answer, and
never let the user's *"yes, that's roughly what we did"* stand in for their account of it —
not under `facts_unvetted` either, because a nod at a benchmark beat is not their account of
anything. The most a session may write into the story file is the question itself, as a gap
item, for the interview to ask — the interview skill's `[BENCHMARK-IS-A-NOD]` is the same fence
on the writing side, where a lift actually happens. `[NEVER-INVENT]` calls a plausible supplied
detail a landmine
with their name on it; this skill builds a field of them, and the fence is the only thing keeping
it useful.

**Same job, different chair.** `[SAME-SITUATION]` The exemplar inherits everything the source
story fixes: the era, the scale, the tech, the org shape, the mandate, the constraints, the
things that were genuinely not available. Only the caliber of judgment varies. Give the
persona a bigger team, a later model, a friendlier VP or a budget the user never had and the
diff stops measuring altitude and starts measuring luck, which teaches nothing. Anachronism is
the commonest failure here, so it has a procedure: before naming any tool, term or practice,
read the source story's `period:` and its `anachronisms_corrected:` block. A term settled in
that block stays out of the exemplar, whatever the persona would call the thing today; anything
else the persona reaches for must have existed in that year, and when unsure, name the
function rather than the product. `[DATE-THE-TERM]` governs the exemplar exactly as it governs
the corpus.

**The level is the user's parameter, and one level up is only the default.**
`[NAME-THE-LEVEL]` *"Benchmark this as a principal engineer"* or *"as a senior EM"* sets the
target, and the answer changes accordingly — a principal telling reaches across orgs and argues
about what the company should build, where a senior telling owns a system and its
consequences. When they name no level, take the source story's role and add one, and **say in
the first line of the response which level you set and that they can ask for another**. Set
the level by scope and verb, never by adjective — see the calibration table below; "more
impressive" is not a level, it is the failure this rule exists to stop. Two things stay true
whatever they name. **Match the track**: a management story gets a manager exemplar, because
modelling an EM's work as an IC's produces a document about a job the user was not doing — and
the track comes from the role the story records, not from the shape of the work, so a
people-and-process story told by someone with no reports still gets an IC persona. Where a
story genuinely spans both tracks, ask which they want rather than splitting the difference.
And **say so when the distance is large**: a senior-engineer story benchmarked at principal is
a legitimate thing to want and a poor target to act on, because almost every beat comes back
unreachable. Write it if they still want it, and name in the frontmatter which gaps are a
*level* problem rather than a *capture* problem, so the file can't be read as a list of things
they failed to do.

**Reachable, not heroic.** `[REACHABLE-NOT-HEROIC]` A flawless exemplar is demoralising and,
worse, uninstructive — the reader learns only that better people exist. The persona operates
under real constraint: a decision made on thin evidence, an argument lost, a thing that broke
with a cost attached, a question still open at handover. At least one beat is a
**strategy-level** misjudgment the persona caught themselves and corrected in public, because
that is the beat that distinguishes altitude from luck, and `[DEMAND-MISTAKE]` explains why a
story where nobody who disagreed turns out to be right reads as a case study.

**Invented numbers show the shape of the evidence, never a value.** `[SHAPE-NOT-NUMBERS]` The
figures exist to make one thing concrete: *what kind of number this beat needs* — a baseline
taken before the work started, a blast radius in hours of other people's time, a cost per unit
of work, a quality floor somebody agreed to in advance. They are never an estimate of what the
user's number was or should have been, and the exemplar never says or implies what their real
figure probably looked like. Every figure the persona gives differs visibly from every number
in the source file — including the ones under `facts_unvetted` and `facts_disputed` — because
a persona's figure that matches the user's is a real number wearing a banner, and nothing
downstream can tell them apart. Keep every number inside the persona's account, where the
banner covers it.

**Model the restraint, not just the achievement.** `[MODEL-THE-RESTRAINT]` The persona
declines the flattering causal claim, names the confound in their own write-up, and draws their
claim boundary unprompted at the end — including saying plainly which parts of the programme
were somebody else's. This is not decoration. Half of what separates a staff+ telling from an
inflated one is knowing what not to claim, and an exemplar that models only accomplishment
teaches the user to inflate.

**Write the exemplar; don't audit the user against it.** `[DIFF-ON-REQUEST]` Deliver the
benchmark and stop. An unrequested comparison reads as a performance review the user didn't
ask for, and it is built on nothing — the skill cannot tell a gap in the *work* from a gap in
the *capture*, and only the user knows which any given beat is. When they do ask for the diff,
run it as a separate pass and sort every finding into **did it and never recorded it** (→
`/career-corpus:interview`), **didn't do it** (→ a lesson, not a defect), and **couldn't have
done it here** (→ discard, and check `[SAME-SITUATION]` held).

## Calibrating the level

Real career ladders separate levels by **the unit you act on and the verb you act with** — not
by how impressive the work sounds. Two tellings of the same project differ by level when the
scope of the noun changes and the verb moves along this ladder:

**does → owns → drives → defines → evangelises, until other teams adopt it without you.**

Published frameworks separate **scope** — what you own — from **reach** — whose plans you
influence without owning them. Keep them apart; conflating them is what makes a benchmark read
as merely bigger rather than higher.

| | Scope: what I own | Reach: who I influence | Horizon | Success looks like |
|---|---|---|---|---|
| **Senior IC** | a service or a workstream, end to end, including the ambiguity in it | my team, starting to spill past it | half a year to a year | it shipped, it holds up, the team's standard rose |
| **Staff / lead IC** | multi-team goals; the seams between teams | other teams' roadmaps bend to mine | one to two years | a system others depend on, and standards the team keeps unprompted |
| **Principal IC** | org-wide goals, or the estate | a group's technical direction; senior leadership are my peers on it | multi-year | something new to the company exists, and other orgs run it without me |
| **Manager** | my team's delivery and people, on well-defined projects | my team and its cross-functional partners | this quarter to the next | the team ships predictably, people grow, problems surface early |
| **Senior manager** | several teams or workstreams, and the operating model | peer orgs; initiatives outside my own area | six to twelve months | outcomes hold across teams I don't run |
| **Director** | a strategic objective tied to a company goal; the portfolio and its budget | the managers below me, and partner functions I up-level | one to two years | it survives my departure, and executives fund it on my framing |

**The five tells** separate levels more reliably than any adjective, and both modes use them
directly.

- **Ambiguity and guidance.** The sharpest of the five, and the one every published ladder
  states in some form: how ill-defined was the problem when it reached them, and how much
  steering did they need? *Clarity created inside a defined problem, with guidance* → *inside
  an ambiguous one, with a little* → *inside a very ambiguous one, with none* → *handing
  decomposed pieces of it to others as their remit*. A story about hard execution on a
  well-specified problem is a level below a story about a problem nobody had specified yet,
  however impressive the execution.
- **Handoff.** Senior work gets finished; principal work gets made *handoverable* — the
  ambiguity is cleared until someone else can carry it.
- **Propagation.** A lead spreads a practice by advocacy; a principal or a senior manager
  builds the mechanism that spreads it without them, and treats organic diffusion as a design
  failure.
- **Stopping.** Junior levels ship things; senior levels also *stop* things — kill a bet,
  retire a tool, cut a scope, decide which initiatives don't continue. The authority to stop
  is one of the clearest level markers there is.
- **Local sacrifice.** From staff upwards, frameworks ask for decisions optimised for the
  wider org over the local project — so the tell is a beat where the author's *own* team took
  the worse deal on purpose, and they can say why. A story where every choice happened to be
  best for the teller's own scope is a story below the level it claims.

**The five pillars**, defined here and nowhere else: **results**, **direction**, **talent**
and **culture**, which frameworks that grade ICs and managers on one rubric expect from both
at every senior level, and **craft** — the technical, design or commercial judgment a role
keeps exercising at every rung, which only a role file can define. The four ladder pillars are
where a benchmark most often comes out miscalibrated: a staff-plus IC exemplar that never says
who got better because of them, or never carries an organisational change they drove adoption
for, is missing a pillar the industry actually promotes on. Craft is the mistake from the
other side: a director exemplar with no system health, no technical judgment, no read on the
competitive landscape. A role file's dimensions are shaped for the stories its craft tends to
produce; no role is excused from the pillars its own list under-serves, which is why each file
names its blind spots.

**Name levels in industry terms, never in an employer's grade codes.** The exemplar says
*principal engineer* or *senior engineering manager*; a company's internal symbol for that
level means nothing outside it and dates the file to one employer.

## Roles — where the craft lives

The ladder above is role-agnostic and stays that way: scope, reach, horizon, the five tells
and the five pillars hold for an engineer, a designer, a marketer or a finance lead alike. What
changes between roles is **the craft** — what the work is made of, what artifacts it produces,
how a story in it characteristically overclaims — and that lives in one file per role under
[`roles/`](roles/), never in this one. That directory sits beside this file, at
`${CLAUDE_PLUGIN_ROOT}/skills/ladder/roles/` — never under the user's corpus — and so do the
templates this skill writes from, at `${CLAUDE_PLUGIN_ROOT}/skills/ladder/templates/`.

**Resolve the role before writing or grading anything.** Take it from the story's own `role:`
field, or from the user's request when they name one, and match it against each role file's
`role:` and `aliases:`. The match is a case-insensitive substring match on the role text with
every parenthesised span removed first — a story's role field routinely carries a grade code, a
promotion arrow or a caveat in brackets, and none of those is the role. Where more than one
alias matches, the longest wins; where the field names two roles with an arrow between them,
resolve the later one and say so. Read the matched file, plus whatever it names in `extends:`.
A filename starting with `_` is a shared fragment, never a role in its own right. Then work
from **that file's** dimension list — six to nine per story, never all of them; forcing the
whole list produces a generic essay about excellence, which is the failure mode to watch for.

**When no role file matches, say so and derive one provisionally.** Build a dimension list
from the five pillars and the five tells, mark the output as running on a provisional role,
and offer to save it as a new role file — [`roles/README.md`](roles/README.md) carries the
schema. Never silently
grade one craft against another's list: a mismatch produces a confident verdict about a job the
user was not doing, which is worse than no verdict.

**A story that spans two roles borrows from each** rather than running both lists end to end,
and the frontmatter or the report says which two.

## Running an exemplar

**Read before writing.** The source story file in full. Its siblings named in `related:`, for
the era, the constraints and the shared vocabulary. `profile.md` for the user's track and
level. Enough to be sure the exemplar is set in the same world. Before drafting, list every
number in the source file — vetted, unvetted, disputed, and in the body prose — and check the
finished draft against that list; a figure that reappears is `[SHAPE-NOT-NUMBERS]` failing, and
a duration or a headcount slips through as easily as a metric.

**Vetting status has no bearing here.** The exemplar takes the story's *shape* — the
situation, the constraints, what kind of thing was built — and an entry under `facts_unvetted`
or `facts_disputed` fixes that shape as well as a vetted one does. Nothing from the story is
carried over as a claim in either case; the persona's account is invented from the first line.
The one exception is a claim the user has struck or withdrawn in place: that records something
that did *not* hold, so it cannot set the situation.

**Ask about two things and only two.** Which story, if they named a company rather than a
file. And the target level — but only when the story's own role is ambiguous or spans both
tracks (`[NAME-THE-LEVEL]`); when they named a level, use it without confirming, and when they
didn't, default to one up and say which you chose.

**Then write the file**, opening with the frontmatter block in
[`templates/exemplar-frontmatter.md`](templates/exemplar-frontmatter.md) — its keys, in its
order, so the shape does not drift between runs — and continuing in this shape:

1. **Frontmatter** — from the template: the banner as the `status:` block; the persona's
   invented name and role; the track and the role file it resolved to; the source story path;
   the target level **and whether the user named it or it was defaulted to one up**; the
   corpus pin; one line on what the file is for; and, only when the distance is large, the
   list of beats that are a level problem rather than a capture problem.
2. **What separates this telling** — four to six structural differences, stated up front, so
   the reader knows what they are looking for before the beats start.
3. **The beats**, six to nine, drawn from the resolved role file's dimensions and ordered as
   the work happened. Each: the situation, what the persona did, the artifact or number it
   produced, and then a short indented **gap line** — the one question this beat would put to
   the reader's own version. The gap line is the mechanism of the whole document; a beat
   without one is just a nicer story.
4. **The bullets this story yields** — three or four résumé lines the exemplar would support,
   so the reader can feel the distance between those and their own at a glance.
5. **The questions this story answers that a weaker one doesn't** — a numbered checklist, and
   the most durable part of the file. It outlives the fiction: the user can run it against
   every other story in the corpus without generating another benchmark.

**Voice.** Write the persona in first person. Third-person summary flattens the altitude
difference into a list of virtues and the document stops working. The banner, the invented
name in the frontmatter and the quarantine path are what carry the containment — not the
pronouns.

**Names.** `[NO-NAMES-CODENAMES]` binds the exemplar too. Real colleagues never appear; the
persona's collaborators are roles. Internal codenames the corpus bans stay banned — render the
function instead.

## Running an assessment

*"Look at what I did at this company and tell me what level that reads as."* The ladder run
backwards: evidence in, level out. It is the mode the user will reach for most, and the one
where being agreeable does the most damage — an assessment that can only flatter is worth
nothing, and they can get that anywhere.

### Rules specific to an assessment

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

### The procedure

1. **Fix the target.** Which company, which period, or the whole corpus — and which track. Ask
   only if it is genuinely ambiguous.
2. **Read the stories in that scope**, including their ceilings, withdrawals and rendering
   decisions. Those are evidence about the *level*, not just about the claim: a user who fences
   their own attribution accurately is demonstrating something a ladder grades. Score from
   `facts_vetted` only (`[VETTED-ONLY]`); everything unvetted or disputed goes straight to the
   interview queue.
3. **Grade against the calibration table first** — scope, reach, horizon — then against the
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

### The report

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

## What this skill is not

- **Not the interviewer.** It asks the user almost nothing and never mines them for material.
  Everything it needs is on disk.
- **Not verification.** It has no opinion on whether the user's claims are true, and it never
  corrects one. Assessment grades what the corpus says at face value, so a story resting on a
  wrong claim gets graded on that claim and the claim stays where it was — that's
  `/career-corpus:verify`, and worth running first if a verdict is going to be leaned on.
- **Not a promotion decision, and not a rating of the person.** An assessment reads one
  session's evidence on one date. It says what a body of written work demonstrates, which is
  a narrower thing than what somebody is capable of, and it should never be handed to anyone
  as though it were the wider claim.
- **Not a rewrite of the user's story.** The exemplar is a *different person's* file and must
  read as one. A polished version of the user's own story is the most dangerous possible
  output: it is the one somebody eventually pastes into a résumé.
- **Not a promotion packet.** It shows the bar; it makes no case that the user cleared it.
  `/career-corpus:render` writes the packet, from the corpus, from vetted claims only.

## Lessons — how this skill personalises to you

This skill ships generic and sharpens by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit. Never edit this
SKILL.md to record a lesson: the method stays stable and shareable; the scar tissue stays
private and personal.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After a correction that generalises, append one dated line**: the mistake, and the rule to
  apply next time. Route it first — a rule that would still hold if the corpus were about
  someone else belongs to the method, not this file. Here that test has a sharp form: a level
  miscalibrated, a horizon wrong, a dimension badly shaped or a tell that fails to separate
  levels is a correction to the ladder or to a role file, whoever is being measured, and it
  reaches the kit through its own process; a dimension the user's domain never had, a
  constraint of their era, or a ceiling on how one of their stories may be told is theirs and
  lands here. Either way the rule lives in a *file*: a rule nobody can diff is a rule nobody
  can review, port, or undo.
- **A lesson leaves this file two ways, each on the user's explicit say-so, entry by entry.**
  One that proves *wrong* is retired in the session where it misfired, struck in place —
  `~~<the entry>~~ retired YYYY-MM-DD: <one clause of why>` — and never applied again; the
  strike records wrongness, which lives nowhere else. One the method has since *absorbed* is
  deleted outright, no strike left behind — a shipped rule's duplicate here can only drift —
  once nothing local remains (no calibration about this user, no number they set, no recorded
  divergence; trim the entry to that residue if any does) and no session still loads a skill
  version without the rule.
