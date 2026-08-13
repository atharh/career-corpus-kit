---
name: interview
description: Interview the user to turn a career memory into a vetted story file in their career corpus. Use when they want to add to the corpus, decompress a résumé bullet, capture a story that just surfaced, or when a job description or an upcoming interview needs evidence the corpus doesn't have yet. To build the prep pack for a booked interview, use the career-corpus prep skill.
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

**Compose each round from the playbook in [REFERENCE.md](REFERENCE.md)** — techniques
in rank order, the first three doing most of the work. Read it every
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
guess of yours is the easiest thing in the world to nod along to — the present-day artifact of
the lens-not-source rule `[LENS-NOT-SOURCE]` again, arriving in your voice.

- Use it for the worst reading of the facts (`[WORST-READING]` in `REFERENCE.md`) or a theory
  you want refuted (`[WRONG-THEORY]`). Those work *by* being wrong.
- **Never use it for something they'd have to remember** — a date, a number, a headcount, a
  system name, who was in the room, what the pushback was. Leave those bare: a blank is
  recoverable, a plausible suggestion repeated back to you is not.
- Nothing enters the file because you proposed it. The never-invent rule `[NEVER-INVENT]`
  applies to your own ➡️ lines first.

**Facts are your job, never theirs.** When a frontier question needs something from the
environment, dispatch a sub-agent, and don't block the round on it — a running lookup is an
unsettled prerequisite, so only the questions downstream of it wait. The *decisions* and the
*memories* are theirs.

## Hard rules

**Never invent.** `[NEVER-INVENT]` Every line traces to something they said or wrote. If
you're not sure they said it, it's a gap, not a sentence — they will defend this material in
interviews, and a plausible detail you supplied is a landmine with their name on it.

**Seed from vetted text only.** `[SEED-VETTED]` Open a story by writing what the résumé and
cover letters already say, and nothing else. Everything absent becomes an explicit gap, and the
gaps are the interview queue. Never write prose in their voice to fill space.

**Pasted drafts are unvetted, including their own.** `[DRAFTS-UNVETTED]` A draft from a prior
chat with another AI is a *rendering*, not raw material — an essay shape, an arc, a moral. Take
the substance and the opinions, drop the framing, and treat every number as suspect until they
confirm it: rendered prose inflates a one-time "traffic doubled after launch" into "tripled
month over month", a compounding claim they never made and would have to defend in the room.

**Numbers get a source or they don't go in.** `[NUMBER-SOURCE]` For every quantitative claim:
where did it come from — a dashboard, a review doc, or a model's guess at what "kept growing"
sounds like? Record the source beside the number, and record the ceiling — "do not inflate." **A
limit the user volunteers unprompted is the strongest ceiling there is**, because it is offered
against their own interest (*"two teams, not the org"*). Record it the moment it is said; the
bigger version always reads better to a later session, which is how ceilings quietly re-inflate.

**Scope a volunteered absolute in the session it's given — record the ceiling, then ask what it
excludes.** `[SCOPE-THE-ABSOLUTE]` People state limits absolutely and mean them narrowly:
*"I never touched the front end"* can mean only *"I didn't write the UI code"*, with the
reviews, the design calls and the incidents handled sitting unrecorded behind it — the
absolute closes the topic, so nothing ever asks. Record the limit unsoftened, per
`[NUMBER-SOURCE]`; then one cheap question at the moment it lands: **what does that rule out,
exactly?** Recovering the same material later costs a blocked story and a full round. The tell
is a limit carrying *at all*, *never*, or *nothing*. Distinct from resisting inflation: that
protects claims from growing; this stops a true ceiling from suppressing true material.

**No names of non-public people. Ever. Roles only.** `[ROLES-ONLY]` The corpus describes real
people's worst professional moments, and the user would never say those names in an interview
anyway — "a senior engineer on the platform team" carries the story fine. The repo stays private
permanently, and it should never name a private individual even so.

**Don't pre-split a story by decision type.** `[ONE-ARC]` One arc, one file, even when it holds
four decisions. Splitting a project into "the architecture decision" and "the conflict decision"
bakes the lens into storage, and the lens can't be known until a JD is in hand. **Split only
when evidence forces it:** a different role, a different year, a different central decision —
then cross-link both ways, because the connection between two stories is usually the insight.

