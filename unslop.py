#!/usr/bin/env python3
"""Flags the mechanical tells of generated prose.

Reads files named on the command line, or standard input when there are none. Prints one line per
finding and exits 1 if there was at least one, so it can run in a hook.

The checks here are the ones a regular expression can make: vocabulary, person, sentence shape,
punctuation, link form. Three of the habits in SKILL.md are out of reach for this script -
personification, aphoristic openers beyond a few fixed forms, and sentences arranged for cadence.
Those need a reader.
"""

import re
import sys
from statistics import mean, pstdev

HARD = "HARD"
CHECK = "CHECK"

FILLER = [
    "robust", "seamless", "cutting-edge", "state-of-the-art", "leverage", "leveraging",
    "empower", "empowers", "empowering", "unlock", "unlocks", "unlocking", "elevate",
    "elevates", "holistic", "transformative", "game-changer", "game-changing", "synergy",
    "paradigm", "journey", "landscape", "tapestry", "delve", "delves", "realm", "myriad",
    "plethora", "bespoke", "turnkey", "best-in-class", "world-class", "next-generation",
    "supercharge", "streamline", "streamlined", "frictionless", "effortless",
]

PHRASES = [
    ("in today's fast-paced world", HARD, "opens with a generalisation nobody will check"),
    ("in today's world", HARD, "opens with a generalisation nobody will check"),
    ("it's important to note", HARD, "says that something matters instead of saying it"),
    ("it is important to note", HARD, "says that something matters instead of saying it"),
    ("it's worth noting", HARD, "says that something matters instead of saying it"),
    ("let's dive in", HARD, "announces the text instead of starting it"),
    ("at the end of the day", HARD, "filler; the sentence works without it"),
    ("when it comes to", CHECK, "usually deletable with no loss"),
    ("needless to say", HARD, "then do not say it"),
    ("that being said", CHECK, "usually deletable with no loss"),
    ("clear and concise", HARD, "noun pair glued together for length"),
    ("robust and scalable", HARD, "noun pair glued together for length"),
    ("fast and reliable", HARD, "noun pair glued together for length"),
    ("safe and secure", HARD, "noun pair glued together for length"),
    ("simple and intuitive", HARD, "noun pair glued together for length"),
    ("quick and easy", HARD, "noun pair glued together for length"),
    ("tried and tested", HARD, "noun pair glued together for length"),
    ("bridge the gap", HARD, "transformation frame"),
    ("bridging the gap", HARD, "transformation frame"),
    ("is only useful if", CHECK, "aphorism used as an opener"),
    ("should not need", CHECK, "moralising"),
    ("shouldn't have to", CHECK, "moralising"),
    ("trusted by", CHECK, "claim with nothing checkable in it"),
]

