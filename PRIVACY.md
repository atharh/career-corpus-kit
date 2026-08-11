# Privacy

Your corpus is the most sensitive thing this kit touches. It holds your work history in more
detail than any résumé, other people's names and correspondence, and sometimes an employer's
confidential material. The kit is built around that, but a few things are your call and worth
understanding before you paste anything in.

## Two classes of material

**Durable and yours** — `corpus/`. Story files, `profile.md`, `through-lines.md`, the queue.
Sensitive about you, but written to be kept: names of non-public people are already banned in
story bodies, internal codenames are already banned, and every claim carries its source.
This is what version control is *for*. Commit it.

**Raw and other people's** — every `_inbox/`. A recruiter thread with someone's real name and
contact details. A take-home brief that belongs to the company that sent it. An old
performance review with your manager's words in it. Unvetted by definition, and the material
you are least likely to want permanently.

`bootstrap` writes a `.gitignore` that keeps every `_inbox/` out of git. That is the default,
and it is the opt-*in* that's deliberate: to keep one file, `git add -f <path>` and mean it.

## Git does not forget

Once raw material is committed and pushed, deleting the file does not remove it. It stays in
history, in every clone, and in the forge's own copies — including in pull requests and
caches that survive a force-push. Rewriting history to remove it is possible, unpleasant, and
unreliable once anyone else has fetched.

So the safe order is: **extract first, commit second.** Drop material in `_inbox/`, run
`/career-corpus:interview` to pull the facts into a vetted story file with sources, then
delete the raw file. The story file is what you keep.

## An employer's confidential material

A take-home brief, an internal document, an unannounced product detail — these are not yours
to store. Prefer a **reference** over a copy: the link, or the path to where it already lives,
with the date. If you must keep a local copy to work on it, keep it outside the repo, and
record in `application.md` what it is and when you'll delete it.

Never commit it. Never put it in a public repo, a gist, or a paste.

## A private repo is not a private computer

This kit runs on a hosted model. When a skill reads a story file, that file's contents are
sent to the model provider — that is how it works at all, and no local file permission
changes it. "Keep the repo private" protects it from other *people*, which is a different
thing from never leaving the machine.

Practically: this is the same exposure as pasting the same text into a chat window, which is
what the alternative usually is. But decide it knowingly. If some material is too sensitive to
send to a model, it is too sensitive for the corpus, and the corpus is not where it goes.

## What never belongs in the corpus

- Credentials, tokens, API keys, `.env` files. Nothing here needs them.
- Other people's names — non-public third parties: colleagues, managers, interviewers,
  recruiters. The skills enforce roles-only in story bodies, and no names in filenames at all,
  because filenames get screenshotted and tab-completed in front of other people. Two things
  are not covered by this: your own identity, which is the point of `profile.md`, and public
  bylines — blog co-authors, conference speakers, anyone already named in public on the work.
- Internal codenames and unannounced products. They mean nothing to a reader and may be
  confidential.
- Anything you aren't free to keep — material prohibited by a contract you've signed, by an
  employer policy, by law, or by a confidentiality obligation you're under. This is the same
  test as the section above, applied to the whole corpus rather than one take-home brief: if
  you'd have to think about whether you're allowed to store it and send it to a model, that
  hesitation is the answer.

## If something did get committed

Assume it is public and act accordingly: rotate the credential, tell whoever owns the
material. Then clean history if it's worth it (`git filter-repo`, then force-push, then ask
the forge to expire its caches). Do the rotation first — it's the part that actually helps.
