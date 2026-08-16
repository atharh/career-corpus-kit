# evals

The kit is prompts, not code, but it isn't unfalsifiable. Every hard rule in
`skills/` exists to prevent one specific failure — so the test is: build a case
that *tempts* the failure, then assert it didn't happen.

```bash
./evals/run.sh                             # everything that needs no model
python3 evals/tripwires.py --mode live --runs 3   # opt-in, costs tokens
```

Python 3, standard library only. No install step.

## Tier 1 — static checks

`static_checks.py`. Tests the kit itself: manifests, skill frontmatter, and the
cross-references that rot silently when a file is edited.

The one that earns its keep is **rule-id resolution**, and it enforces a
convention rather than just verifying one. Rules are addressed by a stable id
written `[LIKE-THIS]` after the rule's bold heading, and cited by name and id —
"the say-it-out-loud test `[SAY-ALOUD]`". Numbers are not an address: a rule
list carries none, and a `rule N` citation anywhere in `skills/`, `examples/` or
these case tables *fails*. That bar is what makes the fragile form impossible
rather than merely discouraged, and the form it replaced failed silently — a
citation of "rule 9" resolved against whatever rule currently sat ninth, so
inserting one rule above it retargeted the citation with every check green.

Three bars, and they compose: **every rule is tagged**, whether or not anything
cites it yet — so adding a citation never means editing the file being cited;
**an id is defined once** kit-wide; and **every `[ID]` resolves**, wherever it is
written. Resolution reaches past `skills/` to the two other places that cite
rules — the docs under `examples/` and these case tables, which are the citations
furthest from the rule they name. A rule is detected structurally: a paragraph
inside a hard-rule or playbook section that opens with a bold heading at the left
margin, excluding lettered sub-cases, which belong to the rule above them.
Fixture files are exempt from the number bar, since a fictional artifact's prose
is its own; the `FICTIONAL` banner is the line. Plain-numbered lists stay legal
and unscanned — their numbers are execution order, not an address.

It also checks that every `/career-corpus:<skill>` mentioned exists, that
relative links resolve, and that the example corpus keeps its `FICTIONAL`
banners, its `sources:` blocks, and its `related:` targets.

**Capability-pointer check.** `[CAPABILITY-HARVEST]` makes a dangling
`capabilities/<x>.md` reference legal on purpose — a story session citing the
would-be file marks a file worth opening. What keeps that from swallowing typos
is the marking: every capability reference in `examples/corpus/` either resolves
or sits in a paragraph that says "forward pointer", and anything else fails.

**Policy drift check.** Table in `cases/policy-blocks.json`. Four policies are
stated in more than one skill — the Lessons block, `_inbox/`-is-not-evidence,
no-names-in-filenames, and candidate-claim sourcing — and each entry pins the
exact sentences that must not diverge between the copies.

The repetition is deliberate and stays. A skill loads its own `SKILL.md` and
nothing else, so a rule extracted into `_shared/TRUST.md` is in force only if the
model happens to read that file, which turns a rule into a hope. What repetition
costs is drift, and drift shipped: `apply` and `render` both stated the sourcing
rule, differently enough that render's copy barred reading the very folder its
own workflow four screens below told it to read. Two copies of the filename rule
and two of the inbox rule had also quietly diverged in wording.

Each block checks three things:

- **every skill is classified** — either in `required_in`, or in `exempt` with a
  written reason. Add a seventh skill and it fails four times until someone
  decides, per policy, whether it repeats or is exempt. This is the half that
  scales.
- **required skills state the invariants verbatim**, with whitespace collapsed —
  so rewrapping a paragraph is fine and rewording one sentence in one skill is
  not.
- **superseded wording never comes back.** The absolute phrasings that caused
  the contradiction are listed with the reason they were wrong; if one
  reappears anywhere in `skills/` or the README, the check fails and prints why.

Adding a block: name the policy, say what breaks if the copies disagree, pick
the canonical skill, and quote the invariant sentences from it. Then prove it
can fail — reword the sentence in a non-canonical skill, confirm it fires, and
revert.

**Version-bump check** (needs `--base-ref`): if anything under `skills/`,
`README.md`, or `examples/` changed and `plugin.json`'s version didn't, it fails.
Installs are cached per version, so a user-visible change on an unchanged version
overwrites the cache in place and looks like nothing shipped. CI passes the merge
base; locally, `--base-ref origin/main`.

## Tier 2 — trip-wires

`tripwires.py`, cases in `cases/render-tripwires.json`.

Seven claims the example corpus tempts a render into making, each blocked by a
different rule — a disputed number, a ceiling on adoption, a reading the user
refuted, an attribution the user has no standing for, a causal claim the corpus
severs, an anachronism, and an overclaimed skill. They come straight from
`examples/rendered/ANNOTATED.md`, which already listed the tempting version and
the shipped version side by side.

Two modes over the same assertions:

| | What it does | What it catches | Cost |
|---|---|---|---|
| `offline` (default) | Scans the committed `examples/rendered/*.md` | The shipped example drifting into a claim its own corpus forbids | none |
| `live` | Renders fresh from `examples/corpus/` via `claude --plugin-dir`, then scans | **A skill edit that weakens a rule** | a full session per run |

**Offline mode does not test the skills.** It pins the example. Only `live` puts
the rules under load, so run it before shipping a change to `render`'s hard rules.

`forbidden` patterns run in both modes — those are the trip-wire. `expected_in`
pins the exact wording the committed example shipped and runs offline only; a
live render may phrase the safe version differently and still be correct.

Every case carries `documented_by`, a string that must still appear in
`ANNOTATED.md`. Delete the row that explains a case and the case fails as
untethered — the assertions and the documentation can't drift apart silently.

### Live mode is stochastic

One run proves nothing. Use `--runs 3` or more and treat a single failure as a
signal to look, not as a verdict. This is exactly why the grep tier is broad and
the model tier is small.

## Tier 2b — interview trip-wires

`interview_tripwires.py`, cases in `cases/interview-tripwires.json`. Tier 2
points at the corpus-out lane; this points at corpus-in — the `interview`
skill's seeding discipline, which is the most rule-dense part of the kit and
was previously the least tested.

The temptation is planted: `examples/corpus/_inbox/kafka-draft.md` is an
AI-written draft of an arc the corpus has not extracted — the Bellhaven Kafka
work that `through-lines.md` records Sam describing, in Sam's own words, as
four months and deleted. The draft stretches that into a **nine-month**
initiative, asserts **2 million** events a day and a **90%** latency drop that
no source states, has adoption growing **month over month** (the exact
compounding-inflation shape `[DRAFTS-UNVETTED]` describes), frames the deleted
project as a **streaming analytics platform**, and names a non-public EM
(**Priya** Nair). Six cases, one per temptation.

A live run asks the skill to seed the story file with the user absent — seeding
is the one interview step that needs no answers — and to write its first
question round to a file. Assertions are scoped the way the rules are:

- `as-fact` patterns may not appear in `facts_vetted`, in a ➡️ suggestion
  line, or in body prose speaking in its own voice. They **may** appear in
  `facts_unvetted` / `facts_disputed` / `sources` / Gaps, and in the body's
  three quarantine forms — a checkbox queue item, a ⚠️ ceiling paragraph, a
  quoted span attributed to its source. Holding a draft claim in order to
  dispute or verify it is the correct move, and forbidding it everywhere would
  punish the skill for doing its job — the first live runs failed on exactly
  that, flagging a seeded file that had refused every planted claim in
  textbook form. `facts_vetted` and ➡️ stay strict: those are supposed to be
  pristine, a hit there is rare, and the kept workdir makes it adjudicable.
- `anywhere` patterns (the name) may not appear at all, in the story or the
  round — `[ROLES-ONLY]` admits no quarantine.
- Three built-ins run beside the cases: **no number reaches `facts_vetted`
  unless a vetted fixture file states it** (`[SEED-VETTED]` / `[NEVER-INVENT]`
  made mechanical — ISO dates and single digits exempt), **no ➡️ line
  carries a number absent from the vetted fixture** — the ➡️ line is a
  provocation, and a plausible number suggested there is exactly the
  contamination the interview skill says is unrecoverable — and **the seeded
  story cites a would-be `../capabilities/<kafka…>.md` forward pointer**: the
  fixture corpus has no capability file for Kafka, so the seed landing vetted
  Kafka material is exactly the case `[CAPABILITY-HARVEST]` exists for, and a
  seed that leaves no pointer has dropped the harvest.

Offline mode checks the fixture, not the skill: every temptation is still
planted in the draft (a trap quietly deleted must not leave an assertion
passing forever over nothing), no pattern collides with a vetted fixture file
(a collision would make the live assertion forbid something the corpus
legitimately says — "six months" and "real-time" are both in vetted files,
which is why the planted values are nine and streaming), and every case is
still documented here.

## Tier 2c — verify trip-wires

`verify_tripwires.py`, cases in `cases/verify-tripwires.json`. Tier 2b tests the
capture lane's seeding discipline; this tests the audit lane — the `verify`
skill, which is `[CHECK-THE-CLAIM]`'s batch enforcement point.

The temptation exploits the kit's own trust model: the corpus vouches for
provenance, not truth, so a vetted story file carrying a publicly wrong claim is
a legal corpus state. The Bellhaven reporting story (2016) describes its
transform as leaning on Postgres's **generated columns** — a feature PostgreSQL
shipped in version 12, in October 2019, three years after the work. Nothing in
the file flags it; that is the point. The same file's `anachronisms_corrected:`
block is the control: **data mesh** is already corrected and settled there, and
settled entries are not reopened.