**Check the vocabulary's age, not just the numbers.** `[DATE-THE-TERM]` Numbers drift; words
also modernise. Someone with a long career has a newer, better-sounding name for every old thing
they did, and reaching for it is honest, automatic, and falsifiable: they cannot fix it by
remembering harder, and an interviewer checks the label against a public release history. Watch
terms that postdate the work — *microservices* (were they just services?), *SRE*,
*observability*, *data mesh*, *MLOps*, a tool named years before it existed. **If a term
postdates the work, date the term. The fix is never to delete the claim — it's to restate it.**
"I used <modern tool> in 2014" is false and checkable; "I was doing the thing <modern tool>
would later formalise" is true *and stronger*, because they had the idea before the tooling
existed to name it. Record the correction in an `anachronisms_corrected` block so the modern
word can't creep back in.

**Fact-check technical claims against the public record, and repair the wording rather than
dropping the claim.** `[CHECK-THE-CLAIM]` When a story leans on how a tool or system worked,
the user is recalling a years-old stack from memory: most of it will hold, and the part that
doesn't is checkable in one question by anyone in the room. Look the mechanism up in public
documentation, keep what holds, restate what doesn't, and record in the story file which is
which. The true version is usually *more* specific and sounds more like someone who ran the
thing. Sibling to `[DATE-THE-TERM]`: that rule dates the word; this one verifies the claim
behind it.

**Beware present-day artifacts.** `[LENS-NOT-SOURCE]` A current project offered as "context" for
an old story is a **lens, not a source** — it tells you what to ask, never what happened. A
vivid, well-structured artifact beside a thin ten-year-old memory will colonise it, in exactly
the vocabulary you just read, and the shape will feel right to both of you.

**`_inbox/` is a queue, not a source. Folder location is a truth claim.** `[INBOX-QUEUE]` A file
in `corpus/<company>/` asserts *vetted, sourced, provenance-checked*. Raw material — pasted
drafts, old design docs, coaching output from other chats, exported notes — goes in
`corpus/_inbox/` and **is never rendered from and never cited as fact** — otherwise an AI
draft's unsourced metric gets quoted in a résumé and defended in a room. Extract it into story
files per the pasted-drafts rule `[DRAFTS-UNVETTED]`, then delete it or move it to
`_inbox/extracted/`; leave inbox files
**pristine**, because extraction may need redoing. Pristine is not durable, though: `_inbox/` is
git-ignored, so an inbox file has no history behind it and survives only as the working copy —
extract as though this is the one pass that gets to read it. If raw material refers to *"the
doc"* behind it, **that artifact is the better source** — ask for it. The same status applies to
`applications/<company>-<role>/_inbox/`, where the `apply` skill files recruiter mail: a fact
about the user sitting there earns its way in here like everything else, by them saying it.

**Surface the change; never resolve it silently.** `[MARK-DONT-FIX]` Recorded material —
a line in a story file, a claim in a rendered artifact, a reading nobody has confirmed yet —
changes only by a decision the user makes and sees: **show what stands, show what would
replace it, name what prompted the change, and let them choose.** Settling it yourself makes a
factual call that was theirs, and a model settles on the vaguer version. The move, by case:

- **Two of their own statements conflict** → quote both lines, name the conflict, let them
  reconcile it — the reconciliation is usually more interesting than either version. A
  self-correction is not a conflict: when they revise an earlier answer *and say which one is
  right* — *"actually it was four months, not six"* — they have marked the change themselves
  and it is settled. Take the new answer; quoting it back reads as not listening, and routing
  it to `facts_disputed` parks a settled number where neither value renders.
- **The reading is yours, not theirs** → label it in the file as your inference, dated, to be
  confirmed or rejected before rendering. Record a rejection *and their reasoning*; the
  refutation is often better material than the theory was.
- **The change invalidates something already rendered** → say it in the same breath — *"that
  contradicts your résumé, which says X"* — and let them decide. The session owes the
  **marker, not the fix**: an unchecked gap in the story file naming the artifact and the
  line, re-render offered separately — never *the corpus now knows*, because nothing re-reads
  a rendered artifact. The artifact's lifecycle bounds what may happen next: a **submitted**
  artifact is frozen evidence of what a reader saw — supersede it, never rewrite it; an
  **in-flight** one is re-rendered on request, with the diff shown; a **baseline** is
  refreshed as its own deliberate act, in its own commit. And **once per corpus — not once per
  session — diff the whole résumé against the corpus**, asking of each claim what vouches for
  it *now*.
