# Career Corpus Kit

A [Claude Code](https://claude.com/claude-code) plugin for building a **career corpus** — a
private, high-depth record of your work history — and producing everything else from it:
résumés, cover letters, interview prep, level assessments, promotion packets.

**Your résumé is an output, not the source of truth.** You write your career down once, at
full depth. Everything you send is rendered from that record and tailored to the role.

## What using it looks like

A condensed run of sessions from the example corpus. Sam Rivera is fictional, a backend
engineer with eleven years at two companies, and every file mentioned below exists in
[`examples/`](examples/). The replies are shortened; the label after **Claude** is the skill
that picked up the request.

> **You:** Here's my résumé. Set me up.
>
> **Claude** · `bootstrap` — Your corpus is set up: a `profile.md` with your roles and skills,
> and a ranked queue of stories to capture. First in the queue is the nightly batch job at
> Tidewater. Your résumé says you cut its runtime by 80%, and a figure like that is the first
> thing an interviewer will push on.

> **You:** Okay, interview me about the batch job.
>
> **Claude** · `interview` — Before we go further: your résumé says 80%, and just now you said
> "about half, honestly." Which one could you defend in the room? … Written to
> `corpus/tidewater/batch-window.md`. The figure is recorded as disputed. Until a dashboard
> turns up, nothing above "at least half" reaches a résumé.

> **You:** Bellhaven called me tech lead. What level does my work actually read as?
>
> **Claude** · `ladder` — The title outranks the evidence. It was a three-person squad,
> nobody reported to you, and the principal engineer made the design call, so that work reads
> as senior scope. Each finding cites a file and line. The gaps are split in two: the ones you can close with
> an interview session, and the ones only new work will close.

> **You:** I want this one: Engineering Lead at Kestrel Freight. <url>
>
> **Claude** · `apply` — Saved the posting and checked it against your corpus. Five
> requirements are backed. The on-call and nightly-build stories are close matches. Line
> management has no evidence at all, and your mentoring story won't survive a follow-up
> question about it. My read: don't apply yet.
>
> **You:** Applying anyway. Name the gap.
>
> **Claude** · `render` — The résumé and cover letter are written. The letter's last paragraph
> names the line-management gap rather than working around it.

> **You:** They booked a panel for next week.
>
> **Claude** · `prep` — Your prep pack is ready: an opener, a story bank mapped to Kestrel's
> criteria, and the probes they will push on. The hardest probe is line management, and it has
> an honest prepared answer.

> **You:** It's done. They asked about a performance conversation that went badly. I had
> nothing.
>
> **Claude** · `prep` — Logged what they asked. Three items went to your interview queue,
> starting with that question.

Sam didn't get the job, and the rejection cited the requirement the fit check named on day two.
The whole thread is in
[`examples/applications/kestrel-freight-engineering-lead/`](examples/applications/kestrel-freight-engineering-lead/).

## What you can ask it

You don't have to remember any commands. Say what you want and the matching skill picks it up.
Each skill also has a slash command, `/career-corpus:<skill>`, if you'd rather be explicit.

**Build the corpus**

| Say something like | What you get | Skill |
|---|---|---|
| "Here's my résumé and LinkedIn. Set me up." | The corpus folders, a `profile.md`, a `.gitignore` that keeps raw inbound mail out of git, and a ranked queue of stories to capture first. Run it once. | `bootstrap` |
| "Interview me about the hardest project I led at <company>." | One memory per session, turned into a vetted story file with its sources, your own limits on each claim, and the gaps still open. This is where the corpus gets its depth. | `interview` |

**Use the corpus**

| Say something like | What you get | Skill |
|---|---|---|
| "I want to apply for this: <posting or URL>" | A folder for the role. The posting is saved before it disappears, and your corpus is checked against it before anything is written. From there it hands off to `render` and `prep`, and logs the outcome. | `apply` |
| "Just the fit check for this posting. Don't write anything yet." | What the role asks for and which parts your corpus can back. Useful when you're deciding whether a role is worth an evening. | `apply` |
| "What's live?" | Every application, its stage, and how long it has been quiet. | `apply` |
| "Tailor my résumé to this job description." | A résumé or cover letter written only from vetted facts. It works without an application folder too. | `render` |
| "I have an interview loop next Tuesday." | A prep pack: an opener, a story bank mapped to this employer's hiring criteria, the probes they will push on with defensible answers, and questions to ask them. No application folder needed. | `prep` |
| "That interview is done. Here's what they asked and where I fumbled." | The questions you couldn't answer, queued for interview sessions. A question you had no answer for is the most precisely targeted gap you'll ever be handed, so this is worth doing even after a rejection. | `prep` |
| "What level does my work at <company> read as?" | A level range, with a citation for each part of the ladder, the level your evidence clearly clears, and what stands between you and the next one. Each gap is marked as either missing from the file or missing from the work. | `ladder` |
| "Benchmark my on-call story at staff level." | How an invented engineer at that level would tell the same story, so you can compare your own file against it. It is fiction, kept in `benchmarks/`, and never reaches a résumé. | `ladder` |
| "Write a self-review for this cycle, grouped by these competencies: <rubric>" | A self-review written from your own evidence. | `render` |
| "Write a promotion packet for <level> against this rubric, and list every line I have no evidence for." | The packet, plus the list of gaps. The list is the more valuable half. Run `ladder` first if you don't yet know which level your evidence supports. | `render` |
| "Write a LinkedIn About section and a 60-word speaker bio." | The same facts at a different length. | `render` |

**Maintain the corpus**

| Say something like | What you get | Skill |
|---|---|---|
| "Clean up my story files." | The resolved gaps and dated back-and-forth pruned out, with the rules that keep renders honest left alone. You see a diff with a reason for each change first. | `compact` |
| "Fact-check the Tidewater stories." | Every publicly checkable technical claim checked against the public record, with citations. You accept, amend, or reject each finding. Nothing is patched silently. | `verify` |
| "What's outstanding in my corpus?" | Seeds still in `_inbox/`, open gaps per story, and the technologies your stories mention that no capability file covers yet. | [`corpus_status.py`](#reference-the-skills-in-two-lanes) |

## Install

Add the marketplace, then install the plugin from it — from inside a Claude Code session or
from your shell, same result.

**In Claude Code:**

```
/plugin marketplace add atharh/career-corpus-kit
/plugin install career-corpus@career-corpus-kit
```

**From the shell:**

```bash
claude plugin marketplace add atharh/career-corpus-kit
claude plugin install career-corpus@career-corpus-kit
```

The skills show up as `/career-corpus:bootstrap`, `/career-corpus:interview`,
`/career-corpus:apply`, `/career-corpus:render`, `/career-corpus:prep`,
`/career-corpus:compact`, `/career-corpus:verify`, and `/career-corpus:ladder`. If the install
summary says
`Run /reload-plugins to activate.`, run that.

<details>
<summary>Or: install from a clone, without the marketplace</summary>

```bash
git clone https://github.com/atharh/career-corpus-kit ~/career-corpus-kit
cd ~/career-corpus-kit
./install.sh
```

`install.sh` symlinks the repo into `~/.claude/skills/career-corpus`, where Claude Code picks
it up as a plugin. Updating is just:

```bash
cd ~/career-corpus-kit && git pull
```

The symlink means the new content is live immediately — no marketplace refresh, no plugin
update, just `/reload-plugins` or a restart. Same skill names either way. Don't use both paths
at once — two plugins named `career-corpus` would provide the same skills.

To scope it to one project instead, symlink the repo into that project's
`.claude/skills/career-corpus` and start Claude Code from the repo root.
</details>

## Set up your corpus

Your corpus lives in its own repo. Make it private, permanently — it will contain real details
about you and, in roles-only form, about people you've worked with.

```bash
mkdir my-career && cd my-career && git init
```

Private stops other *people* reading it. It doesn't mean the text stays on your machine — a
hosted model reads these files, which is how the kit works at all. [PRIVACY.md](PRIVACY.md)
covers what that means and what doesn't belong in a corpus.

From that repo, run `/career-corpus:bootstrap` and follow its handoff. It writes a
`.gitignore` before anything else — every `_inbox/` stays out of git, because raw recruiter
mail and take-home briefs are the one thing you don't want in history forever. Everything
after that is in [What you can ask it](#what-you-can-ask-it).

## Updating later

The marketplace is a git clone of this repo: refreshing it pulls new commits, and updating the
plugin then installs from the refreshed clone. Both steps are needed — the second is the one
that moves you to the new version.

**In Claude Code:**

```
/plugin marketplace update career-corpus-kit
```

Then open `/plugin`, select `career-corpus`, and choose **Update now**. (There's no `/plugin
update` slash command, and re-running `/plugin install` is a no-op while the plugin is
already installed.)

**From the shell:**

```bash
claude plugin marketplace update career-corpus-kit
claude plugin update career-corpus@career-corpus-kit
```

Restart Claude Code — or run `/reload-plugins` — to load the new version. `claude plugin list`
shows what you're on. Installed versions live in
`~/.claude/plugins/cache/career-corpus-kit/career-corpus/<version>/`, so an old directory
sticking around after an update is normal.

## Reference: the skills, in two lanes

Underneath those prompts, the kit is two lanes. One builds the corpus. The other spends
it, one job application at a time.

**Lane 1 — build the corpus**

| Skill | When | What it does |
|---|---|---|
| **`/career-corpus:bootstrap`** | once, at the start | Reads your existing résumé/LinkedIn, sets up the corpus, and generates a prioritized queue of stories worth extracting. Gets you from empty to "start with this one." |
| **`/career-corpus:interview`** | whenever a memory surfaces | Interviews you about one memory and writes a vetted story file. Relentless, works in rounds of a few questions at a time, and it never lets a claim in that you can't defend. |
| **`/career-corpus:compact`** | maintenance | Prunes the sediment interviews leave behind — resolved gaps, dated back-and-forth — while guarding the lines that keep renders honest: your ceilings, rendering decisions, and rejected readings. Run it when a gap list has become more archive than queue. |
| **`/career-corpus:verify`** | maintenance | Reads story files the way a technical interviewer would and checks every publicly checkable technical claim against the public record, with citations. Findings arrive as a report — you accept, amend, or reject each one; nothing is patched silently, and nothing is corrected without a source. |
| **`/career-corpus:ladder`** | a promotion case, or a level check | Grades the vetted corpus against a career ladder: a level range with a `file:line` citation per pillar, the floor, and the delta to the next rung, with every gap sorted into capture versus work. Its other mode writes a synthetic telling of one story at a named level — fiction, quarantined in `benchmarks/`, never rendered — so you can diff your own file against it and find what you never did, measured, or recorded. |

**Lane 2 — run an application**

| Skill | When | What it does |
|---|---|---|
| **`/career-corpus:apply`** | you found a role | Opens the application and owns it end to end. Captures the posting before it 404s, checks the corpus against the role *before* anything gets written, and holds everything that arrives afterwards — recruiter mail, take-home briefs, the outcome — in one folder. |
| **`/career-corpus:render`** | you're writing the application | Reads the vetted corpus + the job description and produces a résumé entry or cover letter — tailored to that role, sourced only from what the corpus vouches for. |
| **`/career-corpus:prep`** | an interview is booked | Builds a prep pack for that specific interview: an opener, a story bank mapped to the employer's own hiring criteria, the probes they'll push on with defensible answers, and questions to ask them. Run it again afterwards to capture what was actually asked. |

`render` produces documents you **send**. `prep` produces a directory you **study** — and its
second half feeds what you fumbled back into `interview`, which is where the loop closes.

An application is a months-long thread, not a document, so `apply` gives each one a folder:

```
applications/acme-staff-engineer/
  jd.md            ← the posting, verbatim, with its URL and the date you captured it
  application.md   ← events as frontmatter, the dated log beneath it, contacts by role
  fit.md           ← what this role wants, and what your corpus can and can't back
  _inbox/          ← raw inbound — recruiter mail, take-home brief. Unvetted, never rendered from
  resume.md, cover-letter.md         ← written by render
  interview-prep.md, 01-…–05-…       ← written by prep
```

`fit.md` is the one people don't expect. It runs **before** the résumé, and "don't apply yet —
nothing in your corpus backs the main thing they're asking for" is a valid answer. That's a
cheaper thing to find out now than in the room.

Ask *"what's live?"* and `apply` runs the one script the kit ships, from your repo root:

```
python3 "${CLAUDE_PLUGIN_ROOT}/tools/application_status.py"
```

Every thread, its stage, how long it has been quiet — all computed from the files, never stored,
so it cannot go stale. Its `NEEDS ATTENTION` block is a conformance check rather than a summary:
each line is one of this kit's stated rules being broken — something sent that was never frozen,
something frozen that nobody sent, a thread whose events can't be read. What it will not tell
you is what to do next. Stage and age are derivations; whether a quiet thread is dead is a
judgement about your career, and the kit doesn't take those.

The corpus side has its own, for what's outstanding there:

```
python3 "${CLAUDE_PLUGIN_ROOT}/tools/corpus_status.py"
```

Seeds still in `_inbox/`, open gaps per story, capability files a story cites before anyone
wrote them, story and capability files whose frontmatter declares nothing — and the capability queue: every technology a story declares in `technologies:`
that no capability file's `covers:` answers for. That last list is derived from two frontmatter
fields and nothing else. There is no lexicon in the tool to fall behind and no dismissal list to
maintain; a family file covers the terms you wouldn't claim standalone, and a recorded clean no
is coverage too.

The kit ships one other script, for when your corpus is older than the guidance:

```
python3 "${CLAUDE_PLUGIN_ROOT}/tools/corpus_doctor.py"
```

The kit can never see your corpus, so it cannot migrate one — this reports where you're behind
and writes nothing. Findings come sorted by what to do with them: **blocking** (nothing else
about that thread is knowable yet), **mechanical** (the fix is unambiguous, and a session can
propose it), **editorial** (detectable, but the fix is a judgement, so no tool should make it),
and **additive**, where nothing is wrong and the list is the whole migration. It never fails —
a corpus that predates a rule isn't a corpus breaking one, and nothing records which version
you've reached, because that marker would be the first thing to go stale.

`render` also works outside a lane — baselines, self-reviews, promo packets, bios. Those belong
to no application, so no folder gets opened for them.

The `.md` files are the repository copies, and raw Markdown is not a sending format. What goes
out is a PDF, a DOCX, or the body pasted into a form — so the provenance frontmatter every
rendered artifact opens with never reaches an employer.

**The kit writes the Markdown and stops there.** Converting it is yours to choose, because a
stylesheet is a design opinion and this kit doesn't hold one. `pandoc resume.md -o resume.docx`
is the shortest path, needs nothing else installed, and drops the frontmatter on the way out —
pandoc reads it as metadata rather than text, so the provenance block can't leak through any
pandoc-based conversion. For a PDF without a heavier toolchain, `pandoc resume.md -o resume.pdf
--pdf-engine=typst` needs one extra binary instead of a TeX install. And if your corpus repo
already has a build pipeline, `render` uses it and re-checks the page count. Whatever you
pick, extract the text back out of the result once and read it: a converter can produce a
perfect-looking page whose text layer no parser can match, and `render`'s `[TEXT-LAYER]` rule
says what to look for.

## Why a corpus

A résumé bullet, a cover-letter paragraph, and a spoken interview answer are the same fact
compressed to three different lengths. Most people write the compressed bullet and throw away
the source, so when an interviewer pushes, there's nothing underneath. This kit inverts that.
You write your career once, at full depth, in Markdown story files, and everything you send is
rendered from them.

It's also how you stop forgetting your own career. Recall is triggered, not enumerated: you
remember the thing you did five years ago only when something nearby jogs it. The interview
skill is built to do that jogging, and to write down what surfaces before it fades.

## See one before you build one

**[`examples/`](examples/)** holds a complete fictional corpus — one invented engineer, two
invented companies, three stories — with the résumé and cover letter rendered from it, and one
whole fictional application: the posting, the fit check, the recruiter's email, the tailored
artifacts, the interview pack and the rejection.

It's deliberately mid-flight rather than polished, because that's the state a real corpus is in
almost always: open gaps, one number the corpus refuses to resolve on the user's behalf, a
through-line the user withdrew, and a theory the model got wrong and had to record as its own
error.

If you read one file, read **[`examples/rendered/ANNOTATED.md`](examples/rendered/ANNOTATED.md)**.
It puts the lines the model wanted to write next to what actually shipped, and names the
corpus rule that stopped each one:

| The tempting version | What shipped |
|---|---|
| "Cut pipeline runtime by 80%" | "roughly halving runtime" |
| "Drove org-wide adoption" | "Two other teams later adopted the same pattern" |
| "Led the team responsible for six services" | "Led a rebuild of the on-call rotation" |
| "Architected a data platform" | "Built and owned the nightly export and transform" |

Every one of those was survivable on paper and unsurvivable in the room, because each invites a
follow-up question the candidate can't answer. That gap is the entire thing this kit exists to
close.

The application folder makes the same argument at thread length, and it ends in a rejection on
purpose. The fit check said *don't apply yet* on day two, named the one requirement the corpus
could not back, and refused to cover it with the adjacent story sitting right there. Five weeks
later that requirement is what the rejection cited.

## What makes the output trustworthy

The value isn't "an AI wrote my résumé" — anything can do that. It's a set of rules, each
learned by getting it wrong, that keep every rendered line defensible in the room:

- **Vetted facts only.** A claim reaches a résumé only if a story file sources it. Raw drafts
  live in `corpus/_inbox/` and are never rendered from.
- **Numbers carry a source and a ceiling.** "Doubled" never drifts to "tripled" because a
  reused draft made it sound better.
- **Vocabulary gets dated.** You don't get described using a tool or job title that didn't
  exist when you did the work — it's the fastest way to get caught.
- **Honest role attribution.** "Proposed and prototyped; the team delivered" never becomes "I
  built it." Bylines are checkable.
- **No names of private people; no internal codenames.** Roles only, always.
- **The true version wins.** In practice the accurate story is almost always stronger than the
  inflated one.
- **Nothing is applied silently.** You see a diff with a reason per change, and every genuine
  judgment call is surfaced as yours to make.

Those rules are written down *and* checked. [`evals/`](evals/) turns the rejected claims in
`ANNOTATED.md` into assertions — a disputed number, a ceiling, a reading the user refuted, an
attribution they have no standing for — and runs them against the committed example output on
every push, alongside static checks on the skills themselves. CI covers repository policy and
the shipped artifacts, so it catches an example drifting into a claim its own corpus forbids;
it does not exercise the skills. A live mode does — it renders fresh from the fixture corpus
in a real session — and because renders are stochastic it's opt-in, run by hand before a
change to a skill's hard rules. `./evals/run.sh` needs nothing but `python3`.

## The skills learn your preferences

They ship generic, but they sharpen to *you* over time. When you correct one in a way that
generalises — a wording you won't use, a framing you reject, a repeated mistake — it appends a
one-line rule to `corpus/LESSONS.md` in your **private** repo and reads it back at the start of
every session. A rule that turns out wrong is retired, not deleted: with your approval it gets
struck through with the date and a reason, and stops being applied. The one exception is a rule
the method itself later absorbs — once a shipped skill carries it in full and nothing about it
is specific to you, you can delete the private copy outright, because a duplicate only drifts.
The method stays public and stable; your scar tissue stays private and personal. That feedback loop — mistake → durable
rule — is what makes a corpus setup genuinely yours.

## Honest caveats

- **The tailoring step is the least-tested part.** Selecting and angling stories from a real
  job description is the newest capability here; treat early tailored drafts as strong first
  drafts and review the diff rather than trusting the selection blindly.
- **It's only as good as your corpus.** The skills can't invent depth. The work is sitting for
  the interviews — which is also the entire point: it's what nobody else will do, and it's why
  the output isn't generic.

## A note on where this came from

These skills were generalised from a working setup built for one person's real job search. The
private career details have been stripped out; what remains is the method and the hard-won
rules. If you find a rule cryptic, it's probably a scar — keep it.

Do what you like with this — [MIT](LICENSE). Attribution appreciated, not required.
