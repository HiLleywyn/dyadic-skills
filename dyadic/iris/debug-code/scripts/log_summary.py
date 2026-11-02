"""Summarize a log file so the first real error stands out.

Usage: log_summary.py FILE [--top N] [--around TEXT]

Prints how many lines there are at each level (ERROR, WARN, INFO, DEBUG and
the like), the first and last timestamps it can read, then the messages
grouped by their shape (numbers, ids, hex, addresses and quoted values
replaced by placeholders, so 900 "timeout after 3012 ms" lines become one
group), most frequent first, each with its count, the line where it first
appeared and one example. Errors and warnings are listed first, in the order
they first appeared, because the earliest one is usually the cause.
--around TEXT also prints the five lines before and after the first line
containing TEXT. Works on plain text and on JSON lines (one object per
line, with a message and level field).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

LEVELS = ("FATAL", "CRITICAL", "ERROR", "WARNING", "WARN", "NOTICE", "INFO", "DEBUG", "TRACE")
SEVERE = {"FATAL", "CRITICAL", "ERROR", "WARNING", "WARN"}
LEVEL = re.compile(r"\b(" + "|".join(LEVELS) + r")\b", re.I)
TIME = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:?\d{2})?|\b\d{2}:\d{2}:\d{2}(?:[.,]\d+)?\b")
SHAPES = [
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "<uuid>"),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?\b"), "<ip>"),
    (re.compile(r"\b0x[0-9a-f]+\b|\b[0-9a-f]{12,}\b", re.I), "<hex>"),
    (re.compile(r"'[^']*'|\"[^\"]*\""), "<str>"),
    (re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?"), "<n>"),
]


def parse(line: str) -> tuple[str, str, str]:
    """(timestamp, level, message) from one line."""
    text = line.rstrip("\n")
    if text.startswith("{"):
        try:
            record = json.loads(text)
        except ValueError:
            record = None
        if isinstance(record, dict):
            level = str(record.get("level") or record.get("severity") or record.get("levelname") or "").upper()
            message = str(record.get("message") or record.get("msg") or record.get("event") or text)
            stamp = str(record.get("time") or record.get("timestamp") or record.get("ts") or record.get("@timestamp") or "")
            return stamp, level, message
    stamp_match = TIME.search(text)
    level_match = LEVEL.search(text)
    message = text
    if level_match:
        message = text[level_match.end():].lstrip(" :|-]")
    elif stamp_match:
        message = text[stamp_match.end():].lstrip(" :|-]")
    return (stamp_match.group(0) if stamp_match else "", level_match.group(1).upper() if level_match else "", message)


def shape(message: str) -> str:
    for pattern, placeholder in SHAPES:
        message = pattern.sub(placeholder, message)
    return " ".join(message.split())[:160]


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a log file.")
    parser.add_argument("file")
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument("--around", default="")
    args = parser.parse_args()
    with open(args.file, encoding="utf-8", errors="replace") as handle:
        lines = handle.readlines()
    levels: Counter = Counter()
    groups: Counter = Counter()
    first: dict[str, tuple[int, str, str]] = {}
    stamps: list[str] = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        stamp, level, message = parse(line)
        levels[level or "(none)"] += 1
        if stamp:
            stamps.append(stamp)
        key = f"{level or '-'} {shape(message)}"
        groups[key] += 1
        first.setdefault(key, (number, level, line.strip()[:300]))
    print(f"{len(lines)} lines in {args.file}")
    if stamps:
        print(f"from {stamps[0]} to {stamps[-1]}")
    print("levels: " + ", ".join(f"{name} {count}" for name, count in levels.most_common()))
    severe = sorted((first[k][0], k) for k in groups if first[k][1] in SEVERE)
    if severe:
        print("\nerrors and warnings, in the order they first appeared:")
        for number, key in severe[: args.top]:
            print(f"  line {number}: x{groups[key]}  {key}\n      e.g. {first[key][2]}")
    print(f"\nmost frequent messages (top {args.top}):")
    for key, count in groups.most_common(args.top):
        print(f"  x{count}  first at line {first[key][0]}  {key}")
    if args.around:
        hit = next((i for i, line in enumerate(lines) if args.around in line), None)
        if hit is None:
            print(f"\n{args.around!r} doesn't appear in the file.")
        else:
            print(f"\naround line {hit + 1}:")
            for i in range(max(0, hit - 5), min(len(lines), hit + 6)):
                print(f"{'>' if i == hit else ' '} {i + 1:6} {lines[i].rstrip()[:300]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
