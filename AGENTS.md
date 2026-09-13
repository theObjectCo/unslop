# Writing rules

Follow these for any prose a person will read: documentation, READMEs, commit messages, code
comments, release notes, emails, marketing copy, and status reports written back to whoever asked
for the work.

`SKILL.md` in this directory holds the full rule set with the reasoning. `anti-patterns.md` holds a
corpus of rejected sentences with the version that replaced each one. Read both before a substantial
piece of writing. The condensed list below is enough for a commit message or a comment.

## Do not

- Address the reader as "you" or speak as "we". Write descriptively instead.
- Use the transformation frame: "from X to Y", "turning X into Y", "bridging the gap".
- Build triads for rhythm. The number of items follows the subject.
- Glue noun pairs together for length: "clear and concise", "robust and scalable".
- Close a paragraph with a punchline, or with "not X but Y".
- Write fragments without a subject and a verb, including in form fields and table cells.
- Use filler vocabulary: `robust`, `seamless`, `leverage`, `empower`, `unlock`, `elevate`,
  `holistic`, `transformative`, `journey`, `landscape`, `delve`.
- Open a paragraph with an unverifiable generalisation about the world, or moralise.
- Use em dashes as the main punctuation.
- Give every item in a list the same amount of room.

## Do

- Include checkable specifics: numbers, tool names, file formats, durations, concrete outputs.
- Include at least one sentence the author would not have written unless it were true: a limit, a
  cost, a case the thing does not cover.
- Write links in full, with `https://`.
- Vary sentence length, because the content varies.
- Personify nothing. A component does not want, know or decide.

## Check before sending

Run the script over the draft:

```
python unslop.py draft.md
```

It flags the mechanical patterns and exits 1 when it finds any. It cannot see personification,
aphoristic openers or cadence, so re-read for those three by hand.
