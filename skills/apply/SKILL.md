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
  application.md   ← the dated event log, and contacts by role. The last line is the stage
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
claimed in the box.

**5. Inbound.** Everything that arrives goes in `_inbox/` with a date, and the log gets a line.
Recruiter mail, rejections, scheduling, the take-home brief, the "we've moved you to the next
round" note.

**6. Prep.** When a round is booked: *"Run `/career-corpus:prep` — the JD and the recruiter's
note are already in the folder."* `prep` reads them from here rather than asking again.

**7. Close.** Record the outcome and the date. Then the part people skip: **a rejection with a
reason in it is corpus material.** So is anything the loop exposed. Route it to
`/career-corpus:interview` and say so explicitly — this is the highest-signal queue the corpus
ever gets, and it evaporates within a week.

**Asked "what's live?"** — read `applications/*/application.md`, report stage, age and next
action per thread, and name the ones that have gone quiet. Compute it; never store it.

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
what it can see and asks; picking between them is a call about someone's career, which rule 8
says is theirs. Say which you suspect and why, as a question.

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

## The log's event vocabulary

`application.md` is a dated, append-only list of events, and the events are named from a fixed
set so a thread can be read at a glance six weeks later. Nine of them:

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

## Hard rules

**1. Capture the posting before it rots.** `[CAPTURE-POSTING]` Postings are pulled, edited and 404'd within weeks,
and `prep` needs the employer's own words months later to map a story bank to their criteria.
`jd.md` holds the text **verbatim**, with the source URL and the capture date at the top.
Summarise in `fit.md` if you want a summary. Never summarise *into* `jd.md` — a paraphrase
silently becomes the thing you prepare against.

**2. `_inbox/` here means what `corpus/_inbox/` means: unvetted, and never rendered from and
never cited as fact.** Folder location is a truth claim — the same rule the `interview` skill
applies to raw material applies here, and it bites harder, because inbound application
material is *fluent and confident and written by someone with an incentive*. A recruiter's
description of the team's scope, the role's remit, or how the last person did is a claim by a
stranger selling a job. It can shape what you *ask* and what you *prepare for*. It can never
become a fact in a letter or an answer. If something in there is a fact about the **user**,
it earns its way into the corpus through `interview`, like everything else.

**3. Never source a claim about the candidate from `applications/`.** The folder holds plenty
a render legitimately needs — `jd.md` is what it tailors *to*, `fit.md` is most of the
selection work already done — and `render` is meant to read all of it rather than ask the user
to paste it again. What it may not do is take a *claim about the user* from here. Everything
in this folder that reads like one is already a rendering: another application's résumé, this
one's earlier draft, a line `fit.md` quoted while making its case. Follow the pointer back to
the corpus story and render the claim from there. `render` warns that tailoring from a
baseline is a telephone game that loses exactly the material the JD needs; tailoring from
another application's output is that failure with a second lossy hop, and it is the single
easiest mistake to make once the folder has a `resume.md` sitting in it that looks nearly
right.

**4. No individual's name in a filename or a folder name.** Roles in filenames, names in the
body if the user wants them. Filenames get screenshotted, screen-shared and tab-completed in
front of other people — including, eventually, in front of someone from that company.

**5. The folder is the memory; the log is dated and append-only.** `[LOG-APPEND-ONLY]` Don't rewrite history in
`application.md` when a stage changes — add a line. What you believed on the 12th matters when
you're working out on the 30th why nobody replied.

**6. Store inputs and events; never store a rollup.** `[NO-ROLLUP]` The test is whether it can be recomputed
from what's already on disk. An open-application count, a "3 live, 1 stalled" summary line, a
`status:` field beside a log that already ends in the current stage — all recomputable, so all
of them rot silently and then lie. Read the folders and compute those each time.

**The other half of the split is the part that gets skipped.** Some things cannot be
reconstructed later, and those get written down at the moment they are true: the corpus commit
a render drew on, the hash of what was actually sent, the URL a posting was captured from. Lose
one and it is gone — the posting 404s, the corpus moves on, and nothing on disk remembers. A
pin is not a rollup; it records an input.

**But a pin is a fingerprint, not a copy.** The `sha256` in a submitted artifact's frontmatter
settles one question and only one: whether a file the user still has is the file that went out.
It recovers nothing. `bootstrap`'s `.gitignore` keeps `*.pdf` and `*.docx` out of git, so by
default the sent bytes survive only as the working copy and the pin outlives them — never
describe the frontmatter as an archive of what a reader saw. A user who wants those bytes in
history can `git add -f <the file that went out>` at the `sent` event. Offer it as their call at
the moment it's live, never as a default: it trades away a privacy default `PRIVACY.md` sets out.

So `application.md` carries no `status:` field: the last line of its log **is** the status, and
a field beside the log is a second copy on its own schedule. And application-level state lives
in `application.md`'s frontmatter, artifact-level state in each artifact's own — **no separate
manifest file**, because a file whose only job is to repeat another file's state goes stale
without anything noticing.

**7. This folder is the most sensitive thing in the repo.** It holds other people's real
names, private correspondence, and sometimes an employer's confidential material. It belongs
in the private corpus repo and nowhere else. Never paste its contents anywhere the user
didn't ask for, and don't commit an employer's take-home brief to anything public.

`_inbox/` is git-ignored by default — `bootstrap` writes that rule, and it is the reason
inbound can be filed here at all without thinking about it each time. **For an employer's
confidential material, prefer a reference over a copy:** the link, or the path to where it
already lives, with the date, in `application.md`. That material is not the user's to store.
If a local copy is genuinely needed to work on it, say plainly that it's staying outside the
repo, and log what it is and when it gets deleted. A brief committed once is in history in
every clone, and deleting the file later doesn't take it back — see `PRIVACY.md` in the kit.

**8. Surface, don't decide.** Whether to apply with a named gap, whether a requirement is
boilerplate, whether a stalled thread is dead — all the user's call. Give them the read and
the reason, not the verdict.

## Lessons — how this skill personalises to you

This skill ships generic. It gets sharper by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After the user corrects this skill in a way that generalises** — how they name folders,
  which requirements they consider boilerplate, a company they won't apply to — append one
  dated line to `corpus/LESSONS.md`: the mistake, and the rule to apply next time. One line
  each. Nothing already in the file is deleted.
- **Route it before you write it: would this rule still hold if the corpus were about someone
  else?** If yes, it belongs to the method — say so and leave it, rather than filing a general
  rule under one person's name. If no, it is this user's, and `corpus/LESSONS.md` is where it
  goes. Either way it goes in a *file*: a rule kept in a session summary or a model's memory
  is in neither place, and **a rule nobody can diff is a rule nobody can review, port, or
  undo.**
- **When a lesson proves wrong, retire it rather than appending its opposite.** Two entries
  that contradict each other both arrive with equal footing in every later session. Retire in
  the session where the lesson misfired and only on the user's explicit say-so, by marking the
  entry in place: `~~<the entry>~~ retired YYYY-MM-DD: <one clause of why>`. A struck entry is
  history and is never applied again.
- **Never edit this SKILL.md to record a lesson,** and never write lessons into the kit repo.

## What "good" looks like

Six weeks after applying, the user opens one folder and has the whole thread: what the posting
actually said, what they claimed, what they were asked, who they spoke to and when, and what
they still can't back. Nothing in it has been quietly upgraded from "a recruiter said" to
"true". And when the loop ends — either way — what it exposed goes back into the corpus
instead of into the bin.
