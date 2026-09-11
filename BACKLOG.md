# Backlog

Things worth building that aren't built. Not a roadmap — a place ideas stop rotting in a chat
log. Newest at the bottom; delete rather than mark done.

This file holds only work that would actually be picked up, plus decisions still open.
Settled calls and deliberate declines live in `DECISIONS.md`; promote-pass state in
`PROMOTE.md`.

---

## Live mode for the application-lane evals

**Deferred 2026-08-12**, when the application fixture and tier 3 shipped. Tier 3 is offline
only, and offline mode has the same limit the trip-wires already admit to: **it pins the
example, it does not test the skills.** Every tier-3 assertion would still pass if `apply`'s
inbox rule were deleted tomorrow, because the committed fixture would not change.

Tier 2 solved this with a live mode that renders fresh from `examples/corpus/` and asserts
over the output. The analogue here is harder in one specific way: a live application run has
to *write a folder*, across three skills and several turns, from a starting state that is a JD
and an inbox file rather than a one-line prompt. The interesting assertions — did `prep`
promote a recruiter's claim, did `fit.md` name the gap or paper over it — are exactly the ones
that need the live run.

**Shape of a fix:** seed a temp dir with `examples/corpus/`, the fictional `jd.md` and the
recruiter note, run `prep` against it, and reuse the tier-3 trip-wire patterns unchanged. The
conformance half stays offline; only the trip-wire half needs a model. Keep it disposable and
optional until it shows a stable signal distinct from the fixture.

**Why deferred:** the fixture had to exist first, and the offline half is what stops the
example itself rotting, which is the failure that has actually happened in this repo.

---

## Open: is a corpus's own tooling part of the promote intake?

**Raised 2026-08-17, no call made.** `CLAUDE.md` fixes the promote intake at three files — the
lesson log, the corpus repo's instructions, the work backlog. A script sitting at a corpus
repo's root is in none of them, so a pass can read a *rule* about a checker while the checker
itself stays invisible. That is not hypothetical: the checker `tools/application_status.py`
ports from was in exactly that position, and it reached the kit because someone raised it by
hand rather than because a pass found it.

Two readings, and they are genuinely different bets:

1. **Working as intended.** The intake is rules; tooling is a different artifact and gets
   raised deliberately, which is what happened here and it worked.
2. **A blind spot.** The application lane is where several of these rules actually get
   *enforced*, so a pass that never sees the enforcement keeps porting rules while the local
   implementation diverges underneath them.

Widening the intake is not free: a script is long, it drags the corpus's own paths and
vocabulary into the session transcript, and **scoping the read is the privacy control** —
which is the argument `CLAUDE.md` makes for keeping the intake narrow in the first place. Any
version of this needs an answer to that, not just an extra row in the table.

**Reopens on:** a second piece of corpus tooling that a pass should have seen and didn't.

**Reopened 2026-09-03, still no call.** The second piece arrived: the corpus's status tool,
ported as `tools/corpus_status.py`, reached the kit the same way — raised by hand, as a brief
from a corpus session, not found by a pass. Two for two on reading 1 working; also two for two
on reading 2's mechanism, since both tools carried a design the rules alone did not state (a
closed grammar, a set difference). What made this one safe to read was that it was a *tool*,
not a corpus file: no personal material in it, and the brief said which commits to look at.
That may be the answer — tooling at the repo root is intake, `corpus/` never is — but one more
instance before writing it into `CLAUDE.md`.

**Third instance, 2026-09-07, and it cuts the other way.** A corpus session raised two PDF
text-layer defects and named the build script and commits to read. This pass **declined the
read** and ported from the brief alone, because the brief already carried the tell, the move
and the traps in generic form — and the fixes were then reproduced from scratch here, on a
throwaway page, which is what actually justified the rule. So the score is three for three on
reading 1, but the mechanism argument for reading 2 weakened: what the pass needed was not the
corpus's implementation but a *reproduction*, and a reproduction can be built in the kit. That
suggests a narrower answer than "root tooling is intake" — **a brief that states the mechanism
is enough when the kit can rebuild the defect**, and the read is the fallback for when it
cannot. Still no call; this is the first instance where declining the read cost nothing.

**Fourth instance, 2026-09-10, a skill rather than a tool.** The corpus grew a local skill
(`.claude/skills/benchmark/`) and raised it by hand with a brief naming the commits and the
gaps. Same position as the tools — in none of the three intake paths, reached the kit only
because someone pointed — and the read was safe for the same reason: no corpus material in it.
Four for four on reading 1. The brief again carried enough that the read served as source,
not as diagnosis. If a fifth arrives, write the narrow answer into `CLAUDE.md`: anything under
the corpus repo's `.claude/` or `tools/` is intake when a brief names it; `corpus/` never is.


## The eval suite's private parsers, and the vocabulary's four copies

**Deferred 2026-08-17**, out of the review pass over 1.24.0–1.30.5. Two findings from that
pass were confirmed and deliberately not fixed inline, because both are consolidation work
rather than a patch:

- `evals/application_checks.py` carries its own frontmatter/event parsers, and they already
  disagree with `tools/appthread.py` at the edges (comment stripping, lifecycle capture —
  both of which just produced real defects in the tools). Green evals therefore do not attest
  that the fixture is *tool*-parseable, only that it satisfies the evals' private grammar.
  The fix is the evals importing `appthread`, or an assertion that the two parsers agree on
  the fixture; either way one grammar, stated once.
