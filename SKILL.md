---
name: unslop
description: Rules for writing prose a person will actually read - documentation, READMEs, marketing copy, offers, profiles, emails, forum posts, commit messages, code comments and chat reports. Use before writing or revising any such text, in any language. Covers the patterns that give generated text away, a corpus of rejected sentences with their fixes, and a script that flags the mechanical ones.
---

# Unslop

Generated prose gives itself away through its rhythm. The facts can be right, the numbers checked,
the structure sound, and the sentences still fall into shapes nobody writes unprompted: triads,
closing punchlines, paired opposites, paragraphs of evenly weighted sentences. The list below covers
those shapes, and `unslop.py` catches the ones a pattern can reach.

It applies to anything a person reads. Not only external copy: the same rhythm shows up in commit
messages, in code comments, and in a status report written back to the person who asked for the
work.

## The core rule

Offer, not diagnosis. State what the thing is and what comes out of it. Do not describe the reader's
problem, do not promise an outcome, do not explain why it matters.

> Pencil sharpening, 2 EUR per pencil, sharpened while you wait.

> Your pencil is blunt, and a blunt pencil is slowing down your whole factory. We fix that.

## What not to do

- **No second person, no corporate first person.** "You will find", "we deliver", "our team" - that
  alternation is the single loudest tell. Write descriptively: what it is, what the output is, how
  long it takes, who does it.
- **No transformation frame.** "from X to Y", "turning X into Y", "bridging the gap between".
- **No triads built for rhythm.** Three adjectives, three examples, three bullet points. The number
  of items follows the subject.
- **No noun pairs used as filler.** "clear and concise", "robust and scalable", "algorithms and
  methods".
- **No "not X but Y" punchline**, and no closing sentence that restates the paragraph with a twist.
- **No telegraphic fragments.** "2-8 weeks, led by an engineer." "Output: a technical report."
  "Trusted by teams worldwide." Every sentence gets a subject and a verb, including inside short
  form fields.
- **No filler vocabulary:** `robust`, `seamless`, `cutting-edge`, `leverage`, `empower`, `unlock`,
  `elevate`, `holistic`, `transformative`, `journey`, `landscape`, `tapestry`.
  Also `in today's fast-paced world`, `it's important to note`, `let's dive in`,
  `at the end of the day`. The full list the script uses is at the top of `unslop.py`.
- **No aphoristic opener.** Do not start a paragraph with an unverifiable generalisation about the
  world ("Most teams never realise...", "Software rarely fails in one place") and do not moralise
  ("and they shouldn't have to"). The first sentence says what is on offer or what happens.
- **No em dashes as the main punctuation.** One in a document is a choice; one per paragraph is a
  habit.
- **No equal weight for every item.** The important thing gets more room than the minor one.

## The five habits to check for

None of these is visible in a single sentence. They show up across a paragraph, which is why the
re-read matters more than the first draft.

1. **"X rather than Y" as a recurring shape.** One real contrast is fine. The problem is the same
   construction carrying every other sentence. A single codebase pass turned up over forty of them,
   three of those in one paragraph.
2. **A punchline closing the paragraph** - a short sentence restating the point with a twist.
3. **Personification.** The component "wants", the panel "knows", the folder "nobody comes back to",
   the API "decides". In code comments this is the most frequent of the five by a wide margin.
4. **Triads for rhythm:** "its name, its type and its access".
5. **Sentences arranged for the sound of them instead of the information in them.** The test is to
   cut the sentence in half and see whether anything was lost.

The fix is the same every time. Plain declaratives, one idea per sentence, length set by the
content, no flourish at the end. State a limitation outright instead of building up to it.

## What to do

- Include checkable specifics: numbers, tool names, file formats, concrete outputs, durations.
- Include at least one sentence the author would not have written unless it were true: a limit, a
  cost, "this takes six months", "not suitable for X".
- Write titles that read like a line item in a price list. 60 to 80 characters even when more are
  allowed.
- Write links in full, with `https://`, including in notes and text meant for pasting.
- Vary sentence length. Short next to long, because the content varies.

## Sets of texts

Several entries side by side: a service list, a price list, a set of project descriptions, a
marketplace profile.

- Each entry owns its subject and does not borrow sentences from its neighbour. The integration
  story belongs to the integration entry. Spread across every entry in small pieces, it leaves each
  one telling half of it.
- No shared template: different paragraph shapes, different endings. One "delivered for A, B and C"
  per set, one stack list per set.
- Where a short and a long description sit together, the long one repeats none of the short one.
- One fact has one wording across the whole set: the same sector name, the same project count, the
  same name for the deliverable.
- **The template is invisible inside a single entry.** Reading entries one at a time will not find
  it. Read the whole set in a row, or hand the set to a separate reviewer whose only job is to find
  the repeated shape. A real set needed four rounds of this before the template was gone.

## Procedure

1. Write it.
2. Run `unslop.py` over the file, or pipe the text in. It flags the mechanical patterns: em dashes,
   the transformation frame, filler vocabulary, first and second person, telegraphic fragments,
   triads, bare links, uniform sentence length, punchline candidates. It does not catch
   personification, aphoristic openers, or cadence, so those still have to be read.
3. Re-read for the five habits above.
4. Give **one** corrected version. Not a menu of options, unless a choice was asked for.

`anti-patterns.md`, beside this file, holds the corpus: rejected sentences, what was wrong with each,
and the sentence that replaced it. Read it when something sounds wrong and the reason will not come.
The same shape is usually in there under different content.

## Running the script

```
python unslop.py draft.md
python unslop.py docs/*.md
cat draft.md | python unslop.py
```

Each finding prints the line, the matched text and a one-line reason. A finding is not a verdict. One
genuine "not X but Y" in a document is fine; six of them is a shape. The script exits 0 when it finds
nothing and 1 when it finds something, so it can be wired into a pre-commit hook if that is wanted.
