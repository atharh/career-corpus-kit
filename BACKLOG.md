# Backlog

Things worth building that aren't built. Not a roadmap — a place ideas stop rotting in a chat
log. Newest at the bottom; delete rather than mark done.

The one exception is *Promote passes* at the bottom, which is state rather than an idea, and
is kept rather than deleted.

---

## Pack staleness detection

**Raised 2026-08-10. Declined at the design stage 2026-08-12 — parked, not dropped.**

A rendered artifact is a snapshot of a corpus that keeps moving, and nothing notices when the
two diverge. **The case that raised it:** a claim was withdrawn from a corpus during an
interview session, and a prep pack written weeks earlier still carried it. Caught by hand,
because someone happened to be editing that file the same day.

**What shipped instead, in release B:** each artifact records its `corpus_pin` and its full
source list. That is the half that cannot be added retroactively, and it earns its place as a
record of what a render read whether or not anything ever consumes it — `apply` rule 6.

**Why the consuming half was declined.** A full design was written and thrown away. The checker
is small; the contract it needs is not — a digest and a risk snapshot per source, stamped on
every render forever, as a breaking change to the artifact format, to serve a check one person
runs across a handful of live artifacts. It also aims at the wrong lane. An application in
flight is the case already in the user's head: the folder was opened, the render was just made,
`application.md` says what came from where, and the fix is a manual edit the design forbids the
tool from making anyway. One caught instance is an anecdote — the same recurrence gate
`CLAUDE.md` applies to promotes.

**Two conclusions worth keeping, so a later pass doesn't re-derive them:**

- **A commit range cannot be the comparison.** `jd.md` and `fit.md` are written and rendered
  from before anything is committed, so a pin routinely points at a commit where the declared
  sources do not exist yet — and the commit that lands the artifact lands its sources with it.
  Any real version compares per-source content digests, not `pin..HEAD`.
- **The cheap 90% needs no new contract.** `sources:` already holds paths. *Which artifacts
  cite this file?* is a grep over artifact frontmatter, answered at the moment a story file is
  edited — which is the only moment memory doesn't already cover.

**What would revive it:** a second missed correction, one that reuse actually carried into a
room; or enough long-lived artifacts accumulating that the reverse lookup above stops being
enough.

### The baseline remains the worse case

Distinct from detection, and still true. A baseline is long-lived by design, nothing
regenerates it from scratch, and it is the artifact most likely to be sent. Two failures follow
from one asymmetry — **several paths write to an artifact and none prune or re-verify it**:
a `RENDERING DECISION` can sit correct in the corpus for weeks while the baseline keeps making
the old claim, and every session that validates a new claim adds to the baseline while nothing
ever removes one.

**A partial fix shipped as discipline** — selection rules and a refresh-reconsiders-everything
instruction in `render`, plus `interview` rule 11b. **Its limit is worth stating: discipline
fails silently, depends on whoever is driving a session, and is judgement rather than string —
so `evals/` cannot test it** (see *Judge layer for the evals*).

---

## Live mode for the application-lane evals

**Deferred 2026-08-12**, when the application fixture and tier 3 shipped. Tier 3 is offline
only, and offline mode has the same limit the trip-wires already admit to: **it pins the
example, it does not test the skills.** Every tier-3 assertion would still pass if `apply`'s
inbox rule were deleted tomorrow, because the committed fixture would not change.

Tier 2 solved this with a live mode that renders fresh from `examples/corpus/` and asserts over
the output. The analogue here is harder in one specific way: a live application run has to
*write a folder*, across three skills and several turns, from a starting state that is a JD and
an inbox file rather than a one-line prompt. The interesting assertions — did `prep` promote a
recruiter's claim, did `fit.md` name the gap or paper over it — are exactly the ones that need
the live run.

**Shape of a fix:** seed a temp dir with `examples/corpus/`, the fictional `jd.md` and the
recruiter note, run `prep` against it, and reuse the tier-3 trip-wire patterns unchanged. The
conformance half stays offline; only the trip-wire half needs a model.

**Why deferred:** the fixture had to exist first, and the offline half is what stops the example
itself rotting, which is the failure that has actually happened in this repo.

---

## Artifact lifecycle has no state for a finished thread

**Deferred 2026-08-12**, noticed while writing the fixture. Lifecycle is `baseline` /
`in-flight` / `submitted`, which is a statement about *what may be done to the file* — and on
that reading it is right, and the three states are load-bearing in `interview` rule 11b.

