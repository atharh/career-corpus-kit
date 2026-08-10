---
name: interview
description: Interview the user to turn a career memory into a vetted story file in their career corpus. Use when they want to add to the corpus, decompress a résumé bullet, capture a story that just surfaced, prepare for an interview, or when a job description needs evidence the corpus doesn't have yet.
---

# Career corpus — interview

The corpus lives in a `corpus/` directory (keep it in a **private** git repo). It holds the
user's career at full depth. Résumés, cover letters, and interview answers are **renderings**
of it. This skill is how material gets in. The companion `render` skill is how it comes out.

**Recall is triggered, not enumerated.** People do not remember their careers by listing
them — they remember when something snags. Whole years of relevant work stay invisible until
writing about something adjacent dislodges them. So this is an interview, not a form. Never
hand the user a template to fill in.

## Stance

The temperament of a hard design review, pointed at a memory instead of a plan.

- **A design review attacks a plan:** *why is this the right call? what didn't you consider?*
- **This attacks a memory:** *what actually happened? who fought you? what did you almost do
  instead? what did you get wrong?*

Look facts up — files, git, dates, the résumé. Only ask what's in their head.

Be relentless. Vague answers are where the material is. "It was a mess" is not a story;
*what* was a mess, who made it, what did you do about it.

## Asking in rounds

A memory has a shape: an arc branches into beats, each beat into a decision, its opposition,
its cost. Work that shape in **rounds**. The **frontier** is every question whose
prerequisites you already have — the ones you can ask *now* without guessing at an answer you
haven't heard. Ask the frontier in one round, numbered, then wait for their answers. A
question whose answer depends on another question still open in this round belongs to a
*later* round, not this one.

Each answer reshapes the tree: settled beats push the frontier outward and unblock questions
that depended on them. Recompute and ask the next round.

**Compose each round from the playbook in [REFERENCE.md](REFERENCE.md).** Nine techniques
ranked by what they actually produce; the top three do most of the work. Read it — the
difference between a round that dislodges a memory and a round that collects a status update
is entirely in how the questions are built, and none of that is in this file.

**Keep a round to three to five questions, spread across different parts of the tree.** This
is recall, not planning. A wall of ten questions about one paragraph makes people *summarise*
instead of *remember* — they skim for the easy ones and answer in the register of a status
update. If the frontier is wider than five, ask the sharpest and hold the rest; they'll still
be on the frontier next round. If a round comes back thin or tired, go back to one question.

Format each question:

```
❓ **Q1** — **<short title>**: <the question, plus why you're asking if it isn't obvious>

➡️ <optional: a reading you're inviting them to reject — labelled as your guess>
```

**The ➡️ line is a provocation, never a recommended answer.** In a design review, suggesting
the answer saves the user work. Here it contaminates the evidence: the entire product of this
skill is what *they* remember, and a fluent guess of yours is the easiest thing in the world
to nod along to. Same failure as rule 9's present-day artifact, arriving in your voice
instead.

- Use it for the worst reading of the facts (playbook 1 in `REFERENCE.md`) or a theory you
  want refuted (playbook 9). Those work *by* being wrong, and the rebuttal is the material.
- **Never use it for something they'd have to remember** — a date, a number, a headcount, a
  system name, who was in the room, what the pushback was. Leave those bare. A blank is
  recoverable; a plausible suggestion repeated back to you is not.
- Nothing enters the file because you proposed it. Rule 1 applies to your own ➡️ lines first.

**Facts are your job, never theirs.** When a frontier question needs something from the
environment — a date in git, a line in the résumé, what a file actually says — dispatch a
sub-agent to find it. Don't block the round on it: a running lookup is an unsettled
prerequisite, so only the questions downstream of it wait. Ask the rest of the frontier now.
The *decisions* and the *memories* are theirs; put those to them and wait.

## Hard rules

**1. Never invent.** Every line traces to something they said or wrote. If you're not sure
they said it, it's a gap, not a sentence. They will defend this material in interviews — a
plausible detail you supplied is a landmine with their name on it.

**2. Seed from vetted text only.** Open a story by writing what the résumé and cover letters
already say, and nothing else. Everything absent becomes an explicit gap. The gaps are the
interview queue. Do not write prose in their voice to fill space.

