> ⚠️ **FICTIONAL EXAMPLE.** Rendered from the fictional corpus in `../corpus/` against an
> invented job description: *Senior Backend Engineer, data infrastructure team, mid-size health
> tech company.*

Dear hiring team,

I've spent the last seven years on the part of the system nobody demos: nightly pipelines,
report generation, and the pager that goes off when either one breaks. Your posting says the
data infrastructure team owns batch reliability alongside new pipeline work, and that
combination is most of what I've done.

The clearest example is a dispatch pipeline at Tidewater that had drifted from 40 minutes to
over three hours, against a delivery time we owed customers contractually. Everyone assumed
volume. It was actually reprocessing every historical partition on every run, so volume was
just the multiplier on a design problem that had been there since the beginning. Moving it to
incremental processing roughly halved the runtime.

The part I'd rather tell you about is how it shipped. Another team owned the scheduler and
didn't want incremental state, on the grounds that a silently stale dispatch file is worse than
a late one. They were right, and I couldn't argue them out of it. So I ran both pipelines side
by side for three weeks and compared the output every night. Two watermark bugs turned up in
the first week. We cut over after the diffs came back clean, and I've used that approach for
every risky migration since.

Your posting also mentions on-call as a shared responsibility rather than a rotation people
dread. I rebuilt one. The useful discovery was that 19 of 31 pages in a quarter needed no human
action — they were alerts on conditions that fixed themselves faster than anyone could open a
laptop. Out-of-hours pages went from 31 to 9 over the year. I also got one part of that project
badly wrong and had to reverse it, which I'm happy to walk through if it's useful.

Health tech is where I started, at a company selling scheduling software to clinics, so I have
some feel for what it means when the thing you're maintaining sits between a patient and an
appointment.

Thanks for reading.

Sam Rivera
sam@example.com
