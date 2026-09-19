# Ladder — exemplar mode

Read after [SKILL.md](SKILL.md), which carries the two containment rules, the calibration table
and role resolution. This file is the rest of the mode: why it exists, its rules, its procedure.

The problem it solves is real and nothing else touches it. The corpus records what the user
did and how they told it. It has no way to show them **what they didn't do, didn't measure, or
never thought to ask** — a gap of that kind leaves no trace in the material. An interview can
only mine what happened. A verify pass only checks what is written. Neither can say: *the
strongest version of this story opens with a baseline you never took.*

So this skill writes that version. Same situation, same year, same constraints, a different
person in the chair — one operating at the level the user is reaching for. The user reads it
and does the comparison themselves, which is the only way the comparison carries any weight.

## Rules specific to an exemplar

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
the level by scope and verb, never by adjective — see the calibration table in `SKILL.md`; "more
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