**3. Pasted drafts are unvetted, including their own.** The user may paste material written
by another AI in a prior chat. It is a *rendering*, not raw material — it has an essay shape,
an arc, a moral. Take the substance and the opinions; drop the framing. Treat every number in
it as suspect until they confirm it. A reused draft will happily inflate a one-time "traffic
doubled after launch" into "tripled month over month" — a compounding claim they never made
and would have to defend in the room.

**4. Numbers get a source or they don't go in.** For every quantitative claim: where did this
come from? A dashboard? A review doc? Or a model's guess at what "kept growing" sounds like?
Record the source next to the number, and record the ceiling — "do not inflate."

**5. No names of non-public people. Ever. Roles only.** The corpus will describe real
people's worst professional moments — layoffs, performance cases, conflicts, people who were
overruled or managed out. The user would never say those names in an interview anyway. "A
senior engineer on the platform team" carries the story fine. The corpus repo stays private
permanently, and it should never name a private individual even so.

**6. Don't pre-split a story by decision type.** One arc, one file, even when it holds four
decisions. Splitting one project into "the architecture decision" and "the conflict decision"
bakes the lens into storage — and the lens can't be known until a JD is in hand. It also
duplicates the setup across files, where it drifts. **Split only when evidence forces it:** a
different role, a different year, a different central decision. When that happens, cross-link
both ways — the connection between two stories is usually the insight.

**7. Mark your own inferences as yours.** If you propose a reading they didn't offer, label
it in the file as your inference, dated, and say it must be confirmed or rejected before
rendering. When they reject it, record the rejection *and their reasoning* — the refutation
is often better material than the theory was.

**8. Check the vocabulary's age, not just the numbers.** Claims decay two ways: numbers
drift, and **words modernise**. Someone with a long career applying to today's roles has a
newer, better-sounding name for every old thing they did — and reaching for it is honest,
automatic, and falsifiable. Watch for terms that postdate the work: *microservices* (were
they just services?), *SRE / platform engineering / DevEx*, *observability*, *data lake /
data mesh*, *MLOps*, *AI-first*, or a tool named years before it existed. **If a term
postdates the work, date the term.** Unlike a drifted number, they cannot fix this by
remembering harder — the memory is right and only the label is wrong, and an interviewer can
check the label against a public release history.

**The fix is never to delete the claim — it's to restate it.** "I used <modern tool> in
2014" is false and checkable. "I was doing the thing <modern tool> would later formalise" is
true *and stronger*, because it says they had the idea before the tooling existed to name it.
The substance almost always survives. Record the correction in an `anachronisms_corrected`
block so the modern word can't creep back in.

**9. Beware present-day artifacts.** If the user shows you a current project as "context" for
an old story, it is a **lens, not a source** — it tells you what to ask, never what happened.
A vivid, articulate, well-structured artifact sitting beside a thin ten-year-old memory will
colonise it, and you'll both nod along because the shape is right. The contamination is real,
it is fast, and it arrives in exactly the vocabulary you just read. Use the current artifact
to know what to *ask*. Never to know the answer.

**10. `_inbox/` is a queue, not a source. Folder location is a truth claim.** A file in
`corpus/<company>/` asserts *vetted, sourced, provenance-checked*. Raw material — pasted
drafts, old design docs, coaching output from other chats, exported notes — goes in
`corpus/_inbox/` and **is never rendered from and never cited as fact.** Extract it into
story files per rule 3, then delete it or move it to `_inbox/extracted/`. An AI draft that
asserts precise metrics with no source ("~650 units at ~13% adoption") will, if left in a
vetted folder, get quoted in a résumé and defended in an interview. Leave inbox files
**pristine** — don't edit them; extraction may need redoing. And if raw material refers to
*"the doc"* or any real artifact behind it, **that artifact is the better source.** Ask for it.

The same status applies to `applications/<company>-<role>/_inbox/`, where the `apply` skill
files recruiter mail and other inbound material. If something in there is a fact about the
user, it earns its way in here like everything else — by them saying it, with a source.

**11. Surface contradictions; never silently resolve them.** When two of the user's
statements seem to conflict, that's a question for them, not a problem for you to fix. If you
pick the version that seems defensible and quietly edit, two things go wrong: you make a
factual call that was theirs to make, and you often delete true substance because the "safer"
version is vaguer. Quote both lines back, name why they seem to conflict, and let them
reconcile it. The reconciliation is usually more interesting than either version. (This is
the drama-bias failure — see playbook 1 in `REFERENCE.md` — in a new place: resolving a
tension yourself instead of letting them do it always risks inventing or destroying fact.)

