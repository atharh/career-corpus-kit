---
name: apply
description: Open and run one job application end to end — capture the posting, check the corpus against it before writing anything, then hold everything that arrives afterwards in one folder. Use when the user has found a role they want to apply for, pastes a job posting or its URL, wants to track or update an application already in flight, or asks what applications are live. Hands off to the career-corpus render skill for the résumé and cover letter, and to prep once an interview is booked.
---

# Career corpus — apply

An application is not a document. It is a **months-long thread** that starts with a posting
and ends with an offer or a no, and along the way it accumulates a JD, two rendered artifacts,
recruiter email, a scheduling note, a take-home brief, an interview pack, and an outcome. This
skill opens that thread, gives it one folder, and keeps the folder honest.

It owns the folder. `render` and `prep` write *into* it.

```
applications/<company>-<role>/
  jd.md            ← the posting, verbatim, with its URL and the date you captured it
  application.md   ← events as frontmatter, the dated log beneath it, contacts by role
  fit.md           ← what this role wants, and what the corpus can and can't back
  _inbox/          ← raw inbound — recruiter mail, take-home brief, notes. UNVETTED.
  resume.md        ┐
  cover-letter.md  ┘ written by /career-corpus:render
  interview-prep.md, 01-…–05-… ← written by /career-corpus:prep, numbered, some skipped
```

One folder per **application**, not per company. Two roles at the same company are two
threads with two JDs, two letters and two loops; the only thing they share is background
reading, and that already lives in the corpus.

Minimal templates for the three files this skill owns are in [`templates/`](templates/). They
are the shape, not a form: a field with nothing true to put in it stays empty rather than
getting a guess. Rendered artifacts carry their own frontmatter block, which belongs to the
skill that writes them — see [`../render/templates/artifact-frontmatter.md`](../render/templates/artifact-frontmatter.md).

## Where this sits

The kit has two lanes. `bootstrap` → `interview` → `compact` builds the corpus. `apply` →
`render` → `prep` spends it, and hands back to `interview` at the end. This skill is the entry
point to the second lane.

The trigger is *"I found a job"* — not *"write me a résumé"*, which is `render` on its own.

## Stages

Re-entrant by design. Run it again on an existing folder and it reads the current state, files
whatever is new, and tells you where the thread stands. Don't recreate what's there.

**1. Open.** Get the posting. If it's a URL, fetch it; if it's pasted text, take it as given;
if it's a screenshot, transcribe it. Derive company and role from the posting, not from the
user's shorthand — `<company>-<role>` in kebab case, short enough to tab-complete. Write
`jd.md` and start `application.md`.

**2. Fit.** Read the corpus against the JD **before anything gets written**. This is the step
that earns the skill; see below.

**3. Render.** Hand off: *"Run `/career-corpus:render` for this application."* Don't write the
résumé or the letter here — `render` carries the faithful-rendering rules and this skill
doesn't repeat them.

**4. Sent.** Log the date and what actually went out, including anything the form asked for
that the folder doesn't hold (a portfolio link, a salary expectation, a "why us" box typed
into a text field). Applications get answered weeks later and nobody remembers what they
claimed in the box. Record the files themselves in `application.md`'s `sent:` block, which is
a separate question from the prose and is asked, never guessed — `[SENT-NAMES-WHAT-WENT]`.

**5. Inbound.** Everything that arrives goes in `_inbox/` with a date, and the log gets a line.
Recruiter mail, rejections, scheduling, the take-home brief, the "we've moved you to the next
round" note.

**6. Prep.** When a round is booked: *"Run `/career-corpus:prep` — the JD and the recruiter's
note are already in the folder."* `prep` reads them from here rather than asking again.

**7. Close.** Record the outcome and the date. Then the part people skip: **a rejection with a
reason in it is corpus material.** So is anything the loop exposed. Route it to
`/career-corpus:interview` and say so explicitly — this is the highest-signal queue the corpus
ever gets, and it evaporates within a week.

**Asked "what's live?"** — read the `events:` block of each `applications/*/application.md`,
report stage, age and next action per thread, and name the ones that have gone quiet. Compute
it; never store it. A thread with a log and no `events:` is unmigrated, and says so — it is
never reported as a thread with no events.

## The fit check — `fit.md`

Read the JD's real requirements (not its boilerplate) against the corpus, and give each one an
**evidence state**, which is exactly one of three:

