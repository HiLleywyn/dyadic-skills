---
name: "fact-check"
description: "Fact check an article, post, transcript or statement claim by claim (each checkable claim quoted exactly, the primary sources that confirm or contradict it, a verdict from a fixed scale with the evidence linked, and what couldn't be checked), and verify a single source before relying on it (who published it and when, whether it's the original, whether it really says what's claimed, rated Reliable, Use With Care, Unreliable or Can't Verify). Use when someone asks to fact check, verify or debunk something, whether an article is accurate, or whether a source, link, quote, screenshot, statistic or study is real or trustworthy."
---

# Fact Check

A fact check tells the reader which claims hold up and shows the evidence
for each verdict, so they can check it themselves.

## 1. Get the text

A link: open it with the Web Page Reader and note the publisher and the
date. Attached or pasted text: use it as given, and ask for the date and
publisher if they matter and aren't there.

## 2. List the checkable claims

A checkable claim states something that could be confirmed or refuted: a
number, a date, a quote, an event, a ranking, a cause and effect. Leave out
opinions, predictions and value judgements, and say you left them out.

- Quote each claim exactly, with where it appears (paragraph, timestamp).
- One claim per line. Split "X rose 30% and caused Y" into two.
- Keep the ten that matter most to the article's argument unless asked for
  all of them, and say how many you skipped.

## 3. Check each claim

1. Find who would know first-hand: the agency that published the figure,
   the study, the court record, the original speech. Search for that, not
   for the claim's own wording.
2. Open the source and find the passage. Use the Source Verification skill
   when you are unsure whether a source is what it seems.
3. Compare exactly: the same number, unit, place and period? A figure for
   one year presented as a trend? A quote cut so it means something else?
4. Look for one independent confirmation, and for credible contradiction.
5. Check against the user's own files with `knowledge.search` when the
   claim is about their work or documents.

## 4. Give a verdict from this scale

- **Supported**: reliable sources confirm it as stated.
- **Mostly supported**: right in substance, wrong in a detail that doesn't
  change the point (say which).
- **Misleading**: true as far as it goes, but missing context that changes
  what a reader would conclude.
- **Unsupported**: you found no evidence for it either way.
- **False**: reliable evidence contradicts it.
- **Disputed**: credible sources disagree; say who says what.

## 5. Write it up

```
**Overall:** two sentences: how accurate the piece is, and the claim that matters most.

| # | Claim (quoted)                  | Verdict    | Evidence                               |
|---|---------------------------------|------------|----------------------------------------|
| 1 | "Ridership fell 40% in 2025"    | Misleading | [Transit report 2025](exact link): ... |

**Notes**: for every verdict other than Supported, one or two sentences on why.

**Couldn't check**: claims you couldn't verify and what you looked for.
```

## Rules

- The verdict is about the claim, never about the author's motives.
- Link only pages you opened, each to the exact page. Never invent a link.
- Judge a claim against what was known on the article's date, and say if
  newer information has changed the answer since.
- No source, no verdict: "Unsupported" is an honest answer.

## Example

An invented post says: "Lake Corrin's water level dropped 3 metres last
summer, the lowest since records began in 1950." That is two claims: the
3-metre drop and the record low. The regional water authority's gauge data
(the primary source) shows a 2.1-metre drop: **Mostly supported**, with the
exact figure in the note. Records at that gauge start in 1972, not 1950, and
show a lower level in 1976: the record claim is **False**.

---

# Also: Source Verification

(This was the separate Source Verification skill; it is part of Fact Check now.)

Verifying a source answers three questions: is it what it claims to be, does
it say what it is said to say, and how much can rest on it?

### 1. Pin down what is being verified

Write down the source (an address, a document, a quoted passage, a figure)
and the exact claim attributed to it. "The health ministry says X" is
checked against what the ministry actually published.

### 2. Who published it, and when

- Open the page itself with the Web Page Reader; don't rely on a search
  snippet or a screenshot.
- Check the address: the real domain of the organization, not a lookalike
  (extra words, a different ending, a swapped letter).
- Find the author or body responsible, the publication date and any update
  or correction notice.

### 3. Original or copy

Many pages repeat one original: a press release, a wire story, a study.
Follow the links and citations upstream until you reach the first source,
and judge that one. Ten articles quoting the same release are one source,
not ten.

### 4. Does it say that?

Find the exact passage, table or quote and compare it with the claim:

- the same number, unit, place and period;
- the full sentence, so a quote isn't cut to mean something else;
- what the source itself says about its limits (a sample size, an estimate,
  a preliminary result).

Quote the passage and say where it is (page, section, table).

### 5. How much weight it can carry

- **Primary and accountable**: an official statistics body, a court record,
  a peer-reviewed study, the organization speaking for itself.
- **Secondary with standards**: established news outlets and reference works
  that name sources and publish corrections.
- **Weak**: anonymous pages, content farms, posts without sources, sites
  with an obvious interest in the answer.

A strong publisher can still be wrong, and a weak one can be right: say what
you checked, not only who published it.

### 6. Rate it

```
**Source:** name, address, date.
**Rating:** Reliable / Use With Care / Unreliable / Can't Verify
**Why:**
- Who published it and whether it is the original.
- Whether it contains the claim, with the passage quoted.
- Any independent confirmation or contradiction.
**Original source:** [name](exact address), if different.
```

### Rules

- Never rate a source you couldn't open: that is Can't Verify.
- Link only pages you opened, exactly.
- Keep it short: the rating and the reasons that decide it.

### Example

A post credits "a Halvern University study" (invented) with "68% of
commuters cycle". The study's own page reports 6.8% of commuters in one
district in one month, and the post's link goes to a blog that misread the
table. Rating for the post: **Unreliable**; for the study: **Reliable**, with
the passage from its results table quoted.
