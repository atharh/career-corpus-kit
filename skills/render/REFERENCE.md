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
| `application.md` | `apply` | The thread's event log and contacts, in the format `apply` owns. Read it for where the thread stands. |
| `_inbox/` | `apply` | Raw inbound. **Unvetted. Never evidence for a candidate claim** — attributed employer context and operational fact only. |
| `interview-prep.md`, `01-…`–`05-…` | `prep` | The study pack for a booked interview. Not this skill's output. |

**Every artifact this skill writes opens with the frontmatter block in
[`templates/artifact-frontmatter.md`](templates/artifact-frontmatter.md)** — baseline and
tailored alike, and `prep`'s pack files too. It records what a re-reader cannot reconstruct:
the lifecycle state, the corpus commit the render read, the files it drew on, the date, and —
once something has been sent — what went out. Fill the slots you know and leave the rest empty;
a guessed pin is worse than none.

Read all of it; source no *candidate claim* from any of it — SKILL.md's claim-sourcing rule
`[CLAIM-SOURCE]`. These files carry employer context and selection work, not evidence about the
user. When `fit.md` names a story as backing a requirement, open that story and render the claim
from there.

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

**What the letter is for.** The résumé already carries the evidence; the letter answers three
questions, in order: who the user is, why they are writing to *this* company, and why they
would be good at *this* work. A hiring manager skims it asking one thing — did a person aim
this at us, or does everyone get this letter?

**Rules of the form:**
- **One thesis, stated in the opening, taken from the part of the posting that describes the
  work** — what this employer is buying and why they're it. Not "I've done many things." A
  posting speaks in two registers: what the job is (what gets built, owned, fixed) and how the
  company likes to work (values, culture, method statements). A thesis can come from the JD
  and still come from the wrong part of it — tailor to the job, and let the second register
  calibrate tone at most.
- **Don't mirror the posting's structure.** If a reader with the posting open can reconstruct
  which requirement each paragraph is discharging — its lines quoted back at it, paragraph
  weight copied from the posting's emphasis, bridges like "you say X" — the letter reads as a
  requirements response, which is the shape of template spam. The JD decides which stories
  appear and which face they wear; the letter's structure is the user's own.
- **The why-them paragraph must be true of the user and not of the next applicant.** That is
  the test it has to pass. Admiration anyone could type — impressive product, resonant
  mission — reads as sent-to-everyone. The corpus earns this paragraph with real contact
  (the product used, the domain worked in, the problem hit first-hand) or it stays short.
- **2–4 beats, each a concrete moment, not a claim.** A specific scene ("you can't
  un-summarise a monthly total back into rows") beats "I solve messy real-world problems."
  Show, don't assert — the corpus has the scenes; use them.
- **Lead with the beat that is the job, and weight the rest by honest relevance.** Not
  chronology. The story matching what the role actually is opens the case; a marginal match
  survives as a clause, not a paragraph — a beat inflated past its relevance is the
  letter-level version of an unsourced number.
- **Write beats as the calls the user made, not the scope they held.** "Chose X over Y,
  cut Z" is evidence; "owned the platform" is a job description. A decision to kill or
  discard something is often the strongest line in the letter. Attribution rules as
  everywhere: `[HONEST-ATTRIBUTION]`, `[TRUE-VERSION]`.
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
