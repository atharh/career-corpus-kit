> ⚠️ **FICTIONAL EXAMPLE.** Invented person, invented project, invented numbers. Never a
> source.
>
> ⚠️ **TRACKED ON PURPOSE.** `_inbox/` is git-ignored in a real corpus repo, and a doctor check
> should flag any tracked `_inbox/` file it finds there. This one is committed because
> `examples/` is not a corpus — the skills never read it, and a fixture with no unvetted
> material in it cannot demonstrate the rule that unvetted material is never a source. The
> exemption is the path: `examples/**/_inbox/`. See `examples/README.md`.

# Pasted 2026-03-09 — draft from a previous AI chat, about the Bellhaven Kafka work

**Unvetted.** AI-written prose from an earlier conversation, pasted as it arrived. An essay
shape, an arc, a moral — and every number in it is a model's guess at what "it worked for a
while" sounds like. Nothing here is a fact until Sam says it is.

---

## From Batch to Real Time: How I Brought Streaming to Bellhaven

When I joined the reporting effort at Bellhaven Health, our data pipeline was firmly stuck in
the past — a nightly batch job in a world that increasingly demanded answers now. Over a
nine-month initiative, I designed and delivered a streaming analytics platform on Apache
Kafka that fundamentally changed how the company thought about its data.

The results spoke for themselves. At its peak, the platform was processing over 2 million
events a day, and report latency dropped by 90% — from overnight to minutes. Adoption grew
month over month as more teams discovered what real-time data could do for them. Our EM,
Priya Nair, championed the project to leadership, and it became a cornerstone of the
engineering roadmap.

Looking back, the biggest lesson wasn't technical. It was that transformation starts with one
team willing to challenge the status quo — and that the best way to predict the future of
your data platform is to build it.
