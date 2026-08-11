# career-corpus-kit

A Claude Code plugin. `.claude-plugin/plugin.json` is the manifest; `skills/` is
discovered by convention.

## Where kit changes get made

Change the kit from the kit repo, not from a corpus session. A session that has just
hit a problem carries that problem in context, and everything it writes gets shaped
by it — the incident's numbers become thresholds, the corpus's own vocabulary becomes
kit vocabulary, and the narrative arrives as prose. All three read as method and none
of it is.

**The test: a rule must be justifiable by reading the kit alone.** If explaining why
it exists requires recounting what happened to one person, it is not method yet. It
may be a real defect — record it in `BACKLOG.md`, which is a defect tracker and can
hold evidence — but the rule waits for a separate pass, made here, on kit-internal
grounds.

This is the same split the skills state in their own Lessons sections: the method is
public and stable, the scar tissue is private and belongs in the user's
`corpus/LESSONS.md`. `evals/static_checks.py` bans gendered singular pronouns in
`skills/` because leaked incident prose almost always carries one.

## Promote — moving a rule up from a live corpus

The method improves where it meets real material and breaks, which is inside somebody's
private corpus. Moving what's learned there into the kit is the point; doing it without
dragging the material along is the constraint. Call it **promote**, not sync: it is
one-way, it is lossy, and most lessons should never make the trip.

**Run it from here.** The kit session reads the corpus; a corpus session never writes
the kit. That direction is the whole safeguard — see the section above for what happens
when it reverses.

**The intake is three files, and nothing else:**

| Read | Yields | Rate |
|---|---|---|
| the corpus's **lesson log** | dated, one-lesson-each entries — interview technique, attribution traps, how to ask | high; most entries generalise |
| the corpus repo's **own instructions** | rules about the repo and its artifacts — lifecycle, commits, manifests | medium, and these are the *design* ports |
| the corpus's **work backlog** | parked designs written up before they were built, often with their own known weaknesses | low volume, high value — port the design, not the parking |

**Not story files, not `applications/`.** Those hold the raw personal detail and a promote
pass has no use for it. Per-fact markers in a story file are calls about one person's career;
read them only if a whole *class* of them implies a mechanism the kit lacks. This matters more
than it looks: the commit stays clean either way, but whatever gets read enters the session
transcript. **Scoping the read is the privacy control, not scoping the write.**

Two gates, and a candidate needs both:

- **Recurrence.** One instance is an anecdote. Promote what recurred across different
  material — "third time now", "same family as" — because that is what will recur for a
  stranger.
- **Generalisation.** Two questions, at two stages. Of the entry: *would this still be true
  for someone with a completely different career?* Of the rule you'd write from it: the test
  above — justifiable by reading the kit alone.

Sorting entries against that first question gives three piles, and **the middle one is the
biggest**:

- **Port** — the entry names a *tell* and a *move*: an observable signal in how someone
  talks, and a specific thing to do about it. That has nothing to do with whose corpus it is.
- **Leave** — the entry is calibration for one person: which numbers they round up, what
  their files are called, how often their corrections have proved right. That last shape is
  the trap, because the *rule* is portable while the evidence for it is private, and the kit
  would get the rule with no evidence at all.
- **In between, and usually** — a portable rule welded to the instance that proves it. Keep
  the opening claim and the move; bin the paragraph in the middle.

**Pin a commit, not a date.** Record the corpus sha you reviewed up to, and start the next
pass from `git log -p <sha>..HEAD -- <intake paths>`. A date can't be diffed and doesn't say
which of several same-day commits it means. A sha also catches the case a date scan misses
entirely: an **amendment to an older entry**, which never appears in a list of new entries and
usually means a rule got broader — which is exactly what porting wants.

**Check the kit first, and check the clone rather than the cache.** Much of the kit is already
there under different wording, and a corpus's notes about it go stale fast. Two copies carry a
version and they disagree — the development clone, and
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, which is what a running session
actually loads and which lags. **The loaded copy governs a session; the clone is what gets
ported.** Read the clone, or a rule already landed and unreleased looks like a gap.

**Redact mechanically.** Port the claim and the move. Cut the instance — company,
project, quoted speech, numbers. Keep the cross-references ("sibling to", "same family
as"); they carry nothing private and they are the structure of the method. If a rule
genuinely needs an example, write a fresh one or use the fictional corpus in `examples/`.
**A lightly disguised instance is still a leak**, and it reads as one to anyone who knows
the person. Before proposing: could a reader of this repo name the employer, the product,
or the person? Then it isn't redacted.

**Propose before landing**, with the diff, which skill file, why it generalises, and what
it replaces. Verification is the usual `./evals/run.sh`, plus a grep of the diff for names
that shouldn't be in it.

**Record what you declined and why**, in the *Promote passes* section at the bottom of
`BACKLOG.md`, along with the date of the pass so the next one can scope its diff. Ported
rules need no record — they're in the skills. Declines do, and not only to save effort:
a rule rejected on purpose leaves no trace, so the next pass reads it again, sees the kit
disagreeing with the corpus, and quietly reverts a deliberate divergence.

## Versioning

Bump `version` in `.claude-plugin/plugin.json` on every user-visible change —
skill behaviour, prompts, templates, README instructions, install steps.

Why: installs are cached at `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`.
Users get new content on `/plugin marketplace update` regardless, since identity
tracks the commit sha. But `version` is the only signal they *see* in `/plugin`,
and an unchanged version overwrites the cache dir in place instead of creating a
new one. Silent updates look like nothing shipped.

Semver: patch for wording and fixes, minor for new skills or new behaviour,
major for anything that breaks an existing corpus layout.

No bump for changes users never load: this file, CI, `.gitignore`, comments.
