# Capability files — the rules

The trigger and the shape live elsewhere: `[CAPABILITY-FILE]` in SKILL.md says when to open
one, `[CAPABILITY-HARVEST]` says how story sessions feed one, and
[templates/capability.md](templates/capability.md) is the skeleton. This file is the
rules that govern the material once a capability file is open. **Read it whenever you open or
update anything under `corpus/capabilities/`** — updates as much as first openings, because
every rule here is about how claims accrete.

## Rules specific to capability files

**A capability file owns no facts.** `[OWNS-NO-FACTS]` It is a derived index: every fact in it
cites the story file that owns it, never restated as this file's own. A fact that surfaces here
with no home yet is held, marked homeless, and **pushed down into the owning company or project
file as soon as placement settles** — a technology claim that never acquires a place it
happened is a claim with no anchor, and an anchorless claim is what a follow-up question
punctures first.

**Every entry carries a depth ceiling, and the file carries the noes.** `[DEPTH-CEILING]`
Record how far each claim can be pushed before it breaks — *administered it* and *my team ran
on it* are different claims, and a file that flattens them reads as uniform confidence, which
is worse than nothing. Keep a noes section — what the user has *not* done with the
technology — the analogue of a through-line's "where it doesn't hold", and the thing that
makes the rest credible in a room.

**Treat each self-named technology as a candidate claim: ask what actually ran on it before
writing it down.** `[LIST-IS-A-QUEUE]` Build the file on what the user did — the list is a
queue of things to disprove, not the file's backbone. A technology survives "have you used it"
and survives "where", then dies at "what ran on it": self-report reliably swaps in a
neighbouring tool or moves a claim to the wrong employer, and the list looks strongest exactly
while it is least tested. This is the ask-what-it-did move from `[WHO-OWNED-IT]`, pointed at
tools.

**A cross-company file finds conflicts a story file can't — hold them, never launder them.**
`[CROSS-FILE-CEILINGS]` "Where did you use X" has no respect for file boundaries, so a
capability file will surface contradictions between one company's recorded ceiling and an
answer given about another — that is an argument for the shape, and also its hazard: a file
assembling claims from five companies can quietly launder one company's ceiling away. When an
answer collides with a recorded ceiling, **block the material and hold the push-down until the
owner of that ceiling settles it**, per `[MARK-DONT-FIX]` — the reconciliation usually
produces material nobody would have gone looking for.
