# Unslop

A skill for Claude Code that catches the patterns making prose read as generated. The checker runs
on its own too, with no agent involved.

The tells are in the rhythm. A draft can be accurate and still announce itself through the shapes
its sentences fall into. Those shapes survive an edit for accuracy, because nothing in them is
wrong.

`SKILL.md` is the rule set. `anti-patterns.md` is a corpus of rejected sentences with the version
that replaced each one. `unslop.py` flags the patterns a regular expression can reach.

Nothing here is tied to one product. `SKILL.md`, `AGENTS.md` and `anti-patterns.md` are markdown,
`unslop.py` is Python with no dependencies, and the rules themselves predate any of the tools below.
The only part that follows a vendor convention is the YAML header on `SKILL.md`, which is what makes
Claude Code load it without being asked.

## Claude Code

As a plugin, which is one command and updates in place:

```
/plugin marketplace add theObjectCo/unslop
/plugin install unslop@unslop
```

Or as a plain skill directory, which keeps the files visible and editable:

```
# for every project on this machine
git clone https://github.com/theObjectCo/unslop ~/.claude/skills/unslop

# for one repository, checked in with it
git clone https://github.com/theObjectCo/unslop .claude/skills/unslop
```

Either way it loads on its own when there is prose to write or revise, and on request with
`/unslop`. The repository is both the skill and its own single-plugin marketplace, so the same
files serve both routes.

## Other agents

The same rules, in the file each tool reads. `AGENTS.md` is the condensed version and stands on its
own; every one of these can also be pointed at `SKILL.md` for the full set.

| Tool | Where the file goes |
| --- | --- |
| Codex, Jules, Zed, anything following the AGENTS.md convention | `AGENTS.md` at the repository root |
| Cursor | `.cursor/rules/unslop.mdc`, with `alwaysApply: true` in its header |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cline | `.clinerules/unslop.md` |
| Windsurf | `.windsurf/rules/unslop.md` |
| Aider, Continue, anything with a system prompt | paste `AGENTS.md` into it |

For a tool that reads only one instruction file, append the contents of `AGENTS.md` to whatever that
file already says. The rules do not depend on anything else being present.

## Running the script without Claude

Python 3.8 or newer, no dependencies.

```
python unslop.py draft.md
python unslop.py docs/*.md
cat draft.md | python unslop.py
```

Output is one line per finding: file, line, severity, rule, the matched text, and why it was
flagged. Exit status is 1 when there is at least one finding, so it works in a pre-commit hook.

Findings marked `HARD` are patterns that are almost never the right call: filler vocabulary, the
transformation frame, bare links, label-and-value fragments, second person. Findings marked `CHECK`
are candidates, and being flagged is not a verdict. Triads, parallel clauses, oppositions and em
dashes are also counted per file, and the script says so when a count crosses the line between a
choice and a habit.

Fenced code blocks, indented code and block quotes are skipped, and so is anything inside quotation
marks or backticks, since that is how a document quotes the writing it is arguing against. The
quotation check runs a line at a time, so a quotation that wraps onto a second line is only skipped
as far as the line break. Markdown headings and table rows are checked for vocabulary but not for
sentence shape.

### What the script cannot see

Three of the five habits in `SKILL.md` are out of reach for pattern matching and need a reader:

- **Personification.** "The component wants", "the folder nobody comes back to". Grammatical,
  specific, and the most common of the five in code comments.
- **Aphoristic openers** beyond the handful of fixed phrases in the list.
- **Cadence.** Sentences arranged for the sound of them instead of the information in them. The
  script measures the spread of sentence lengths and flags a file where it is too even, which finds
  some of these and misses the rest.

A clean run means the mechanical patterns are gone, which is a lower bar than the text being good.

## Where the rules came from

Editing sessions where a human rejected sentence after sentence and said why. The corpus in
`anti-patterns.md` is those sentences, generalised to remove anything identifying, each with the
replacement that was accepted. One pass over a mid-sized codebase rewrote 337 comment blocks across
74 files under these rules, which is where the code-comment examples come from.

The rules are opinionated and some of them will not suit every house style. The list is meant to be
edited: delete a rule that does not fit, add the phrase a particular set of drafts keeps reaching
for.

## Licence

The licence is MIT, in the `LICENSE` file.
