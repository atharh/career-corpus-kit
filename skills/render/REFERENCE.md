# Rendering reference — per-artifact shapes

Shared rules live in SKILL.md. This file is the shape each artifact takes.

## Where files live

| | Baseline (no JD) | Tailored (with JD) |
|---|---|---|
| Résumé | `resume.md` | `applications/<company>-<role>/resume.md` |
| Cover letter | `cover-letter-<family>.md` | `applications/<company>-<role>/cover-letter.md` |

The tailored column lives inside a folder the `apply` skill opens and owns. Read what's
already there before asking for anything:

| File | Owner | What it is |
|---|---|---|
| `jd.md` | `apply` | The posting verbatim, with URL and capture date. Read it; don't ask for the JD again. |
| `fit.md` | `apply` | What the corpus backs, backs thinly, and can't back for this role. Most of the selection work. |
| `application.md` | `apply` | Dated log — stage, contacts by role, next action. |
| `_inbox/` | `apply` | Raw inbound. **Unvetted. Never a source for anything.** |
| `interview-prep.md`, `01-…`–`05-…` | `prep` | The study pack for a booked interview. Not this skill's output. |

Read all of it; source no *candidate claim* from any of it (SKILL.md rule 1). These files
carry employer context and selection work, not evidence about the user. When `fit.md` names a
story as backing a requirement, open that story and render the claim from there.

If you keep a PDF build pipeline that globs top-level `*.md`, an `applications/` subfolder
won't be swept into the baseline build — run the build with explicit paths for tailored
files. Role-family cover letters (if you keep several) are effectively *baselines per role
family*; for a tailored render, start from whichever is closest, but re-source from the corpus.

---

## Résumé entry

**Form:** terse, verb-led bullets. `###` role, then `**Company** | dates | location`, then
bullets.

**Rules of the form:**
- **Lead with the strongest evidence for *this* JD**, not chronology-within-role. A concrete
  systems-rebuild bullet outranks a vaguer summary bullet when the role wants systems depth.
- **One arc per bullet.** If the corpus has merged three résumé bullets into one story,
  consider merging them here too so the bullet stops reading generic — but only if it fits the
  role.
- **Numbers early, sourced, ceilinged.** Lead a bullet with the metric the corpus vouches for.
- **Cut ruthlessly.** Adding a strong bullet usually means removing a weak one; an entry can't
  hold ten. Propose what comes *out*, not just what goes in.
- **No war-story detail.** The narrative belongs in interview prep; the résumé gets the
  compressed claim ("diagnosed complex production issues across X, Y, Z").

---

## Cover letter

**Form:** prose, one page. ~350–600 words; one page is a hard ceiling. If a build pipeline
turns single newlines into breaks, keep signature lines on their own lines.

**Rules of the form:**
- **One thesis, stated in the opening**, drawn from the JD — what this employer is buying and
  why they're it. Not "I've done many things."
- **2–4 beats, each a concrete moment, not a claim.** A specific scene ("you can't
  un-summarise a monthly total back into rows") beats "I solve messy real-world problems."
  Show, don't assert — the corpus has the scenes; use them.
- **Order by relevance, not time.** Lead with the beat that most directly answers the role.
- **Honest framing device or none.** A neat opener that outruns the facts ("done it twice" when
  one instance only half-qualifies) will break under one interview question. Reframe to what's
  defensible word-for-word.
- **Close briefly.** No throat-clearing, no "I would welcome the opportunity" boilerplate if a
  plainer line is truer to their voice.

---

## Interview-prep answers

For a **booked** interview, `prep` owns this — it builds a whole pack against the employer's
criteria and writes it into the application folder. What follows is the shape of a spoken
answer on its own, for the ad-hoc case: rehearsing one story, or answering a question that
arrived out of band. `prep` renders answers in this shape too.

**Form:** spoken-shaped, longer than a bullet, structured but not robotic — stories that
follow the flow an interview actually takes.

**Rules of the form:**
- **STAR rendered *from* prose, never as a filled-in template.** Situation/Task/Action/Result
  as a skeleton the good corpus prose hangs on — the corpus already stores arcs this way
  (setup → beats → outcome → what-it-cost).
- **Prep the follow-ups, because the corpus already found them.** Every story file's `gaps` and
  `⚠️` notes are the exact places a sharp interviewer pushes. Surface the question *and* the
  defensible answer.
- **Carry the mistake.** The corpus deliberately keeps the failure in each story. A story with
  no misstep reads as a case study — interviewers can smell it.
- **Match story to question type.** Tag which corpus stories answer "hardest problem,"
  "conflict," "failure," "leadership," "ambiguity." One story can serve several through
  different lenses — but **note where a story is already spent**, so the same anecdote isn't
  reused across answers in a single loop.
- **Through-lines are talking points, not scripts.** Offer them as ways to connect stories,
  never as claims to recite. Let the interviewer's question pick the lens, same as the JD does
  for a letter.
