# Role files — the schema

The ladder in `SKILL.md` is role-agnostic on purpose. Scope, reach, horizon, the five tells
and the five pillars hold for an engineer, a designer, a marketer and a finance lead alike —
what changes between roles is **the craft: what the work is made of, what artifacts it
produces, and how a story in that craft typically overclaims.** That is what a role file
holds, and it is the only thing that should live here.

One file per role. Adding a role means writing one of these, not editing `SKILL.md`.

## Frontmatter

```yaml
role: Product Manager          # how the exemplar names the role, in industry terms
track: ic | manager            # which mode of the ladder applies
aliases: [PM, product owner]   # what the user might call it; used to resolve a request
extends: _manager-core         # optional; a manager role inherits the function-agnostic list
```

## Sections, in order

**1. `## Scope by level`** — a short table giving this craft's nouns for each rung of the
ladder: what is owned, and what "success" is made of here. Three or four rows, ending at the
level the user is plausibly reaching for. This does not restate the ladder's axes; it makes
them concrete. *An engineer owns a service; a PM owns an outcome and a roadmap; a designer
owns a surface and a system.*

**2. `## Dimensions`** — twelve to eighteen story-shaped bullets in a standalone role file,
four to eight in an overlay that `extends:` a shared fragment; the combined list has no cap,
because the pick at run time is six to nine either way. These are the things a strong telling
in this craft covers. Each names a specific piece of evidence, not a virtue. **"Had good
judgment" is not a dimension; "a written criterion agreed before the decision" is.** These are
picked from at run time, six to nine per story — never all of them.

**3. `## Named artifacts`** — what this craft actually produces, by name. The exemplar reaches
for these to stay concrete, and an assessment uses their absence as a question. *RFC, runbook,
golden set / PRD, roadmap, launch review / design system, research plan, critique.*

**4. `## How stories in this craft overclaim`** — the role's characteristic inflation, so the
exemplar models the restraint and the assessment knows what to discount. Every craft has one:
engineers claim causality from correlated metrics, PMs claim engineering outcomes as their own,
managers claim their team's work in the first person.

**5. `## Pillar blind spots`** — which of the five pillars `SKILL.md` defines — results,
direction, talent, culture, craft — this craft's stories habitually under-serve, so a benchmark can supply what the ladder will ask for and the
story never does.

## Rules for writing one

- **Craft only.** If a bullet would be equally true for a different role, it belongs in
  `SKILL.md` or in `_manager-core.md`, not here. Duplication across role files is how the two
  drift apart.
- **A manager role extends `_manager-core`** and adds only the craft overlay — the technical,
  design or commercial bar that function keeps at every level. Do not restate the inherited
  list.
- **Name evidence, never qualities.** Each dimension should be answerable with a thing that
  exists: a document, a number, a decision with a date, a person who changed.
- **No employer-specific vocabulary.** Industry terms only, so the file survives a job change.

## Files starting with `_`

Not roles — shared fragments other role files extend. They are never matched against a user's
request.
