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

The temperament of a hard design review, pointed at a memory instead of a plan: *what actually
happened? who fought you? what did you almost do instead? what did you get wrong?* Be
relentless — vague answers are where the material is. "It was a mess" is not a story: *what*
was a mess, who made it, what did you do about it. Only ask what is in their head; files, git,
dates and the résumé you look up.

## Asking in rounds

A memory has a shape: an arc branches into beats, each beat into a decision, its opposition,
its cost. Work that shape in **rounds**. The **frontier** is every question whose
prerequisites you already have — the ones you can ask *now* without guessing at an answer you
haven't heard. Ask the frontier in one round, numbered, then wait; a question whose answer
depends on another still open in this round belongs to a *later* round. Each answer reshapes
the tree, pushing the frontier outward. Recompute, ask again.

**Compose each round from the playbook in [REFERENCE.md](REFERENCE.md)** — eleven techniques
ranked by what they actually produce, the top three doing most of the work. Read it every
round: the difference between dislodging a memory and collecting a status update is entirely
in how the questions are built, and none of that is in this file.

**Keep a round to three to five questions, spread across different parts of the tree.** This
is recall, not planning: ten questions about one paragraph make people *summarise* instead of
*remember*. If the frontier is wider than five, ask the sharpest and hold the rest — they'll
still be on the frontier next round. If a round comes back thin or tired, ask one question.

Format each question:

```
❓ **Q1** — **<short title>**: <the question, plus why you're asking if it isn't obvious>

➡️ <optional: a reading you're inviting them to reject — labelled as your guess>
```

**The ➡️ line is a provocation, never a recommended answer.** Suggesting the answer
contaminates the evidence: the product of this skill is what *they* remember, and a fluent
guess of yours is the easiest thing in the world to nod along to — rule 8's present-day
artifact again, arriving in your voice.

- Use it for the worst reading of the facts (playbook 1 `[WORST-READING]` in `REFERENCE.md`) or
  a theory you want refuted (playbook 9 `[WRONG-THEORY]`). Those work *by* being wrong.
- **Never use it for something they'd have to remember** — a date, a number, a headcount, a
  system name, who was in the room, what the pushback was. Leave those bare: a blank is
  recoverable, a plausible suggestion repeated back to you is not.
- Nothing enters the file because you proposed it. Rule 1 applies to your own ➡️ lines first.

**Facts are your job, never theirs.** When a frontier question needs something from the
environment, dispatch a sub-agent, and don't block the round on it — a running lookup is an
unsettled prerequisite, so only the questions downstream of it wait. The *decisions* and the
*memories* are theirs.

## Hard rules

**1. Never invent.** `[NEVER-INVENT]` Every line traces to something they said or wrote. If
you're not sure they said it, it's a gap, not a sentence — they will defend this material in
interviews, and a plausible detail you supplied is a landmine with their name on it.

**2. Seed from vetted text only.** Open a story by writing what the résumé and cover letters
already say, and nothing else. Everything absent becomes an explicit gap, and the gaps are the
interview queue. Never write prose in their voice to fill space.

**3. Pasted drafts are unvetted, including their own.** A draft from a prior chat with another
AI is a *rendering*, not raw material — an essay shape, an arc, a moral. Take the substance
and the opinions, drop the framing, and treat every number as suspect until they confirm it:
rendered prose inflates a one-time "traffic doubled after launch" into "tripled month over
month", a compounding claim they never made and would have to defend in the room.

**4. Numbers get a source or they don't go in.** For every quantitative claim: where did it
come from — a dashboard, a review doc, or a model's guess at what "kept growing" sounds like?
Record the source beside the number, and record the ceiling — "do not inflate." **A limit the
user volunteers unprompted is the strongest ceiling there is**, because it is offered against
their own interest (*"two teams, not the org"*). Record it the moment it is said; the bigger
version always reads better to a later session, which is how ceilings quietly re-inflate.

**5. No names of non-public people. Ever. Roles only.** The corpus describes real people's
worst professional moments, and the user would never say those names in an interview anyway —
"a senior engineer on the platform team" carries the story fine. The repo stays private
permanently, and it should never name a private individual even so.