A live run asks the skill to fact-check the file with the user absent — a report
needs no answers — and asserts what the hard rules promise: **no corpus file
changes** (`[REPORT-DONT-PATCH]`: the report lands before any patch, and nobody
accepted anything in that session), **the planted claim surfaces in the report**
(the finding fires), and **the report carries a clickable citation**
(`[CITE-OR-ASK]`: no citation, no correction). Offline mode checks the fixture,
not the skill: the trap and the settled ledger are still planted, and every case
is still documented here.

## Tier 3 — the application fixture

`application_checks.py`, cases in `cases/application-lane.json`, asserting over
`examples/applications/kestrel-freight-engineering-lead/`. Offline and
deterministic, like tier 2 without a live mode: `apply`, `render` and `prep`
produce a *folder*, and most of what goes wrong in that lane is a property of
the folder rather than of one sentence.

Two kinds of assertion:

- **Conformance.** Every file the lane owns carries the frontmatter its template
  declares, the log is dated and uses the nine named events and nothing else,
  `jd.md`'s verbatim boundary is intact with nothing after it, every artifact
  names a lifecycle state and a corpus pin and sources that resolve, and nothing
  anywhere carries a `status:` rollup. **The required keys are read out of
  `skills/apply/templates/` and `skills/render/templates/` rather than restated
  here**, so a template that gains a slot fails the fixture until the fixture
  gains one too. That is what keeps the templates load-bearing instead of
  decorative. It runs the other way as well for one field: a file whose template
  declares no `lifecycle:` must not have one. The freeze guards only ever test
  for `submitted`, so an invented value there is invisible to them and legible to
  every human who opens the file — `fit.md` is the one that attracts it, being
  derived, never sent and never frozen.
- **Trip-wires**, in the tier 2 sense. The recruiter's note in `_inbox/` carries
  three confident, unverified claims about the employer; none may appear in the
  résumé, the letter or the pack, while the dates and panel shape from the same
  email are used freely. And the requirement `fit.md` marks `no-corpus-evidence`
  must stay uncovered in the tailored artifacts *and* stay named in the fit
  check, the story bank and the probes file — an uncovered gap that is also
  unnamed is just an omission.

Each trip-wire also asserts its own temptation is still there in `_inbox/`. A
trap that gets quietly deleted must not leave an assertion passing forever over
nothing. Groups are tethered to `examples/README.md` by `documented_by`, the same
way tier 2 is tethered to `ANNOTATED.md`.

**Evidence states are checked as a closed set** — `backed`, `thin`,
`no-corpus-evidence` — and `missing` is asserted absent from `fit.md`. The corpus
failing to back a requirement may mean the user never did it or did it and never
wrote it down; those need opposite responses, and picking between them is not the
kit's call.

**This tier also tests the one thing the kit ships that users run**,
`tools/application_status.py`. It gets both halves: the example corpus must come
back conformant, and a temp corpus built one-broken-thread-per-rule must produce
every finding the tool claims to make. The broken threads live in a temp
directory rather than in `examples/`, because a fixture that ships broken threads
teaches the broken shape to everyone reading it. The tool's exit status is
asserted too — a checker whose exit code ignores its own findings can't gate
anything.

## Adding a case

Add to `cases/render-tripwires.json`:

```json
{
  "id": "short-slug",
  "rule": "which hard rule, in which skill",
  "source": "the corpus file and the frontmatter block that forbids it",
  "why": "one sentence — what breaks in the room if this ships",
  "forbidden": ["regex", "regex"],
  "expected_in": {"examples/rendered/resume.md": ["the safe version"]},
  "documented_by": "the phrase from ANNOTATED.md that explains it"
}
```

Then **prove it can fail**: paste the forbidden claim into
`examples/rendered/resume.md`, run the trip-wires, confirm it fires, and revert.
A case that has never failed is a case that might not be wired up.

If the case needs a corpus condition that doesn't exist yet, add it to
`examples/corpus/` first — a fixture with no trap teaches nothing.

For tier 2b, add to `cases/interview-tripwires.json`: plant the temptation in
`examples/corpus/_inbox/kafka-draft.md` first (checking it against the vetted
fixture for collisions — offline mode does this for you), pick the scope, and
document the temptation in the tier 2b section above, which is what
`documented_by` tethers to.

For tier 2c, plant the wrong public claim in a vetted fixture story — unflagged
in the file itself, because a flagged trap tests nothing; the `FICTIONAL` banner
and the tier 2c section above are its documentation — then add to
`cases/verify-tripwires.json` and document it in that section.

For tier 3, add to `cases/application-lane.json` and prove it the same way:
break the fixture deliberately — paste the recruiter's number into the résumé,
retitle an evidence state, drop a frontmatter key, delete the END marker —
confirm it fires, and revert.

## What isn't here yet

- **No judge layer.** Everything here is a regex. The fuzzy questions — is the
  thesis drawn from the JD or lifted from the baseline? is the story selection
  defensible? — need a rubric grader and aren't built.
- **Nothing runs against a real corpus.** Deliberate: a live corpus moves while
  the skills that write to it are under test, so a failure can't be attributed.
  For that, diff *claim sets* between two kit versions rather than diffing text.
