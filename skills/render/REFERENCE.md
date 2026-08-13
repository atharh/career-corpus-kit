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

**Form:** prose, ~300–450 words — a full page with greeting and sign-off, and never more.
The ceiling is not a style preference: the reader is time-poor and skeptical, and a letter
that can't prioritise is evidence about a candidate whose job is prioritising. Under ~200
words reads as an afterthought. Structure carries more than raw length — three or four tight
paragraphs, each doing one job, beat one dense block at the same word count. If a build
pipeline turns single newlines into breaks, keep signature lines on their own lines.

**What the letter is for.** The résumé already carries the evidence; the letter's one job is
to buy the conversation. A hiring manager gives it ten or twenty seconds and skims for three
things: did a person aim this at us, or does everyone get this letter; have they done
something like this work before; and can they write clearly — the letter is itself the
sample for that last one. Every rule below serves those three.

**Rules of the form:**
- **One thesis, stated in the opening: the specific work the user would own here**, taken
  from the part of the posting that describes the work — what this employer is buying and
  why they're it. Specificity is the proof the posting was read. Not "I've done many things." A
  posting speaks in two registers: what the job is (what gets built, owned, fixed) and how the
  company likes to work (values, culture, method statements). A thesis can come from the JD
  and still come from the wrong part of it. The test for which register is which: ask what
  this person will be doing on a Wednesday. Weight the letter there; the second register
  earns a clause, not a beat.
- **Don't mirror the posting's structure.** If a reader with the posting open can reconstruct
  which requirement each paragraph is discharging — its lines quoted back at it, paragraph
  weight copied from the posting's emphasis, bridges like "you say X" — the letter reads as a
  requirements response, which is the shape of template spam. The JD decides which stories
  appear and which face they wear; the letter's structure is the user's own.
- **The why-them paragraph must be true of the user and not of the next applicant.** That is
  the test it has to pass. Admiration anyone could type — impressive product, resonant
  mission — reads as sent-to-everyone. The corpus earns this paragraph with real contact
  (the product used, the domain worked in, the problem hit first-hand) or it stays short.
- **One story, told fully — a second only if both stay short.** Three or four sentences:
  the situation, the calls made, the measurable outcome. The story's job is to make the
  thesis vivid, not to survey the career — the résumé does the surveying, and a letter
  stuffed with mini-anecdotes is a résumé with worse formatting. Tell it as a concrete
  moment, not a claim: a specific scene ("you can't un-summarise a monthly total back into
  rows") beats "I solve messy real-world problems." The corpus has the scenes; use them.
- **Pick the story by honest relevance, not chronology or pride.** The story matching what
  the role actually is carries the case; a marginal second match survives as a clause, not
  a paragraph — material inflated past its relevance is the letter-level version of an
  unsourced number.
- **Position in the lane the posting is in.** A leadership role is answered with judgment
  calls, org outcomes, and work done through others; a senior hands-on role with craft
  depth and cross-team leverage. The corpus often backs both; the JD picks which face the
  story wears. Strong evidence from the wrong lane reads as applying for a different job.
- **Write the story as the calls the user made, not the scope they held.** "Chose X over Y,
  cut Z" is evidence; "owned the platform" is a job description. A decision to kill or
  discard something is often the strongest line in the letter. Attribution rules as
  everywhere: `[HONEST-ATTRIBUTION]`, `[TRUE-VERSION]`.
- **Don't restate the résumé.** The reader has it. The letter carries what a bullet cannot:
  why the user did it that way, and what they were thinking at the time. A sentence that
  would survive unchanged as a résumé bullet is in the wrong document.
- **Honest framing device or none.** A neat opener that outruns the facts ("done it twice" when
  one instance only half-qualifies) will break under one interview question. Reframe to what's
  defensible word-for-word.
- **Close with a plain ask, and put the practical facts there.** One unadorned line asking
  for the conversation; location, timezone, availability — the close and nowhere else. No
  throat-clearing, no "I would welcome the opportunity" boilerplate if a plainer line is
  truer to their voice.

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
