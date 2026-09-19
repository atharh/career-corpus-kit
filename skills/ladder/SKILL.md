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

Every other skill in this kit exists to keep invented detail out. The exemplar manufactures it
on purpose, which makes it the most dangerous thing in the kit and the reason its containment
rules come before its method.

**It is an instrument, not an artifact.** It has no standing as evidence, its numbers are
invented, and it is worthless the moment anyone mistakes it for a record.

## Which file to read

This file holds what both modes share: the two containment rules, the calibration table and
role resolution. Each mode's own rules and procedure sit beside it, in
`${CLAUDE_PLUGIN_ROOT}/skills/ladder/`, and **neither mode is runnable from this file alone**:

- **Exemplar** — read [EXEMPLAR.md](EXEMPLAR.md) in full before opening the source story.
- **Assessment** — read [ASSESSMENT.md](ASSESSMENT.md) in full before opening the corpus.

Read the one the request needs, and both when the user chains them.

## Hard rules

These two hold in both modes, because a benchmark on disk can be misused from either. The
exemplar's remaining rules are in [EXEMPLAR.md](EXEMPLAR.md); assessment's are in
[ASSESSMENT.md](ASSESSMENT.md).

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
