# Backlog

Things worth building that aren't built. Not a roadmap — a place ideas stop rotting in a chat
log. Newest at the bottom; delete rather than mark done.

The one exception is *Promote passes* at the bottom, which is state rather than an idea, and
is kept rather than deleted.

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

### Scope correction — the baseline is the worse case

This entry was scoped to packs and tailored output, and judged uncommon on the grounds that
regenerating before each interview is cheap. The **baseline** was outside that scope and is the
worse case: it is long-lived by design, nothing regenerates it from scratch, and it is the
artifact most likely to be sent.

Two failures follow from it, and they share one cause:

- **Recorded decisions don't propagate.** A `RENDERING DECISION` can sit correct in the corpus
  for weeks while the baseline keeps making the old claim. Recording feels like finishing.
- **The baseline accumulates.** Every session validates new claims and the baseline is where
  they land; nothing ever removes one.

**The root cause is one asymmetry: several paths write to an artifact and none prune or
re-verify it.** Worth treating as one problem rather than two.

**A partial fix shipped as discipline** — selection rules and a refresh-reconsiders-everything
instruction in `render`, and `interview` rule 11b (fix the rendering in the same session; diff
the whole résumé against the corpus once per corpus). **Its limit is honest and worth stating:
discipline fails silently, depends on whoever is driving a session, and is judgement rather than
string — so `evals/` cannot test it** (see *Judge layer for the evals*). That makes the tooling
case stronger, not weaker, and its highest-value target is the baseline rather than the packs.
If the corpus doctor below gets built, this belongs inside it.

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

---

## Promote passes

State, not an idea — see `CLAUDE.md` for the workflow. Kept, not deleted.

**Reviewed up to corpus commit `d2c6601` (2026-08-11), lesson log and repo instructions read
in full.** Start the next pass from `git log -p d2c6601..HEAD -- <intake paths>`. Advance this
sha when a pass finishes, and don't replace it with a date — a date can't be diffed, and it
misses amendments to older entries.

**Landed 2026-08-11:** the three attribution tells (grammar, authority, articulacy) as one
playbook entry; provenance-of-a-number as another; derived conclusions inheriting their input's
error bars, split across the skill that produces them and the skill that consumes them; a
baseline refresh that reconsiders rather than only adds; and fixing a rendering in the same
session as the correction that changed it.

### Open candidates from the 2026-08-11 full read

Ranked. Each was checked against the kit before being listed.

1. **Artifact lifecycle — and it makes an already-shipped rule unsafe.** Three classes with
   three rules: *submitted* (frozen permanently — it is evidence of what a reader saw),
   *in-flight* (re-render on request, show the diff, own commit), *baseline* (deliberate act,
   own commit, never bundled with corpus edits). The interview rule that says fix a rendered
   claim in the same session draws no class distinction, so applied to a submitted artifact it
   destroys the evidence. **Fix that carve-out whether or not the rest lands.** Carries the
   `corpus_pin` question below.
2. **The direct ask for a mistake returns nothing.** *Demand the mistake* instructs the move
   that has been observed to fail: asked point-blank, people have no topic and no memory; asked
   what they actually did, step by step, the misjudgement arrives on its own, attached to the
   decision that produced it — which is also the only form in which it is tellable. Amend the
   existing playbook entry rather than adding one.
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
6. **A limit the user volunteers unprompted is a ceiling.** Strongest kind, since it is offered
   against their own interest — and the easiest for a later session to quietly re-inflate
   because the bigger version reads better.
7. **Don't render hindsight as design intent.** Building something that became infrastructure is
   not the same claim as having planned it that way. "Noticed their own work was worth
   generalising" survives a follow-up; "designed a system" often doesn't.
8. **Don't overshoot after a pushback.** One line: correcting an over-dramatic reading shouldn't
   flip to an under-claiming one.

**Declined — do not re-propose.** A rule that was considered and rejected leaves no trace in
the skills, so without this list every pass re-argues it, and the dangerous case is a
*deliberate divergence* being quietly reverted to match the corpus that suggested it.

- **"One structural slot per company for the role itself."** The kit deliberately allows more
  than one: role and scope bullets are structural, don't compete for outcome slots, and a
  promotion or role change inside one company needs a second. The divergence is intentional.

**Deferred — real, blocked on a decision.** Application lifecycle with a per-application
manifest recording a `corpus_pin`. It belongs to the pack-staleness entry at the top of this
file, and *"a date is not a pin"* is that entry's own insight arriving from the other side. It
collides with `apply` rule 6, *never store derived state*: a `status` field is exactly the
status rollup that rule forbids, but a pin is not derived — it records an input, and unlike a
status it cannot be recomputed later, which is the whole reason to write it down. **Settle
whether rule 6 should name that distinction before porting any of it.**
