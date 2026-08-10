---
name: render
description: Render a résumé entry or cover letter from the user's vetted career corpus, tailored to a target job description. The corpus-out counterpart to the career-corpus interview skill. Use when they want to write or tailor a résumé or cover letter, or adapt their application to a specific role or JD. For a booked interview, use the career-corpus prep skill instead.
---

# Career corpus — render

The `corpus/` directory is the source of truth. Résumés, cover letters, and interview answers
are **renderings** of it — never the other way round. This skill turns vetted corpus material
into one of those artifacts, aimed at a specific role. Material gets *into* the corpus with
the companion `interview` skill.

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

**Tailored (with JD) — a per-application derivative.** Given a posting, produce a version
aimed at *that* role. Write outputs to `applications/<company>-<role>/` so they stay separate
from the baselines and from other applications.

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
tailored output as a strong first draft, and lean on the diff-and-decide review (rule 9)
rather than trusting the selection blindly.

## Hard rules — faithful rendering

**1. Vetted facts only. Never render from `_inbox/`.** A claim reaches the artifact only if a
corpus story vouches for it (`facts_vetted` / published sources). `_inbox/` is raw ore — its
numbers are unsourced and forbidden until extracted into a story file.

**2. Numbers carry their source and their ceiling.** Render only figures a corpus file
sources, at the value it sources. If a metric was confirmed as "doubled," never the "tripled"
a draft inflated it to. If a file says "do not inflate" or "do not quote a count," obey it.

**3. Date the vocabulary, not just the facts.** No term that postdates the work. If the corpus
says they were "doing data modelling in 2014," don't render it as a tool that shipped in 2016.
Check `anachronisms_corrected` blocks before using any tool or role name.

**4. No names of non-public people. No internal codenames.** Roles, not names ("a senior
engineer," not the person). Say "the company's service catalog," not the internal project
codename; "~10 teams," not the internal team names. Internal names mean nothing to a reader
and may be confidential. Public bylines (blog co-authors, conference talks) are fine.

**5. Attribute their role honestly.** Match the corpus `role:` / `authorship:` exactly. Idea
+ prototype + sponsorship renders as "proposed and prototyped; the team delivered" — never "I
built." Being one author of five is not sole authorship. Over-claiming is checkable and fatal.

**6. Obey recorded rendering decisions.** The corpus stores calls the user has already made —
which framing to use, what not to cite, wording still pending. Search the relevant files for
`RENDERING DECISION` / `⚠️` notes and honor them. Don't relitigate a settled call.

**7. Prefer the true version.** The accurate version is stronger than the inflated one
essentially every time. "Built a format others filled, still in use years later" beats "wrote
50 modules." Reach for precision, not superlatives.

**8. Keep provenance in the corpus, not in the prose.** Track "how we know this" in corpus
frontmatter. The artifact itself gets clean, confident claims — no hedges that leak the
research process into the sentence the reader sees.

**9. Surface diffs and decisions; never silently apply.** Show current → proposed with a
one-line reason per change. Flag genuine choices — accurate-but-different vs safe-but-vague
wording, whether to include a team win, what to cut for length — as *the user's* call, not
yours. Reconciling their own material is their decision, not yours.

**10. Make it sound like the user, not a model — always, as the last step.** Rendered prose
that reads as AI-written gets binned. Two moves, in order:
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
  the mistake, and the rule to apply next time. One line each. Append-only.
- **Never edit this SKILL.md to record a lesson,** and never write lessons into the kit repo.
  The method stays stable and shareable; the scar tissue stays private and personal.

## Workflow

1. **Decide the tier.** JD in hand → tailored (write to `applications/<company>-<role>/`). No
   JD → baseline (update the canonical repo file). Say which you're doing.
2. **If tailored, read the JD first.** Name what the role actually rewards, in one or two
   lines — that's the thesis.
3. **Read the corpus** — `through-lines.md`, the relevant `background.md` and story files, and
   any `RENDERING DECISION` notes. For a tailored render, also read the closest baseline as a
   voice reference (but source facts from the corpus, not from it).
4. **Select** the 2–4 stories that are the strongest evidence — for the JD if tailored, in
   general if baseline. Leave the rest out; a résumé cuts as much as it adds.
5. **Render** in the artifact's shape — see [REFERENCE.md](REFERENCE.md) for résumé / cover
   letter / interview-prep specifics.
6. **Present as a reviewable diff**, decisions flagged, before applying anything.
7. **On approval**, apply. If a PDF pipeline is present, rebuild and confirm the page count.

## What "good" looks like

Every line traces to the corpus. Nothing outruns its source. The role's real requirements are
answered by specific evidence, not adjectives. A hostile interviewer with the JD and the
public record open finds nothing to puncture. And it reads like the user — plain, precise, no
inflation.