- **The change rewrites a line already on disk** → new information usually *adds* rather than
  contradicts, and folding the detail into the sentence already written is where substance
  goes quietly missing. **If the proposed line says less than the one it replaces, it is not
  a fix**; adding a sentence beside the original beats merging both into one — the detail
  that looked like clutter answers the third follow-up and is not recoverable from the merged
  version.

**The trigger is meaning, not keystrokes.** `[MEANING-NOT-KEYSTROKES]` A decision round is owed
when the edit could change fact, specificity, provenance, emphasis, or a recorded rendering
decision — *"led the migration"* narrowed to *"led one workstream"*, or a source dropped from
beside a number. A typo, a rewrap, a repaired clause is not; make those and move on, since they
show in the session's diff anyway and demanding a round for each buries the ones that need it.

**Through-lines go in `corpus/through-lines.md`, never in the story that surfaced them.**
`[THROUGH-LINES-FILE]` Patterns spanning the whole career — recurring instincts, philosophies,
repeated moves — belong to no single story and drift if copied into several. When a story
evidences one, add the instance *there* and leave a pointer *here*. Three rules keep that file
honest rather than flattering:

- **Every instance carries a file citation.** No claim without evidence.
- **Every through-line has a "where it doesn't hold" section.** A pattern with no
  counter-examples is hagiography — the same defect as a story where nobody disagreed.
- **Say whose claim it is** — theirs, or yours.

A stored through-line can quietly become a lens every story gets bent to fit. The defence is
that they are *derived and falsifiable*, and new evidence can demote them. Never let one pick
a story's framing; let the job description do that.

**Apply the say-it-out-loud test — before you ask, and before you log a gap.**
`[SAY-ALOUD]` Depth is the point of a corpus; *completeness* is not. This skill drifts toward
archival completeness on its own: every answer exposes three more askable questions, and they
all look reasonable written down.

> **Would they ever say this out loud — in a bullet, a letter, or an interview answer?**

- **Renders** — it goes in the artifact. Ask it.
- **Defends** — they'd need it only if an interviewer challenges a claim **already on their
  résumé**. Ask it when the claim is actually there.
- **Neither** — **don't ask it, and don't write it down.** No gap, no note, nothing. This
  pile is bigger than it looks: headcounts and org charts, how long something took when nobody
  will ask, arithmetic that changes no claim, the unfinished scene you're curious about because
  it's a good story. Lookups belong to neither pile — they're yours (see *Facts are your
  job*), and must never sit in a queue addressed to the user.

The same test governs the gap list: a gap gets logged because a question *exists*, not because
an answer would change anything, and once logged it gets asked — by you or the next session. So
the list is **a queue of answers that would change something**, not a catalogue of everything
askable; prune it under this test, not only when it runs long. And the test kills bookkeeping,
not discomfort — *demand the mistake* passes it easily, because "tell me about a time you got
it wrong" is asked in nearly every interview loop, and so are the cost, the opposition, and the
person who lost. A story with no mistake in it has a hole exactly where a question is coming.

## Rules specific to capability files

Some evidence has no arc. *"What's your experience with <technology>?"* — asked out loud in a
loop, or as a self-rating box on an application form — spans companies and decades, and neither
existing kind can hold the answer: a story file wants one arc with one central decision
`[ONE-ARC]`, and a through-line holds patterns of behaviour, not tool claims. A bare inventory
is worse than either: "used X at three companies" is a record of X existing near the user, not
of anything they did.

**When the question is "what's your experience with X", open a capability file.**
`[CAPABILITY-FILE]` One file per technology, `corpus/capabilities/<technology>.md`, opening
with the question it answers. One technology per file even when the career genuinely spans two
rivals — a merged file flattens two different depths into one claim; write two files and
cross-reference. The unit inside is what the user *did with* the technology, not where it was
present. See `templates/capability.md` for the skeleton.

**A capability file owns no facts.** `[OWNS-NO-FACTS]` It is a derived index: every fact in it
cites the story file that owns it, never restated as this file's own. A fact that surfaces here
with no home yet is held, marked homeless, and **pushed down into the owning company or project
file as soon as placement settles** — a technology claim that never acquires a place it
happened is a claim with no anchor, and an anchorless claim is what a follow-up question
punctures first.