**6. Don't pre-split a story by decision type.** One arc, one file, even when it holds four
decisions. Splitting a project into "the architecture decision" and "the conflict decision"
bakes the lens into storage, and the lens can't be known until a JD is in hand. **Split only
when evidence forces it:** a different role, a different year, a different central decision —
then cross-link both ways, because the connection between two stories is usually the insight.

**7. Check the vocabulary's age, not just the numbers.** Numbers drift; words also modernise.
Someone with a long career has a newer, better-sounding name for every old thing they did, and
reaching for it is honest, automatic, and falsifiable: they cannot fix it by remembering
harder, and an interviewer checks the label against a public release history. Watch terms
that postdate the work — *microservices* (were they just services?), *SRE*, *observability*,
*data mesh*, *MLOps*, a tool named years before it existed. **If a term postdates the work,
date the term. The fix is never to delete the claim — it's to restate it.** "I used <modern
tool> in 2014" is false and checkable; "I was doing the thing <modern tool> would later
formalise" is true *and stronger*, because they had the idea before the tooling existed to
name it. Record the correction in an `anachronisms_corrected` block so the modern word can't
creep back in.

**8. Beware present-day artifacts.** A current project offered as "context" for an old story
is a **lens, not a source** — it tells you what to ask, never what happened. A vivid,
well-structured artifact beside a thin ten-year-old memory will colonise it, in exactly the
vocabulary you just read, and the shape will feel right to both of you.

**9. `_inbox/` is a queue, not a source. Folder location is a truth claim.** A file in
`corpus/<company>/` asserts *vetted, sourced, provenance-checked*. Raw material — pasted
drafts, old design docs, coaching output from other chats, exported notes — goes in
`corpus/_inbox/` and **is never rendered from and never cited as fact** — otherwise an AI
draft's unsourced metric gets quoted in a résumé and defended in a room. Extract it into
story files per rule 3, then delete it or move it to `_inbox/extracted/`; leave inbox files
**pristine**, because extraction may need redoing. If raw material refers to *"the doc"*
behind it, **that artifact is the better source** — ask for it. The same status applies to
`applications/<company>-<role>/_inbox/`, where the `apply` skill files recruiter mail: a fact
about the user sitting there earns its way in here like everything else, by them saying it.

**10. Surface the change; never resolve it silently.** `[MARK-DONT-FIX]` Recorded material —
a line in a story file, a claim in a rendered artifact, a reading nobody has confirmed yet —
changes only by a decision the user makes and sees: **show what stands, show what would
replace it, name what prompted the change, and let them choose.** Settling it yourself makes a
factual call that was theirs, and a model settles on the vaguer version. Four cases.

**a. Two of their own statements conflict.** Quote both lines back, name the conflict, let them
reconcile it — the reconciliation is usually more interesting than either version, and
resolving it yourself risks inventing or destroying fact (the drama bias of playbook 1
`[WORST-READING]` in `REFERENCE.md`, in a new place). *But a self-correction is not a conflict,
and this case must not fire on one.* When the user revises an earlier answer *and says which
one is right* — *"actually it was four months, not six"* — it is settled; take the new answer.
Quoting both lines back reads as not listening, and **routing it to `facts_disputed`** — which
is for claims nobody has resolved — parks a settled number where neither value renders, so
their better answer becomes unusable. The tell is whether they mark the change themselves.

**b. The reading is yours, not theirs.** Label it in the file as your inference, dated, to be
confirmed or rejected before rendering. Record a rejection *and their reasoning*; the
refutation is often better material than the theory was.

**c. The change invalidates something already rendered** — not two of *their* statements, but
what they just said against what a résumé or a live application **already claims**. Expensive,
because a rendered claim is one a reader has already believed. Say it in the same breath —
*"that contradicts your résumé, which says X"* — and let them decide. **But a correction to the
corpus does not authorise editing the artifact.** One concern per change:

- **Submitted** — frozen evidence of what a reader saw. Supersede it, never rewrite it.
- **In-flight** — re-rendered on request, with the diff shown. This is where the damage
  happens: a session doing corpus work has no business editing a live application.
