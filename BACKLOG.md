# Backlog

Things worth building that aren't built. Not a roadmap — a place ideas stop rotting in a chat
log. Newest at the bottom; delete rather than mark done.

---

## Pack staleness detection

**Deferred 2026-08-10.** A rendered artifact is a snapshot of a corpus that keeps moving, and
nothing currently notices when the two diverge.

**The concrete case that raised it:** a résumé claim was withdrawn from a corpus during an
interview session, and an interview prep pack written weeks earlier still carried it. It was
caught by hand, because someone happened to be editing the file that day. Nothing would have
caught it otherwise.

**The shape of a fix**, roughly:

- Rendered packs record which corpus files and which specific claims each section drew on,
  probably in frontmatter.
- Re-running `prep` (or a `--check` mode) reports what changed underneath: withdrawn claims,
  numbers whose ceilings moved, stories that gained a `RENDERING DECISION` since.
- Loudest signal reserved for **withdrawn or shrunk** claims, since those are the ones that
  turn into a false statement in a room rather than merely a stale one.

**Why it's deferred rather than dropped:** regenerating a pack from scratch before each
interview is cheap and mostly solves it. The failure only bites when a pack is reused for a
later round, or when several applications are live at once and a correction lands in the
middle. That's a real scenario, just not the common one.

**Applies to `render` output too**, not only `prep` — a tailored résumé sitting in
`applications/` has exactly the same problem.

---

## Example application folder

**Deferred 2026-08-10**, when `apply` shipped. `examples/` shows corpus in and artifacts out,
but not the folder an application actually accumulates — the JD, the fit check, the dated log,
the inbound material. That folder is where most of the new skill's shape lives, and reading it
would teach it faster than the SKILL.md does.

**Why deferred:** it means fabricating a job posting *and* a recruiter email, in a repo whose
first rule is "never invent". The existing example corpus is bounded by a per-file FICTIONAL
banner and its own tree; a fake posting attributed to a fake company is a step further, and a
fake recruiter email is a step further again. Worth doing carefully, not quickly.

**If built:** the `fit.md` is the file to get right — specifically a requirement the example
corpus genuinely cannot back, ending in "don't apply yet". A fit check where everything lines
up teaches the opposite of the point.

**Now also blocking evals** — `evals/` has no cases for `apply` or `prep` because there's no
application fixture to run them against.

---

## Judge layer for the evals

**Deferred 2026-08-11**, when `evals/` shipped. Every assertion in there is a regex, which
covers the rules that forbid a *string* and none of the rules that forbid a *judgement*.

Untested today, and not testable by grep:

- Is the thesis drawn from the JD, or lifted from the baseline? (`render`'s central claim, and
  the part its own SKILL.md admits is least battle-tested.)
- Is the story *selection* the strongest evidence for this role, or just the first two files?
- Does `fit.md` name a real gap, or paper one over with an adjacent story?
- Does the prose read as the user, or as a model? (Rule 10 — currently unenforced.)

**Shape of a fix:** a rubric grader that answers specific yes/no questions with the corpus,
the JD and the output in context — never a 1–10 score, which compresses away the reason. Run
per-question, log the reason, require a majority across runs.

**Why deferred:** the grep tier catches the failures that have actually happened, costs
nothing, and runs on every push. A judge is a second stochastic system evaluating the first,
and a flaky judge is worse than no judge — it teaches you to ignore red.

---

## Tier 3 — claim-diffing against a real corpus

**Deferred 2026-08-11.** The fixture corpus has four stories. A real one has dozens, and
selection pressure is the thing fixtures can't reproduce: with 30 stories, *which four* a
render picks is most of the quality, and no assertion in `evals/` looks at that.

**Why not just run the evals against the real corpus:** it moves while the skills that write
to it are under test, so a changed render can't be attributed to the change. And it's private,
so CI and contributors can never see it.

**Shape of a fix:** run the same prompt at two kit versions against a *pinned commit* of a
real corpus, extract the set of factual claims from each output, and diff the claim sets.
Surfaces "v1.5 stopped selecting the batch-window story" instead of "600 words changed".
The claim extractor is the hard part and is itself a judge — see above.

---

## Privacy defaults, not privacy warnings

**Deferred 2026-08-11**, from an external review. Every skill says the corpus and the
application folder are sensitive. Nothing in the kit acts on it. A private remote is access
control, and the two things most likely to hurt — an employer's confidential take-home, and a
recruiter thread with other people's names in it — go straight into git history, where
deleting them later doesn't delete them.

Three separable pieces, cheapest first:

- **`bootstrap` writes a corpus `.gitignore`.** It already creates `corpus/`; it can create
  the ignore file in the same breath. Ignore `_inbox/` and `applications/**/_inbox/` by
  default, and make tracking raw inbound the opt-in rather than the opt-out. This is the one
  worth doing on its own even if the rest never happens.
- **`apply` prefers a reference over a copy** for confidential employer material — a path or
  a link with a classification and a delete-by date, rather than the brief itself in the repo.
- **A short `PRIVACY.md`** on what belongs in the corpus, what never does, and what git
  history does and doesn't let you take back.

**And one honesty gap the warnings currently paper over:** "keep it in a private repo" reads
as "it never leaves your machine", which is false the moment a hosted model reads a story
file. Say so plainly somewhere the user meets early.

