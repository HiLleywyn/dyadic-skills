---
name: "csv-cleanup"
description: "Clean up a messy spreadsheet or CSV - tidy headers, trim stray spaces, standardise dates and numbers, drop blank and duplicate rows - and report every change. Use when data has inconsistent formats, duplicates or junk rows, or before analyzing it."
---

# CSV Cleanup

Clean data so it can be trusted, and say exactly what you changed. Never
delete information silently.

## The script

`scripts/clean_csv.py IN OUT [--dates day-first|month-first] [--dedupe]`
does the routine work with the standard library:

- headers in `snake_case`, unique, with no blanks;
- leading and trailing spaces trimmed in every cell;
- fully blank rows dropped;
- dates in a column where most values are dates rewritten as `YYYY-MM-DD`
  (ambiguous `03/04/2027` needs `--dates`);
- numbers in a column where most values are numbers: thousands separators,
  currency signs and spaces removed;
- with `--dedupe`, exact duplicate rows dropped (the first one kept);
- a report of every column it changed and every row it dropped.

It is read-only at `/mnt/skills/csv-cleanup/scripts/`. Run it with
`workspace.python`:

```python
import runpy, sys
sys.argv = ["clean_csv.py", "contacts.csv", "contacts-clean.csv", "--dedupe"]
runpy.run_path("/mnt/skills/csv-cleanup/scripts/clean_csv.py", run_name="__main__")
```

## Steps

1. Save the data to the workspace if it only came in the message.
2. Look at it first (the data-analysis skill's `profile.py` helps): which
   columns are dates, numbers, categories; what "messy" means here.
3. Ask before anything that loses information the user may want: merging
   near-duplicates, dropping columns, filling missing values.
4. Run the script into a **new** file. Never overwrite the original.
5. Check the result: row counts before and after, a few sample rows, and
   any value the script couldn't parse (it lists them).
6. Fix what's left by hand or with a short program: category spellings
   ("N/A", "n/a", "-" to empty), units, split or merged columns.
7. Report: the new file's name, rows in and out, and a short list of the
   changes. Mention anything you left alone and why.

## Rules

- Keep the original file untouched.
- A value you can't interpret stays as it was, and goes in the report.
- If the workspace is read-only for this run, say so and show the plan.
