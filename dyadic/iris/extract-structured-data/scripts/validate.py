"""Check extracted records against a schema, and optionally write them as CSV.

Usage: validate.py DATA.json --schema SCHEMA.json [--csv OUT.csv]

DATA.json is a JSON array of objects (one per record). SCHEMA.json is
{"fields": {"name": {"type": "string|number|integer|date|boolean",
"required": true}}}. Fields starting with an underscore (like _source) are
kept but not checked. Standard library only.
"""
import csv
import datetime
import json
import sys

TYPES = ("string", "number", "integer", "date", "boolean")


def arg(argv, name, default=None):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default


def problem(value, kind):
    """Why value isn't of kind, or None."""
    if value is None:
        return None
    if kind == "string":
        return None if isinstance(value, str) else "is not text"
    if kind == "number":
        return None if isinstance(value, (int, float)) and not isinstance(value, bool) else "is not a number"
    if kind == "integer":
        return None if isinstance(value, int) and not isinstance(value, bool) else "is not a whole number"
    if kind == "boolean":
        return None if isinstance(value, bool) else "is not true or false"
    if kind == "date":
        try:
            datetime.date.fromisoformat(str(value))
            return None
        except ValueError:
            return "is not a date like 2026-03-31"
    return None


def main(argv):
    if not argv or "--schema" not in argv:
        print(__doc__)
        return 2
    with open(argv[0], encoding="utf-8") as handle:
        records = json.load(handle)
    with open(arg(argv, "--schema"), encoding="utf-8") as handle:
        fields = json.load(handle).get("fields") or {}
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        print("DATA must be a JSON array of objects, one per record.")
        return 1
    bad = [name for name, spec in fields.items() if spec.get("type", "string") not in TYPES]
    if bad:
        print(f"Unknown types for: {', '.join(bad)}. Use {', '.join(TYPES)}.")
        return 1
    issues, empty, seen, duplicates = [], {}, {}, []
    for number, record in enumerate(records, start=1):
        for name, spec in fields.items():
            value = record.get(name)
            if value is None or value == "":
                empty[name] = empty.get(name, 0) + 1
                if spec.get("required"):
                    issues.append(f"record {number}: {name} is required but empty")
                continue
            why = problem(value, spec.get("type", "string"))
            if why:
                issues.append(f"record {number}: {name} = {value!r} {why}")
        extra = [k for k in record if k not in fields and not k.startswith("_")]
        if extra:
            issues.append(f"record {number}: fields not in the schema: {', '.join(extra)}")
        key = json.dumps({k: record.get(k) for k in fields}, sort_keys=True)
        if key in seen:
            duplicates.append((seen[key], number))
        seen.setdefault(key, number)
    print(f"{len(records)} records, {len(fields)} fields.")
    for name in fields:
        if empty.get(name):
            print(f"  {name}: empty in {empty[name]} of {len(records)}")
    for first, again in duplicates:
        print(f"  record {again} repeats record {first}")
    for line in issues[:200]:
        print("  " + line)
    if len(issues) > 200:
        print(f"  ... and {len(issues) - 200} more")
    out = arg(argv, "--csv")
    if out:
        columns = list(fields) + sorted({k for r in records for k in r if k.startswith("_")})
        with open(out, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows([{k: ("" if r.get(k) is None else r.get(k)) for k in columns} for r in records])
        print(f"Wrote {out}.")
    print("OK" if not issues and not duplicates else f"{len(issues)} problems, {len(duplicates)} duplicates.")
    return 0 if not issues and not duplicates else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