**Every entry carries a depth ceiling, and the file carries the noes.** `[DEPTH-CEILING]`
Record how far each claim can be pushed before it breaks — *administered it* and *my team ran
on it* are different claims, and a file that flattens them reads as uniform confidence, which
is worse than nothing. Keep a noes section — what the user has *not* done with the
technology — the analogue of a through-line's "where it doesn't hold", and the thing that
makes the rest credible in a room.

**The self-named list is a queue of things to disprove, not the file's backbone.**
`[LIST-IS-A-QUEUE]` A technology survives "have you used it" and survives "where", then dies
at "what ran on it" — self-report reliably swaps in a neighbouring tool or moves a claim to
the wrong employer, and the list looks strongest exactly while it is least tested. Build the
file on what the user did; treat each listed technology as a candidate claim and ask what
actually ran on it before writing it down. This is the ask-what-it-did move from
`[WHO-OWNED-IT]`, pointed at tools.

**A cross-company file finds conflicts a story file can't — hold them, never launder them.**
`[CROSS-FILE-CEILINGS]` "Where did you use X" has no respect for file boundaries, so a
capability file will surface contradictions between one company's recorded ceiling and an
answer given about another — that is an argument for the shape, and also its hazard: a file
assembling claims from five companies can quietly launder one company's ceiling away. When an
answer collides with a recorded ceiling, **block the material and hold the push-down until the
owner of that ceiling settles it**, per `[MARK-DONT-FIX]` — the reconciliation usually
produces material nobody would have gone looking for.

## Lessons — how this skill personalises to you

This skill ships generic and sharpens by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit. Never edit this
SKILL.md to record a lesson: the method stays stable and shareable; the scar tissue stays
private and personal.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After a correction that generalises, append one dated line**: the mistake, and the rule to
  apply next time. Route it first — a rule that would still hold if the corpus were about
  someone else belongs to the method, not this file. Either way the rule lives in a *file*: a
  rule nobody can diff is a rule nobody can review, port, or undo.
- **A lesson leaves this file two ways, each on the user's explicit say-so, entry by entry.**
  One that proves *wrong* is retired in the session where it misfired, struck in place —
  `~~<the entry>~~ retired YYYY-MM-DD: <one clause of why>` — and never applied again; the
  strike records wrongness, which lives nowhere else. One the method has since *absorbed* is
  deleted outright, no strike left behind — a shipped rule's duplicate here can only drift —
  once nothing local remains (no calibration about this user, no number they set, no recorded
  divergence; trim the entry to that residue if any does) and no session still loads a skill
  version without the rule.

## The file

Context nests, and each layer is written exactly once:

```
corpus/
  profile.md              ← career spine: years, education, contact, skills
  through-lines.md        ← cross-career findings. See `[THROUGH-LINES-FILE]`.
  capabilities/
    <technology>.md       ← one technology, whole career. See `[CAPABILITY-FILE]`.
  personal-projects/
    <project>.md          ← a story file whose arc belongs to no employer
  _inbox/                 ← raw, unextracted material. NEVER a source. See `[INBOX-QUEUE]`.
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

**A personal project is a story file that belongs to no employer.** Same skeleton, same rules,
filed under `corpus/personal-projects/` because there is no company folder to claim it. Its
`authorship:` frontmatter matters doubly there, because no employer context bounds the claim:
whether the user wrote the thing by hand, directed an agent that produced it, or was one
author of several is exactly what `[WHO-OWNED-IT]`'s provenance tell establishes — and
authorship is not proficiency in the stack; lifting one claim never lifts the other.

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
5. **Prune the queue as you go**, per the say-it-out-loud test `[SAY-ALOUD]`. A gap that
   survives three sessions unasked is
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
unreachable, and the say-it-out-loud test `[SAY-ALOUD]` exists because you will keep finding
another question.

A session is done when the frontier holds nothing that passes the say-it-out-loud test, or
when they've had enough. What survives the test becomes the gaps list; what doesn't gets
dropped, not parked. Most stories will not get there in one session, and that's fine — depth
accretes, and a short honest queue is worth more than a long thorough one nobody works through.
