---
name: verify
description: Fact-check the user's vetted corpus story files against the public record, the way a technical interviewer would — release dates, feature sets, how a mechanism actually works — reporting findings with citations and proposed restatements, never patching silently. Use when the user asks to verify, fact-check, or audit a story file, a company directory, or the whole corpus, or after an interview session has landed new technical material. Corpus only — it never reads renderings or _inbox/, and it is not drift detection.
---

# Career corpus — verify

The corpus vouches for **provenance** — *the user said this, here, on this date* — and
deliberately not for truth; see "What 'vetted' means" in the interview skill. Nothing in the
capture lane vouches for the **public record**: that the tool existed in that year, that the
feature is real, that the mechanism works the way the sentence says. An interviewer checks
exactly those things, in the room, with nothing at stake for them and everything at stake for
the user. This skill runs that check first, on disk, with citations.

It is the **batch enforcement point** of the interview skill's fact-check rule
`[CHECK-THE-CLAIM]` — one rule, two enforcement points, the way a linter and a reviewer catch
the same bug at different times. `[CHECK-THE-CLAIM]` and its sibling `[DATE-THE-TERM]` fire in
conversation, while the user can still answer; this skill applies the same obligation to
material already on disk, with nobody in the room. Don't restate those rules; cite them.

It exists for two outcomes at once, and the second is not optional decoration:

1. **The corpus stays technically pristine** — no claim survives that one search by an
   interviewer would kill.
2. **The user learns the correction.** Every finding teaches: what is actually true, why, and
   what the defensible sentence is. Surfacing the gap here is cheaper than surfacing it in an
   interview loop.

## Where this sits — and where it must not reach

- **The corpus only.** Point it at one story file, a company directory, or the whole corpus —
  every vetted `.md` under the target. With no target named, ask; don't guess.
- **Never a rendering.** This skill never reads or edits renderings. A résumé still carrying a
  claim the corpus has since corrected is *drift*, a different defect, deliberately out of
  scope — two jobs in one skill would do neither cleanly.
- **Never `_inbox/`.** Unvetted material isn't worth verifying — extraction may redo it from
  scratch (`[INBOX-QUEUE]`), and a correction filed against a queue entry evaporates with it.
- **`anachronisms_corrected:` is the settled ledger.** Re-running on a checked file is cheap
  and safe because settled entries are not reopened: the block records the old wording, the
  new wording, and the citation, which is what stops the wrong word creeping back in.

## Hard rules

**No citation, no correction.** `[CITE-OR-ASK]` The fact-checker is the same machine that
invents facts, and a wrong correction is worse than a wrong claim — it arrives carrying
authority and provenance the original never had. Every finding cites a source that would
survive being clicked by a stranger: a release history, a changelog, official documentation.
Look it up fresh, in this run — training memory is a hypothesis, never a citation. What cannot
be sourced becomes a **question addressed to the user**, clearly marked as unverified, and is
never written into a story file as fact.

**Report first; patch only on the user's decision.** `[REPORT-DONT-PATCH]` This is
`[MARK-DONT-FIX]` applied to a batch audit: the full report lands before any file changes.
Per finding the user accepts, amends, or rejects — and a rejection is recorded *with their
reasoning*, because a refuted finding is usually better material than the finding was: what
reads as a wrong claim is often the user's own shorthand, and only they can say which. Then
apply what they accepted **in the same session** — an accepted finding left unapplied is a
recorded decision that never reached the file.

**Restate, never delete.** `[RESTATE-NOT-DELETE]` The fix for a wrong label is the sentence
that is true — the restatement move `[DATE-THE-TERM]` prescribes for anachronisms, applied
here to every class of finding. If a proposed line says less than the line it replaces, it is
not a fix. Deleting a claim outright is the user's call alone, and only when nothing true is
left under it.

**Verify the world, never the person.** `[PUBLIC-FACTS-ONLY]` This skill checks claims where
the public record is the authority: dates, feature sets, how a technology works, what a term
meant in a given year. It has **no standing** on the user's numbers, their attribution, their
memory of who decided — those belong to the capture lane, with its own rules and its own
interviewer. A throughput figure is not a finding; a throughput figure *attributed to a
feature the tool never had* is.

