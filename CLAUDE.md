# career-corpus-kit

A Claude Code plugin. `.claude-plugin/plugin.json` is the manifest; `skills/` is
discovered by convention.

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
