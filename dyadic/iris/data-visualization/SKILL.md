---
name: "data-visualization"
description: "Turn data into the right chart, drawn cleanly, as SVG for the web, PNG for Word documents and PDFs, or a native chart in an Excel workbook. Use when someone asks for a chart, graph or plot, or when numbers would be clearer as a picture."
---

# Data Visualization

A chart answers one question at a glance. Choose the form for what the data
has to show, compute the numbers first, and draw it so the finding is the
loudest thing on the page.

## 1. Is it a chart at all?

- One number, or a few headline numbers: write them as text or a small
  table, not a one-bar chart.
- More than about 8 categories that all matter: a sorted table, or a
  horizontal bar chart.
- Otherwise pick by the job:

| The reader must see | Draw | chart.py kind |
|---|---|---|
| Which is bigger, across categories | columns, sorted | `bar --sort` |
| The same, with long names or many items | horizontal bars | `hbar --sort` |
| How it changed over time | a line (one line per series) | `line` |
| One series over time, as a volume | an area | `area` |
| Parts of a whole, compared across groups | stacked columns | `stacked` |
| Whether two measures move together | dots | `scatter` |
| How values are spread | a histogram | `hist` |
| The one bar the story is about | that bar in color, the rest gray | `bar --highlight LABEL` |

Avoid pie charts: lengths compare better than angles. If someone asks for
one, use a single stacked bar or a sorted bar chart and say why; in an Excel
workbook, `spreadsheets.write` can still draw a pie when they insist.

Never put two measures with different units on one chart with two y-axes:
draw two charts, or index both to 100 at the start.

## 2. Get the numbers right first

Compute what the chart shows with Python in the sandbox (the Data Analysis
skill helps) and save it as a small CSV: one column for the categories or
dates, one column per series, already aggregated and in the order to show.
Check the totals before drawing.

## 3. Draw it

`chart.py` is read-only at `/mnt/skills/data-visualization/scripts/`. Run it
with `workspace.python`:

```python
import runpy, sys
sys.argv = ["chart.py", "monthly.csv", "--x", "month", "--y", "north,south",
            "--kind", "line", "--title", "North pulled ahead from April",
            "--y-title", "Orders", "--out", "charts/orders.svg"]
runpy.run_path("/mnt/skills/data-visualization/scripts/chart.py", run_name="__main__")
```

- `--out` ending in `.svg` for the web and Markdown, `.png` for Word
  documents and PDFs (they can't take SVG).
- `--title` states the finding ("North pulled ahead from April"), not the
  chart type. `--subtitle` adds the scope or source. `--y-title` gives the
  unit.
- Up to 8 series (3 for scatter). More than that: fold the smallest into
  "Other" or draw several charts.
- Colors come in a fixed, color-blind-safe order; a legend appears for two
  or more series, and lines are labeled at their ends.

## 4. Put it where it's needed

- In the chat: give the file name; it is in the user's Workspace files.
- In a Word document or PDF: draw a PNG, then `documents.write` with
  Markdown that includes it: `![Orders by month](charts/orders.png)`. The
  text in brackets becomes its caption.
- In an Excel workbook: let Excel draw it natively with `spreadsheets.write`
  (`"charts": [{"type": "line", "data": "B1:C13", "categories": "A2:A13",
  "title": "..."}]`), next to the data, so it updates when the numbers do.

## 5. Check it

Look at what you made before you hand it over: does the title match what
the chart shows, do the bars start at zero, are the units on the axis, can
every label be read? Then give the finding in one sentence with the key
numbers, so the chart supports the answer rather than replacing it.
