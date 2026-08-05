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

## The three skills

| Skill | When | What it does |
|---|---|---|
| **`/career-corpus:bootstrap`** | once, at the start | Reads your existing résumé/LinkedIn, sets up the corpus, and generates a prioritized queue of stories worth extracting. Gets you from empty to "start with this one." |
| **`/career-corpus:interview`** | corpus **in** | Interviews you about one memory and writes a vetted story file. Relentless, one question at a time, and it never lets a claim in that you can't defend. |
| **`/career-corpus:render`** | corpus **out** | Reads the vetted corpus + a job description and produces a résumé entry, cover letter, or interview-prep answers — tailored to that role, sourced only from what the corpus vouches for. |

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

That's it — the three skills show up as `/career-corpus:bootstrap`, `/career-corpus:interview`,
and `/career-corpus:render`. If the install summary says `Run /reload-plugins to activate.`,
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