But a prep pack for an application that ended in a rejection is still `in-flight`, forever,
because none of the three fits and there is nothing to re-render it for. The smell is small and
the fix is not obviously a fourth state: "the thread is closed" is a property of
`application.md`'s log, which already ends in an `outcome` event, and duplicating it into every
artifact's frontmatter is the rollup `apply` rule 6 forbids.

**Probably the honest answer is that nothing is wrong** and `in-flight` means "not frozen, not a
baseline". Recorded because the next person to read the fixture will notice it too, and a
deliberate divergence with no trace gets re-litigated.

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
- **Does `interview` actually read `REFERENCE.md` and compose rounds from the playbook?**
  Moving it out of `SKILL.md` traded always-loaded for a pointer the model has to follow.
  Static checks prove the pointer *resolves*; nothing proves it gets used, and the symptom
  if it doesn't — blander questions — is exactly the kind a regex can't see.

**Shape of a fix:** a rubric grader that answers specific yes/no questions with the corpus,
the JD and the output in context — never a 1–10 score, which compresses away the reason. Run
per-question, log the reason, require a majority across runs.

**Why deferred:** the grep tier catches the failures that have actually happened, costs
nothing, and runs on every push. A judge is a second stochastic system evaluating the first,
and a flaky judge is worse than no judge — it teaches you to ignore red.

---

## Claim-diffing against a real corpus

**Deferred 2026-08-11.** Was called "tier 3" when it was written; tier 3 is now the application
fixture, so it is named for what it does instead. The fixture corpus has four stories. A real
one has dozens, and selection pressure is the thing fixtures can't reproduce: with 30
stories, *which four* a render picks is most of the quality, and no assertion in `evals/`
looks at that.

**Why not just run the evals against the real corpus:** it moves while the skills that write
to it are under test, so a changed render can't be attributed to the change. And it's private,
so CI and contributors can never see it.

**Shape of a fix:** run the same prompt at two kit versions against a *pinned commit* of a
real corpus, extract the set of factual claims from each output, and diff the claim sets.
Surfaces "v1.5 stopped selecting the batch-window story" instead of "600 words changed".
The claim extractor is the hard part and is itself a judge — see above.

---

## Stable identifiers for rule cross-references

**Deferred 2026-08-11**, when the policy drift check shipped. Rules are cited by number —
`compact` cites `interview`'s rule 13, `render` cites its own rule 9. Tier 1 proves those
references *resolve*; nothing proves they resolve to the same rule they did before someone
inserted one above them. The reference stays green while silently changing meaning.

**Shape of a fix:** give load-bearing rules stable names — `CLAIM-SOURCE`, `SAY-ALOUD`,
`INBOX-NOT-EVIDENCE` — and cite those. They survive reordering and read better at the call
site than a number does.

**Why deferred:** it touches every rule list in the kit for a failure that hasn't happened
yet, and the numbering check makes the loud version of it (two rule 6s) impossible already.

**The case got stronger when the playbook moved to `interview/REFERENCE.md`.** Those
`playbook N` citations now cross a file boundary, which is where a silent renumber is most
likely and hardest to eyeball. Tier 1 checks they resolve; it still can't check they mean the
same thing they did.

---

## Coverage report, and a doctor for the corpus

**Deferred 2026-08-11.** The kit ranks what to extract *next* by interview value, but never
shows the user what the corpus already covers. "What should I work on?" is answerable today
only by reading `QUEUE.md` and remembering everything not on it.

A computed report — never a stored file; see `apply` rule 6 — could show roles and years with
no stories, résumé claims with nothing decompressing them, interview dimensions with zero or
one story, stories being spent across several live applications at once, and skills in
`profile.md` no story cites.

The same reader answers a second question as the format evolves: absent files, dangling
`related:` links, inbox files that got tracked by accident, application artifacts older than
the corpus they drew on. That last one **is** the pack-staleness entry at the top of this
file — if a doctor gets built, staleness is a check inside it rather than a separate feature.

⚠️ **The tracked-`_inbox/` check has one exemption and it must be written into the check, not
discovered by it.** `examples/applications/*/_inbox/` is committed on purpose — `examples/` is
not a corpus, the skills never read it, and a fixture with no unvetted material in it cannot
demonstrate the rule that unvetted material is never evidence. The exemption is the path,
`examples/**/_inbox/`, and the fixture file carries a banner saying so. A doctor that "fixes"
it deletes the only trap tier 3 has for the recruiter-claim assertions.

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

---

## Promote passes

State, not an idea — see `CLAUDE.md` for the workflow. Kept, not deleted.

