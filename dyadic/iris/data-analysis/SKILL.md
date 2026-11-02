---
name: "data-analysis"
description: "Analyze a CSV or table in the Python sandbox - profile the columns, answer the question with numbers you computed, and draw an SVG chart. Use when someone shares data or asks for trends, totals, comparisons or a chart."
---

# Data Analysis

Answer questions about data with numbers you computed, not numbers you
estimated. The sandbox runs standard-library Python only (no pandas or
matplotlib), offline, for a few seconds per run, so this skill brings two
small scripts:

- `scripts/profile.py FILE` prints every column: its type, how many values
  are missing, and its range, average and median, or its most common values.
- `scripts/chart.py FILE --x COLUMN --y COLUMN [--kind bar|line] [--out chart.svg] [--title TEXT]`
  draws a bar or line chart as an SVG file. `--y` may name several columns,
  separated by commas, for a line chart with one line each.

They are read-only at `/mnt/skills/data-analysis/scripts/`. Run one with
`workspace.python` and this code, changing the arguments:

```python
import runpy, sys
sys.argv = ["profile.py", "sales.csv"]
runpy.run_path("/mnt/skills/data-analysis/scripts/profile.py", run_name="__main__")
```

File names are relative to the user's workspace.

## Steps

1. **Find the data.** It may be an attached file (its text is in the
   message), a file in the workspace (list it with `workspace.files`), or a
   table in the conversation. If it only exists in the message, save it to
   the workspace first so code can read it.
2. **Profile it** with `profile.py` before answering anything. Check the row
   count, the column types, missing values and anything odd (a number column
   read as text, dates in two formats, totals rows mixed in with data). If
   the data needs cleaning, the csv-cleanup skill does that.
3. **Restate the question as a computation**: which rows, which columns,
   grouped by what, compared how. Say any assumption out loud.
4. **Compute** with a short Python program. Print the intermediate numbers
   you rely on, so the result can be checked. Keep each run small: the
   sandbox stops a run after a few seconds.
5. **Chart it** when a picture helps: a line for change over time, bars for
   comparing categories. One message per chart, with a title that says what
   it shows ("Monthly orders, Jan to Jun"), not what it is ("Chart").
6. **Answer**: the finding in one or two sentences, then the supporting
   numbers in a small table, then the chart's file name. Mention caveats
   (missing months, small samples, outliers you left in or took out).

## Rules

- Never report a number you didn't compute or read from the data.
- Keep the units and say what they are.
- Percentages: say of what. "Up 12%" needs "compared with March".
- If the workspace is read-only for this run (it read outside content), the
  chart can't be saved. Say so, and offer to save it once the user approves.

## Example

`orders.csv` (invented) has `month`, `region` and `orders`. "Which region grew
fastest?" becomes: total orders per region for the first and last month,
growth as last over first minus one, sorted. The answer names the region,
gives its growth with both monthly totals, and shows a line chart of orders
per month for each region, saved as `orders-by-region.svg`.
