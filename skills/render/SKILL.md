---
name: render
description: Render a résumé entry or cover letter from the user's vetted career corpus, tailored to a target job description. The corpus-out counterpart to the career-corpus interview skill. Use when they want to write or tailor a résumé or cover letter, or adapt their application to a specific role or JD. To open and track a whole application, use the career-corpus apply skill; for a booked interview, use the career-corpus prep skill.
---

# Career corpus — render

The `corpus/` directory is the source of truth. Résumés, cover letters, and interview answers
are **renderings** of it — never the other way round. This skill turns vetted corpus material
into one of those artifacts, aimed at a specific role. Material gets *into* the corpus with
the companion `interview` skill.

Rendering a tailored artifact is one step inside an application that `apply` opens and owns.
Baselines, self-reviews, promo packets and bios belong to no application; this skill handles
those on its own.

Every LLM can "write a résumé." The value here is **rendering faithfully** — saying only what
the corpus vouches for, in the form the artifact needs, tailored to the job. The rules below
each exist because someone got them wrong.

## Two tiers: baseline and tailored

Two deliverables, related but distinct. Know which one you're producing.

**Baseline (no JD) — a maintained checkpoint.** The strongest *general* version of each
artifact, kept current as the corpus grows. What the user sends when there's no specific
posting, and the voice/style reference every tailored version starts from. Keep these as
canonical repo files, e.g.:
- `resume.md` — the résumé
- `cover-letter-<family>.md` — one per role family they apply to (e.g. leadership, ic, etc.)

Refresh a baseline when the corpus gains material that would change it. A baseline obeys every
faithful-rendering rule below; it just selects the generally-strongest evidence instead of
JD-specific evidence.

⚠️ **Read that instruction again: it only points one way.** Every corpus session validates new
claims, the baseline is the obvious place for them to land, and nothing in this skill has ever
said *remove*. Left alone, a baseline stops being the strongest general version and becomes the
union of everything ever vetted — at which point the strongest evidence is buried among the
merely true, and a reader who stops early never reaches it. **A refresh that only ever adds is
not a refresh.** Every baseline refresh reconsiders what is already there, not just what is new.

**A bullet earns its slot on all three** — the hard rules below, applied at *selection* time
rather than at writing time:

- **A decision that was actually theirs** — honest attribution `[HONEST-ATTRIBUTION]`. Being
  present while a team shipped is not a slot.
- **A mechanism specific enough that nobody else could have written the sentence** — the true
  version `[TRUE-VERSION]`. If it would fit on a stranger's résumé unchanged, it is describing
  a job, not their work.
- **An outcome or scope figure that survives one follow-up question** — a number's source and
  ceiling `[NUMBER-CEILING]`. Failing this one
  is the usual killer: an outcome nobody measured is the same defect as an unsourced number.

Bullets that establish the **role and its scope are structural, not outcomes** — they answer
"what was this person" rather than "what did they do", and they don't compete for outcome slots.
A promotion or a change of role inside one company can need more than one.

**Cutting costs nothing, and say so when the user hesitates.** The material stays in the corpus,
and a tailored render pulls it straight back for a role that wants it — JD relevance admits a
bullet the baseline cut, which is what the tiering is *for*. A claim is only lost if it was never
extracted.

**Tailored (with JD) — a per-application derivative.** Given a posting, produce a version
aimed at *that* role. Write outputs to `applications/<company>-<role>/` so they stay separate
from the baselines and from other applications.

That folder belongs to the `apply` skill. **If it already exists, read it instead of asking
the user to paste things again** — `jd.md` is the posting verbatim and `fit.md` already names
what the corpus can and can't back for this role, which is most of the selection work done. If
it doesn't exist and the user has a JD in hand, offer to open the application first
(`/career-corpus:apply`) rather than dropping two files into a bare directory; the folder is
where everything that arrives later has to go.

**The rule that keeps tailoring honest: tailor from the CORPUS, not from the baseline.** The
baseline is a starting point and a voice reference — read it to see the default and match
their register — but pull facts, story *selection*, and *angling* from the corpus itself. A
baseline has already baked in a JD-less thesis and cut stories a given role might want;
rendering the tailored version *from* it is a telephone game that loses exactly the material
the JD needs. Read both; source from the corpus.

### The JD is the thesis (tailored mode)