# Finite verbs and auxiliaries common enough that a sentence without any of them is probably a
# fragment. Imperatives are in here too, so "Write it." does not get flagged.
VERBS = set("""
is are was were be been being am has have had do does did will would can could shall should may
might must get gets got make makes made take takes took give gives gave go goes went come comes
came run runs ran see sees saw know knows knew think thinks use uses used find finds found want
wants need needs needed work works worked call calls called try tries tried ask asks asked keep
keeps kept let lets put puts say says said show shows showed write writes wrote read reads build
builds built send sends sent open opens opened close closes closed set sets start starts started
stop stops stopped hold holds held bring brings brought happen happens happened return returns
returned become becomes became leave leaves left mean means meant add adds added check checks
checked cover covers covered carry carries carried report reports reported answer answers answered
appear appears appeared apply applies applied arrive arrives arrived belong belongs cost costs
delete deletes deleted depend depends draw draws drew exist exists expect expects fail fails
failed fix fixes fixed follow follows followed include includes included install installs
installed list lists listed load loads loaded look looks looked move moves moved pass passes
passed pick picks picked produce produces produced provide provides provided read reduce reduces
remain remains remove removes removed replace replaces replaced require requires required save
saves saved sit sits sat solve solves solved stay stays stayed store stores stored support
supports supported turn turns turned wait waits waited watch watches watched deliver delivers
delivered offer offers offered handle handles handled accept accepts accepted allow allows
allowed avoid avoids avoided begin begins began break breaks broke bring build change changes
changed choose chooses chose collect collects collected compare compares compared connect
connects connected consider considers contain contains continue continues create creates created
decide decides decided describe describes described design designs designed develop develops
enable enables enabled end ends ended enter enters entered explain explains explained fill fills
filled finish finishes finished fit fits force forces forced gather gathers generate generates
grow grows grew help helps helped hide hides hid identify identifies improve improves improved
increase increases indicate indicates introduce introduces join joins joined lead leads led learn
learns learned lose loses lost manage manages managed mark marks marked match matches matched
measure measures measured miss misses missed name names named note notes noted notice notices
obtain obtains occur occurs offer order orders ordered own owns owned pay pays paid perform
performs place places placed plan plans planned point points pointed prefer prefers prepare
prepares present presents prevent prevents print prints printed process processes processed
protect protects prove proves proved publish publishes published pull pulls pulled push pushes
pushed raise raises raised reach reaches reached receive receives received recognise recognises
record records recorded refer refers reflect reflects register registers registered reject
rejects relate relates release releases released rely relies render renders rendered repeat
repeats repeated request requests requested reset resets resolve resolves resolved respond
responds rest rests restore restores restored result results resulted reveal reveals review
reviews reviewed rewrite rewrites rewrote round rounds rounded scale scales scaled search
searches select selects selected serve serves served share shares shared ship ships shipped sign
signs signed skip skips skipped sort sorts sorted sound sounds sounded speak speaks split splits
spread spreads stand stands stood state states stated suggest suggests suggested supply supplies
switch switches switched teach teaches test tests tested track tracks tracked train trains
trained transfer transfers treat treats treated understand understands update updates updated
upload uploads validate validates verify verifies wrap wraps wrapped yield yields yielded
override overrides overrode implement implements press presses click clicks type types declare
declares compile compiles compiled restore restores restored disable disables copy copies paste
pastes expose exposes derive derives inherit inherits annotate annotates drag drags drop drops
edit edits edited dock docks docked bake bakes baked
""".split())

ABSTRACT_OPENERS = re.compile(
    r"^(Most|Every|Everyone|Everybody|Nobody|No one|Anyone|Anybody|All|Many|Few|Some|People|"
    r"Teams|Companies|Engineers|Developers|Users|Software|Technology|Businesses)\b",
)

TLDS = "com|org|net|io|dev|ai|app|co|sh|me|eu|info|tech"


