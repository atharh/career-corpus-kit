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
