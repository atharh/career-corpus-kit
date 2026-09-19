# Apply — the sent stage

Read at stage 4 of [SKILL.md](SKILL.md), before writing the `sent` event, and whenever a check
reports on a `sent:` block, a `lifecycle:` value or a pin. `[PIN-THE-INPUTS]` and `[NO-ROLLUP]`,
which these rules lean on, are in SKILL.md.

## Rules specific to the sent stage

**A pin is a fingerprint, not a copy — so keep the copy.** `[PIN-NOT-ARCHIVE]` A `sha256`
settles one question and only one: whether a file the user still has is the file that went out.
It recovers nothing, and frontmatter is never an archive of what a reader saw. That matters
more than it reads, because **a generated artifact usually cannot be rebuilt**: PDF and DOCX
writers stamp a creation time into the output, so the same Markdown through the same tool
usually gives different bytes every run, and once the working copy is gone the sent file is
gone with it. Some tools can be pinned to a fixed timestamp and some ignore the attempt — but a
tool that is reproducible today still stops being so at its next upgrade, and the folder
outlives the toolchain. So
`git add -f <what went out>` at the moment the artifact freezes — the `sent` event, when its
`lifecycle:` becomes `submitted`. Before the freeze it is regenerable working state and belongs
nowhere near git; after it, it is the only evidence of what a reader saw.

This covers what the kit generated from committed source and nothing else. A PDF built from the
folder's own Markdown carries nothing the Markdown does not, so tracking it spends no privacy
the repo has not already spent. **Inbound binaries never qualify** — an employer's brief, a
recruiter's attachment, a scan — and that half of `bootstrap`'s `.gitignore` is what
`[FOLDER-IS-SENSITIVE]` is really for. Leave the ignore rules alone either way: a path pattern
cannot tell a frozen artifact from a working one, and one that tried would commit every
in-flight re-render.

Keep the hash for the case it was built for — bytes that genuinely cannot be tracked: sent from
another machine, uploaded to a portal that kept no copy, or a file the user declines to commit.
Opting out is theirs to choose and it is a real trade, so say what it costs rather than just
recording their answer: the sent bytes stop being recoverable. Growth from doing this is
bounded but monotonic — two or three files per application, once each, never rewritten.

**Never pin a hash inside the file it hashes.** `[PIN-NOT-SELF]` Writing the pin changes the
file, so the recorded value is wrong the instant it is saved and every later check reports
tampering that never happened. That is worse than having no pin: it manufactures alarms at
exactly the moment someone is trying to trust the folder. A pin references a different file, or
a delimited region of its own. The case that catches people is a form field taking **pasted
text** rather than an upload — there is no uploaded artifact to point at, so the obvious move is
to hash the answer's own Markdown, which the hash then invalidates. Hash a delimited block and
say where it begins and ends, or record the commit instead and skip the hash.

**Record which files the employer actually received.** `[SENT-NAMES-WHAT-WENT]` The `sent:`
block names them, and it is new information rather than a rollup: nothing else on disk knows
which of the things the user prepared went out. Without it, an artifact prepared and
deliberately not sent looks exactly like a defect — the thread reached `sent`, the file still
reads `lifecycle: in-flight`, and a check reports a problem that isn't one. Recording the fact
beats naming the condition, so this is also why there is no fourth `lifecycle:` value for
*prepared and not sent*: it is already expressible as absence from the list. Two invariants
follow, and they only work as a pair: everything in `artifacts:` carries `lifecycle: submitted`
— or something went out unfrozen — and nothing outside it does, or something is frozen that
nobody sent. Ask for the list; never infer it from what happens to be in the folder.

`baselines:` is for a thread that sent something living outside its folder — the maintained
résumé, a letter kept per role family — which is the normal shape of an application older than
the user's folder convention. Without it such a thread can say neither what went out nor that
nothing local did, because an empty `artifacts:` list reads as *nothing was sent*. **Baselines
are deliberately never held to `lifecycle: submitted`**: a baseline goes on being edited, and
freezing one would be wrong rather than merely noisy. One `baseline_pin` covers every file in
the list, because it pins a repo commit and not a file version — `git show <pin>:<path>`
recovers each of them as it stood. A per-file pin invites recording the commit that last
*touched* that file, which quietly asserts nothing else in the send had moved.
