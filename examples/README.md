# An example corpus, and an example application

> ⚠️ **Everything in this directory is fictional.** Sam Rivera does not exist. Neither do
> Tidewater Logistics, Bellhaven Health or Kestrel Freight Network. Every number, quote,
> colleague, job posting and recruiter email is invented to illustrate the format.
>
> **Nothing here is a source, and it must never be copied into a real corpus as fact.** It lives
> under `examples/` rather than `corpus/` on purpose — in this kit, folder location is a truth
> claim, and the skills only ever read from a `corpus/` you point them at.

Two trees, one for each lane of the kit. `corpus/` and `rendered/` are the corpus lane:
material in, artifacts out. `applications/` is the application lane: one job application from
the posting to the rejection.

The hardest thing to explain about a career corpus is what a *good* one looks like when it's
half-finished, which is the state it's in essentially always. So this example is deliberately
mid-flight: open gaps, one unresolved number, a withdrawn through-line, a rejected reading, and
a story that's thinner than the others.

## Read it in this order

1. **[`rendered/resume.md`](rendered/resume.md)** — the output. A perfectly ordinary,
   slightly understated résumé. This is the point: the corpus doesn't make your résumé sound
   impressive, it makes it survive follow-up questions.
2. **[`rendered/ANNOTATED.md`](rendered/ANNOTATED.md)** — **start here if you only read one
   file.** Seven lines the model wanted to write, what shipped instead, and the exact corpus
   rule that stopped each one.
3. **[`corpus/tidewater/oncall-rebuild.md`](corpus/tidewater/oncall-rebuild.md)** — a story with
   a real, specific, self-reported mistake in it, and a rendering decision explaining why the
   mistake stays out of the résumé and goes to the interview.
4. **[`corpus/tidewater/batch-window.md`](corpus/tidewater/batch-window.md)** — a disputed
   number the corpus refuses to resolve on the user's behalf, plus a rejected reading recorded
   as the model's error.
5. **[`corpus/bellhaven/reporting-migration.md`](corpus/bellhaven/reporting-migration.md)** — an
   `anachronisms_corrected` block. "Basically a data mesh" turned out to be a cron job and a
   second Postgres, and *data mesh* postdates the work by three years.
6. **[`corpus/through-lines.md`](corpus/through-lines.md)** — a pattern with its
   counter-example attached, and a second pattern the user withdrew.
7. **[`corpus/capabilities/postgresql.md`](corpus/capabilities/postgresql.md)** — one
   technology across the whole career: an index that owns no facts, a depth ceiling per claim,
   and the noes that make the yeses credible.
8. **[`corpus/LESSONS.md`](corpus/LESSONS.md)** — how the skills personalise. Ships empty, fills
   with the things you had to say twice.

## What to notice

- **The corpus is longer than the résumé by a factor of about fifteen.** That ratio is the
  whole design. Three résumé bullets sit on top of three story files, and the story files hold
  the answers to the questions those bullets invite.
- **Every number is either sourced or flagged.** One of them is flagged as disputed and does not
  appear in the résumé at all.
- **The user's own limits are written down as ceilings** — *"two teams, not the org"*, *"I led
  the work, not the team"* — so a later session can't quietly restore the bigger version because
  it reads better.
- **The model's wrong theories are kept**, dated, labelled as errors. They're recurrence
  prevention, and they're often better material than the theory was.
- **The gaps that remain are ones whose answers would change something.** Questions that would
  never reach a bullet, a letter, or a spoken answer aren't parked here — they're deleted.

---

# The application

[`applications/kestrel-freight-engineering-lead/`](applications/kestrel-freight-engineering-lead/)
is one application, opened against a fictional posting at a fictional freight company, run to a
rejection. Same candidate, same corpus, five weeks later.

It is deliberately an application that **did not work**, and it fails for the reason the fit
check named on day two.

## Read it in this order

1. **[`jd.md`](applications/kestrel-freight-engineering-lead/jd.md)** — the posting, captured
   verbatim between two markers. The markers are the point: `apply` forbids summarising into
   this file, and a boundary is what makes that checkable by something other than good
   intentions.
2. **[`fit.md`](applications/kestrel-freight-engineering-lead/fit.md)** — **start here if you
   only read one file.** Nine requirements, each with an evidence state, and the read at the
   bottom is *don't apply yet*.
3. **[`_inbox/2026-04-21-recruiter-note.md`](applications/kestrel-freight-engineering-lead/_inbox/2026-04-21-recruiter-note.md)**
   — the recruiter's reply. Fluent, confident, and full of claims about the team that nothing
   in the folder is allowed to repeat.
4. **[`cover-letter.md`](applications/kestrel-freight-engineering-lead/cover-letter.md)** — the
   last paragraph names the gap out loud rather than routing around it.
5. **[`04-probes-and-defences.md`](applications/kestrel-freight-engineering-lead/04-probes-and-defences.md)**
   — the prepared answer to the question Sam cannot answer, and then, at the bottom, that exact
   question arriving in the room.
6. **[`application.md`](applications/kestrel-freight-engineering-lead/application.md)** — the
   whole thread as a dated event log, opened to closed, fifteen lines.

## What to notice

- **The fit check said don't apply, Sam applied anyway, and the requirement it named is what
  the rejection cited.** That is the fixture working. `fit.md` gives the read; the last column
  is the user's, and the two disagree in writing, dated.
- **Two requirements have no corpus evidence and they get opposite responses.** One is
  *absent* — the corpus records eleven years with no reports and a ceiling in Sam's own words.
  One is *unwritten* — a withdrawn through-line mentions four months of streaming work that was
  never extracted. The state is called `no-corpus-evidence`, never `missing`, because the file
  can see which of the two it is roughly as well as you can from here: not at all.
- **The adjacent story is right there and nothing reaches for it.** "Mentored two juniors" would
  cover the line-management requirement for about one follow-up question. It stays classified as
  mentoring in `fit.md`, in the résumé, in the story bank, and in the room.
- **The recruiter's claims never become facts.** The team's size, the seat being new, the
  headcount, how far along the build already is — none of it appears in the letter, the résumé
  or the pack. The dates and the panel shape from the same email are used freely, because those
  are scheduling, not claims. The split is written down in the note itself.
- **The log has no `status:` field.** The last line is the status. Anything else is a second
  copy going stale on its own schedule — `apply`'s no-rollup rule `[NO-ROLLUP]`.
- **Every artifact says which corpus it came from.** `corpus_pin: a3f19c2` in the frontmatter of
  the résumé, the letter and every file in the pack, alongside the files it drew on, the date,
  a lifecycle state, and — for the two things that were actually sent — a hash of what went out.
  Same rule as the absent `status:` field, pointing the other way: none of that is recomputable from
  what is on disk, and a corpus that has moved on cannot be asked what it used to say.
- **`_inbox/` is committed here on purpose.** It is git-ignored in a real corpus repo, and a
  future doctor check should flag any tracked `_inbox/` file it finds in one. `examples/` is not
  a corpus — the skills never read it — so the exemption is the path, `examples/**/_inbox/`, and
  the file carries a banner saying so. A fixture with no unvetted material in it cannot
  demonstrate the rule that unvetted material is never evidence.

## What this example is not

It's not a template to fill in. A corpus written to a template comes out as a form, and the
whole method depends on it being an interview instead. Run `/career-corpus:bootstrap` against
your own résumé and let the shape emerge from your own material — it will not look like Sam's,
and it shouldn't.