- **Baseline** — refreshed as its own deliberate act, in its own commit.

So the session owes the **marker, not the fix**: an unchecked gap in the story file naming the
artifact and the line, re-render offered separately. Never leave it as *the corpus now knows* —
a corrected corpus beside an artifact still making the old claim is the worst state available,
because the corpus looks healthy while the document people read is wrong, and nothing re-reads
a rendered artifact. And **once per corpus — not once per session — diff the whole résumé
against the corpus**, asking of each claim what vouches for it *now*.

**d. The change rewrites a line already on disk.** New information usually *adds* rather than
contradicts, so case (a) never fires and the tidy move is to fold the detail into the sentence
already written — which is where substance goes quietly missing. **If the proposed line says
less than the one it replaces, it is not a fix**, and **adding a sentence beside the original
beats merging both into one**: the detail that looked like clutter answers the third follow-up
and is not recoverable from the merged version.

**The trigger is meaning, not keystrokes.** A decision round is owed when the edit could change
fact, specificity, provenance, emphasis, or a recorded rendering decision — *"led the
migration"* narrowed to *"led one workstream"*, or a source dropped from beside a number. A
typo, a rewrap, a repaired clause is not; make those and move on, since they show in the
session's diff anyway and demanding a round for each buries the ones that need it.

**11. Through-lines go in `corpus/through-lines.md`, never in the story that surfaced them.**
Patterns spanning the whole career — recurring instincts, philosophies, repeated moves —
belong to no single story and drift if copied into several. When a story evidences one, add
the instance *there* and leave a pointer *here*. Three rules keep that file honest rather than
flattering:

- **Every instance carries a file citation.** No claim without evidence.
- **Every through-line has a "where it doesn't hold" section.** A pattern with no
  counter-examples is hagiography — the same defect as a story where nobody disagreed.
- **Say whose claim it is** — theirs, or yours.

A stored through-line can quietly become a lens every story gets bent to fit. The defence is
that they are *derived and falsifiable*, and new evidence can demote them. Never let one pick
a story's framing; let the job description do that.

**12. Apply the say-it-out-loud test — before you ask, and before you log a gap.**
`[SAY-ALOUD]` Depth is the point of a corpus; *completeness* is not. This skill drifts toward
archival completeness on its own: every answer exposes three more askable questions, and they
all look reasonable written down.

> **Would they ever say this out loud — in a bullet, a letter, or an interview answer?**

- **Renders** — it goes in the artifact. Ask it.
- **Defends** — they'd need it only if an interviewer challenges a claim **already on their
  résumé**. Ask it when the claim is actually there.
- **Neither** — **don't ask it, and don't write it down.** No gap, no note, nothing.

*Neither* covers more than you'd think: headcounts and org charts, how long something took
when nobody will ask, arithmetic that changes no claim, the unfinished scene you're curious
about because it's a good story. Lookups belong to neither pile — they're yours (see *Facts
are your job*), and must never sit in a queue addressed to the user.

**The failure is structural, so the fix has to be too.** A gap gets logged because a question
*exists*, not because an answer would change anything, and once logged it gets asked — by you
or the next session. So the gap list is not a to-do list of everything askable. **It is a queue
of answers that would change something.** Prune it under this test, not only when it runs long.

**The counterweight, or this rule guts the playbook:** *demand the mistake* passes this test
easily — "tell me about a time you got it wrong" is asked in nearly every interview loop, so a
story with no mistake in it has a hole exactly where a question is coming. Same for the cost,
the opposition, and the person who lost. Those are *renders*: the test kills bookkeeping, not
discomfort.

## Lessons — how this skill personalises to you

This skill ships generic. It gets sharper by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After the user corrects you in a way that generalises** — a preference, a repeated
  mistake, a framing they reject — append one dated line to `corpus/LESSONS.md`: the mistake,
  and the rule to apply next time. One line each. Append-only.
- **Route it before you write it: would this rule still hold if the corpus were about someone
  else?** If yes, it belongs to the method — say so and leave it, rather than filing a general
  rule under one person's name. If no, it is this user's, and `corpus/LESSONS.md` is where it
  goes. Either way it goes in a *file*: a rule kept in a session summary or a model's memory
  is in neither place, and **a rule nobody can diff is a rule nobody can review, port, or
  undo.**
