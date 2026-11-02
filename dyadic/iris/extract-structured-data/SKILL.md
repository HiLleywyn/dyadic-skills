---
name: "extract-structured-data"
description: "Extract specific fields from documents into structured data (JSON, CSV or an Excel table), such as invoice totals, contract parties and dates, receipt line items or survey answers, with each value checked and traced to where it was found. Use when someone wants information pulled out of files into rows and columns."
---

# Extract Structured Data

The goal is a table someone can trust: the right fields, every value taken
from the source (never guessed), in one consistent format, with a way to
check where it came from.

## 1. Agree the fields first

Write the schema down before extracting anything: each field's name, type
(`string`, `number`, `integer`, `date`, `boolean`), unit or currency, and
whether it is required. If the user only said "the important bits", propose
a schema from one sample document and ask them to confirm or change it.
Save it as `schema.json` in the workspace:

```json
{"fields": {
  "vendor":     {"type": "string", "required": true},
  "invoice_no": {"type": "string", "required": true},
  "date":       {"type": "date",   "required": true},
  "total":      {"type": "number", "required": true, "unit": "EUR"},
  "paid":       {"type": "boolean"}
}}
```

One record per what? Say it: one per invoice, one per line item, one per
clause. Line items usually belong in their own table that repeats the
document's id.

## 2. Read each source fully

- PDFs, Word, Markdown and text: `documents.read` (keep calling with
  `next_start`). Spreadsheets and CSV: `spreadsheets.read`.
- Scans, photos, receipts and screenshots: `vision.read_text`. It costs a
  small amount per page: for more than a few pages, ask first. Its tables
  keep the layout; numbers that matter are worth a second look.
- Many files: `knowledge.search` finds which ones hold the fields; then read
  those in full.

## 3. Extract

For each record and field:

- Take the value as written, then normalize it: dates as `YYYY-MM-DD`,
  amounts as plain numbers (`1234.50`) with the currency in its own field
  or the schema's unit, percentages as numbers (`12.5`), yes/no as
  `true`/`false`.
- **Not in the source: `null`.** Never fill a gap from memory or an
  assumption. If a value is ambiguous (two different totals), choose none,
  set `null` and note why.
- Keep where it came from in a `_source` field: the file and page or cell,
  like `"invoice-17.pdf p. 2"`.

## 4. Check it

Write the records as a JSON array to `data.json` and run the validator in
the Code Sandbox:

```python
import runpy, sys
sys.argv = ["validate.py", "data.json", "--schema", "schema.json", "--csv", "data.csv"]
runpy.run_path("/mnt/skills/extract-structured-data/scripts/validate.py", run_name="__main__")
```

It reports missing required values, values of the wrong type, dates that
aren't real dates and duplicate records, and writes a CSV when asked. Fix
what you can from the source, and report what stays empty.

## 5. Deliver

- A few records: show them as a table in the chat.
- Otherwise save them: JSON (`data.json`), CSV, or an Excel workbook with
  `spreadsheets.write` (a table with a header row, number formats for
  amounts and dates, and a totals row with formulas when it helps).
- Always say: how many records, how many sources were read, which fields
  are empty and why, and anything read by OCR that should be checked.
