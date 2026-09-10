---
role: Software Engineer
track: ic
aliases: [SWE, engineer, backend engineer, frontend engineer, full-stack engineer, senior engineer, staff engineer, principal engineer, tech lead, platform engineer, infrastructure engineer]
---

## Scope by level

| | What is owned | What success is made of |
|---|---|---|
| **Engineer** | well-defined tasks inside a service someone else shaped | it works, it is tested, it did not need rework |
| **Senior engineer** | a service or a workstream end to end, including the ambiguity in it | it shipped, it holds up under load and change, the team's standard rose |
| **Staff / lead engineer** | multi-team goals; the seams and contracts between systems | others build on it without asking, and the standards hold unprompted |
| **Principal engineer** | org-wide technical direction, or the estate | something new to the company exists, other orgs run it without the author, and the technical choice had consequences wide enough to argue about |

## Dimensions

- **Diagnosis before action.** What the bottleneck actually was, measured, before anything was
  chosen. The strongest openings are a number that predates the work and explains its shape.
- **A baseline that predates the intervention.** Without one, every later before/after claim is
  unfalsifiable — and the teller usually doesn't notice until an interviewer does.
- **A thesis with a falsifier.** What they believed, and what evidence would have made them
  abandon it.
- **Written criteria with a date on them** — especially the criteria for killing something,
  agreed while everyone still liked it. Turns a later political fight into arithmetic.
- **Cost, disclosed by the author.** Money, compute, headcount, opportunity. Work that hides
  its cost gets cancelled by whoever finds it.
- **A safety case for the risky choice.** The bold design decision plus the budget, the circuit
  breaker, the escape hatch, the staged ramp and the rollback that made it defensible. Without
  these, the same decision reads as recklessness that happened to work.
- **The evaluation apparatus.** The labelled set, the holdout, the harness, the load test —
  whatever distinguishes an improvement from a regression. Its absence is what separates
  engineering from tinkering, and it is the artifact to reach for when asked what made this
  rigorous.
- **Measurement honesty.** Confounds named by the person reporting the number; causal claims
  declined where the design can't support them.
- **The failure, quantified.** Duration, blast radius in human terms, and the root cause owned
  — *our config was wrong*, not *the vendor changed something*.
- **A strategy-level misjudgment, caught and corrected in public**, that cost the teller
  something.
- **Dissent, manufactured where the environment suppressed it.** When objecting was a career
  risk, silence carried no information — so what channel did they build instead?
- **Second-order effects nobody asked them to measure**, including at least one that stayed
  unresolved.
- **Security, privacy or compliance handled before the thing shipped**, not after.
- **Durability.** Ownership, on-call, runbook, a deprecation path for their own work, and what
  was still running a year later.
- **Somebody who got better.** Named by role, with what the author actually did and how it
  showed in that person's work — not in the author's opinion of it. Senior ladders grade
  mentorship as heavily as design, and it is the beat engineers most often leave out.
- **Knowledge that outlived the author.** The doc, the talk, the review practice, the runbook
  other teams picked up. Distinct from durability, which is about the system; this is about
  what the people around it learned.
- **An organisational change they drove adoption for.** Not just a technical decision — a way
  of working other teams had to be persuaded into, and what the persuasion cost.
- **The claim boundary, drawn by the teller**, unprompted, with the story still good inside it.

## Named artifacts

RFC or design doc and the objections on it, technical spec, architecture decision record,
runbook, on-call rotation and its load, postmortem, load or chaos test, golden or labelled
evaluation set, benchmark harness, migration plan with a rollback, deprecation notice, service
level objective, dashboard, the review comment that changed a design.

## How stories in this craft overclaim

**Correlation dressed as causation.** A metric improved during the window the work shipped, and
the telling makes the work its cause — while a model upgrade, a traffic change and a training
push sat in the same window. Naming the confound is what makes every other number in the story
credible.

**Scale borrowed from the employer.** *"Serving millions of users"* is the company's scale, not
the author's scope. The defensible version is what they personally owned inside it.

**The tool as the achievement.** Adopting a technology is not the same claim as making it work
where it did not, and the second one is both smaller and much stronger.

## Pillar blind spots

**Talent** and **culture** — engineering stories are almost entirely results and craft, while
senior IC ladders grade mentorship, knowledge spread and cross-team persuasion as heavily as
design. A staff-plus exemplar with nobody in it who got better is missing a pillar the ladder
actually promotes on.
