# Decisions

Calls that are settled, kept so they stay settled. A decline that leaves no trace gets
re-proposed by the next pass that has the same idea, and a deliberate divergence with no
trace gets quietly reverted. Each entry is the problem, the call, and what would reopen it —
not the design history, which git keeps.

Buildable work lives in `BACKLOG.md`. Promote-pass state lives in `PROMOTE.md`.

---

## Pack staleness: record the inputs, don't build the checker

**Declined at the design stage 2026-08-12.** A rendered artifact is a snapshot of a corpus
that keeps moving, and nothing notices when the two diverge. The half that shipped in release
B: every artifact records its `corpus_pin` and full source list — `[PIN-THE-INPUTS]` — because
that is the half that cannot be added retroactively. The checker half was designed and thrown
away: it needs a digest and risk snapshot per source, stamped on every render forever as a
breaking format change, to serve a check one person runs across a handful of live artifacts.
One caught instance is an anecdote — the same recurrence gate `CLAUDE.md` applies to promotes.

Two conclusions a revival must not re-derive:

- **A commit range cannot be the comparison.** `jd.md` and `fit.md` are rendered before
  anything is committed, so a pin routinely points at a commit where the declared sources do
  not exist yet. Any real version compares per-source content digests, not `pin..HEAD`.
- **The cheap 90% needs no new contract.** *Which artifacts cite this file?* is a grep over
  artifact `sources:` frontmatter, run at the moment a story file is edited — the only moment
  memory doesn't already cover.

The baseline is the worse case: long-lived by design, never regenerated from scratch, the
artifact most likely to be sent — several paths write to it and none prune or re-verify. The
shipped mitigation is discipline (`render`'s selection rules and `[SELECTION-AS-SELECTION]`,
`interview`'s `[MARK-DONT-FIX]`), and discipline fails silently where `evals/` cannot see it —
which is the judge-layer entry below.

**Reopens on:** a second missed correction that reuse actually carried into a room, or enough
long-lived artifacts that the grep-based reverse lookup stops being enough.

---

## No fourth lifecycle state for a finished thread

**Settled 2026-08-12.** `baseline` / `in-flight` / `submitted` is a statement about what may
be *done to the file*, and on that reading a prep pack for a rejected application is correctly
`in-flight` forever: not frozen, not a baseline. "The thread is closed" is a property of
`application.md`'s log, which already ends in an `outcome` event — duplicating it into every
artifact's frontmatter is the rollup `[NO-ROLLUP]` forbids. Recorded because the next reader
of the fixture will notice the smell too.

---

## Judge layer for the evals — not until a failure demands it

**Deferred 2026-08-11; boundary reaffirmed 2026-08-12 by an external review.** Every assertion
in `evals/` is a regex, which covers the rules that forbid a *string* and none of the rules
that forbid a *judgement*: whether the thesis is drawn from the JD or lifted from the
baseline, whether the story selection is the strongest evidence or the first two files,
whether `fit.md` names a real gap or papers one over, whether the prose reads as the user
(`[THEIR-VOICE]` — currently unenforced), whether `interview` actually composes rounds from
`REFERENCE.md` rather than just resolving the pointer.

**Shape, when it's earned:** a rubric grader answering specific yes/no questions with the
corpus, the JD and the output in context — never a 1–10 score, which compresses away the
reason. Per-question, logged reason, majority across runs.

**Reopens on:** a repeated, user-visible failure the regex tier missed. Not before — a judge
is a second stochastic system evaluating the first, and a flaky judge is worse than no judge:
it teaches you to ignore red.

---

## Claim-diffing against a real corpus

**Deferred 2026-08-11.** Fixture corpora cannot reproduce selection pressure: with 30 stories,
*which four* a render picks is most of the quality, and nothing in `evals/` looks at that. The
real corpus can't simply be the target either — it moves while the skills are under test, and
it is private, so CI and contributors never see it.

**Shape, when it's earned:** the same prompt at two kit versions against a *pinned commit* of
a real corpus; extract the factual claims from each output and diff the claim sets — "v1.5
stopped selecting the batch-window story", not "600 words changed". The claim extractor is
itself a judge, so this reopens only after the judge layer does.

---

## Coverage report and a corpus doctor

**Deferred 2026-08-11.** A computed report — never a stored file, `[NO-ROLLUP]` — showing what
the corpus already covers: roles and years with no stories, résumé claims nothing decompresses,
interview dimensions with zero or one story, stories being spent across several live
applications at once, skills in `profile.md` no story cites. The same reader answers a second
question as the format evolves: absent files, dangling `related:` links, inbox files tracked by
accident, artifacts older than the corpus they drew on — which is the pack-staleness entry
above, folded in as one check rather than a separate feature.

⚠️ **If this is ever built, the tracked-`_inbox/` check exempts `examples/**/_inbox/` by path,
written into the check, not discovered by it.** The fixture inbox is committed on purpose —
`examples/` is not a corpus, the skills never read it, and a fixture with no unvetted material
in it cannot demonstrate the rule that unvetted material is never evidence. A doctor that
"fixes" it deletes the only trap tier 3 has for the recruiter-claim assertions.

**Reopens on:** corpora with dozens of stories, where "what should I work on?" stops being
answerable by reading `QUEUE.md`.

---

## Raw Markdown is not a sendable artifact

**Settled 2026-08-12.** Rendered artifacts carry provenance and lifecycle frontmatter — right
for the repository copy, wrong for an employer's eyes. The sending paths are PDF, DOCX, or
body text pasted into a form; the artifact-frontmatter template and the README both say so,
and a paste hands over the body alone. No export pipeline gets built for this — stripping a
frontmatter block is not a feature.

**Conversion is the user's, and the reason is not portability.** A résumé stylesheet is a
design opinion — fonts, margins, how a section rule looks — and the kit already refuses this
class of call in `[LENGTH-IS-THEIRS]`: a preference invented here is imposed on every user.
Shipping a converter means shipping a look. The README names `pandoc` as the shortest path
without shipping one, and `render` uses a pipeline that already exists in the user's repo.

**One mechanism worth not re-testing:** pandoc parses YAML frontmatter as a metadata block and,
absent `--standalone`, drops it — verified against both HTML-fragment and DOCX output. Any
pandoc-based conversion enforces the repository-only rule for free, so the instruction and the
tooling agree rather than the rule resting on someone remembering it.

**Reopens on:** a real sending path that consumes the Markdown file itself.
