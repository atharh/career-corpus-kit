---
name: render
description: Render a résumé entry or cover letter from the user's vetted career corpus, tailored to a target job description. The corpus-out counterpart to the career-corpus interview skill. Use when they want to write or tailor a résumé or cover letter, or adapt their application to a specific role or JD. To open and track a whole application, use the career-corpus apply skill; for a booked interview, use the career-corpus prep skill.
---

# Career corpus — render

The `corpus/` directory is the source of truth. Résumés, cover letters and interview answers
are **renderings** of it, never the other way round. This skill turns vetted corpus material
into one of those artifacts, aimed at a specific role. Material gets *into* the corpus with
the companion `interview` skill.

Rendering a tailored artifact is one step inside an application that `apply` opens and owns.
Baselines, self-reviews, promo packets and bios belong to no application; this skill handles
those on its own.

The job is **rendering faithfully**: say only what the corpus vouches for, in the form the
artifact needs, tailored to the job.

## Lessons — how this skill personalises to you

This skill ships generic and sharpens by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit. Never edit this
SKILL.md to record a lesson: the method stays stable and shareable; the scar tissue stays
private and personal.

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

## Two tiers: baseline and tailored

There are two deliverables, related but distinct. Know which one you are producing.

**Baseline (no JD): a maintained checkpoint.** The strongest *general* version of each
artifact, kept current as the corpus grows. The user sends it when there is no specific
posting, and every tailored version starts from it for voice and style. Keep these as
canonical repo files, for example:
- `resume.md`, the résumé;
- `cover-letter-<family>.md`, one per role family they apply to (for example `leadership`, `ic`).

Refresh a baseline when the corpus gains material that would change it. A baseline obeys every
faithful-rendering rule below; it selects the generally strongest evidence instead of
JD-specific evidence.

**A refresh removes as well as adds.** Every corpus session vets new claims, and the baseline
is where they tend to land. A baseline that only accumulates ends up holding everything ever
vetted, and its strongest evidence sits among merely true lines where a reader who stops early
never reaches it. On every refresh, reconsider what is already there, not only what is new.

**Which families exist is derived, never stored.** Derive them from what `applications/` shows
the user has targeted and what the corpus can evidence. When asked which baselines are
missing, or before proposing one under `[SUGGEST-DONT-SPAWN]`, follow *Deriving the family
list* in [REFERENCE.md](REFERENCE.md).

**A bullet earns its slot on all three of these.** They are the hard rules below, applied when
you select material rather than when you write it:

- **A decision that was actually theirs** (`[HONEST-ATTRIBUTION]`). Being present while a team
  shipped does not earn a slot.
- **A mechanism specific enough that nobody else could have written the sentence**
  (`[TRUE-VERSION]`). A line that would fit a stranger's résumé unchanged describes a job, not
  their work.
- **An outcome or scope figure that survives one follow-up question** (`[NUMBER-CEILING]`).
  Of the bullets that fail, most fail this one: an outcome nobody measured is the same defect
  as an unsourced number.

Bullets that establish the **role and its scope are structural, not outcomes.** They answer
"what was this person" rather than "what did they do", and they do not compete for outcome
slots. A promotion or a change of role inside one company can need more than one.

**Cutting costs nothing, and say so when the user hesitates.** The material stays in the
corpus, and a tailored render brings it back for a role that wants it: relevance to a JD can
admit a bullet the baseline cut, which is why there are two tiers. A claim is lost only if it
was never extracted.

**Tailored (with JD): a per-application derivative.** Given a posting, produce a version aimed
at *that* role. Write outputs to `applications/<company>-<role>/` so they stay separate from
the baselines and from other applications.

That folder belongs to the `apply` skill. **If it already exists, read it instead of asking the
user to paste things again.** `jd.md` is the posting verbatim, and `fit.md` already names what
the corpus can and can't back for this role, which is most of the selection work. If the
folder doesn't exist and the user has a JD in hand, offer to open the application first
(`/career-corpus:apply`) rather than dropping two files into a bare directory, because
everything that arrives later belongs in that folder.

**Tailor from the corpus, not from the baseline.** Read the baseline to see the default and to
match the user's register, but take facts, story *selection* and *angling* from the corpus
itself. A baseline was written without a JD and has already cut stories a given role might
want, so a tailored version rendered from it loses exactly the material that JD needs. Read
both; source from the corpus.

### The JD is the thesis (tailored mode)