**Reviewed up to corpus commit `e2e2c91` (2026-08-11), lesson log and repo instructions read
in full.** Start the next pass from `git log -p e2e2c91..HEAD -- <intake paths>`. Advance this
sha when a pass finishes, and don't replace it with a date — a date can't be diffed, and it
misses amendments to older entries.

**Landed 2026-08-11:** the three attribution tells (grammar, authority, articulacy) as one
playbook entry; provenance-of-a-number as another; derived conclusions inheriting their input's
error bars, split across the skill that produces them and the skill that consumes them; a
baseline refresh that reconsiders rather than only adds; and fixing a rendering in the same
session as the correction that changed it.

**Landed 2026-08-11, release A** — candidates 1, 2, 6 and 7 below, prompted by an external
review that independently reached candidate 1 and rated it P0. Rule 11b now marks rather than
fixes, and carries the three classes; *Demand the mistake* walks the decision chronologically
first; an unprompted limit is named as the strongest ceiling; hindsight-as-design-intent sits
under honest attribution. Candidate 8 turned out to be **already in the kit** — playbook 1's
failure-mode block ends with *"don't overshoot the other way"* — so it was recorded, not written.
Candidate 1's `corpus_pin` question stays open and belongs to *Pack staleness detection*.

**Landed 2026-08-12, release B** — the application lane got its templates, a worked fixture and
eval cases, and three things parked below landed with them. `apply` rule 6 now names the split
between a recomputable rollup and an unrecoverable input, and says out loud that
`application.md` carries no `status:` field and that there is no separate manifest. `fit.md`
records `no-corpus-evidence` rather than `missing`, and asks rather than deciding which of
*absent* and *unwritten* it is. Artifact frontmatter carries the `corpus_pin`, the sources, the
lifecycle state and — once sent — a hash of what went out. **Staleness checking and hashing
logic are not built**; only the slots to hold their inputs are, which is the half that cannot be
added retroactively.

### Open candidates from the 2026-08-11 full read

Ranked. Each was checked against the kit before being listed. Landed ones are struck from this
list; the numbering is left alone so the release note above still resolves.

3. **A later answer supersedes an earlier one.** Recall improves across a conversation. The new
   answer wins by default, but record the supersession with both dates rather than overwriting,
   because the *shape* of the drift is itself evidence. The kit knows supersession only as
   something `compact` must preserve, never as a capture rule.
4. **Don't edit existing text to align it with new information when the edit changes meaning.**
   Distinct trigger from surfacing a contradiction between two statements: here you are about to
   rewrite text that already exists, and the reconciled-but-vaguer version deletes true
   substance. Quote both lines and wait.
5. **Where a rule lives, and the routing test.** A rule that isn't in a repo can't be diffed,
   reviewed, or ported — so never hold one in a model's memory or a session summary. Routing:
   would this rule still apply if the corpus were about someone else? Yes → the method. No →
   the user's own lessons file. The kit says where to append and never says what belongs there.

**Landed 2026-08-12, release B — a fit check distinguishes *absent* from *unwritten* by
refusing to.** The recurrence-gated version of this (one observed instance, wait for a second)
turned out not to be needed: the kit-internal argument stands on its own, which is that the kit
never takes a call that is the user's and *absent* versus *unwritten* is exactly such a call.
`fit.md` now records `no-corpus-evidence`, never `missing`, and asks. Left here rather than
deleted because the *gated* version is still sitting in the corpus, and a later pass that reads
it without this note will re-derive it and wonder why the kit disagrees.

**Declined — do not re-propose.** A rule that was considered and rejected leaves no trace in
the skills, so without this list every pass re-argues it, and the dangerous case is a
*deliberate divergence* being quietly reverted to match the corpus that suggested it.

- **"One structural slot per company for the role itself."** The kit deliberately allows more
  than one: role and scope bullets are structural, don't compete for outcome slots, and a
  promotion or role change inside one company needs a second. The divergence is intentional.

**Landed, release B — application lifecycle and the `corpus_pin`.** This arrived as a request
for a per-application manifest and collided with `apply` rule 6, *never store derived state*.
Settled on the distinction the entry had already half found: *rule 6 bars recomputable rollups,
not unrecoverable inputs.* Rule 6 now says that in the skill. The pin, the hash of what was sent
and the captured JD URL are stored because they cannot be reconstructed; "three applications
live" is not, because it can. And there is **no separate manifest** — artifact-level state in
the artifact's own frontmatter, application-level in `application.md`'s, because a file whose
only job is to repeat another file's state goes stale on its own schedule.

The consuming half — noticing that a pin has gone stale — is still unbuilt and still belongs to
*Pack staleness detection* at the top of this file. What release B added is the record it will
need, which is the part that cannot be added retroactively.
