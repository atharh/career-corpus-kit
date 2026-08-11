---
artifact: cover-letter
application: kestrel-freight-engineering-lead
lifecycle: submitted
generated: 2026-04-09
corpus_pin: a3f19c2
sources:
  - corpus/profile.md
  - corpus/tidewater/background.md
  - corpus/tidewater/batch-window.md
  - corpus/tidewater/oncall-rebuild.md
  - applications/kestrel-freight-engineering-lead/jd.md
  - applications/kestrel-freight-engineering-lead/fit.md
submitted:
  date: 2026-04-09
  as: PDF uploaded to the Kestrel careers form
  sha256: 1c07a5e93b6f4d28ae5710b2cf8934d6e0a17f45b93c28de6014ab7f3c2905ee
---

> ⚠️ **FICTIONAL EXAMPLE.** Rendered from the fictional corpus in `../../corpus/` against the
> fictional posting in `jd.md`. Never a source.

Dear hiring team,

Your posting is about an overnight build that depots need by 05:00, and about moving it without
anybody noticing. I have done the first thing for seven years and the second one once, carefully,
and I would rather tell you about the second one.

At Tidewater the nightly job that turns bookings into dispatch instructions had drifted from 40
minutes to over three hours, against a delivery time we owed customers contractually. Everyone
assumed volume, because bookings had roughly tripled. It was actually reprocessing every
historical partition on every run, so volume was just the multiplier on a design problem that
had been there from the start. Moving it to incremental processing roughly halved the runtime.

The part that matters for your posting is who owned the thing I was changing, which was not me.
The scheduler belonged to another team, and they did not want incremental state — a silently
stale dispatch file is worse than a late one, because a late file gets a phone call and a wrong
file sends a truck to the wrong depot. They were right and I could not argue them out of it. So
I ran both pipelines side by side for three weeks and compared the output every night. Two
watermark bugs turned up in week one. We cut over once the diffs came back clean, and I have
used that approach on every risky migration since.

You also want the on-call rotation to stop being something people endure. I rebuilt one. The
useful finding was that 19 of 31 pages in a quarter needed no human action — alerts on
conditions that cleared themselves faster than anyone could open a laptop. Out-of-hours pages
went from 31 to 9 across that year. I also got one part of that project badly wrong, made the
best responders' lives worse, and reversed it seven weeks later in public. That is the half I
would want to talk about.

One thing to be straight about, because you will find it in the first ten minutes otherwise: I
have never been anyone's manager. Eleven years, no reports. I have led projects, run on-call and
mentored two juniors through their first year, and none of that is the same as owning somebody's
growth or sitting on the other side of a performance conversation. If the lead part of this role
is the part you are hiring for, I am not the strongest candidate you will see, and I would
rather say that here than have it come out in round two.

Thanks for reading.

Sam Rivera
sam@example.com
