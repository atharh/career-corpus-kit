# Rendering reference — per-artifact shapes

## Contents

- Where files live
- Deriving the family list
- Résumé entry
- Cover letter
- Interview-prep answers
- The outbound file

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
| `_inbox/` | `apply` | Raw inbound. **Unvetted. Never evidence for a candidate claim**: attributed employer context and operational fact only. |
| `interview-prep.md`, `01-…`–`05-…` | `prep` | The study pack for a booked interview. Not this skill's output. |

**Every artifact this skill writes opens with the frontmatter block in
[`templates/artifact-frontmatter.md`](templates/artifact-frontmatter.md)**, baseline and
tailored alike, and `prep`'s pack files too. It records what a re-reader cannot reconstruct:
the lifecycle state, the corpus commit the render read, the files it drew on, the date, and,
once something has been sent, what went out. Fill the slots you know and leave the rest empty;
a guessed pin is worse than none.

Read all of it, but source no *candidate claim* from any of it (SKILL.md's `[CLAIM-SOURCE]`).
These files carry employer context and selection work, not evidence about the user. When
`fit.md` names a story as backing a requirement, open that story and render the claim from
there.

If you keep a PDF build pipeline that globs top-level `*.md`, it won't pick up files in an
`applications/` subfolder, so build tailored files with explicit paths. Role-family cover
letters, if you keep several, are baselines per role family: for a tailored render, start from
whichever is closest, but re-source from the corpus.

---

## Deriving the family list

Baseline cover letters are kept one per role family, as `cover-letter-<family>.md`. The
filename sets the convention, but nothing says where the families come from, so a corpus
invents the set by accident: a letter gets rendered for a role, gets kept, and a family exists.
Nothing afterwards asks whether the set is complete. Derive it instead, from two things already
on disk:

- the role families the user has actually targeted in `applications/`, which is the only
  evidence of intent a corpus holds;
- what the corpus can evidence, because a family nothing can back is not a candidate however
  often it has been targeted.

The output is a report: the families, which baseline artifacts each one has, and the gap. A
family with a letter and no résumé is the common case, and this derivation is what finds it.
Derive it on the spot and never store it: a stored family list goes stale exactly like the
`status:` field that `apply`'s `[NO-ROLLUP]` bans. The status checker deliberately does not
compute it, because which family an application belongs to is a judgement about a role rather
than a field on disk, and a tool that guessed would be confidently wrong on the interesting
cases.

---

## Résumé entry

**Form:** terse, verb-led bullets. `###` role, then `**Company** | dates | location`, then
bullets.

**Rules of the form:**
- **Lead with the strongest evidence for *this* JD**, not chronology within the role. A concrete
  systems-rebuild bullet outranks a vaguer summary bullet when the role wants systems depth.
- **One arc per bullet.** If the corpus has merged three résumé bullets into one story,
  consider merging them here too so the bullet stops reading as generic, but only if it fits
  the role.
- **Numbers early, sourced, within their ceiling.** Lead a bullet with the metric the corpus
  vouches for.
- **Cut hard.** Adding a strong bullet usually means removing a weak one; an entry can't hold
  ten. Propose what comes *out*, not just what goes in.
- **No detailed narrative.** The narrative belongs in interview prep; the résumé gets the
  compressed claim ("diagnosed complex production issues across X, Y, Z").

---

## Cover letter

**Form:** prose, ~300–450 words: a full page with greeting and sign-off, and never more. The
ceiling is not a style preference. The reader is short of time and sceptical, and a letter
that can't prioritise is evidence about a candidate whose job is prioritising. Under ~200 words
reads as an afterthought. Structure matters more than raw length: three or four tight
paragraphs, each doing one job, read better than one dense block of the same length. If a build
pipeline turns single newlines into breaks, keep signature lines on their own lines.

**What the letter is for.** The résumé already carries the evidence; the letter's one job is
to get the user an interview. A hiring manager gives it ten or twenty seconds and skims for
three things: whether a person aimed this at this employer or sends everyone the same letter;
whether the user has done something like this work before; and whether they write clearly,
which the letter itself shows. Every rule below serves those three.

**Rules of the form:**
- **The opening paragraph names the role, why this role, and what ties the user's background
  to it, in about three sentences.** The tie is the thesis: the specific work the user would
  own here, taken from the part of the posting that describes the work, which says what this
  employer is buying and why the user fits. Specificity proves the posting was read; "I've done
  many things" proves nothing. A posting speaks in two registers: what the job is (what gets
  built, owned, fixed) and how the company likes to work (values, culture, method statements).
  A thesis can come from the JD and still come from the wrong part of it. To tell the two
  apart, ask what this person will be doing on a Wednesday. Weight the letter there; the second
  register gets a clause, not a paragraph.
