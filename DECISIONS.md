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
`application.md`'s events, which already end in an `outcome` — duplicating it into every
artifact's frontmatter is the rollup `[NO-ROLLUP]` forbids. Recorded because the next reader
of the fixture will notice the smell too.

**And none for *prepared and deliberately not sent*, settled the same way 2026-08-17.** That
one has a real failure behind it — an artifact left at `lifecycle: in-flight` in a thread that
reached `sent` reads as a defect to any check, and answering it in the log does nothing to stop
it recurring. It is still not a lifecycle value, because the state is a fact about the *send*
rather than about what may be done to the file, and it is expressible without a new word:
absence from `sent.artifacts` in a thread with a `sent` event — `[SENT-NAMES-WHAT-WENT]`.
Recording the fact beats naming the condition.

---

## The examples stay engineering — the kit reads as engineering-focused, and that is fine

**Settled 2026-08-15, by the maintainer.** The backlog carried this as an open positioning
call: the metadata promises a general career tool while `examples/` delivers a backend
engineering one, with a choice between narrowing the positioning and building a credible
second-domain corpus. The call: neither gets built. The kit itself has grown steadily more
technical — capability files are per-*technology*, `verify` checks claims against release
histories and changelogs, the harvest rule derives candidates from technology mentions — so
the examples being engineering is the product matching itself, not a gap. No second-domain
corpus, and no vocabulary-neutralising sweep of the skills.

What this entry does *not* settle: the README and plugin description still use general
wording ("your work history"). That stays as-is until it demonstrably disappoints someone —
tightening it is an afternoon of wording whenever wanted, and doing it preemptively chooses a
smaller audience for no observed cost.

**Reopens on:** audience expansion becoming real work someone intends to do — at which point
the old bar still applies: a second-domain example has to be convincing or it is worse than
none.

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

---

## A generated artifact is tracked at freeze, not fingerprinted

**Settled 2026-08-17.** `[PIN-NOT-ARCHIVE]` used to end at *offer `git add -f` as the user's
call, never as a default*, resting on the premise that a rendered file is rebuildable from
committed Markdown. That premise is false, and it was measured on the kit's own recommended
path rather than assumed: two `pandoc` DOCX builds of one unchanged file differ, and differ
only in a `dcterms:created` timestamp inside `docProps/core.xml`. Headless-Chrome PDF output
behaves the same way for the same reason. So the old default guaranteed eventual permanent loss
of the one artifact an application folder exists to preserve, while spending a frontmatter
field on a fingerprint of the thing being lost.

The rule now force-adds the sent bytes at the freeze and drops `sha256` where they are tracked;
the hash stays for bytes that genuinely cannot be — another machine, a portal that kept no
copy, a user who declines. The `.gitignore` is unchanged, deliberately: a path pattern cannot
tell a frozen artifact from a working one, and one that tried would commit every in-flight
re-render.

**Two things a revival must not re-derive.** `SOURCE_DATE_EPOCH=<n> pandoc …` *does* make the
DOCX byte-identical, verified — so a determinism escape hatch exists for that path and does not
change the conclusion, because reproducibility also requires the toolchain version to hold
still for as long as the application folder is worth keeping, and it will not. And the privacy
argument covers **inbound** binaries only: an employer's brief, a recruiter attachment, a scan.
An outbound PDF built from committed Markdown carries no privacy delta over the Markdown.

**Reopens on:** a sending format the kit generates deterministically end to end, toolchain
version included.