def findings_for(text, name):
    out = []
    lines = text.split("\n")
    prose = strip_code(lines)

    for number, line in enumerate(prose, 1):
        if line is None:
            continue
        line = blank_quotations(line)
        low = line.lower()

        for word in FILLER:
            for hit in re.finditer(r"\b" + re.escape(word) + r"\b", low):
                out.append((number, HARD, "filler", hit.group(0),
                            "cannot be checked; deleting it deletes no information"))

        for phrase, level, why in PHRASES:
            start = low.find(phrase)
            if start >= 0:
                out.append((number, level, "phrase", phrase, why))

        for hit in re.finditer(r"\b(you|your|yours|we|our|ours|we're|we've|let's)\b", low):
            out.append((number, HARD, "person", hit.group(0),
                        "the you/we alternation is the loudest tell; write descriptively"))

        for hit in re.finditer(r"\bfrom\s+(\w+)(?:\s+\w+){0,2}\s+to\s+(\w+)", low):
            if not (hit.group(1).isdigit() or hit.group(2).isdigit()):
                out.append((number, HARD, "transformation", hit.group(0),
                            "the from X to Y frame"))

        for hit in re.finditer(r"\b(turn|turning|turns|transform|transforming|transforms)\b"
                               r"[^.]{0,40}\binto\b", low):
            out.append((number, HARD, "transformation", hit.group(0)[:50],
                        "the turning X into Y frame"))

        for hit in re.finditer(r"\brather than\b|\bnot\s+\w+[^.]{0,40}?\bbut\b|,\s*not\s+\w+", low):
            out.append((number, CHECK, "opposition", hit.group(0).strip()[:50],
                        "fine once; a habit when it is the shape of every other sentence"))

        for hit in re.finditer(r"\b[\w-]+,\s+[\w-]+,?\s+and\s+[\w-]+\b", line):
            out.append((number, CHECK, "triad", hit.group(0)[:50],
                        "three items: check the count comes from the subject, not the rhythm"))

        # Three or more parallel clauses, each of them several words long: "the facts can be right,
        # the numbers checked, the structure sound". A plain list of names is not this, which is why
        # every member has to carry at least three words before it counts.
        member = r"[\w'`()-]+(?:\s+[\w'`()-]+){2,}"
        for hit in re.finditer(r"(?:%s,\s+){2,}%s" % (member, member), line):
            out.append((number, CHECK, "parallel", hit.group(0)[:50],
                        "a run of parallel clauses, which is a triad with more members"))

        if re.search(r"\s—\s|\s--\s", line):
            out.append((number, CHECK, "em dash", "—",
                        "one per document is a choice, one per paragraph is a habit"))

        # The trailing guard lets a domain end a sentence but keeps it from matching part of a
        # longer name, so docs.example.com. is a link and example.company.name is not.
        for hit in re.finditer(r"(?<![\w/@.:])((?:[\w-]+\.)+(?:" + TLDS + r"))(?![\w@])(?!\.\w)",
                               line):
            # A capitalised name with no path after it is a product, not an address: Claude.ai,
            # Framer.app. A real bare link is lower case, or carries a path.
            product = hit.group(0)[0].isupper() and not line[hit.end():hit.end() + 1] == "/"
            if not product and "://" not in line[max(0, hit.start() - 8):hit.start()]:
                out.append((number, HARD, "bare link", hit.group(0),
                            "write links in full, with https://"))

        if re.match(r"^\s*(Output|Result|Deliverable|Duration|Stack|Timeline|Scope)\s*:", line):
            out.append((number, HARD, "telegraph", line.strip()[:40],
                        "a label and a value, not a sentence"))

    out.extend(sentence_findings(prose))
    return [(name,) + f for f in out]


def strip_code(lines):
    """Blanks out what is not the author's own prose: code blocks, indented code, block quotes."""
    kept = []
    fenced = False

    # YAML front matter is metadata a machine reads, not prose a person reads.
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                lines = [""] * (index + 1) + lines[index + 1:]
                break

    for line in lines:
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            fenced = not fenced
            kept.append(None)
            continue
        quoted = line.lstrip().startswith(">")
        kept.append(None if fenced or quoted or line.startswith("    ") else line)
    return kept


def blank_quotations(line):
    """Replaces quoted text and code spans with spaces, keeping every column where it was.

    A document about bad writing is full of bad writing in quotation marks, and so is any honest
    style guide. Quoted material belongs to whoever is being quoted.
    """
    out = list(line)
    for hit in re.finditer(r"\"[^\"]*\"|`[^`]*`|“[^”]*”|«[^»]*»", line):
        for index in range(hit.start(), hit.end()):
            out[index] = " "
    return "".join(out)


def split_sentences(text, at_offset):
    """Splits on end punctuation followed by a capital, which leaves example.org in one piece."""
    out = []
    start = 0
    for boundary in re.finditer(r"[.!?]+[\"')\]]*\s+(?=[A-Z\d\"'(\[])", text):
        piece = text[start:boundary.end()].strip()
        if piece:
            out.append((piece, at_offset(start)))
        start = boundary.end()
    tail = text[start:].strip()
    if tail:
        out.append((tail, at_offset(start)))
    return out


def is_fragment(words):
    """True when nothing in the sentence can be a finite verb. Deliberately cautious.

    A word counts as verb enough if it is in the list, or if it ends in ed, ing or s. That last one
    lets plural nouns through and so misses some fragments, which is the trade this check makes: a
    false alarm on a correct sentence costs more than a fragment that slips past.
    """
    if not 2 <= len(words) <= 10:
        return False
    for word in words:
        low = word.lower()
        if low in VERBS or low.endswith(("ed", "ing")) or (len(low) > 3 and low.endswith("s")):
            return False
    return True


