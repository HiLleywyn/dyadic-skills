---
name: "compare-documents"
description: "Compare two or more documents, or two versions of one document, side by side - what matches, what differs and what one leaves out - in a table with the exact wording and where it is, then the differences that matter most. Use when someone asks to compare quotes, offers, contracts, policies, drafts or versions, or asks what changed."
---

# Compare Documents

A comparison answers "how do these differ, and does it matter?" from the
documents themselves.

## 1. Get every document in full

Attached files are in the message; files in the workspace are read with
`workspace.files`; others are found with `knowledge.search` (scope files)
and read in full where possible. If you only have passages of one, say so:
a difference you can't see isn't proof there is none.

## 2. Decide what kind of comparison it is

- **Versions of one document** (a draft and its revision): what was added,
  removed and changed.
- **Different documents on one subject** (two quotes, two job offers, two
  policies): the same points, side by side.

## 3. Versions: find every change exactly

For anything longer than a page, compute the differences instead of reading
for them. Save both texts in the workspace if they aren't there, then run
`workspace.python` with the standard library:

```python
import difflib
old = open("v1.txt").read().splitlines()
new = open("v2.txt").read().splitlines()
for line in difflib.unified_diff(old, new, "v1", "v2", n=0, lineterm=""):
    print(line)
```

Then report the changes that matter in words, grouped by section, quoting
the old and new wording for anything that changes a number, a date, an
obligation or a right. Mention that small wording changes were left out.

## 4. Different documents: one table

Choose the points that matter for the user's decision (ask what they are
deciding if it isn't clear), then:

```
| Point          | Quote A (supplier-a.pdf) | Quote B (supplier-b.pdf) |
|----------------|--------------------------|--------------------------|
| Total price    | 4,800 incl. tax (p. 1)   | 4,350 plus tax (p. 2)    |
| Delivery       | 10 working days (p. 2)   | Not stated               |
```

- Exact values with their units and where they are (page, section, clause).
- "Not stated" when a document doesn't say. Never fill it in.
- Make values comparable before judging: tax included or not, per month or
  per year, gross or net. Say how you converted.

## 5. Say what matters

After the table: the two or three differences most likely to change the
user's decision, each in one sentence. Recommend one only when asked, and
say which of their criteria decided it.

## Rules

- Cite each document by its name or cite tag the first time it appears.
- Don't call something identical unless you checked the wording.
- Keep your view separate from what the documents say.
