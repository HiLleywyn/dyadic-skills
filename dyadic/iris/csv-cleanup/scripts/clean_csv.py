"""Clean a CSV file into a new one and report every change.

Usage: clean_csv.py IN OUT [--dates day-first|month-first] [--dedupe]
Standard library only.
"""
import csv
import re
import sys
from datetime import datetime

ISO = ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%d %b %Y", "%d %B %Y", "%b %d %Y", "%B %d %Y", "%b %d, %Y", "%B %d, %Y")
DAY_FIRST = ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y")
MONTH_FIRST = ("%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y")
NUMBER = re.compile(r"^[-+]?[$£€]?\s?[\d.,\s]+%?$")


def snake(name, seen):
    base = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip()).strip("_").lower() or "column"
    out, n = base, 2
    while out in seen:
        out, n = f"{base}_{n}", n + 1
    seen.add(out)
    return out


def as_date(text, formats):
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def as_number(text):
    if not NUMBER.match(text):
        return None
    cleaned = re.sub(r"[$£€\s%]", "", text)
    if cleaned.count(",") and cleaned.count("."):
        cleaned = cleaned.replace(",", "") if cleaned.rfind(".") > cleaned.rfind(",") else cleaned.replace(".", "").replace(",", ".")
    elif cleaned.count(",") > 1 or re.search(r",\d{3}$", cleaned):
        cleaned = cleaned.replace(",", "")
    else:
        cleaned = cleaned.replace(",", ".")
    try:
        float(cleaned)
    except ValueError:
        return None
    return cleaned


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    source, target = argv[0], argv[1]
    if source == target:
        print("Write to a new file; the original stays as it is.")
        return 2
    order = argv[argv.index("--dates") + 1] if "--dates" in argv else ""
    formats = ISO + (DAY_FIRST if order == "day-first" else MONTH_FIRST if order == "month-first" else ())
    with open(source, newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.reader(handle, dialect))
    if not rows:
        print("The file is empty.")
        return 1
    seen = set()
    header = [snake(name, seen) for name in rows[0]]
    report = [f"Headers: {', '.join(header)}"] if header != rows[0] else []
    body = [[cell.strip() for cell in row] + [""] * (len(header) - len(row)) for row in rows[1:]]
    trimmed = sum(1 for row in rows[1:] for cell in row if cell != cell.strip())
    if trimmed:
        report.append(f"Trimmed spaces in {trimmed} cells")
    kept = [row for row in body if any(row)]
    if len(kept) < len(body):
        report.append(f"Dropped {len(body) - len(kept)} blank rows")
    unparsed = []
    for index, name in enumerate(header):
        values = [row[index] for row in kept if index < len(row) and row[index]]
        if not values:
            continue
        dates = [as_date(v, formats) for v in values]
        numbers = [as_number(v) for v in values]
        if sum(d is not None for d in dates) >= 0.8 * len(values):
            convert, kind = (lambda v: as_date(v, formats)), "dates"
        elif sum(n is not None for n in numbers) >= 0.8 * len(values):
            convert, kind = as_number, "numbers"
        else:
            continue
        changed = 0
        for row in kept:
            value = row[index] if index < len(row) else ""
            if not value:
                continue
            new = convert(value)
            if new is None:
                unparsed.append(f"{name}: {value!r}")
            elif new != value:
                row[index], changed = new, changed + 1
        if changed:
            report.append(f"{name}: {changed} {kind} standardised")
    if "--dedupe" in argv:
        unique, seen_rows = [], set()
        for row in kept:
            key = tuple(row)
            if key not in seen_rows:
                seen_rows.add(key)
                unique.append(row)
        if len(unique) < len(kept):
            report.append(f"Dropped {len(kept) - len(unique)} duplicate rows")
        kept = unique
    with open(target, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(row[:len(header)] for row in kept)
    print(f"{source}: {len(rows) - 1} rows in, {len(kept)} rows out, written to {target}")
    for line in report or ["Nothing needed changing"]:
        print(f"- {line}")
    if unparsed:
        print(f"Left as they were ({len(unparsed)}): " + "; ".join(unparsed[:20]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
