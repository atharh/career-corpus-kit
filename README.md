# Career Corpus Kit

A [Claude Code](https://claude.com/claude-code) plugin for building a **career corpus** — a
private, high-depth record of your work history — and rendering résumés, cover letters, and
interview prep from it.

The premise: **your résumé is an output, not the source of truth.** A résumé bullet, a cover-
letter paragraph, and a spoken interview answer are the same fact compressed to three
different lengths. Most people author the compressed bullet and throw away the source — so
when an interviewer pushes, there's nothing underneath. This kit inverts that. You author your
career once, at full depth, in Markdown story files. Everything you send is *rendered* from
that corpus on demand and tailored to the specific role.

It's also how you stop forgetting your own career. Recall is triggered, not enumerated — you
remember the thing you did five years ago only when something adjacent jogs it. The interview
skill is built to do that jogging, and to write down what surfaces before it evaporates.

## The five skills

| Skill | When | What it does |
|---|---|---|
| **`/career-corpus:bootstrap`** | once, at the start | Reads your existing résumé/LinkedIn, sets up the corpus, and generates a prioritized queue of stories worth extracting. Gets you from empty to "start with this one." |
| **`/career-corpus:interview`** | corpus **in** | Interviews you about one memory and writes a vetted story file. Relentless, works in rounds of a few questions at a time, and it never lets a claim in that you can't defend. |
| **`/career-corpus:render`** | corpus **out** | Reads the vetted corpus + a job description and produces a résumé entry or cover letter — tailored to that role, sourced only from what the corpus vouches for. |
| **`/career-corpus:prep`** | an interview is booked | Builds a prep pack for one specific interview: an opener, a story bank mapped to the employer's own hiring criteria, the probes they'll push on with defensible answers, and questions to ask them. Run it again afterwards to capture what was actually asked. |
| **`/career-corpus:compact`** | maintenance | Prunes the sediment interviews leave behind — resolved gaps, dated back-and-forth — while guarding the lines that keep renders honest: your ceilings, rendering decisions, and rejected readings. Run it when a gap list has become more archive than queue. |

`render` produces documents you **send**. `prep` produces a directory you **study** — and its
second half feeds what you fumbled back into `interview`, which is where the loop closes.

### The skills learn your preferences

They ship generic, but they sharpen to *you* over time. When you correct one in a way that
generalises — a wording you won't use, a framing you reject, a repeated mistake — it appends a
one-line rule to `corpus/LESSONS.md` in your **private** repo and reads it back at the start of
every session. The method stays public and stable; your scar tissue stays private and personal.
That feedback loop — mistake → durable rule — is what makes a corpus setup genuinely yours.

## Install

In Claude Code:

```
/plugin marketplace add atharh/career-corpus-kit
/plugin install career-corpus@career-corpus-kit
```

That's it — the skills show up as `/career-corpus:bootstrap`, `/career-corpus:interview`,
`/career-corpus:render`, `/career-corpus:prep`, and `/career-corpus:compact`. If the install summary says `Run /reload-plugins to activate.`,
run that. Later, `/plugin marketplace update career-corpus-kit` pulls new versions.

<details>
<summary>Or: install from a clone, without the marketplace</summary>

```bash
git clone https://github.com/atharh/career-corpus-kit ~/career-corpus-kit
cd ~/career-corpus-kit
./install.sh
```

`install.sh` symlinks the repo into `~/.claude/skills/career-corpus`, where Claude Code picks
it up as a plugin, so a later `git pull` updates it. Same skill names either way. Don't use
both paths at once — two plugins named `career-corpus` would provide the same skills.

To scope it to one project instead, symlink the repo into that project's
`.claude/skills/career-corpus` and start Claude Code from the repo root.
</details>

## Quick start

1. **Make a private repo for your corpus.** It will contain real details about you and, in
   roles-only form, about people you've worked with. Keep it private, permanently.
   ```bash
   mkdir my-career && cd my-career && git init
   mkdir corpus
   ```
2. **Bootstrap from your résumé.** In Claude Code, from that repo:
   ```
   /career-corpus:bootstrap
   ```
   Paste in your résumé (and anything else you have). It sets up the corpus, writes
   `profile.md`, and hands you a ranked queue of the stories worth extracting first.
3. **Fill it, one story at a time.**
   ```
   /career-corpus:interview the hardest project I led at <company>
   ```
   Answer the questions. It writes a story file under `corpus/<company>/`, marks every open
   thread as a gap, and stops when you're out of energy. Come back and do another whenever a
   memory surfaces. Depth accretes.
4. **Render when you need to apply.** With a job description in hand:
   ```
   /career-corpus:render tailor a résumé and cover letter for this JD: <paste>
   ```
   Without a JD, it produces a strong *baseline* you maintain as a checkpoint. With one, it
   tailors from the corpus for that specific role.
5. **Prep when they call you back.**
   ```
   /career-corpus:prep loop booked for this role: <paste JD + recruiter email>
   ```
   Builds a study pack for that specific interview. Run it again the same day afterwards — what
   you fumbled goes back into the corpus, and it's better material than any question a model
   would have invented.

## What else you can do with it

Once the corpus exists, it's a sourced, dated record of your work — and a résumé is only the
most obvious thing to render from it. Each of these is just a prompt:

- **Résumés and cover letters** — the default path.
  `/career-corpus:render tailor a résumé and cover letter for this JD: <paste>`
- **Interview prep** — a full pack for one booked interview, mapped to the employer's own
  hiring criteria and including the questions they'll push back on.
  `/career-corpus:prep I have a loop next week for this role: <paste JD + recruiter email>`
- **Self-reviews and 360s** — performance season, written from your own evidence instead of a
  blank box at 11pm. Map the corpus onto whatever competency model your company uses.
  `/career-corpus:render a self-review for this cycle, grouped by these competencies: <paste rubric>`
- **Promotion packets** — a promo doc is a rubric plus evidence, and the corpus is the evidence.
  The second half of this prompt is the valuable half.
  `/career-corpus:render a promotion packet for <level> against this rubric: <paste> — and list every line I have no evidence for`
- **Gap analysis before you apply** — find out what your corpus *can't* support yet, while
  there's still time to do something about it.
  `/career-corpus:render compare my corpus against this JD and list what it can't back up — don't write anything yet: <paste>`
- **LinkedIn, bios, speaker blurbs** — the same facts at a different compression.
  `/career-corpus:render a LinkedIn About section and a 60-word conference speaker bio`
- **Post-interview capture** — the loop that compounds. Right after a real interview, record
  what you were asked and where you had nothing good to say.
  `/career-corpus:prep that interview is done — here's what they actually asked and where I fumbled`

The last one is worth doing even when you don't get the job. A question you couldn't answer is
the most precisely targeted gap you'll ever be handed — better than anything a model would
have guessed, because a real interviewer found it.

## See one before you build one

**[`examples/`](examples/)** holds a complete fictional corpus — one invented engineer, two
invented companies, three stories — and the résumé and cover letter rendered from it.

It's deliberately mid-flight rather than polished, because that's the state a real corpus is in
almost always: open gaps, one number the corpus refuses to resolve on the user's behalf, a
through-line the user withdrew, and a theory the model got wrong and had to record as its own
error.

If you read one file, read **[`examples/rendered/ANNOTATED.md`](examples/rendered/ANNOTATED.md)**.
It puts seven lines the model wanted to write next to what actually shipped, and names the
corpus rule that stopped each one:

| The tempting version | What shipped |
|---|---|
| "Cut pipeline runtime by 80%" | "roughly halving runtime" |
| "Drove org-wide adoption" | "Two other teams later adopted the same pattern" |
| "Led the team responsible for six services" | "Led a rebuild of the on-call rotation" |
| "Architected a data platform" | "Built and owned the nightly export and transform" |

Every one of those was survivable on paper and unsurvivable in the room, because each invites a
follow-up question the candidate can't answer. That gap is the entire thing this kit exists to
close.

## What makes the output trustworthy

The value isn't "an AI wrote my résumé" — anything can do that. It's a set of rules, each
learned by getting it wrong, that keep every rendered line defensible in the room:

- **Vetted facts only.** A claim reaches a résumé only if a story file sources it. Raw drafts
  live in `corpus/_inbox/` and are never rendered from.
- **Numbers carry a source and a ceiling.** "Doubled" never drifts to "tripled" because a
  reused draft made it sound better.
- **Vocabulary gets dated.** You don't get described using a tool or job title that didn't
  exist when you did the work — it's the fastest way to get caught.
- **Honest role attribution.** "Proposed and prototyped; the team delivered" never becomes "I
  built it." Bylines are checkable.
- **No names of private people; no internal codenames.** Roles only, always.
- **The true version wins.** In practice the accurate story is almost always stronger than the
  inflated one.
- **Nothing is applied silently.** You see a diff with a reason per change, and every genuine
  judgment call is surfaced as yours to make.

## Honest caveats

- **The tailoring step is the least-tested part.** Selecting and angling stories from a real
  job description is the newest capability here; treat early tailored drafts as strong first
  drafts and review the diff, don't trust the selection blindly.
- **It's only as good as your corpus.** The skills can't invent depth. The work is sitting for
  the interviews. That work is also the entire point — it's what nobody else will do, and it's
  why the output isn't generic.

## A note on where this came from

These skills were generalised from a working setup built for one person's real job search. The
private career details have been stripped out; what remains is the method and the hard-won
rules. If you find a rule cryptic, it's probably a scar — keep it.

Do what you like with this — [MIT](LICENSE). Attribution appreciated, not required.
