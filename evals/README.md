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

The one that earns its keep is **rule-reference resolution**. `compact` cites the
interview skill's rule 13; `render` cites its own rule 9. Insert a rule near the
top of either list and those pointers quietly aim at the wrong rule, with nothing
to notice. `playbook N` is checked the same way and matters more, because those
references cross a file boundary — `interview/SKILL.md` cites techniques that
live in `interview/REFERENCE.md`, and nothing else keeps the two renumbering in
step. It also checks each numbered list runs `1..N` with no gaps, that every
`/career-corpus:<skill>` mentioned exists, that relative links resolve, and that
the example corpus keeps its `FICTIONAL` banners, its `sources:` blocks, and its
`related:` targets.

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
  decorative.
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
