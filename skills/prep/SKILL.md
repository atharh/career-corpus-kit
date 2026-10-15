---
name: prep
description: Build an interview prep pack for one scheduled interview — an opener, a story bank mapped to the employer's own hiring criteria, the probes they'll push on with defensible answers, questions to ask them, and one page to read from during the interview itself. Use when an interview or an interview loop is booked, when preparing for a specific round, or after an interview to capture what was asked.
---

# Career corpus — prep

`render` produces artifacts you **send**. This produces a directory you **study**, for one
scheduled interview, and then captures what happened afterwards.

It is the corpus pointed at a room you're about to walk into. Everything it writes is a
rendering, bound by the contract below — `render`'s rules, in render's own words. The contract
is complete for a pack; read [`../render/SKILL.md`](../render/SKILL.md) only when producing
something to **send**.

## Lessons — how this skill personalises to you

This skill ships generic and sharpens by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit. Never edit this
SKILL.md to record a lesson.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with this skill's hard rules.
- **After a correction that generalises, append one dated line**: the mistake, and the rule to
  apply next time. Route it first — a rule that would still hold if the corpus were about
  someone else belongs to the method, not this file. Either way the rule lives in a *file*: a
  rule nobody can diff is a rule nobody can review, port, or undo.
- **A lesson leaves this file only on the user's explicit say-so, entry by entry, by the two
  exits its header states.** A struck entry — `~~<the entry>~~ retired YYYY-MM-DD: <one clause
  of why>` — is never applied again. Delete an absorbed one only once nothing local remains in
  it, trimming it to that residue if any does.

## The rendering contract

- **Every claim about the candidate comes from the vetted corpus, and from nothing else.**
  (`[CLAIM-SOURCE]`) `_inbox/` is not the corpus — see below.
- **Numbers carry their source and their ceiling.** (`[NUMBER-CEILING]`) A figure in
  `facts_disputed` is spoken at neither value.
- **Date the vocabulary, not just the facts.** (`[DATE-VOCABULARY]`) No term that postdates
  the work. Check `anachronisms_corrected` blocks before using any tool or role name.
- **Attribute their role honestly.** (`[HONEST-ATTRIBUTION]`) Match the corpus `role:` /
  `authorship:` exactly. And don't render hindsight as design intent. (`[NOT-HINDSIGHT]`)
- **Prefer the true version.** (`[TRUE-VERSION]`) The accurate version is stronger than the
  inflated one essentially every time — and it is the one the user can defend at depth three.
- **No names of non-public people. No internal codenames.** (`[NO-NAMES-CODENAMES]`) In the
  pack's prose, not only its filenames.
- **Obey recorded rendering decisions.** (`[OBEY-DECISIONS]`) A call the user has already
  settled doesn't reopen because a room might reward the other version.
- **Surface diffs and decisions; never silently apply.** (`[SHOW-THE-DIFF]`) Genuine choices
  are the user's call, not yours.
- **Make it sound like the user, not a model — always, as the last step.** (`[THEIR-VOICE]`)
  Pull their recorded voice from the corpus first; a humanizing pass finishes, it doesn't
  invent.

One render rule is left out on purpose: `[PROVENANCE-NOT-PROSE]` keeps hedges out of artifacts
you send, but a pack is study material and *should* show its seams — `[NAME-THE-WEAK]` below
depends on it.

Two more hold across the whole kit, and both are about what *not* to write down:

- **Not every doubt is a blocker.** (`[NOT-EVERY-DOUBT-IS-A-BLOCKER]`) Most uncertainty is not
  a blocker. The test is whether being wrong would be expensive or hard to undo — if it would
  not, say it once, in a clause, and carry on. Three things still earn a gate: editing a frozen artifact, putting an unsourced claim in
  front of an employer, and anything the user has said is theirs to decide. `[NAME-THE-WEAK]`
  is not in tension with this: naming a weakness once is the clause, and a pack that returns
  to it in four files has stopped preparing the user and started worrying at them.