- **Then a positioning summary: the written form of "tell us about yourself".** Two or three
  sentences: years, domains, the kinds of systems and contexts worked in, and the through-line
  that aims all of it at this role. It is the same thing as `prep`'s `01-about-me.md` opener,
  compressed to prose. A technology inventory is not positioning: a stack gets a clause where
  the role demands one, never a list, because the résumé carries the inventory. A through-line
  aimed at the role is positioning; a tour of achievements is the résumé again.
- **Don't mirror the posting's structure.** If a reader with the posting open can tell which
  requirement each paragraph answers (its lines quoted back, paragraph weight copied from the
  posting's emphasis, bridges like "you say X"), the letter reads as a requirements response,
  which is what template spam looks like. The JD decides which stories appear and how each is
  framed; the letter's structure is the user's own.
- **The why-them paragraph must be true of the user and not of the next applicant.** Admiration
  anyone could type, such as an impressive product or a resonant mission, reads as sent to
  everyone. The corpus earns this paragraph with real contact (the product used, the domain
  worked in, the problem met first-hand), or the paragraph stays short.
- **One story, told fully; a second only if both stay short.** Three or four sentences: the
  situation, the calls made, the measurable outcome. The story makes the thesis concrete; it
  does not survey the career. The résumé does the surveying, and a letter full of
  mini-anecdotes is a résumé with worse formatting. Tell it as a concrete moment, not a claim:
  a specific scene ("you can't un-summarise a monthly total back into rows") beats "I solve
  messy real-world problems". The corpus has the scenes; use them.
- **Introduce a story with the claim it proves.** One sentence of argument before the scene,
  tying it to the role's work, then the story as its evidence. A story the reader wasn't
  prepared for reads like a stray résumé bullet. Opening on a scene with no claim is an essay
  technique, and a letter is an argument.
- **Pick the story by honest relevance, not chronology or pride.** The story that matches what
  the role actually is carries the case. A marginal second match gets a clause, not a
  paragraph: material inflated past its relevance is the letter's version of an unsourced
  number.
- **Position in the lane the posting is in.** Answer a leadership role with judgment calls, org
  outcomes, and work done through others; answer a senior hands-on role with craft depth and
  cross-team leverage. The corpus often backs both, and the JD picks which framing the story
  gets. Strong evidence from the wrong lane reads as applying for a different job.
- **Write the story as the calls the user made, not the scope they held.** "Chose X over Y,
  cut Z" is evidence; "owned the platform" is a job description. A decision to kill or discard
  something is often the strongest line in the letter. Attribution rules apply as everywhere:
  `[HONEST-ATTRIBUTION]`, `[TRUE-VERSION]`.
- **Don't restate the résumé.** The reader has it. After the positioning summary, the letter
  carries what a bullet cannot: why the user did it that way, and what they were thinking at
  the time. A sentence that would work unchanged as a résumé bullet is in the wrong document.
- **Honest framing device or none.** A neat opener that claims more than the facts ("done it
  twice" when one instance only half-qualifies) will break under one interview question.
  Reframe to what is defensible word for word.
- **The letter never describes its own structure.** No "the shorter one", no "my second
  example": the argument itself connects the paragraphs.
- **Close with a plain ask, and put the practical facts there.** One plain line asking for the
  conversation. Location, timezone and availability go in the close and nowhere else. No
  throat-clearing, and no "I would welcome the opportunity" boilerplate if a plainer line is
  truer to their voice.

**A baseline (no JD) letter has a different shape, not a tailored letter with blanks.** Every
structural rule above depends on a posting: the thesis, the lane, which story gets the slot,
why-them. With no posting, all that remains of those rules is "tell a scene vividly", and a
fully told story that nothing selected reads as arbitrary. So a baseline leads with its
summary: the opening tie and the positioning summary for its role family carry it, stories get
one clause each at most, and a real JD later picks which one to expand. It is the draft a
tailored render starts from, not a finished letter; say so if the user is about to send one
unedited.

---

## Interview-prep answers

For a **booked** interview, `prep` owns this: it builds a whole pack against the employer's
criteria and writes it into the application folder. What follows is the shape of a spoken
answer on its own, for the ad-hoc case: rehearsing one story, or answering a question that
arrived outside a loop. `prep` renders answers in this shape too.

**Form:** spoken, longer than a bullet, structured but not stiff: stories that follow the
order an interview actually takes.

**Rules of the form:**
- **STAR rendered *from* prose, never as a filled-in template.** Situation, Task, Action and
  Result are an outline the corpus prose already fits, because the corpus stores arcs this way
  (setup, beats, outcome, what it cost).
- **Through-lines are talking points, not scripts.** Offer them as ways to connect stories,
  never as claims to recite. Let the interviewer's question pick the framing, as the JD does
  for a letter.
- **The rest is `prep`'s, and holds here too:** bullets and a first line, never a script
  (`[NO-SCRIPT]`); answer the follow-ups down to depth three (`[DEPTH-THREE]`); carry the
  mistake (`[CARRY-MISTAKE]`); and track which story is spent on which question
  (`[SPEND-STORIES]`). See [`../prep/SKILL.md`](../prep/SKILL.md).

---

## The outbound file

This applies to every artifact above, and only at the point one becomes a PDF or a DOCX. The
kit holds no stylesheet and has no opinion on how a page looks. It does have one on what the
file says.

A PDF carries two things: the image a person sees and the characters a machine extracts. They
can disagree, and when they do **nothing looks wrong**: the page is right, the extracted text
is not, and the first reader of an application is usually the extracted text. This is the same
distinction `[LENGTH-IS-THEIRS]` draws for the page ceiling: a design opinion is the user's, but
whether a reader can read the file is a fact about the reader.

A browser-based build breaks it in two ways, both invisible on screen:

- **Ligatures.** Some renderers map the fi/ff/ffi glyph to its Unicode presentation form
  (U+FB00–FB04) rather than to the letters it stands for. Every extractor then reads `staﬀ`,
  `ﬁrst`, `certiﬁed`, `workﬂows`, and a parser matching the posting's own "Staff" or
  "workflows" finds nothing. The affected words are ordinary and carry keywords, which makes
  this the more serious of the two. One declaration fixes it: `font-variant-ligatures: none` on
  the body.
- **List markers drawn as vector art.** A default bullet is often a vector path with no
  character behind it, so each bullet reaches a parser as an unmarked paragraph. Line structure
  survives and most parsers split on lines, so this is the less serious of the two. The fix
  emits a real character instead:

  ```css
  ul { list-style: none; }
  li { text-indent: -13.7px; }
  li::before { content: "\2022"; padding-right: 10px; }
  ```

  **Those two numbers are calibration, not constants.** They reproduce the default marker's
  geometry for one particular `ul` padding and body font size. Change the font and the bullets
  move; re-measure rather than carrying the numbers across.

Tell the user the trade-off: the bullet becomes a real `•` in the page's font rather than the
browser's drawn disc, so it sits slightly smaller. That is the cost of it being text, and
being text is the point.

**Verify by reading the text layer, never by eye.** Both defects render perfectly, so a fix
that looks correct on the page is not evidence. Extract the text and search it for the words
you expect, or check whether any font's `ToUnicode` table maps U+2022 and U+FB00–FB04. Confirm
the page count has not changed while you are there.

**A check that reports the same numbers before and after may not have run.** Rebuilds are the
usual cause: a stale file on disk, or a build that failed and left the last good output in
place. Compare a hash of the two files before you believe two readings that agree, and keep
one deliberately broken case around to confirm the check can still fail.