The core design principle, and what makes tailoring more than reformatting: **the job
description decides which stories appear and which face they wear.** Don't pick a stance in
advance and fit the corpus to it. Extract what the role actually rewards (real requirements,
not boilerplate), choose the 2–4 corpus stories that are the strongest evidence *for it*, and
render each through the lens that fits. One story can be "aligned three orgs" for a leadership
role and "engineering judgment under pressure" for a staff role — same facts, different face.

⚠️ **This thesis-from-JD step is the least battle-tested part of the system.** Treat early
tailored output as a strong first draft, and lean on the diff-and-decide review
`[SHOW-THE-DIFF]` rather than trusting the selection blindly.

## Hard rules — faithful rendering

**Every claim about the candidate comes from the vetted corpus, and from nothing else.**
`[CLAIM-SOURCE]` A claim reaches the artifact only if a corpus story vouches for it
(`facts_vetted` / published sources). Three kinds of material feed a tailored render, and only
the first is evidence about the user:

- **Candidate claims** — what they did, built, decided, chose against, achieved, know. Vetted
  corpus files only.
- **Employer context** — what the role wants, what the company does, what the team is for.
  `jd.md`, the employer's own public material, clearly attributed inbound. This is what you
  tailor *to*. It is never a fact about the user.
- **Derived analysis** — `fit.md`, an earlier draft, another application's résumé. Read it to
  use the work already done. Never cite it as evidence, and treat its conclusions as carrying
  the error bars of whatever they were computed from: analysis calculated off a résumé inherits
  that résumé's mistakes, so a confident-sounding gap or strength can be an artefact of a wrong
  input rather than a finding about the user.

So: **read `applications/`, but never source a candidate claim from it.** `fit.md` has already
matched the corpus against this JD, which is most of the selection work — take its pointers,
then open the story file it names and render the claim from *there*. Anything in that folder
that reads like a finished claim is already a rendering, and taking it at face value is the
baseline telephone game above with a second lossy hop. It is the easiest mistake to make once
the folder holds something that looks nearly right.

`_inbox/` is **never evidence for a candidate claim** — in the corpus and in an application
alike. It may supply attributed employer context and operational fact: what the role is said to
want, when the interview is, what format it takes. Nothing more. It is raw ore: its numbers are
unsourced and forbidden until extracted into a story file, and a recruiter's account of the role
is a claim by a stranger with an incentive, never a verified fact about the company or the user.
It can shape what you emphasise. It can never become a sentence the user has to defend.

**Numbers carry their source and their ceiling.** `[NUMBER-CEILING]` Render only figures a
corpus file sources, at the value it sources. If a metric was confirmed as "doubled," never the
"tripled" a draft inflated it to. If a file says "do not inflate" or "do not quote a count,"
obey it.

A number in `facts_disputed` renders at **neither** value. If the user has already settled a
floor both sources agree on — recorded as a `RENDERING DECISION` — render that. Never pick
the floor yourself: choosing which version of a contested number to say is exactly the call
that block exists to take away from you. And note what `facts_vetted` does and doesn't mean —
it says the user is on record, not that anyone checked. See "What 'vetted' means" in
`interview`.

**Date the vocabulary, not just the facts.** `[DATE-VOCABULARY]` No term that postdates the
work. If the corpus says they were "doing data modelling in 2014," don't render it as a tool
that shipped in 2016. Check `anachronisms_corrected` blocks before using any tool or role name.

**No names of non-public people. No internal codenames.** `[NO-NAMES-CODENAMES]` Roles, not
names ("a senior engineer," not the person). Say "the company's service catalog," not the
internal project codename; "~10 teams," not the internal team names. Internal names mean nothing
to a reader and may be confidential. Public bylines (blog co-authors, conference talks) are
fine.

**Attribute their role honestly.** `[HONEST-ATTRIBUTION]` Match the corpus `role:` /
`authorship:` exactly. Idea + prototype + sponsorship renders as "proposed and prototyped; the
team delivered" — never "I built." Being one author of five is not sole authorship.
Over-claiming is checkable and fatal.

**And don't render hindsight as design intent.** `[NOT-HINDSIGHT]` Building something that later
became infrastructure is not the same claim as having planned it that way, and the corpus rarely
says the second one. "Noticed their own work was worth generalising" survives the follow-up
question; "designed a platform" invites one they can't answer. Outcome the user didn't foresee
is still theirs — credit it as what it was.

**Obey recorded rendering decisions.** `[OBEY-DECISIONS]` The corpus stores calls the user
has already made — which framing to use, what not to cite, wording still pending. Search the
relevant files for `RENDERING DECISION` / `⚠️` notes and honor them. Don't relitigate a settled
call.

