---
name: career-corpus-interview
description: Interview the user to turn a career memory into a vetted story file in their career corpus. Use when they want to add to the corpus, decompress a résumé bullet, capture a story that just surfaced, prepare for an interview, or when a job description needs evidence the corpus doesn't have yet.
---

# Career corpus — interview

The corpus lives in a `corpus/` directory (keep it in a **private** git repo). It holds the
user's career at full depth. Résumés, cover letters, and interview answers are **renderings**
of it. This skill is how material gets in. The companion skill `career-corpus-render` is how
it comes out.

**Recall is triggered, not enumerated.** People do not remember their careers by listing
them — they remember when something snags. Whole years of relevant work stay invisible until
writing about something adjacent dislodges them. So this is an interview, not a form. Never
hand the user a template to fill in.

## Stance

The temperament of a hard design review, pointed at a memory instead of a plan.

- **A design review attacks a plan:** *why is this the right call? what didn't you consider?*
- **This attacks a memory:** *what actually happened? who fought you? what did you almost do
  instead? what did you get wrong?*

Ask **one question at a time** and wait. Two questions is bewildering and they'll answer the
easier one.

Look facts up — files, git, dates, the résumé. Only ask what's in their head.

Be relentless. Vague answers are where the material is. "It was a mess" is not a story;
*what* was a mess, who made it, what did you do about it.

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

**11. Surface contradictions; never silently resolve them.** When two of the user's
statements seem to conflict, that's a question for them, not a problem for you to fix. If you
pick the version that seems defensible and quietly edit, two things go wrong: you make a
factual call that was theirs to make, and you often delete true substance because the "safer"
version is vaguer. Quote both lines back, name why they seem to conflict, and let them
reconcile it. The reconciliation is usually more interesting than either version. (This is
the drama-bias failure — see the playbook — in a new place: resolving a tension yourself
instead of letting them do it always risks inventing or destroying fact.)

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

**Never use a STAR template.** Situation/Task/Action/Result produces dead checklist prose,
they'll resent filling it in, and it's unnecessary — STAR can be rendered *from* good prose,
but life can't be put back into prose born as a form.

See `templates/story.md` for the skeleton.

## The question playbook

Ranked by what actually produces material. The top three do most of the work.

**1. State the worst reading and make them rebut it.** The highest-yield technique by far.
*"That's the third incumbent decision you overruled — that's either exceptional judgment or
steamrolling."* People answer a charge with evidence they'd never volunteer to a neutral
question — the pushback, the constraint they were under, the thing they tried first.

> **⚠️ This technique's failure mode.** You will reach for **drama**, and most careers are
> more collaborative and more boring than the charge implies. The interesting rebuttal — a
> controlled comparison, a constraint, a definition — is theirs to supply, and it's usually
> the best material in the story.
>
> **It works only because they push back.** Someone who wanted a better story would simply
> accept the frame — and then an invented conflict is sitting in a file with their name on
> it, ready to be told in an interview. So: make the charge, then **believe the rebuttal over
> your own theory.** Record the refutation in the file as *your* error, dated, so it can't
> drift back later. Never grade a story on how good it sounds.
>
> **And when they correct you, don't overshoot the other way.** "You invented this" → they
> hedge "it evolved" → don't swing to "so it wasn't even yours." The truth is usually an
> unglamorous middle. A correction is a data point, not a new thesis. Apply it locally; don't
> re-plot the arc around it.

**2. Cross-check the arithmetic.** Dates, durations, and role changes contradict each other
constantly. "You shipped it in three months, but you also did the migration in your final
months a year later — which was it?" often splits one muddled story into two clean ones.

**3. Interrogate the compressed phrase.** Find the phrase carrying the most weight and demand
it decompress. "A two-year cross-functional deadlock involving three organizations" is
fourteen words holding up an entire story.

**4. Demand the mistake.** No story where everyone who disagreed turns out wrong is credible.
If there are no missteps, it's a case study, and interviewers can smell it.

**5. Ask who was told.** Technical stories go human-shaped under this. Who lost, who was
overruled, who had to be told their work was being binned, did they stay?

**6. Chase the generic word.** When the résumé says the abstract thing — "improving
discoverability org-wide" — ask what it *actually* did. The specific answer is almost always
more concrete and more interesting than the abstraction hiding it.

**7. Close the causal loop.** They'll report a decision and an outcome in the same breath
without connecting them. "Did the decision *cause* the outcome?" often surfaces the strongest
line in the story.

**8. Name a pattern across stories.** When the same idea appears twice, ask if it's a
philosophy. A single diagnosis applied in two places is often the seed of a through-line.

**9. Offer a wrong theory, invite rejection.** A concrete reading they can push against beats
an open question. The refutation — a comparison or distinction you didn't have — is frequently
better than the theory would have been.

## Workflow

1. **Read first.** The résumé, the relevant `background.md`, related stories. Facts you can
   look up are not questions.
2. **Seed the file** from vetted text only. Gaps stay loudly gaps.
3. **Interview.** One question, wait, write, repeat. Update the file as you go rather than at
   the end — they correct what's on screen.
4. **Resolve gaps explicitly.** `- [x] ~~question~~ Resolved YYYY-MM-DD: answer.` The gaps
   list is the queue for next time; leaving it honest is what makes the corpus resumable.
5. **Stop when they defer.** If they say a topic is for another session, log it as a gap and
   leave it. Don't ruin a productive thread by pushing.

## What "done" looks like

A story is done enough when it could survive an interviewer who wants to spend twenty minutes
on it: the setup has stakes, the decisions have alternatives and opposition, the numbers have
sources, someone disagreed, something went wrong, and a real person somewhere in it is more
than an obstacle.

Most stories will not get there in one session. That's fine. Depth accretes — the gaps list
is the contract with the next session.