**Scepticism is symmetric.** `[CHECK-THE-CHECK]` Before reporting a finding, try to refute
the finding itself: an older feature under a different name, an earlier release, a plugin or
extension that existed then. A finding that dies under its own check was never a finding.
When the record is genuinely ambiguous, say so and classify the claim uncheckable rather than
picking a side.

## The four finding classes

Every finding is exactly one of these, because they demand different handling:

| Class | Looks like | Handling |
|---|---|---|
| **Anachronism** — true work, wrong-era word | a tool or feature named in a year before it shipped | Cite the release history. Restate as precedence per `[DATE-THE-TERM]` — the user had the idea before the tooling named it — and log it in `anachronisms_corrected:` |
| **Wrong about the technology** | a mechanism described the way it doesn't work; a feature attributed to a version that never had it | Cite the docs. The only class that is flatly an error. Correct the sentence; the tutor note carries why |
| **Compressed, not false** — shorthand that fails a follow-up | *"the broker gave us retries"* when the retry logic sat on top of it | The commonest and the most valuable. Not an error — a restatement that survives the room. Expect *"I knew that, I compressed it"*, and record it as the user's shorthand, not their gap |
| **Uncheckable** | internal systems, private metrics, the user's own designs | Named explicitly in the report, with no opinion attached — silence would read as verified |

## The report

Findings ranked by what an interviewer would catch first, each carrying:

1. **The claim, quoted**, with `file:line`.
2. **Its class**, from the table.
3. **What the record says** — with the citation.
4. **The tutor note** — *why* the true version is true, in enough depth to be learned from
   rather than merely complied with. This is the half that compounds.
5. **The proposed restatement** — the sentence that survives a follow-up, usually stronger
   than the original because it is more specific.

Close the report with the clean bill: which claims were checked and held. A report that only
lists problems teaches nothing about what is already defensible — and the checked-and-held
list is what makes re-runs meaningful.

## Applying accepted findings

- The correction lands **in the story file that owns the claim**: the body restated, and one
  dated entry in `anachronisms_corrected:` carrying the old wording, the new wording, and the
  citation — so the wrong word cannot creep back and the next run knows it is settled.
- **A correction here never authorises touching a rendering.** If the corrected claim is
  already in a rendered artifact, say so, name the artifact and the line, and stop — the
  session owes the marker, never the fix (`[MARK-DONT-FIX]`), and the artifact's lifecycle
  rules in the render and apply skills govern what happens next.

## What this skill is not

- **Not the interviewer.** It asks the user nothing except what it could not source — no
  frontier rounds, no story-shaping. One question class only: *"this is uncheckable; do you
  want it flagged or left?"*
- **Not a style pass.** Prose quality, story shape, ceilings and attribution belong to the
  capture lane. A sentence that is technically right and badly written is out of scope here.
- **Not drift detection.** Corpus-vs-rendering disagreement is a different defect, and this
  skill never reads a rendering to find it.

## Lessons — how this skill personalises to you

This skill ships generic and sharpens by accumulating the user's own corrections in
`corpus/LESSONS.md` — in their **private** corpus repo, never in the kit. Never edit this
SKILL.md to record a lesson: the method stays stable and shareable; the scar tissue stays
private and personal.

- **At the start of a session, read `corpus/LESSONS.md`** if it exists. Treat each entry as an
  additional rule for this user, on equal footing with the hard rules above.
- **After a correction that generalises, append one dated line**: the mistake, and the rule to
  apply next time. Route it first — a rule that would still hold if the corpus were about
  someone else belongs to the method, not this file. Either way the rule lives in a *file*: a
  rule nobody can diff is a rule nobody can review, port, or undo.
- **A lesson leaves this file two ways, each on the user's explicit say-so, entry by entry.**
  One that proves *wrong* is retired in the session where it misfired, struck in place —
  `~~<the entry>~~ retired YYYY-MM-DD: <one clause of why>` — and never applied again; the
  strike records wrongness, which lives nowhere else. One the method has since *absorbed* is
  deleted outright, no strike left behind — a shipped rule's duplicate here can only drift —
  once nothing local remains (no calibration about this user, no number they set, no recorded
  divergence; trim the entry to that residue if any does) and no session still loads a skill
  version without the rule.
