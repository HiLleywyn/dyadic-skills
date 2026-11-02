"""Profile a CSV file: each column's type, missing values and summary.

Usage: profile.py FILE [--delimiter ,]
Standard library only.
"""
import csv
import statistics
import sys
from collections import Counter
from datetime import datetime

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d.%m.%Y", "%Y-%m")


def number(text):
    cleaned = text.replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def date(text):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            continue
    return None


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    path = argv[0]
    delimiter = argv[argv.index("--delimiter") + 1] if "--delimiter" in argv else None
    with open(path, newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        if delimiter is None:
            try:
                delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
            except csv.Error:
                delimiter = ","
        rows = list(csv.DictReader(handle, delimiter=delimiter))
    if not rows:
        print("No rows.")
        return 1
    print(f"{path}: {len(rows)} rows, {len(rows[0])} columns, delimiter {delimiter!r}")
    for column in rows[0]:
        values = [(row.get(column) or "").strip() for row in rows]
        present = [v for v in values if v]
        missing = len(values) - len(present)
        numbers = [n for n in (number(v) for v in present) if n is not None]
        dates = [d for d in (date(v) for v in present) if d is not None]
        line = f"- {column}: "
        if present and len(numbers) == len(present):
            line += (f"number; min {min(numbers):g}, max {max(numbers):g}, mean {statistics.fmean(numbers):.4g}, "
                     f"median {statistics.median(numbers):g}")
        elif present and len(dates) == len(present):
            line += f"date; from {min(dates):%Y-%m-%d} to {max(dates):%Y-%m-%d}"
        else:
            common = Counter(present).most_common(3)
            shown = ", ".join(f"{value!r} x{count}" for value, count in common)
            line += f"text; {len(set(present))} distinct; most common {shown}"
            if numbers and len(numbers) < len(present):
                line += f" ({len(numbers)} of {len(present)} look like numbers: check for stray text)"
        if missing:
            line += f"; {missing} missing"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