**The job description decides which stories appear and how each is framed.** This is what
makes tailoring more than reformatting. Don't pick a stance in advance and fit the corpus to
it. Extract what the role actually rewards (real requirements, not boilerplate), choose the
2–4 corpus stories that are the strongest evidence *for it*, and frame each one for that
requirement. One story can be "aligned three orgs" for a leadership role and "engineering
judgment under pressure" for a staff role: the same facts, framed differently.

## Hard rules — faithful rendering

**Every claim about the candidate comes from the vetted corpus, and from nothing else.**
`[CLAIM-SOURCE]` A claim reaches the artifact only if a corpus story vouches for it
(`facts_vetted` or published sources). Three kinds of material feed a tailored render, and only
the first is evidence about the user:

- **Candidate claims:** what they did, built, decided, chose against, achieved, know. Vetted
  corpus files only.
- **Employer context:** what the role wants, what the company does, what the team is for. This
  comes from `jd.md`, the employer's own public material, and clearly attributed inbound.
  It is what you tailor *to*, and it is never a fact about the user.
- **Derived analysis:** `fit.md`, an earlier draft, another application's résumé, and
  `corpus/directions.md`, which is a hypothesis about where the evidence *could* point and never
  evidence itself (`[DIRECTIONS-FILE]`). Read it to use the work already done. Never cite it as
  evidence. Its conclusions are only as good as their inputs: analysis computed from a résumé
  inherits that résumé's mistakes, so a confident-sounding gap or strength may come from a
  wrong input rather than from the user's record.

So **read `applications/`, but never source a candidate claim from it.** `fit.md` has already
matched the corpus against this JD: take its pointers, then open the story file it names and
render the claim from *there*. Anything in that folder that reads like a finished claim is
already a rendering, and copying it repeats the baseline problem above with one more copy in
between. This mistake is easiest to make once the folder holds something that looks nearly
right.