- **`backed`** — a story file is evidence for it. Name the file. A requirement with a named
  file behind it needs no further work.
- **`thin`** — there's something adjacent, but it would fold under a second question.
- **`no-corpus-evidence`** — nothing in the corpus speaks to it.

**Call the third one `no-corpus-evidence` and never `missing`**, because those are different
claims and only one of them is yours to make. A requirement the corpus can't back may be one
the user never did, or one they did and never recorded — *absent* versus *unwritten* — and the
two need opposite responses: don't apply, versus book an interview session. This file records
what it can see and asks; picking between them is a call about someone's career, which the
surface-don't-decide rule `[SURFACE-DONT-DECIDE]` says is theirs. Say which you suspect and
why, as a question.

**The third state is the point, and "don't apply yet" is a valid result.** A requirement with
nothing behind it doesn't get solved by rendering harder at it; it gets solved by an
`interview` session, or by deciding to apply anyway with the gap named and a plan for the
question. Both are fine. Papering over it with the nearest adjacent story is not — that story
gets one follow-up question in the room and collapses, and everything either side of it gets
discounted with it.

Say which requirements you judged to be real and which you discarded as boilerplate, so the
user can disagree. Every posting asks for ten years of a five-year-old technology.

**A judgement in here is only as good as what you computed it from.** When a line of `fit.md`
rests on a rendered artifact rather than on something the user said — a résumé bullet, an older
cover letter — it inherits that artifact's errors, and a gap that is really a stale bullet reads
exactly like a gap in the corpus. Confirm the input before the conclusion hardens into a
section, because once it is written down the next reader treats it as a finding. Say which
inputs a judgement rests on where it isn't obvious.

Where the corpus is thin, the useful output is a **pointer, not a verdict**: *"nothing backs
'led a platform migration' — the closest is `corpus/<company>/<story>.md`, and an interview
session on <arc> would probably produce it."*

## The event vocabulary

A thread is a dated list of events, named from a fixed set so it can be read at a glance six
weeks later. Every event is written in two places at once: a line in `events:` for anything
that reads state, and a line in the log for the reader who wants to know why — `[STATE-IS-DATA]`.
Nine events:

| Event | What it marks |
|---|---|
| `opened` | The posting was captured and the folder created. |
| `fit-checked` | `fit.md` was written or revised, and what the user decided off the back of it. |
| `rendered` | An artifact was produced or re-rendered. |
| `sent` | The application went out. Record what actually went out, including the form-only fields this folder doesn't hold. |
| `inbound` | Something arrived and was filed in `_inbox/`. Name the file. |
| `scheduled` | A round was booked. |
| `interviewed` | A round happened. |
| `outcome` | Offer, rejection, or the user withdrawing. Say which, and quote any reason given. |
| `routed` | Something this thread exposed went back to the corpus queue. |

Something that fits none of them is usually two events. A fixed vocabulary is also what lets a
reader — or a check — see at a glance that a thread was never `sent`, or was `interviewed`
without ever being `routed`.

## Migrating a thread that has no `events:` block

A thread opened before the frontmatter existed still has all its events, in prose. Offer to
migrate it when you next touch the folder, and run the migration like this:

- **Assisted, never automatic.** Propose the block, report what you could not resolve, and let
  the user confirm before writing — report-then-patch, the shape `verify` already uses.
- **The mechanical half only.** Lift the events into `events:` and fold the existing body into
  the collapsed block **verbatim**. Don't rewrite paragraphs into one-liners and don't decide
  what still binds: auto-summarising provenance is a silent lossy edit, and compression is a
  judgement the user makes thread by thread, possibly never for a closed one.
- **Ask for `sent.artifacts`.** Which files an employer received is not on disk anywhere, which
  is the whole reason the block exists. A plausible guess here is indistinguishable from a fact.
- **A log older than the vocabulary is expected to defeat you.** Say which lines you could not
  parse and leave them alone. A confident wrong answer here is worse than an unmigrated thread,
  because the unmigrated one reports itself as unmigrated and this one reports itself as done.
- **Touch `application.md` and nothing else**, so a migration can never collide with a frozen
  artifact, and run it twice safely.

## Hard rules

**Capture the posting before it rots.** `[CAPTURE-POSTING]` Postings are pulled, edited and
404'd within weeks, and `prep` needs the employer's own words months later to map a story bank
to their criteria. `jd.md` holds the text **verbatim**, with the source URL and the capture date
at the top. Summarise in `fit.md` if you want a summary. Never summarise *into* `jd.md` — a
paraphrase silently becomes the thing you prepare against.

