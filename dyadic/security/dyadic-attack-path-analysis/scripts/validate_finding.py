#!/usr/bin/env python3
"""Validate a Dyadic security finding record without third-party packages.

This intentionally checks the operational invariants used by the security
skills. The JSON Schema remains the interchange contract; use a Draft 2020-12
validator in environments that already provide one.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED = {
    "schema_version",
    "id",
    "title",
    "target",
    "snapshot",
    "status",
    "confidence",
    "severity",
    "root_cause",
    "attack_path",
    "impact",
    "evidence",
    "counterevidence",
    "limitations",
}

ALLOWED = REQUIRED | {
    "claim_state",
    "cvss",
    "cwe",
    "preconditions",
    "affected_versions",
    "fixed_versions",
    "remediation",
    "duplicate_of",
    "external_reference",
}

STATUSES = {
    "candidate",
    "needs-evidence",
    "validated-reportable",
    "validated-nonreportable",
    "disproven",
    "hardening-only",
    "fixed",
    "closed",
}
CONFIDENCE = {"high", "medium", "low"}
SEVERITY = {"critical", "high", "medium", "low", "informational", "undetermined"}
CLAIM_STATES = {"CONFIRMED", "CORROBORATED", "INFERRED", "UNRESOLVED", "DISPROVEN"}
EVIDENCE_KINDS = {"source", "test", "runtime", "history", "document", "response", "other"}


def is_nonempty_string(value: Any, minimum: int = 1) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum


def string_list(value: Any, *, minimum: int = 0) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def validate(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record must be a JSON object"]

    missing = sorted(REQUIRED - record.keys())
    unknown = sorted(record.keys() - ALLOWED)
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")

    if record.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    if not is_nonempty_string(record.get("id"), 3) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{2,127}", str(record.get("id", ""))
    ):
        errors.append("id must match the finding schema identifier pattern")
    if not is_nonempty_string(record.get("title"), 8):
        errors.append("title must contain at least 8 non-whitespace characters")
    if not is_nonempty_string(record.get("target")):
        errors.append("target must be a non-empty string")
    if record.get("status") not in STATUSES:
        errors.append(f"status must be one of: {', '.join(sorted(STATUSES))}")
    if record.get("confidence") not in CONFIDENCE:
        errors.append(f"confidence must be one of: {', '.join(sorted(CONFIDENCE))}")
    if record.get("severity") not in SEVERITY:
        errors.append(f"severity must be one of: {', '.join(sorted(SEVERITY))}")
    if "claim_state" in record and record["claim_state"] not in CLAIM_STATES:
        errors.append("claim_state is not recognized")
    if record.get("status") == "validated-reportable" and record.get("confidence") == "low":
        errors.append("validated-reportable findings cannot have low confidence")

    snapshot = record.get("snapshot")
    if not isinstance(snapshot, dict):
        errors.append("snapshot must be an object")
    else:
        if not is_nonempty_string(snapshot.get("revision"), 7):
            errors.append("snapshot.revision must identify an immutable artifact")
        assessed_at = snapshot.get("assessed_at")
        if not is_nonempty_string(assessed_at):
            errors.append("snapshot.assessed_at is required")
        else:
            try:
                datetime.fromisoformat(assessed_at.replace("Z", "+00:00"))
            except ValueError:
                errors.append("snapshot.assessed_at must be an ISO-8601 date-time")
        digest = snapshot.get("artifact_sha256")
        if digest is not None and not re.fullmatch(r"[a-fA-F0-9]{64}", str(digest)):
            errors.append("snapshot.artifact_sha256 must be 64 hexadecimal characters")

    if not is_nonempty_string(record.get("root_cause"), 20):
        errors.append("root_cause must contain at least 20 characters")
    if not string_list(record.get("attack_path"), minimum=1):
        errors.append("attack_path must be a non-empty list of strings")
    if not is_nonempty_string(record.get("impact"), 20):
        errors.append("impact must contain at least 20 characters")
    if not string_list(record.get("counterevidence")):
        errors.append("counterevidence must be a list of non-empty strings")
    if not string_list(record.get("limitations"), minimum=1):
        errors.append("limitations must be a non-empty list of strings")

    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            prefix = f"evidence[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            if item.get("kind") not in EVIDENCE_KINDS:
                errors.append(f"{prefix}.kind is not recognized")
            if not is_nonempty_string(item.get("locator")):
                errors.append(f"{prefix}.locator must be non-empty")
            if not is_nonempty_string(item.get("observation"), 4):
                errors.append(f"{prefix}.observation must contain at least 4 characters")
            digest = item.get("sha256")
            if digest is not None and not re.fullmatch(r"[a-fA-F0-9]{64}", str(digest)):
                errors.append(f"{prefix}.sha256 must be 64 hexadecimal characters")

    cwes = record.get("cwe", [])
    if not isinstance(cwes, list) or any(not re.fullmatch(r"CWE-[1-9][0-9]*", str(cwe)) for cwe in cwes):
        errors.append("cwe must be a list of CWE identifiers such as CWE-209")

    cvss = record.get("cvss")
    if cvss is not None:
        if not isinstance(cvss, dict):
            errors.append("cvss must be an object")
        else:
            if cvss.get("version") not in {"3.1", "4.0"}:
                errors.append("cvss.version must be '3.1' or '4.0'")
            if not is_nonempty_string(cvss.get("vector"), 10):
                errors.append("cvss.vector must be a complete vector string")
            score = cvss.get("score")
            if score is not None and (not isinstance(score, (int, float)) or not 0 <= score <= 10):
                errors.append("cvss.score must be between 0 and 10")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="Path to a finding JSON file")
    args = parser.parse_args()

    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate(record)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
