# Anti-patterns

Sentences that were written, rejected, and replaced. Each entry gives the original, what was wrong
with it, and the sentence that went in instead. The originals are real drafts, generalised to
remove anything identifying.

Read this when a sentence sounds wrong and the reason will not come. The shape is usually in here
under different content.

---

## Aphoristic opener

> Most people who need to look at a 3D model do not have a CAD licence and should not need one.

An unverifiable generalisation about the world, followed by moralising. Two tells in one sentence,
and it delays the first fact to the second sentence.

**Replaced with:** Operators, sales staff and customers open the same 3D model as the engineers, in
a browser.

---

## The same figure stretched over two sentences

> Before the work package starts, a consortium needs to know whether the method will hold up outside
> the lab. This study answers that question.

A lecture about what the reader must know, then a question, then a punchline claiming to answer it.
The aphoristic opener wearing a longer coat.

**Replaced with:** The study checks whether an algorithm that runs on its author's machine also runs
on the partner's data, on the partner's hardware.

---

## Explaining the obvious to an expert

> A scan of a used part arrives as a cloud of points, and before the part can be repaired,
> remanufactured or inspected, that cloud has to become geometry a factory can use.

Explains to a specialist what a point cloud is. Adds the "before X, Y must happen" drama, a triad
(repaired, remanufactured, inspected) and an empty qualifier ("a factory can use").

**Replaced with:** Point clouds and meshes from scanned parts are processed into CAD geometry:
aligned to the design, segmented, compared against it, then repaired or rebuilt as parametric models
with tolerances.

---

## Announcement instead of content

> This is the capability the team was built around.

> In a consortium, the division of labour is simple.

Both promise that something is about to be said, and say nothing. Delete and start with the content.

---

## Telegraphic fragment

> 2-8 weeks, led by an engineer.

The sentence has no subject and no verb. It turns up most often in form fields, where it reads as a
database record instead of a sentence.

**Replaced with:** The work takes two to eight months and is run by one engineer, not a team.

---

## The transformation frame

> Technical consulting: from a research result to a software specification a consortium can build.

"From X to Y", 107 characters, and abstract at both ends. The colon is doing the work a verb should
do.

**Replaced with:** Feasibility study and software architecture for a research demonstrator.

---

## Triad, noun pair and transformation in one line

> Feasibility studies, software architecture and proof-of-concept work for turning algorithms and
> lab methods into tools industrial users can operate.

Three items chosen for rhythm, a noun pair glued together for length ("algorithms and lab methods"),
"turning X into", an empty verb ("operate"), and no finite verb anywhere in the sentence.

**Replaced with:** The result is a software architecture and a proof of concept running on the
industrial partner's own data, usually within two months.

---

## Alternating between reader and company

> You have an algorithm that works on your data. We check whether it survives contact with a
> production line.

The rhythm gives it away before the content registers.

**Replaced with:** The study takes an algorithm that works on its author's data and checks whether
it survives contact with a production line.

---

## The "not X but Y" punchline

> Every engagement is led by an engineer who has shipped such tools before, not by a consultant.

The negative half exists to make the positive half land. It also picks a fight with a job title
instead of stating a fact.

**Replaced with:** One engineer runs the engagement and hands over the result.

---

## Personification

> The component wears the icon it was given.

> A working folder nobody comes back to.

> The panel wants to stay the way it was arranged.

Objects do not wear, want, or come back. In code comments this is the most common habit of the five
and the easiest to fix, because the real subject is always nearby.

**Replaced with:** The icon set on the component, or null for the default.

**Replaced with:** A working folder that nothing has compiled from in a week.

**Replaced with:** The arrangement is saved in the document, so it survives reopening the file.

---

## "X rather than Y" as a skeleton

> Read from the assembly rather than from a file, because an icon read from disk registers in a
> debug build rather than in a release one, which is a trap worth avoiding rather than discovering.

One genuine contrast per document is fine. Three in a sentence is a shape. Watch for it in
comments explaining a decision, where it multiplies fastest.

**Replaced with:** Read from the assembly, not from a file. An icon loaded from disk registers in a
debug build and silently fails to in a release one.

---

## Closing punchline

> The code is not stored on disk, because the code lives in the document.

The sentence adds nothing the previous one did not say; it exists to close the paragraph with a
beat. Delete it, or promote the one fact inside it.

**Replaced with:** (deleted - the preceding sentence already said where the code is stored)

---

## Cadence over information

> A jump leaves you wondering which way the canvas went; a short move shows you.

Two clauses balanced against each other, second person, and a claim about the reader's mental state.
Cutting it in half loses nothing.

**Replaced with:** A jump gives no indication of which direction the canvas travelled.

---

## Equal weight for unequal things

A list where a two-year certification and a one-afternoon file conversion get the same three lines
each. Length is a claim about importance, and an even list claims everything matters the same.

**Fix:** Give the important item a paragraph and the minor one a clause, or drop the minor one.

---

## Filler vocabulary

> A robust, seamless pipeline that empowers teams to unlock insights across the data landscape.

Nothing in this sentence can be checked, and removing every adjective removes no information.

**Replaced with:** The pipeline ingests 40 GB a day and answers queries in under two seconds at the
95th percentile.

---

## The bare link

> More at example.org/demo

Fails to be clickable in plain text, in a terminal, in a form field and in a pasted note.

**Replaced with:** More at https://example.org/demo
