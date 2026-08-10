# An example corpus

> ⚠️ **Everything in this directory is fictional.** Sam Rivera does not exist. Neither do
> Tidewater Logistics or Bellhaven Health. Every number, quote, and colleague is invented to
> illustrate the format.
>
> **Nothing here is a source, and it must never be copied into a real corpus as fact.** It lives
> under `examples/` rather than `corpus/` on purpose — in this kit, folder location is a truth
> claim, and the skills only ever read from a `corpus/` you point them at.

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
7. **[`corpus/LESSONS.md`](corpus/LESSONS.md)** — how the skills personalise. Ships empty, fills
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

## What this example is not

It's not a template to fill in. A corpus written to a template comes out as a form, and the
whole method depends on it being an interview instead. Run `/career-corpus:bootstrap` against
your own résumé and let the shape emerge from your own material — it will not look like Sam's,
and it shouldn't.