`_inbox/` is **never evidence for a candidate claim**, in the corpus or in an application
(`apply`'s `[INBOX-NOT-EVIDENCE]`). It may supply attributed employer context and operational
fact: what the role is said to want, when the interview is, what format it takes. Nothing more.

**Numbers carry their source and their ceiling.** `[NUMBER-CEILING]` Render only figures a
corpus file sources, at the value it sources. If a metric was confirmed as "doubled", never
render the "tripled" a draft inflated it to. If a file says "do not inflate" or "do not quote a
count", obey it.

A number in `facts_disputed` renders at **neither** value. If the user has already settled a
floor both sources agree on, recorded as a `RENDERING DECISION`, render that. Never pick the
floor yourself: deciding which version of a contested number to say is the call that block
exists to keep from you. Note also that `facts_vetted` means the user is on record, not that
anyone checked; see "What 'vetted' means" in `interview`.

**A technology claim renders from its capability file, at its recorded depth.**
`[CAPABILITY-CLAIMS]` When the artifact wants a skills line, a form's self-rating, or an answer
to "what's your experience with X", source it from the `corpus/capabilities/` file whose
`covers:` names X, where one exists. Match on that line, not on the filename, since a family
file answers for terms it isn't named after. The file already carries the depth ceilings and
the noes, so render inside them, and never flatten its different depths into one uniformly
confident list: *administered it* and *my team ran on it* are different claims, and a list
that reads them alike over-claims the weaker one. Where no capability file exists, the claim renders only
what story files back, which for a bare skills-line entry may be nothing; say so rather than
padding the list.

**Date the vocabulary, not just the facts.** `[DATE-VOCABULARY]` No term that postdates the
work. If the corpus says they were "doing data modelling in 2014", don't render it as a tool
that shipped in 2016. Check `anachronisms_corrected` blocks before using any tool or role name.

**Derive a figure that ages; never copy it.** `[DERIVE-AT-RENDER]` The render-side half of
`[RECORD-WHAT-LASTS]` in `interview`. Compute an elapsed figure, such as years of experience or
how long something has run, from the corpus's dates on the day of the render; never copy it
from a line that stated it. A count of something still growing, or a present-tense claim about
a moving state, renders in the corpus's named form where one exists. Where the corpus holds
only a bare figure, render it with the date it was recorded or leave it out, and tell the user
it needs re-reading. An artifact may speak in the present about the current role, because the
day it is sent dates it; what it must not do is carry a stored count forward as today's. ⚠️ A
`[NUMBER-CEILING]` figure about completed work does not age, and renders exactly as recorded.

**No names of non-public people. No internal codenames.** `[NO-NAMES-CODENAMES]` Roles, not
names ("a senior engineer", not the person). Say "the company's service catalog", not the
internal project codename, and "~10 teams", not the internal team names. Internal names mean
nothing to a reader and may be confidential. Public bylines (blog co-authors, conference
talks) are fine.

**Attribute their role honestly.** `[HONEST-ATTRIBUTION]` Match the corpus `role:` and
`authorship:` exactly. Idea, prototype and sponsorship render as "proposed and prototyped; the
team delivered", never "I built". Being one author of five is not sole authorship.
Over-claiming is checkable, and an interviewer who catches it discounts everything else.

**And don't render hindsight as design intent.** `[NOT-HINDSIGHT]` Building something that
later became infrastructure is a different claim from having planned it that way, and the
corpus rarely makes the second one. "Noticed their own work was worth generalising" survives
the follow-up question; "designed a platform" invites one they can't answer. An outcome the
user didn't foresee is still theirs; credit it as what it was.

**Obey recorded rendering decisions.** `[OBEY-DECISIONS]` The corpus stores calls the user has
already made: which framing to use, what not to cite, wording still pending. Search the
relevant files for `RENDERING DECISION` and `⚠️` notes and honour them. Don't reopen a settled
call.

**A constraint has one home.** `[CONSTRAINT-HAS-ONE-HOME]` A limit on a claim lives in the
corpus file that owns the claim, and an application thread never repeats it. Mentioning a
ceiling while rendering is right. Copying it into `applications/` so the next reader sees it is
not, because nothing keeps the copy true: correct the corpus later and the copy still states
the old position. The reason given for a copy is always that *a future render might miss it*,
but such a render is already broken, because `[OBEY-DECISIONS]` requires reading the file and
the file holds everything the render needs. So the copy guards against a failure that would
happen anyway, and adds a second thing to keep true. **Grep the corpus before writing a
constraint into an application thread.** A session that believes it is not duplicating
anything will still duplicate unless it checks, and "this exists nowhere else" is what people
write when they have not looked. `fit.md` is the exception: it assesses rather than records,
names the file each ceiling came from, and is regenerated rather than maintained, so a stale
citation gets rewritten.

One of `apply`'s rules is held alongside it:

- **Not every doubt is a blocker.** (`[NOT-EVERY-DOUBT-IS-A-BLOCKER]`) Most uncertainty is not a
  blocker. The test is whether being wrong would be expensive or hard to undo — if it would not,
  say it once, in a clause, and carry on. A render that will not go out until some unresolved
  question is settled has usually escalated a question that no answer would have changed. Three
  things still earn a gate: editing a frozen artifact, putting an unsourced claim in front of an
  employer, and anything the user has said is theirs to decide.

**The user's say-so overrides the corpus and this skill, immediately and without argument.**
`[USER-OVERRIDES]` The corpus exists to stop the user drifting and a model inflating; it has no
standing against the user. If they direct a claim rendered, render it; if they say a story's
shape is wrong, change the shape. Never answer their instruction with "the corpus can't back
that", and never make them say it twice. Record the override as one line of story-file
frontmatter, `overridden: <date> — <what they directed>`, and never as a hedge in the artifact
(`[PROVENANCE-NOT-PROSE]` keeps it out of anything they send). The line lets a later session
tell a claim the corpus vouches for from one the user directed. That matters to the user in a
room: a directed claim is defended as their own recollection, and they must not reach for a
source that was never there. Two things are not overrides:

1. **An inferred or stale instruction.** An override must be explicit and current: never
   inferred from a passing remark, and never an old one carried forward to reinstate something
   since withdrawn. When unsure, ask in this session, in one line.
2. **A checkable public technical fact.** Say-so does not make it true. Per the interview
   skill's `[CHECK-THE-CLAIM]`, look it up, tell the user what the public record says, then
   render what they decide.

**Prefer the true version.** `[TRUE-VERSION]` The accurate version is stronger than the
inflated one essentially every time. "Built a format others filled, still in use years later"
beats "wrote 50 modules". Write precise claims, not superlatives.

**Keep provenance in the corpus, not in the prose.** `[PROVENANCE-NOT-PROSE]` Track how each
claim is known in corpus frontmatter. The artifact itself states clean, confident claims, with
no hedges that show the research process in the sentence the reader sees.

**Surface diffs and decisions; never silently apply.** `[SHOW-THE-DIFF]` Show current → proposed
with a one-line reason per change. Flag genuine choices as *the user's*
call, not yours: accurate-but-different versus safe-but-vague wording, whether to include a
team win, what to cut for length. Reconciling their own material is their decision.

**On a baseline refresh, present the selection as a selection.** `[SELECTION-AS-SELECTION]`
Show not only what changed but what is in, what is out, and one line of why for each.
Otherwise a cut looks like a loss instead of a choice, and what to cut for length quietly
becomes your call rather than theirs.

**Suggest a missing baseline; never create one.** `[SUGGEST-DONT-SPAWN]` Name the missing
member, say what it would be for, and stop. A baseline needs upkeep: every corpus change can
make every baseline stale, and every refresh is a selection the user has to review. Creating
one per family multiplies that staleness and creates review work nobody asked for. Retiring a
family is equally not your call, because someone who has stopped targeting a role family may
still want its checkpoint; that is `apply`'s `[SURFACE-DONT-DECIDE]`.

**How long an entry should run is theirs to set, and this skill states no number.**
`[LENGTH-IS-THEIRS]` The first time it comes up, ask, and write the shape they accept into
`corpus/LESSONS.md`, which is where their preferences live. Afterwards hold to it without
re-asking; reopen the question only when a refresh would exceed what they set. A number written
here would impose one preference on every user of the kit. The cover-letter bounds in
[REFERENCE.md](REFERENCE.md) are not an exception: a page ceiling is a fact about the reader,
not a preference about the user. A *tighter* target than the ceiling is a preference, and goes
in `corpus/LESSONS.md` with the rest.

**Make it sound like the user, not a model — always, as the last step.** `[THEIR-VOICE]`
Readers discard prose that reads as AI-written. Two steps, in order:
- **Use the user's own recorded voice.** The corpus records how they actually talk: their
  quotes, blunt phrasings, the concrete scenes. Use those rather than smoothing them into
  competent generic prose. A generic humanizer removes AI tells but can't *invent* their voice;
  the corpus already has it.
- **Finish with a humanizing pass.** If a dedicated `humanizer` skill is installed, invoke it on
  the draft. If not, edit for the reliable tells yourself: em-dash pile-ups (cut to near zero),
  uniform sentence length (vary it hard), rule-of-three cadence, filler or throat-clearing, and
  inflated vocabulary. Which words read as machine-written changes as models change, so edit
  against the stock words current models overuse; *leverage* and *delve* are examples, not the
  list.

This applies to human-facing prose only (cover letters, interview answers). Corpus story files
are internal working files and stay as they are.

**The text layer has to say what the page says.** `[TEXT-LAYER]` Last of all, and only when the
Markdown becomes a PDF or a DOCX. A generated file carries an image for a person and characters
for a machine. The two can disagree without anything looking wrong: the page is right, the
extracted text is wrong, and the extracted text is usually what reads an application first. Two
defects cause this. Ligatures written as U+FB00–FB04 stop `staff` and `workflows` matching the
posting's own words, and list markers drawn as vector art make every bullet arrive unmarked.
The check and the fix for each are in [REFERENCE.md](REFERENCE.md). **Verify by reading the
extracted text, never by eye**: both defects render perfectly, so the page is no evidence.
Whether a reader can read the artifact is a fact about the reader, like the page ceiling under
`[LENGTH-IS-THEIRS]`, so this rule does not make the kit hold opinions about stylesheets.

## Workflow

1. **Decide the tier.** With a JD in hand, render tailored and write to
   `applications/<company>-<role>/`. With no JD, render a baseline and update the canonical repo
   file. Say which you are doing.
2. **If tailored, find the application folder.** With more than one live application and none
   named, by the user or by the session's own context, list them and ask. Never guess, because
   a render against the wrong JD looks exactly like a correct one. If the folder exists, read
   `jd.md` and `fit.md` from it; if it doesn't, offer `/career-corpus:apply` first. Then read
   the JD and name what the role actually rewards, in one or two lines. That is the thesis.
3. **Read the corpus:** `through-lines.md`, the relevant `background.md` and story files, any
   `capabilities/` files the role's stack touches, and any `RENDERING DECISION` notes. For a
   tailored render, also read the closest baseline for voice, but source facts from the corpus,
   not from it.
4. **Select** the 2–4 stories that are the strongest evidence: for the JD if tailored, in
   general if baseline. Leave the rest out; a résumé cuts as much as it adds.
5. **Render** in the artifact's shape. See [REFERENCE.md](REFERENCE.md) for résumé, cover
   letter and interview-prep specifics, and
   [templates/artifact-frontmatter.md](templates/artifact-frontmatter.md) for the block every
   artifact opens with.
6. **Present it as a reviewable diff**, with decisions flagged, before applying anything.
7. **On approval, apply.** If a PDF pipeline is present, rebuild, confirm the page count, and
   check the text layer against the page (`[TEXT-LAYER]`).

## What "good" looks like

Every line traces to the corpus, and nothing claims more than its source. The role's real
requirements are answered by specific evidence, not adjectives. A hostile interviewer with the
JD and the public record open finds nothing to puncture. And it reads like the user: plain,
precise, no inflation.