- The nine-event vocabulary exists in four unsynced copies (appthread, the application
  template, apply's SKILL.md, the examples README) and nothing pins them to
  `appthread.EVENTS`. A tenth event added to one copy drifts silently.

Same family: `[NOT-EVERY-DOUBT-IS-A-BLOCKER]` and `[CONSTRAINT-HAS-ONE-HOME]` are each stated
near-verbatim in three SKILL.md files — a CLAUDE.md-consolidate-pass candidate, not a defect.

**Added 2026-09-03.** A third copy of a different predicate: what counts as a corpus file and
where `_inbox/` stops is now defined in `tools/corpus_status.py` and, four times over, in
`tools/corpus_doctor.py`. They agree today only because 1.31.1 aligned them by hand after the
status tool shipped counting `_inbox/` checkboxes as corpus gaps. One `corpus_files` helper
both import is the fix; same shape as the `appthread` item above.

**Reopens on:** the next change to the event vocabulary or to either parser.

---

## A user-owned career framework that shadows the shipped ladder

**Designed 2026-09-11, not built.** `ladder`'s calibration is baked into the kit: the level
table in its `SKILL.md` and three role files. That costs twice. It may not be the bar the user
is actually graded against, and it covers three roles. The provisional-role path only half
covers the second, because it offers to "save a new role file" and names no place to save it.
The only place it could mean is the plugin cache, which the next update overwrites. The payoff
is a kit that grades against the framework the user's own promotion committee and review
cycle use.

**Split method from calibration.** The method stays in the kit and cannot be overridden. That
means both modes' hard rules, the five tells used as probes, `[VETTED-ONLY]`, capture versus
work, range and floor, and citations. Calibration becomes the user's: the ordered levels and
what each one owns (scope, reach, horizon, success), the competencies being graded, and each
role's craft (dimensions, artifacts, overclaim, blind spots). A framework can replace
calibration. Nothing in it can switch off a rule. A framework that says "grade on title" still
loses to `[LEVEL-FROM-EVIDENCE]`.

**It lives at `ladder/` in the corpus repo root**, beside `corpus/`, `benchmarks/` and
`applications/`. It does not go under `corpus/`, because `tools/corpus_status.py:57` counts
every file there as a story unless an allowlist excludes it. Verify would also try to
fact-check it. And it is not evidence about the user: it is an employer's bar, the same kind
of thing as a JD.

**Resolution checks the corpus first and falls back to the kit.** Role matching works as it
does today (aliases, parenthesised spans stripped, longest match wins). It searches
`ladder/roles/` before the kit's `roles/`, and a corpus file with a matching alias shadows the
kit's file completely, with no merge. If `ladder/levels.md` exists, it replaces the
calibration table. Every output records which source resolved. `role_file:` in both templates
becomes either `ladder/roles/<file>.md` or `kit:roles/<file>.md@<version>`.

**Seed by fork, not by copying everything.** Bootstrap should not copy the whole set into
every corpus. An unedited copy is a snapshot that stops receiving kit fixes: 86048fd's product
dimensions would never reach a corpus seeded the day before. Bootstrap's own rule also says an
empty file is an invitation to fill it. There are three paths instead:

1. **Default.** Nothing is copied and the kit fallback just works.
2. **Fork.** Copy one kit file into `ladder/` with `forked_from: <file>@<kit version>`. A later
   session can then diff the kit's newer copy against the fork and offer the changes. Deleting
   the fork puts the user back on the kit's version.
3. **Import.** Distil a company framework the user drops into `_inbox/` into the schema, with
   the user confirming each level. The source stays in `_inbox/`, which is gitignored. Company
   ladders are often confidential, and they carry the same exposure as the rest of the corpus.

**The schema** extends `roles/README.md` with a levels file. It lists the levels in order,
each with scope, reach, horizon, success and an optional `industry_equivalent:`, plus a
competency list when the framework's pillars differ from the kit's five. The
`industry_equivalent:` field is what keeps the exemplar's "one up" and outbound rendering
working when a framework uses opaque level names.

**Conflicts to settle when building it:**

- **Level names.** `ladder` says to name levels in industry terms, never in an employer's grade
  codes, and `roles/README.md` bans employer-specific vocabulary. A company framework is
  employer vocabulary by definition. Proposed restatement: internal outputs (an assessment, a
  self-review) may use the framework's level names. Outbound outputs (render, apply, an
  exemplar) use the industry equivalent. The README ban then applies only to files the kit
  ships.
- **Stories from an earlier employer.** Which ladder grades them? Proposed: one active
  framework carries the verdict. Stories from earlier employers are graded on its
  scope/reach/horizon axes and never on its employer-specific competencies. That is the same
  move as `[RECENT-ROLE-CARRIES]` grading an old story in its own year.
- **One framework per company.** Start with a single framework. `ladder/<company>/` is the
  extension if keeping an old employer's ladder turns out to matter.

**Touches:** `ladder`'s SKILL.md (resolution, the split, the naming rule, the provisional save
target), `roles/README.md`, both templates, and bootstrap, which gets one offer (default,
fork or import) and still does not create `ladder/` unless one is chosen. Render and prep read
the framework for a promotion packet or an internal interview and apply the outbound naming
rule. Verify and compact already read only `corpus/`, so they need a confirmation, not a
change. `corpus_doctor` gets a schema check and fork-drift reporting. The evals get a
fictional framework in `examples/` with cases for shadowing, fork drift, and a framework that
tries to disable a hard rule. The README needs updating too. This is a minor version bump.

---

## Self-review for a review cycle

**Depends on the framework item above.** It is the payoff the framework exists for. It is
shaped like render: a document other people read, built from vetted claims only. It is scoped
to a date window, organised by the framework's competencies, and carries the assessment's floor
and delta. Peer feedback in a 360 is third-party raw inbound. It goes in `_inbox/`, and none
of it becomes a claim until the user states it. That is the same fence as
`[BENCHMARK-IS-A-NOD]`. Keep it out of the framework change: it is a new output with its own
rules, not a resolution change.