**`_inbox/` here means what `corpus/_inbox/` means: unvetted, and never rendered from and
never cited as fact.** `[INBOX-NOT-EVIDENCE]` Folder location is a truth claim — the same rule
the `interview` skill applies to raw material applies here, and it bites harder, because
inbound application material is *fluent and confident and written by someone with an
incentive*. A recruiter's description of the team's scope, the role's remit, or how the last
person did is a claim by a stranger selling a job. It can shape what you *ask* and what you
*prepare for*. It can never become a fact in a letter or an answer. If something in there is a
fact about the **user**, it earns its way into the corpus through `interview`, like everything
else.

**Never source a claim about the candidate from `applications/`.** `[NOT-FROM-APPLICATIONS]` The
folder holds plenty a render legitimately needs — `jd.md` is what it tailors *to*, `fit.md` is
most of the selection work already done — and `render` is meant to read all of it rather than
ask the user to paste it again. What it may not do is take a *claim about the user* from here.
Everything in this folder that reads like one is already a rendering: another application's
résumé, this one's earlier draft, a line `fit.md` quoted while making its case. Follow the
pointer back to the corpus story and render the claim from there. `render` warns that tailoring
from a baseline is a telephone game that loses exactly the material the JD needs; tailoring from
another application's output is that failure with a second lossy hop, and it is the single
easiest mistake to make once the folder has a `resume.md` sitting in it that looks nearly right.

**No individual's name in a filename or a folder name.** `[NO-NAMES-IN-FILENAMES]` Roles in
filenames, names in the body if the user wants them. Filenames get screenshotted, screen-shared
and tab-completed in front of other people — including, eventually, in front of someone from
that company.

**State is data; prose is for the reader.** `[STATE-IS-DATA]` Anything deriving a thread's
state — a status check, this skill on re-entry — reads `events:` in `application.md`'s
frontmatter and never the log body. Parsing prose fails in the unsafe direction: nothing can
tell *this thread has no events* from *this thread has events I couldn't read*, so one
malformed line makes a sent application look like it is still being written, and every check
gated on having reached `sent` goes quiet at the same moment. No regex fixes that, because with
prose as the surface the ambiguity is real. So: the frontmatter is authoritative for tooling,
the body for *why*. This is not the second copy `[NO-ROLLUP]` forbids — it is the only
machine-readable copy, and nothing parses the body.

The grammar is closed on purpose: `<YYYY-MM-DD> <event>`, one plain string per line,
never a mapping. Mappings need a real YAML parser and a kit cannot assume the user has one, and
a grammar narrow enough to read with one anchored expression is a grammar nobody has to guess
at. Strip comments before parsing, whole-line and trailing — a user annotating why a date is an
estimate or what a pin covers must not be committing a syntax error, or the annotation moves to
some other file, away from the value it explains.

**The folder is the memory; the log is dated and append-only.** `[LOG-APPEND-ONLY]` Don't
rewrite history in `application.md` when a stage changes — add a line. What you believed on the
12th matters when you're working out on the 30th why nobody replied. Append-only forbids
editing what is already there; it does not license paragraphs. One dated line per event, and
don't log history to prevent an error the current state already prevents: a corrected fact
needs no note of what it used to be, because the corrected file is the enforcement, and a
recurrence shows up as a visible contradiction that costs one question to settle. A claim
deliberately left *out* is the exception that isn't one — that is a live constraint rather than
history, and it belongs beside the fact it constrains under `render`'s `[OBEY-DECISIONS]`.
Sibling conventions in this kit prune dead material on every revision; this one never does.
An application log is potentially evidence of what a user decided and why, so it compresses and
folds, and it does not delete.

**The state is at the top; the chronology is below it.** `[STATE-FIRST]` A reader must never
have to reconstruct *where does this stand* by working forward through a log. `events:` is at
the top of the file and ends in the current stage, and the paragraph under the heading says
what the thread is waiting on and whose move it is next — the part that is genuinely not
derivable. Don't restate the stage there; that would be the rollup `[NO-ROLLUP]` forbids.
Entries that no longer bear on the next decision move into a collapsed `<details>` block, which
folds on GitHub and stops dead material from reading as live.

