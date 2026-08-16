# Career Corpus Kit

A [Claude Code](https://claude.com/claude-code) plugin for building a **career corpus** — a
private, high-depth record of your work history — and rendering résumés, cover letters, and
interview prep from it.

The premise: **your résumé is an output, not the source of truth.** A résumé bullet, a cover-
letter paragraph, and a spoken interview answer are the same fact compressed to three
different lengths. Most people author the compressed bullet and throw away the source — so
when an interviewer pushes, there's nothing underneath. This kit inverts that. You author your
career once, at full depth, in Markdown story files. Everything you send is *rendered* from
that corpus, tailored to the specific role.

It's also how you stop forgetting your own career. Recall is triggered, not enumerated — you
remember the thing you did five years ago only when something adjacent jogs it. The interview
skill is built to do that jogging, and to write down what surfaces before it evaporates.

## Five things you'll do with it

Everything else in this README is detail under one of these.

**1. Build my corpus** — once, at the start.

```
/career-corpus:bootstrap
```

Paste in your résumé and anything else you have. You get the corpus structure, a `profile.md`,
and a ranked queue of the stories worth extracting first — so you're never staring at an empty
directory wondering where to begin.

**2. Capture this memory** — the ongoing work, and where the depth comes from.

```
/career-corpus:interview the hardest project I led at <company>
```

One memory per session, turned into a vetted story file with sources, ceilings and open gaps.
This is also where a real interview's misses land afterwards — the highest-quality material
the corpus will ever get.

**3. Work this application** — one role, end to end.

```
/career-corpus:apply <paste the posting, or its URL>
```

Opens a folder for the role, captures the posting before it 404s, and checks your corpus
against it *before* anything gets written. From there it hands off on its own: the résumé and
cover letter when you're ready to send (that's `/career-corpus:render` — it also works
standalone, for tailoring to a posting you're not tracking), the prep below when an interview
gets booked, and the outcome logged when it lands.

**4. Prep this interview** — booked, whether or not you applied through the kit.

```
/career-corpus:prep
```

A recruiter's call, a referral, an internal loop — there doesn't have to be an application
folder. You get an opener, a story bank mapped to what this employer actually hires for, the
probes they'll push on with defensible answers, and questions to ask them. Run it again the
day the interview ends — that's where intention 2's highest-quality material comes from.

**5. Maintain my corpus** — supervised, and rarer than the rest.

```
/career-corpus:compact
```

Prune the sediment interviews leave behind, and re-render a stale baseline rather than editing
it by hand. Both show you a diff with a reason per change before anything moves.

```
/career-corpus:verify
```

Fact-check the corpus's technical claims against the public record — release dates, feature
sets, how the mechanism really worked — the way a technical interviewer would, with citations.
You accept, amend, or reject each finding; nothing is patched silently.

**You don't have to remember the commands.** Each skill advertises when it applies, so "help me
capture what happened on the migration project" or "I have a loop next Tuesday" routes to the
right one. The slash commands are the explicit form, for when you want to be sure.

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
`/career-corpus:compact`, and `/career-corpus:verify`. If the install summary says
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
after that is one of the five intentions above.

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

## Beyond the résumé

Once the corpus exists, it's a sourced, dated record of your work — and a résumé is only the
most obvious thing to render from it. Each of these is just a prompt:

- **Self-reviews and 360s** — performance season, written from your own evidence instead of a
  blank box at 11pm. Map the corpus onto whatever competency model your company uses.
  `/career-corpus:render a self-review for this cycle, grouped by these competencies: <paste rubric>`
- **Promotion packets** — a promo doc is a rubric plus evidence, and the corpus is the evidence.
  The second half of this prompt is the valuable half.
  `/career-corpus:render a promotion packet for <level> against this rubric: <paste> — and list every line I have no evidence for`
- **Gap analysis before you apply** — find out what your corpus *can't* support yet, while
  there's still time to do something about it. This is step 2 of `apply`, so you get it for
  free; ask for it on its own when you're deciding whether a role is worth the evening.
  `/career-corpus:apply just the fit check for this posting — don't write anything yet: <paste>`
- **LinkedIn, bios, speaker blurbs** — the same facts at a different compression.
  `/career-corpus:render a LinkedIn About section and a 60-word conference speaker bio`
- **Post-interview capture** — the loop that compounds. Right after a real interview, record
  what you were asked and where you had nothing good to say.
  `/career-corpus:prep that interview is done — here's what they actually asked and where I fumbled`

The last one is worth doing even when you don't get the job. A question you couldn't answer is
the most precisely targeted gap you'll ever be handed — a real interviewer found it for you.

## Reference: the seven skills, in two lanes

Underneath the five intentions, the kit is two lanes. One builds the corpus. The other spends
it, one job application at a time.

**Lane 1 — build the corpus**

| Skill | When | What it does |
|---|---|---|
| **`/career-corpus:bootstrap`** | once, at the start | Reads your existing résumé/LinkedIn, sets up the corpus, and generates a prioritized queue of stories worth extracting. Gets you from empty to "start with this one." |
| **`/career-corpus:interview`** | whenever a memory surfaces | Interviews you about one memory and writes a vetted story file. Relentless, works in rounds of a few questions at a time, and it never lets a claim in that you can't defend. |
| **`/career-corpus:compact`** | maintenance | Prunes the sediment interviews leave behind — resolved gaps, dated back-and-forth — while guarding the lines that keep renders honest: your ceilings, rendering decisions, and rejected readings. Run it when a gap list has become more archive than queue. |
| **`/career-corpus:verify`** | maintenance | Reads story files the way a technical interviewer would and checks every publicly checkable technical claim against the public record, with citations. Findings arrive as a report — you accept, amend, or reject each one; nothing is patched silently, and nothing is corrected without a source. |

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
already has a build pipeline, `render` uses it and re-checks the page count.

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