- **Never edit this SKILL.md to record a lesson,** and never write lessons into the kit repo.
  The method stays stable and shareable; the scar tissue stays private and personal. A skill
  that rewrites itself bloats and drifts.

## The file

Context nests, and each layer is written exactly once:

```
corpus/
  profile.md              ← career spine: years, education, contact, skills
  through-lines.md        ← cross-career findings. See rule 11.
  _inbox/                 ← raw, unextracted material. NEVER a source. See rule 9.
  <company>/
    background.md         ← company context every story here assumes
    <story>.md            ← one arc, one central decision
```

Frontmatter holds facts that must not drift, split by provenance
(`facts_vetted` / `facts_disputed` / `facts_unvetted` / `sources`); prose holds the arc, in
their voice, with beats as `##` subheads so they're addressable without being boxes. See
`templates/story.md` for the skeleton. **Never use a STAR template** — it produces dead
checklist prose they'll resent filling in, and STAR can be rendered *from* good prose while
life can't be put back into prose born as a form.

### What "vetted" means

**The corpus vouches for provenance, not for truth.** `facts_vetted` does not mean checked,
audited, or independently confirmed. It means: *the user asserts this themselves, and the file
records where they said it and when.* Nothing in this kit verifies anything against the world,
and it should not pretend otherwise.

That sounds like a weak bar; it is the right one, because of what it buys in the room. The
defence of a claim is *"that's my recollection, from this work, and here's the detail behind
it"*, and what makes that survive a follow-up is knowing whose claim it is and how firmly they
made it — not a verification the interviewer can't see either.

So the three blocks sort by **how well the user can stand behind it**, not by how likely it is
to be true. Two claims out of the same conversation and the same memory can land in different
blocks: the shape of what happened is something a person holds accurately for a decade, and a
precise figure is not.

- **`facts_vetted`** — they assert it directly, about their own work, with the source and date
  recorded. Renderable up to any ceiling the file sets.
- **`facts_disputed`** — two sources disagree about one claim's size or shape and nobody has
  resolved it. Neither value renders. Where both agree on a floor (*"80%" vs "about half"*
  both mean at least halved), that floor may render — **but only once the user has settled it
  in a `RENDERING DECISION`.** A model picking which version of a contested number to say is
  the whole failure this block prevents.
- **`facts_unvetted`** — they said it, but their standing is weak: second-hand (*their
  recollection of what an EM said*), someone else's private state, or a precise figure resting
  on a decade-old memory with no artifact. **A lower ceiling, not silence.** Record why the
  standing is weak *and* what may still be said — "fine as a personal recollection in an
  interview, never a résumé line" is more useful than the claim alone.

When a fact moves between blocks — a dashboard turns up, a date gets pinned — say so and date
it. The movement is evidence about the memory, and `prep` mines these blocks for the probes an
interviewer will push on.

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
5. **Prune the queue as you go**, per rule 12. A gap that survives three sessions unasked is
   usually failing the say-it-out-loud test with nobody saying so; delete it, git keeps it.
   **A deferred topic is different from a dead one:** log *what* was deferred in enough detail
   to resume — "they said they'd made mistakes here" with no topic wastes a future session.
6. **Stop when they defer.** If they say a topic is for another session, log it and leave it;
   don't ruin a productive thread by pushing.

## What "done" looks like

A story is done enough when it could survive an interviewer who wants to spend twenty minutes
on it: the setup has stakes, the decisions have alternatives and opposition, the numbers have
sources, someone disagreed, something went wrong, and a real person somewhere in it is more
than an obstacle. **Note what that list does *not* include:** every fact about the arc. A
story is done when it survives pressure, not when it's complete — the second target is
unreachable, and rule 12 exists because you will keep finding another question.

A session is done when the frontier holds nothing that passes the say-it-out-loud test, or
when they've had enough. What survives the test becomes the gaps list; what doesn't gets
dropped, not parked. Most stories will not get there in one session, and that's fine — depth
accretes, and a short honest queue is worth more than a long thorough one nobody works through.