**Store inputs and events; never store a rollup.** `[NO-ROLLUP]` The test is whether it can be
recomputed from what's already on disk. An open-application count, a "3 live, 1 stalled" summary
line, a `status:` field beside a log that already ends in the current stage — all recomputable,
so all of them rot silently and then lie. Read the folders and compute those each time.

**Pin what cannot be reconstructed later, at the moment it is true.** `[PIN-THE-INPUTS]` The
other half of `[NO-ROLLUP]`'s split, and the part that gets skipped: the corpus commit a
render drew on, the hash of what was actually sent, the URL a posting was captured from. Lose
one and it is gone — the posting 404s, the corpus moves on, and nothing on disk remembers. A
pin is not a rollup; it records an input.

**But a pin is a fingerprint, not a copy.** `[PIN-NOT-ARCHIVE]` The `sha256` in a submitted
artifact's frontmatter settles one question and only one: whether a file the user still has is
the file that went out. It recovers nothing. `bootstrap`'s `.gitignore` keeps `*.pdf` and
`*.docx` out of git, so by default the sent bytes survive only as the working copy and the pin
outlives them — never describe the frontmatter as an archive of what a reader saw. A user who
wants those bytes in history can `git add -f <the file that went out>` at the `sent` event.
Offer it as their call at the moment it's live, never as a default: it trades away a privacy
default `PRIVACY.md` sets out.

So `application.md` carries no `status:` field: the last line of its `events:` **is** the
status, and a field beside it is a second copy on its own schedule. And application-level state
lives in `application.md`'s frontmatter, artifact-level state in each artifact's own — **no
separate manifest file**, because a file whose only job is to repeat another file's state goes
stale without anything noticing.

**Record which files the employer actually received.** `[SENT-NAMES-WHAT-WENT]` The `sent:`
block names them, and it is new information rather than a rollup: nothing else on disk knows
which of the things the user prepared went out. Without it, an artifact prepared and
deliberately not sent looks exactly like a defect — the thread reached `sent`, the file still
reads `lifecycle: in-flight`, and a check reports a problem that isn't one. Recording the fact
beats naming the condition, so this is also why there is no fourth `lifecycle:` value for
*prepared and not sent*: it is already expressible as absence from the list. Two invariants
follow, and they only work as a pair: everything in `artifacts:` carries `lifecycle: submitted`
— or something went out unfrozen — and nothing outside it does, or something is frozen that
nobody sent. Ask for the list; never infer it from what happens to be in the folder.

`baselines:` is for a thread that sent something living outside its folder — the maintained
résumé, a letter kept per role family — which is the normal shape of an application older than
the user's folder convention. Without it such a thread can say neither what went out nor that
nothing local did, because an empty `artifacts:` list reads as *nothing was sent*. **Baselines
are deliberately never held to `lifecycle: submitted`**: a baseline goes on being edited, and
freezing one would be wrong rather than merely noisy. One `baseline_pin` covers every file in
the list, because it pins a repo commit and not a file version — `git show <pin>:<path>`
recovers each of them as it stood. A per-file pin invites recording the commit that last
*touched* that file, which quietly asserts nothing else in the send had moved.

**Keep this folder in the private corpus repo and nowhere else.** `[FOLDER-IS-SENSITIVE]` It is
the most sensitive thing in the repo — other people's real names, private correspondence, and
sometimes an employer's confidential material. Never paste its contents anywhere the user
didn't ask for, and don't commit an employer's take-home brief to anything public.

`_inbox/` is git-ignored by default — `bootstrap` writes that rule, and it is the reason
inbound can be filed here at all without thinking about it each time. **For an employer's
confidential material, prefer a reference over a copy:** the link, or the path to where it
already lives, with the date, in `application.md`. That material is not the user's to store.
If a local copy is genuinely needed to work on it, say plainly that it's staying outside the
repo, and log what it is and when it gets deleted. A brief committed once is in history in
every clone, and deleting the file later doesn't take it back — see `PRIVACY.md` in the kit.

**Surface, don't decide.** `[SURFACE-DONT-DECIDE]` Whether to apply with a named gap, whether a
requirement is boilerplate, whether a stalled thread is dead — all the user's call. Give them
the read and the reason, not the verdict.

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

## What "good" looks like

Six weeks after applying, the user opens one folder and has the whole thread: what the posting
actually said, what they claimed, what they were asked, who they spoke to and when, and what
they still can't back. Nothing in it has been quietly upgraded from "a recruiter said" to
"true". And when the loop ends — either way — what it exposed goes back into the corpus
instead of into the bin.