def flatten(paragraph):
    """Joins a paragraph into one string and answers a function mapping an offset to a line."""
    text = ""
    starts = []
    for number, line in paragraph:
        starts.append((len(text), number))
        text += line + " "

    def at_offset(offset):
        found = starts[0][1]
        for start, number in starts:
            if start <= offset:
                found = number
            else:
                break
        return found

    return text.strip(), at_offset


def sentence_findings(prose):
    """Checks that need a whole sentence or a whole paragraph."""
    out = []
    paragraphs = []
    current = []

    for number, line in enumerate(prose, 1):
        # A heading or a table row is not a sentence and is not expected to read like one.
        heading = line is not None and re.match(r"^\s*(#{1,6}\s|\||!\[|\[!)", line)
        if line is None or heading or not line.strip():
            if current:
                paragraphs.append(current)
                current = []
            continue
        current.append((number, line))
    if current:
        paragraphs.append(current)

    lengths = []

    for paragraph in paragraphs:
        joined, at_offset = flatten(paragraph)
        if not joined.strip():
            continue

        sentences = split_sentences(joined, at_offset)
        if not sentences:
            continue

        for text, line in sentences:
            words = re.findall(r"[\w'-]+", text)
            lengths.append(len(words))
            if is_fragment(words) or re.match(r"^\d+\s*[-–]\s*\d+\s+\w+,", text):
                out.append((line, CHECK, "telegraph", text[:50],
                            "no finite verb; give it a subject and a verb"))

        opener, line = sentences[0]
        opener = re.sub(r"^[#>*\-\d.\s]+", "", opener)
        if ABSTRACT_OPENERS.match(opener) and not re.search(r"\d", opener):
            out.append((line, CHECK, "opener", opener[:50],
                        "opens with a generalisation about the world; start with the fact"))

        if len(sentences) > 1:
            closer, line = sentences[-1]
            words = re.findall(r"[\w'-]+", closer)
            if len(words) <= 12 and re.match(r"^(That|This|It|Which|And that)\b", closer):
                out.append((line, CHECK, "punchline", closer[:50],
                            "short closing sentence restating the paragraph"))

    if len(lengths) >= 6:
        spread = pstdev(lengths) / mean(lengths)
        if spread < 0.40:
            out.append((1, CHECK, "cadence",
                        "%d sentences, %.0f words on average" % (len(lengths), mean(lengths)),
                        "sentence lengths are too even; vary them with the content"))

    return out


def main(argv):
    targets = argv[1:]
    reports = []

    if targets:
        for name in targets:
            try:
                with open(name, encoding="utf-8-sig") as handle:
                    reports.extend(findings_for(handle.read(), name))
            except OSError as problem:
                print("cannot read %s: %s" % (name, problem), file=sys.stderr)
                return 2
    else:
        reports.extend(findings_for(sys.stdin.read(), "stdin"))

    reports.sort(key=lambda f: (f[0], f[1]))

    for name, line, level, rule, matched, why in reports:
        print("%s:%d  [%s] %-14s %-34s %s" % (name, line, level, rule, repr(matched)[:34], why))

    # One of these is a choice. Six of them is the shape the skill is about, so say so. Counted per
    # file, because a habit belongs to a document and pooling several would invent one.
    for name in dict.fromkeys(f[0] for f in reports):
        for rule, limit, note in (("opposition", 4, "not X but Y"),
                                  ("triad", 4, "three item lists"),
                                  ("em dash", 3, "em dashes")):
            count = sum(1 for f in reports if f[0] == name and f[3] == rule)
            if count >= limit:
                print("\n%s: %s appears %d times. One is a choice; %d is a habit."
                      % (name, note, count, count))

    hard = sum(1 for f in reports if f[2] == HARD)
    if reports:
        print("\n%d findings, %d of them hard. The three habits this script cannot see are "
              "personification, aphorism and cadence: read for those." % (len(reports), hard))
    else:
        print("nothing mechanical found. Still read for personification, aphorism and cadence.")

    return 1 if reports else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