- **A constraint has one home.** (`[CONSTRAINT-HAS-ONE-HOME]`) A limit on a claim lives in the
  corpus file that owns the claim, and an application thread never repeats it. A pack cites a
  ceiling to prepare an answer, which is fine; what it must not do is restate it as a standing
  rule the folder now owns. **Grep the corpus before writing a constraint into an application
  thread.**

## When this fires, and what it needs

The trigger is *"I have an interview"*, not *"I'm applying"*. That means inputs `render`
doesn't have:

- **The JD**, and the recruiter's email or scheduling note — those often name the format, the
  rounds, the interviewers' roles, and sometimes the assessment criteria outright.
- **The employer's published hiring criteria**, if any. Many companies publish competencies,
  focus areas, or levelling guides. **When they exist, they are the story bank's sections.**
- **The loop structure and the date.** How many rounds, with whom, over what period. The pack
  is a study plan as well as a document, and a plan needs a clock.

**Read `applications/<company>-<role>/` before you ask for any of it.** The `apply` skill
opened that folder and most of this is already sitting in it:

- `jd.md` — the posting, verbatim;
- `_inbox/` — the recruiter's mail and the scheduling note;
- `fit.md` — what the corpus can't back for this role;
- `application.md` — the dates and who's involved.

Use the application the user named or the session has already established; with more than one
live application and neither, list them and ask — never guess, because a pack built against the
wrong loop looks exactly like a correct one. Ask only for what's genuinely missing, and file
anything the user hands you now into `_inbox/` so the next round inherits it. If the folder
doesn't exist, offer `/career-corpus:apply` to open it — a booked interview is exactly when the
thread starts needing a memory.

