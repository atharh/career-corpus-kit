---
artifact: study-pack-section
application: kestrel-freight-engineering-lead
lifecycle: in-flight
generated: 2026-05-06
corpus_pin: a3f19c2
sources:
  - corpus/profile.md
  - corpus/through-lines.md
  - corpus/tidewater/background.md
  - corpus/tidewater/batch-window.md
  - corpus/tidewater/oncall-rebuild.md
  - applications/kestrel-freight-engineering-lead/fit.md
---

> ⚠️ **FICTIONAL EXAMPLE.** Invented company, invented questions, invented candidate. Never a
> source.

# Probes and defences

Where the panel will push, and the answer. Sourced from the corpus's own disputed facts,
ceilings and open gaps, and from `fit.md`'s thin and no-corpus-evidence rows.

---

## The two the whole loop turns on

**"Tell me about a team you've grown."** There is no story here and there is not going to be
one. The answer is *"I haven't run a team. Eleven years, no reports."* — then the closest true
thing, which is two juniors mentored through a first year, named as mentoring and not upgraded.
Then hand it back: ask what the group needs in the first six months, because that is a real
question and it is better than filling the silence.

Do not reach for the on-call rebuild here. It is a story about a rotation, it is already spent
in section 4, and using it as a people-management answer is exactly the stretch `fit.md` refused
to make on 7 April.

**"Have you moved a workload onto Kafka?"** No. The corpus cannot back it and neither can Sam.
The closest true thing is a migration onto incremental processing, de-risked by a parallel run,
and the transferable part is the de-risking rather than the technology. Say that, and say that
the streaming work at the previous employer is four months Sam has never written down and is not
going to describe from memory in an interview.

## The numbers

**"You said the pipeline got faster — by how much?"** *Roughly halved.* Not the figure on the
old résumé. `corpus/tidewater/batch-window.md` records the two sources disagreeing and Sam
settling the floor both agree on. Volunteer the smaller number before being asked; "80% of what,
measured how" is a question with no good answer available.

**"How widely was the pattern adopted?"** Two other teams. Their ceiling, in their own words:
*"Two teams took it. Not the org. There are still batch jobs doing the exact same dumb thing
today."*

**"Did the on-call improvement hold?"** Unknown, and this is an open gap in
`corpus/tidewater/oncall-rebuild.md` from before this application existed. Q4 2023 is the last
number recorded and it is now 2026. The honest answer says the number, says when it stops, and
says what Sam would check first.

## The ceilings

**Kubernetes.** *"I use Kubernetes. I have never run a cluster."* The posting asks for operating
a footprint alongside the platform team. Deploys to it, has never operated one — say it in that
order, and say it before the technical screen finds it.

**"Led the team."** Never true. Led the work, ran on-call, mentored two. An engineering manager
establishes this in one question.

## The shape of the career

Eleven years, individual contributor throughout, applying to a lead posting. Nobody needs to
guess why that will be asked. The answer is the same as the cover letter's last paragraph and it
should sound like the same person saying it.

## Things not to say

- *"Cut runtime by 80%."* Withdrawn — see the numbers above.
- *"Drove adoption across the org."* Two teams.
- *"Identified an architectural flaw."* Rejected reading, recorded in the corpus as the model's
  error. Sam got woken up by it four times and fixed the thing hurting them.
- *"We designed the reporting schema."* A contractor designed it. Built and owned the export.
- Anything about Kestrel's internals that came from the recruiter rather than from Kestrel.

---

## After the panel — 2026-05-06

Written the same day, per the prep skill's post-interview step.

**What was actually asked, in the director round:**

- The parallel-run story, in the shape section 4 prepared. It landed.
- *"Tell me about a performance conversation that went badly."* Not "tell me about a team you've
  grown" — sharper, and pointed at the same hole. Sam had nothing and said so. It went as well
  as that can go, which is not very.
- *"Did the on-call number hold after you moved on?"* The open gap in the corpus, asked out loud
  by a real interviewer, three years after the last figure. Sam did not know.

**Routed to the corpus queue the same day** (`/career-corpus:interview`), and logged in
`application.md`:

1. The performance-conversation question. Whether there is anything at all here — a peer
   escalation, a contractor, a disagreement Sam had to carry — is worth one session, and the
   answer may still be no.
2. The on-call follow-up. It was already an open gap; a real interviewer asking it is the
   evidence that it deserves the lookup rather than another quarter parked.
3. The four months of streaming work that has never been written down. Second posting this year
   to want it.

**What this round proved about the pack.** The weak section was named at the top of
`interview-prep.md`, prepared honestly in this file, and asked about anyway — and the prepared
version of "no" is still a "no". Naming a gap makes it survivable, not absent.
