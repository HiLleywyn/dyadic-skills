---
name: "summarize-documents"
description: "Summarize one or more documents (an attached PDF or Word file, a file in the workspace, a Workspace file, or pasted text) into the main point, the key points with where each one is, exact numbers and dates, and what's left open; or turn a PDF into structured notes (a summary, an outline that follows the document, key terms, numbers, dates and actions, each citing its page). Use when someone asks for a summary, an overview, the key points, notes, a breakdown or a study guide of a document."
---

# Summarize Documents

A summary lets someone act on a document without reading it. It says what
the document says, in less space, and nothing it doesn't say.

## 1. Get the whole document

- **Attached**: its text is in the message.
- **In the file workspace**: read it with `workspace.files` (action read).
- **Somewhere in the Workspace**: find it with `knowledge.search` (scope
  files), then read the file itself if you can. Search returns passages, not
  whole documents.
- **A link**: open it with the Web Page Reader.

If you only have passages (a file you can't open in full), say so at the
top: "Based on the parts I could read: ...". Never fill gaps from memory.

## 2. Settle length and reader

Unless asked otherwise: one screen, for someone who knows the subject but
hasn't read this document. "TL;DR" means three sentences at most. "Detailed"
means a section-by-section outline.

## 3. Write it

```
**Main point:** one or two sentences: what the document is and what it concludes or asks for.

**Key points**
- A point, in your words (section 2, or p. 4).
- Another point, with its numbers and dates exactly as written.

**Left open**
- What the document doesn't settle, defers or contradicts.
```

- Keep names, figures, units and dates exact. "About 40%" in the document
  stays "about 40%".
- Mark opinions as the author's: "The authors argue that ...".
- Quote only where the exact words matter (a definition, a commitment, a
  deadline), and keep quotes short.
- Name the document once at the top, by its cite tag when Knowledge Search
  found it (`[path:reports/q3.md]`) or by its file name (`[q3-report.pdf]`).

## 4. Several documents

Summarize each one separately under its name, in the same shape, then add
**Across them**: what they agree on, where they differ, and what only one of
them covers. If the user wants them side by side, use the Compare Documents
skill instead.

## Rules

- Nothing that isn't in the document. If something important seems missing,
  put it under **Left open**, don't supply it.
- Don't evaluate unless asked; a summary isn't a review.
- Long documents: read them in parts and keep notes per section before you
  write, so the end of the document gets the same attention as the start.

## Example

`tenancy-renewal.pdf` (invented) is a six-page letter. A good main point:
"The landlord, Harrowgate Lettings, offers a 12-month renewal from 1 March at
1,240 a month, up from 1,180, and needs an answer by 31 January." Key points
then give the notice period (section 3), the new pet clause (p. 4) and the
deposit, which stays the same; **Left open** notes that the letter doesn't
say whether the parking space is included.

---

# Also: PDF to Structured Notes

(This was the separate PDF to Structured Notes skill; it is part of Summarize Documents now.)

Good notes let someone skip the PDF and still find anything in it. They
follow the document's own structure, say what each part establishes, and
cite the page for every point so it can be checked.

### 1. Find the PDF and read all of it

- An attached PDF has its text in the message, but long ones are cut short:
  read it with `documents.read` (`file_id` from `[file:<id>]`) whenever the
  text you have stops early. A PDF in the workspace: `documents.read` with
  its `path`. Several candidates: `knowledge.search` for the topic, then read
  the right one.
- Pages are marked `--- Page N ---`. Keep calling with `start=next_start`
  until `next_start` is null. Don't write notes from the first chunk alone.
- **Scanned PDF** (`scanned_pdf`): its pages are images. Tell the user how
  many pages it has and that OCR costs a small amount per page, and ask
  before reading it with `vision.read_text` (5 pages a call by default,
  `pages="6-10"` and so on). Pages read before are free.
- Over about 80 pages: say so, ask whether to cover everything or certain
  sections, and work through the parts in order.

### 2. Map the structure first

Before writing, list the document's own parts: its headings, numbered
sections, chapters or slides, with their page ranges. The notes follow this
order. If the PDF has no headings, group its pages by topic and name each
group in a few words.

### 3. Write the notes

Use this shape, leaving out any section that would be empty:

```markdown
## <Title of the document>

**Source:** <file name>, <N> pages. <Author or organization, date, if stated.>

### Summary
3 to 6 bullets: what the document is, its main conclusions or demands, and
anything a reader must act on. Each bullet ends with its page: (p. 4).

### Outline
#### <Section name> (pp. 3-7)
- The point the section makes, in your words. (p. 3)
- Supporting detail that matters: a figure, a condition, an exception. (p. 5)

### Key terms
| Term | Meaning in this document | Page |

### Numbers and dates
| What | Value | Page |

### Actions, obligations and deadlines
- Who must do what, by when. (p. 12)

### Open questions
- What the document leaves unclear, contradicts or doesn't cover.
```

Rules:

- **Page for every point**, as (p. 4) or (pp. 4-6). The page is the PDF's
  page number from the markers, not a number printed on the page.
- **Paraphrase**, but quote exact wording where it matters: definitions,
  obligations, figures, legal terms. Keep quotes short and in quotation
  marks.
- **Never add** facts, background or opinions that aren't in the PDF. If
  something is unclear, it goes under Open questions.
- Keep numbers exactly as written, with units and currency.
- Tables and charts: give their finding in a sentence and the key values.
- A slide deck: one Outline entry per section of slides, not per slide.

### 4. Deliver

- Post the notes in the chat.
- If the user asks for a file, save them with `documents.write`: `notes.md`
  by default, or `.docx` / `.pdf` when they ask for Word or PDF (the same
  Markdown works). Say the file name; it is in their Workspace files.
- End with one line on coverage: "Covers all 34 pages." or "Covers pages
  1-40 of 120; ask for the rest."