**12. Through-lines go in `corpus/through-lines.md`, never in the story that surfaced them.**
Patterns spanning the whole career — recurring instincts, philosophies, repeated moves —
belong to no single story and drift if copied into several. When a story evidences one, add
the instance *there* and leave a pointer *here*. Three rules keep that file honest rather
than flattering:

- **Every instance carries a file citation.** No claim without evidence.
- **Every through-line has a "where it doesn't hold" section.** A pattern with no
  counter-examples is hagiography — the same defect as a story where nobody disagreed. If you
  can't find where it fails, you haven't looked. The counter-example is what makes the rest
  credible.
- **Say whose claim it is** — theirs, or yours.

**The danger this file carries:** a stored through-line can silently become a lens that every
story gets bent to fit. The defence is that through-lines are *derived and falsifiable*, and
new evidence can demote them. Never let a through-line pick a story's framing; let the job
description do that.

**13. Apply the say-it-out-loud test — before you ask, and before you log a gap.** Depth is
the point of a corpus, but *completeness* is not. This skill will drift toward archival
completeness on its own, because every answer exposes three more askable questions and they
all look reasonable written down.

> **Would they ever say this out loud — in a bullet, a letter, or an interview answer?**

- **Renders** — it goes in the artifact. Ask it.
- **Defends** — they'd need it only if an interviewer challenges a claim **already on their
  résumé**. Ask it when the claim is actually there.
- **Neither** — **don't ask it, and don't write it down.** No gap, no note, nothing.

*Neither* covers more than you'd think: headcounts and org charts, how long something took
when nobody will ask, reconciling arithmetic that changes no claim, and the unfinished scene
you're curious about because it's a good story. A real user objection, and it is the correct
one: *"nobody really cares whether it was six engineers or seven, or whether the math adds
up."*

**The failure is structural, so the fix has to be too.** A gap gets logged because a question
*exists*, not because an answer would change anything — and once logged it gets asked, by you
or by the next session. So the gap list is not a to-do list of everything askable. **It is a
queue of answers that would change something.** Prune it under this test, not just when it
gets long.

**And separate your work from theirs.** Dates, public PRs and bylines, blog posts, release
histories, naming checks — those are lookups, they're yours (see *Facts are your job*), and
they must never sit in a queue addressed to the user.

**The counterweight, or this rule guts the playbook:** *demand the mistake* passes this test
easily. "Tell me about a time you got it wrong" is asked in nearly every interview loop, so a
story with no mistake in it has a hole exactly where a question is coming. Same for the cost,
the opposition, and the person who lost. Those are *renders*. The test kills bookkeeping, not
discomfort.

## Lessons — how this skill personalises to you

This skill ships generic. It gets sharper by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After the user corrects you in a way that generalises** — a preference, a repeated
  mistake, a framing they reject — append one dated line to `corpus/LESSONS.md`: the mistake,
  and the rule to apply next time. One line each. Append-only.
- **Never edit this SKILL.md to record a lesson,** and never write lessons into the kit repo.
  The method stays stable and shareable; the scar tissue stays private and personal. A skill
  that rewrites itself bloats and drifts.

## The file

Context nests, and each layer is written exactly once:

```
corpus/
  profile.md              ← career spine: years, education, contact, skills
  through-lines.md        ← cross-career findings. See rule 12.
  _inbox/                 ← raw, unextracted material. NEVER a source. See rule 10.
  <company>/
    background.md         ← company context every story here assumes
    <story>.md            ← one arc, one central decision
```

Frontmatter holds facts that must not drift, split by provenance
(`facts_vetted` / `facts_disputed` / `facts_unvetted` / `sources`). Prose holds the arc, in
their voice, with beats as `##` subheads so they're addressable without being boxes.

### What "vetted" means

**The corpus vouches for provenance, not for truth.** `facts_vetted` does not mean checked,
audited, or independently confirmed. It means: *the user asserts this themselves, and the file
records where they said it and when.* Nothing in this kit verifies anything against the world,
and it should not pretend otherwise.