**But `_inbox/` is unvetted** (`apply`'s `[INBOX-NOT-EVIDENCE]`). Use it to aim the pack, never
as a claim in the user's mouth: the interviewer knows what the team actually does.

If a round is with a named individual, keep that name **out of filenames**. Roles in
filenames, names in the body if the user wants them. Filenames get screenshotted, screen-shared
and tab-completed in front of other people.

## The pack

The pack goes in the application's own directory, `applications/<company>-<role>/`, alongside
the JD and the rendered artifacts — the same folder `apply` opened and `render` wrote into.
Files are numbered so the reading order is the preparation order.

| File | What it holds |
|---|---|
| `interview-prep.md` | The index. The frame — what this employer is actually buying. The loop, the dates, what to do on which day. |
| `01-about-me.md` | The opener. Two to three minutes, spoken, ending on why you're in this conversation. |
| `02-why-<company>.md` | The "why us" answer, built from their own material, not from adjectives. |
| `03-story-bank.md` | Stories mapped to **their** criteria — one section per criterion. |
| `04-probes-and-defences.md` | Where they'll push, and the answer. See below; this is the file that earns the pack. |
| `05-questions-to-ask.md` | What to ask them, and what not to. |
| `06-interview-script.html` | The one page read from **during** the interview: the round in its own order, on a clock, its spoken lines copied from `01`–`05`. See below. |

Skip files that don't apply. A 30-minute screen doesn't need six — say in `interview-prep.md`
which ones you skipped, so a later round doesn't read the gap as an oversight.

Every file in the pack is a rendering, so every one of them opens with the artifact frontmatter
block in [`../render/templates/artifact-frontmatter.md`](../render/templates/artifact-frontmatter.md),
inside an HTML comment in `06`.
A pack is `in-flight` by definition: it belongs to a live application, and it gets re-rendered
rather than edited when the corpus underneath it moves.

## `03` — map to their criteria, never to generic categories

If the employer publishes focus areas, competencies, or a levelling rubric, **the story bank's
sections are theirs, verbatim**, and each section names the corpus stories that serve it. A
criterion that names a technology also pulls the `corpus/capabilities/` file whose `covers:`
names it — a family file answers for terms it isn't named after — and its ceilings bound what
the answer may claim.

The value is in what this exposes. A criterion with three strong corpus stories behind it is
fine and needs no work. **A criterion with nothing behind it is the actual finding**, and it
should be stated plainly at the top of the file rather than papered over with the nearest
adjacent story. The user can then decide to prepare a thinner honest answer, or to go and
extract a story that fits, or to accept it as the weak spot and prepare for the question.

Where no criteria are published, derive sections from the JD's own emphasis — but say that's
what you did, so nobody mistakes your inference for their rubric.

## `04` — the probes file, and where probes come from

**The corpus has already written down where this candidate is weak, in the candidate's own
words** — that is why a corpus-backed pack beats generic prep.

Source probes from, in order of yield:

1. **`facts_disputed` and `facts_unvetted`.** A number the corpus won't vouch for is a number
   an interviewer can push on. The defence is usually to volunteer the smaller sourced figure
   before being asked.
2. **Open gaps.** The interview skill logged them because an answer would change something —
   which is very close to why an interviewer would ask.
3. **⚠️ ceilings.** Every ceiling exists because a claim could be over-read. Assume it will be.
   A capability file's depth ceilings and noes are this list pre-built for technology probes —
   *"how advanced is your X"* gets asked in exactly the form `corpus/capabilities/` answers.
4. **Résumé claims with thin corpus backing.** Anything on the page that no story file
   decompresses is a bullet the candidate cannot currently defend for more than one follow-up.
5. **The shape of the career itself** — employment gaps, level changes, an IC↔manager move, a
   short tenure, a domain they haven't worked in. These are asked in almost every loop and they
   are not in the corpus, because the corpus stores stories and these are facts about the
   résumé's silhouette.
6. **What the JD wants that the corpus can't evidence.** If `apply` ran, `fit.md` has already
   written this list — its "backs thinly" and "can't back" sections are probes with the work
   done. The honest version of the answer is nearly always "no, and here's the closest thing I
   have", which lands far better than a stretched analogy that collapses under one question.

**Write the defence at spoken length, and never invent a strength to cover a gap.** If the true
answer is "I haven't done that", the prep is *how to say that well and what to pivot to*, not a
way around it. An interviewer who catches one stretched claim discounts everything else.

Finish the file with a short **"things not to say"** list — the framings the corpus has already
ruled out, the codenames that stay internal, the numbers that were withdrawn. Under pressure
people reach for the version they've said most often, which is frequently the one the corpus
retired six months ago.

## `06` — the live script

`01`–`05` are read before the interview; `06` is read during it, glancing up between answers, in
light or dark mode, sometimes while sharing a screen. So it is one HTML page built from
[`templates/interview-script.html`](templates/interview-script.html), which carries the whole
stylesheet and the clock; fill its slots and keep its look. It sits beside the story bank and
does not replace it: the ceilings, the follow-ups and the full never-say list stay in `03` and
`04`, because they are needed to prepare and are too long to read live.

The page's form:

- **The round's own order.** One section per part of the interview, each with its start time and
  length, linked from a sticky bar that holds a live clock in the interview's time zone. Near the
  top, one line says what to cut when time runs short.
- **The thread at a glance.** One paragraph with the main message, and a strip of the numbers the
  answers lean on, each at the pack's ceiling.
- **Typed lines.** SAY is the exact words, in bold. DO is an action or a cue. PAUSE is stop and
  wait for an answer. A never-say line from `04` sits as a short warning under the answer it
  guards. Only SAY lines are spoken.
- **What each person needs.** The opening asks every interviewer what would make the hour useful
  and notes one word per person; later answers and the close refer back to it.
- **Questions collapsed under their wording**, grouped by the employer's focus areas (the
  recruiter's stated criteria, when given) or by who will ask. Each answer runs in one order: their
  words back, the main message, one story and its one number, an offer of depth. An unknown gets
  one fixed line, *"I don't have that number. I'll have it by <day>."*
- **Recovery lines**: how to take a correction (*"That changes the arithmetic, not the
  approach."*), how to stop rambling, how to find the thread again.
- **An earlier round's probe gets an answer here.** Whatever the last round pressed on is the
  likeliest question in this one. A method question gets the method in one line, one story per
  step, and a one-line close.

A behavioural or hiring-manager round has three parts: the open, their questions by focus area,
and the candidate's questions. A build-and-demo panel follows its own agenda and adds a closing
part that steps out of role: the decisions made and why, what you'd change, and how you'd lead
the team that builds it. A round with no published shape gets the behavioural three.

## Rules specific to prep

**Bullets and a first line, never a script.** `[NO-SCRIPT]` A written-out answer gets memorised
and then *sounds* memorised, and it collapses the moment the question arrives in a slightly
different shape. So the study files give each answer its opening sentence and its beats, and
write out in full only a line worth saying as-is. `06` holds those lines and nothing longer; the
beats between them are DO cues.

**The live page copies its spoken lines; it never writes them.** `[SAY-FROM-PACK]` Every SAY line
in `06` appears word for word in `01`–`05`, or is one of the template's fixed lines, and the
page's opening comment says the two must stay in step. A fact changes in the pack first, then in
the page. Restated in new words, it becomes a second version of the fact that the next re-render
of the pack will not update, and the page is the one that gets read in the room.

**Spend the stories deliberately.** `[SPEND-STORIES]` Track which story serves which criterion
and which question type. One anecdote reused across three answers in a single loop is a tell —
it reads as a candidate with one good year. Where a story must serve twice, note which *lens*
each use takes, and make sure they're genuinely different.

**A line that fits several moments is said at the first one.** `[SAY-IT-ONCE]` A gap line, or any
line two questions could call for, sits in `06` where it is likeliest to come up first, and a
DO cue at the later moments says it has been said. Naming a gap once is honest; naming it twice
in one hour is the candidate worrying at it out loud.

**Carry the mistake into the room.** `[CARRY-MISTAKE]` The corpus keeps the failure in each
story precisely so the pack can use it. Prep the mistake as an answer, not as damage control.

**Prep the follow-up, not just the answer.** `[DEPTH-THREE]` For each story, the second and
third questions are usually already written down as that story's gaps. Answer down to depth
three.

**The homework is part of the pack.** `[HOMEWORK-IN-PACK]` If there's a take-home, a
presentation, or a "prepare a case" instruction, it goes in `interview-prep.md` with the dates,
not in a separate mental note. It is the single most skippable and least skippable part of a
loop.

**Say what you don't have.** `[NAME-THE-WEAK]` A pack that reads as though the candidate is
strong on everything is a pack that hasn't been read against the criteria properly. Name the
weak sections at the top of `interview-prep.md`.

## After the interview — this is half the skill

Run this again the same day, while it's fresh. Three outputs:

- **Update the pack** with what was actually asked, which answers landed, and which didn't.
  A later round with the same company inherits it, and its `06` gets an answer for whatever this
  round pressed on.
- **Add a dated line to `application.md`** — round, date, how it went, what happens next. The
  log is what makes a thread readable six weeks later.
- **Feed the misses back into the corpus.** Anything the user fumbled, couldn't source, or
  got asked and hadn't considered becomes a queue for `/career-corpus:interview` — and it is
  the highest-quality queue the corpus will ever get, because it comes from a real interviewer
  rather than a model guessing what one might ask.

**Do this even when the outcome was bad, and especially then.** A question that landed badly is
a precisely targeted gap someone else handed you for free.

## What "good" looks like

The user can hold the whole pack in their head before walking in: one frame, one opener, a
story per criterion, an answer to each thing they're afraid of being asked, and three questions
worth asking. Nothing in it is a claim they can't defend at depth three, and the parts they're
weak on are named rather than hidden.

A pack that makes the user feel prepared but says something they'd have to walk back in the
room has failed, however good it reads.