**Why deferred rather than blocking:** a `.gitignore` the user didn't ask for is the kit
writing policy into their repo, and the classification/retention machinery is a system where
today there's a sentence. Ship the ignore file first and see whether anything else is wanted.

---

## Split the interview playbook out of the skill

**Deferred 2026-08-11.** `interview/SKILL.md` is 343 lines and does four jobs: invariant
rules, round mechanics, the storage schema, and a nine-part interviewing playbook. Only the
playbook is *technique* — the rest is contract. It loads on every invocation regardless.

`render` already solved this: hard rules in `SKILL.md`, artifact specifics in `REFERENCE.md`.
Same move — leave source rules, round/frontier mechanics, the file-update contract, and
stop/resume in the skill; move the playbook to `interview/REFERENCE.md` and point at it from
the step that actually needs it.

**Why deferred:** it's a refactor of the most load-bearing file in the kit, and the live
trip-wires that would catch a regression only cover `render`. Do it after there's something
watching.

**Not to be confused with** the broader "extract shared policy into `skills/_shared/`"
suggestion, which is a different and worse idea — see the drift-check entry below for why.

---

## A drift check for duplicated policy

**Deferred 2026-08-11.** The same blocks appear across skills nearly verbatim: the Lessons
section, the `_inbox/` rule, the no-private-names rule, the sourcing rule. An external review
read that as duplication to be extracted into shared policy files that each skill reads.

**That refactor is the wrong fix.** A skill loads its own `SKILL.md`. A rule living in
`_shared/TRUST.md` is in force only if the model reads the file, and a rule you *hope* got
loaded is not a rule. Skills fire independently and must each stand alone; the repetition is
the design.

**The risk it names is still real, though.** It has already bitten once — `apply` rule 3 and
`render` rule 1 both state the applications-are-not-a-source rule, and they state it
differently enough that one of them contradicts its own workflow.

**Shape of a fix:** mark the canonical copy of each repeated block, and add a static check
that every other copy matches it. Drift becomes a red CI run instead of a slow divergence.
Tier 1 already parses every skill file, so this is an assertion, not a new harness.

**Related and smaller:** rule cross-references are numbers (`interview`'s rule 13). The
checker proves they *resolve*; it can't prove they resolve to the same rule they did before
someone inserted one above it. Stable names (`CLAIM-SOURCE`, `INBOX-NOT-EVIDENCE`) survive
reordering and read better at the call site. Worth doing while touching the same files.

---

## Define what "vetted" means

**Deferred 2026-08-11.** The story template's provenance taxonomy conflates two different
properties. `facts_vetted` is defined as *their own words — résumé, letters, or interview*,
and `facts_unvetted` as *stated once, no independent source*. So "vetted" currently means
**the user said it and we wrote down where**, not **we checked it**. Every rule downstream —
what may render, what a probe is, what a ceiling protects — hangs on that word, and the word
carries the wrong implication to anyone reading it fresh.

The kit's actual position is defensible and worth stating outright: *the corpus vouches for
provenance, not for truth. It knows who claimed a thing and when. That's what makes a claim
defensible under a follow-up question — not that it was independently verified.*

**Shape of a fix:** one paragraph in the template and one in `interview`, defining the term
rather than adding fields. Splitting it into `confirmed_by_user` / `independently_verified` /
`renderable` is more taxonomy than the material supports.

**One adjacent rule worth revisiting at the same time:** `facts_disputed` blocks *both*
versions until settled. Sometimes the floor is safe — if one source says doubled and the
other tripled, "more than doubled" is true under either. Decide whether the safe intersection
may render with an explicit ceiling, or whether the whole fact stays blocked. Either is
fine; right now the template says one thing and nobody has thought about the other.

---

## Coverage report, and a doctor for the corpus

**Deferred 2026-08-11.** The kit ranks what to extract *next* by interview value, but never
shows the user what the corpus already covers. "What should I work on?" is answerable today
only by reading `QUEUE.md` and remembering everything not on it.

A computed report — never a stored file; see `apply` rule 6 — could show roles and years with
no stories, résumé claims with nothing decompressing them, interview dimensions with zero or
one story, stories being spent across several live applications at once, and skills in
`profile.md` no story cites.

The same reader answers a second question as the format evolves: missing files, dangling
`related:` links, inbox files that got tracked by accident, application artifacts older than
the corpus they drew on. That last one **is** the pack-staleness entry at the top of this
file — if a doctor gets built, staleness is a check inside it rather than a separate feature.

**Why deferred:** it's the first thing here that reads the user's whole corpus and renders a
judgement about it, which is a bigger surface than any current skill. And half its value
lands only once there are dozens of stories.

---

## The examples are all engineering

**Deferred 2026-08-11.** The fixture corpus is two backend companies. The playbook reaches
for services, incidents, on-call, migrations, PRs and dashboards when it wants a concrete
example. The plugin keywords say `career`.

The method generalises — decisions, opposition, cost, and a number are not engineering
concepts. The *language* doesn't. Someone in design, sales, research or people management
reads the examples and correctly concludes this wasn't built for them.

**Two honest options, and they're different products:** add a second short example corpus in
another discipline and neutralise the playbook's default vocabulary, or narrow the positioning
to engineering and stop implying otherwise.

**Why deferred:** a second example corpus is the same fabrication cost as the application
fixture above, and that one is already blocking evals. Do them in that order.