**Prefer the true version.** `[TRUE-VERSION]` The accurate version is stronger than the
inflated one essentially every time. "Built a format others filled, still in use years later"
beats "wrote 50 modules." Reach for precision, not superlatives.

**Keep provenance in the corpus, not in the prose.** `[PROVENANCE-NOT-PROSE]` Track "how we know
this" in corpus frontmatter. The artifact itself gets clean, confident claims — no hedges that
leak the research process into the sentence the reader sees.

**Surface diffs and decisions; never silently apply.** `[SHOW-THE-DIFF]` Show current → proposed
with a one-line reason per change. Flag genuine choices — accurate-but-different vs
safe-but-vague wording, whether to include a team win, what to cut for length — as *the user's*
call, not yours. Reconciling their own material is their decision, not yours.

**On a baseline refresh, present the selection as a selection.** `[SELECTION-AS-SELECTION]` Not
just what changed — what is in, what is out, and one line of why for each. Otherwise a cut looks
like a loss instead of a choice, and "what to cut for length" quietly becomes your call rather
than theirs.

**How long an entry should run is theirs to set, and this skill states no number.**
`[LENGTH-IS-THEIRS]` The first time it comes up, ask, and write the shape they accept into
`corpus/LESSONS.md` — that file is where their preferences live, not this one. Afterwards hold
to it without re-asking; reopen the question only when a refresh would exceed what they set. A
number invented here would be a preference imposed on every user of the kit, which is exactly
what that file exists to prevent.

**Make it sound like the user, not a model — always, as the last step.** `[THEIR-VOICE]`
Rendered prose that reads as AI-written gets binned. Two moves, in order:
- **Use the user's own recorded voice.** The corpus captures how they actually talk — their
  quotes, blunt phrasings, the concrete scenes. Pull those in rather than smoothing them into
  competent generic prose. A generic humanizer strips AI tells but can't *invent* their voice;
  the corpus already has it. This step is unique to this system — do it first.
- **Run a humanizing pass to finish.** If a dedicated `humanizer` skill is installed, invoke
  it on the draft. If not, self-edit for the reliable tells: em-dash pile-ups (cut to near
  zero), uniform sentence length (vary it hard), rule-of-three cadence, inflated vocabulary
  (*leverage, robust, seamless, testament, delve*), and filler/throat-clearing.

This applies to human-facing prose only (cover letters, interview answers) — corpus story
files are internal scaffolding and stay as they are.

## Lessons — how this skill personalises to you

This skill ships generic. It gets sharper by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After the user corrects a render in a way that generalises** — a wording preference, a
  claim they won't make, a framing they reject — append one dated line to `corpus/LESSONS.md`:
  the mistake, and the rule to apply next time. One line each. Nothing already in the file is
  deleted.
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
  The method stays stable and shareable; the scar tissue stays private and personal.

## Workflow

1. **Decide the tier.** JD in hand → tailored (write to `applications/<company>-<role>/`). No
   JD → baseline (update the canonical repo file). Say which you're doing.
2. **If tailored, find the application folder.** If it exists, read `jd.md` and `fit.md` from
   it; if it doesn't, offer `/career-corpus:apply` first. Then read the JD and name what the
   role actually rewards, in one or two lines — that's the thesis.
3. **Read the corpus** — `through-lines.md`, the relevant `background.md` and story files, and
   any `RENDERING DECISION` notes. For a tailored render, also read the closest baseline as a
   voice reference (but source facts from the corpus, not from it).
4. **Select** the 2–4 stories that are the strongest evidence — for the JD if tailored, in
   general if baseline. Leave the rest out; a résumé cuts as much as it adds.
5. **Render** in the artifact's shape — see [REFERENCE.md](REFERENCE.md) for résumé / cover
   letter / interview-prep specifics, and
   [templates/artifact-frontmatter.md](templates/artifact-frontmatter.md) for the block every
   artifact opens with.
6. **Present as a reviewable diff**, decisions flagged, before applying anything.
7. **On approval**, apply. If a PDF pipeline is present, rebuild and confirm the page count.

## What "good" looks like

Every line traces to the corpus. Nothing outruns its source. The role's real requirements are
answered by specific evidence, not adjectives. A hostile interviewer with the JD and the
public record open finds nothing to puncture. And it reads like the user — plain, precise, no
inflation.