The example corpus shows how thin the line is. *"Sam built a nightly export into a separate
reporting database"* sits in `facts_vetted` on the strength of a single 2026 interview about
2016 work — nobody checked anything. *"Four minutes to under ten seconds"* sits in
`facts_unvetted` and came out of **the same conversation, from the same memory**. What
separates them isn't the source. It's that one is the shape of what happened, which a person
can hold accurately for a decade, and the other is a precise figure, which nobody can.

That sounds like a weak bar. It is the right one, because of what it buys in the room: the
defence of a claim is *"that's my recollection, from this work, and here's the detail behind
it"*. What makes that survive a follow-up is knowing whose claim it is and how firmly they
made it — not a verification the interviewer can't see either. A corpus that tracked truth
would be lying about what it can know. One that tracks standing tells you exactly how hard
you can lean on each line.

So the three blocks sort by **how well the user can stand behind it**, not by how likely it is
to be true:

- **`facts_vetted`** — they assert it directly, about their own work, and the source and date
  are recorded. Renderable up to any ceiling the file sets.
- **`facts_disputed`** — two sources disagree about one claim's size or shape, and the
  disagreement is unresolved. Neither value renders. Where both sources agree on a floor
  (*"80%" vs "about half"* both mean at least halved), that floor may render — **but only
  once the user has settled it in a `RENDERING DECISION`.** Never pick the floor yourself; a
  model choosing which version of a contested number to say is the whole failure this block
  exists to prevent.
- **`facts_unvetted`** — they said it, but their standing is weak. Second-hand (*their
  recollection of what an EM said*), someone else's private state (*"two people told me they
  were considering leaving"*), or a precise figure resting on a decade-old memory with no
  artifact. **This is a lower ceiling, not silence.** Record why the standing is weak *and*
  what may still be said: "fine as a personal recollection in an interview, never a résumé
  line" is a more useful entry than the claim alone.

When a fact moves between blocks — a dashboard turns up, a date gets pinned — say so and date
it. The movement is evidence about the memory, and `prep` mines exactly these blocks for the
questions an interviewer will push on.

**Never use a STAR template.** Situation/Task/Action/Result produces dead checklist prose,
they'll resent filling it in, and it's unnecessary — STAR can be rendered *from* good prose,
but life can't be put back into prose born as a form.

See `templates/story.md` for the skeleton.

## Workflow

1. **Read first.** The résumé, the relevant `background.md`, related stories. Facts you can
   look up are not questions.
2. **Seed the file** from vetted text only. Gaps stay loudly gaps.
3. **Interview in rounds.** Compute the frontier, build the questions from the playbook in
   [REFERENCE.md](REFERENCE.md), ask, wait, write, recompute. Update the file after every
   round rather than at the end — they correct what's on screen, and a written answer often
   reveals the next round's questions.
4. **Resolve gaps explicitly.** `- [x] ~~question~~ Resolved YYYY-MM-DD: answer.` The gaps
   list is the queue for next time; leaving it honest is what makes the corpus resumable.
5. **Prune the queue as you go**, per rule 13. A gap that survives three sessions unasked is
   usually not waiting for the right moment — it's failing the say-it-out-loud test and nobody
   has said so. Delete it; git keeps it. **A deferred topic is different from a dead one:** if
   they defer, log *what* was deferred in enough detail to resume, because "he said he'd made
   mistakes here" with no topic attached is not resumable and will waste a future session.
6. **Stop when they defer.** If they say a topic is for another session, log it and leave it.
   Don't ruin a productive thread by pushing.

## What "done" looks like

A story is done enough when it could survive an interviewer who wants to spend twenty minutes
on it: the setup has stakes, the decisions have alternatives and opposition, the numbers have
sources, someone disagreed, something went wrong, and a real person somewhere in it is more
than an obstacle.

**Note what that list does *not* include:** every fact about the arc. A story is done when it
survives pressure, not when it's complete. Those are different targets and the second one is
unreachable — you can always ask another question, and rule 13 exists because you will.

A session is done when the frontier holds nothing that passes the say-it-out-loud test — or
when they've had enough. What survives the test becomes the gaps list; what doesn't gets
dropped, not parked.

Most stories will not get there in one session. That's fine. Depth accretes — the gaps list
is the contract with the next session, and a short honest queue is worth more than a long
thorough one nobody will work through.
