#!/usr/bin/env python3
"""Validate Dyadic security skill manifests, frontmatter, and local links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR_PATTERN = re.compile(r"^dyadic-[a-z0-9-]+$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def frontmatter_name(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    for line in text[4:end].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    return None


def validate() -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    names: set[str] = set()

    for folder in sorted(path for path in ROOT.iterdir() if path.is_dir() and SKILL_DIR_PATTERN.fullmatch(path.name)):
        skill_path = folder / "SKILL.md"
        manifest_path = folder / "skill.json"
        if not skill_path.is_file():
            errors.append(f"{folder.name}: missing SKILL.md")
            continue
        if not manifest_path.is_file():
            errors.append(f"{folder.name}: missing skill.json")
            continue

        text = skill_path.read_text(encoding="utf-8")
        name = frontmatter_name(text)
        if name != folder.name:
            errors.append(f"{folder.name}: frontmatter name is {name!r}")

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{folder.name}: invalid skill.json: {exc}")
            continue

        manifest_id = manifest.get("id")
        if manifest_id != folder.name:
            errors.append(f"{folder.name}: manifest id is {manifest_id!r}")
        if manifest_id in ids:
            errors.append(f"{folder.name}: duplicate manifest id {manifest_id!r}")
        ids.add(manifest_id)

        display_name = manifest.get("name")
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"{folder.name}: manifest name is empty")
        elif display_name in names:
            errors.append(f"{folder.name}: duplicate display name {display_name!r}")
        names.add(display_name)

        if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
            errors.append(f"{folder.name}: version is not semantic x.y.z")
        if not isinstance(manifest.get("description"), str) or len(manifest["description"].strip()) < 20:
            errors.append(f"{folder.name}: manifest description is too short")
        if not isinstance(manifest.get("changes"), list) or not manifest["changes"]:
            errors.append(f"{folder.name}: changes must be non-empty")

        for link in MARKDOWN_LINK.findall(text):
            if "://" in link or link.startswith("#") or link.startswith("mailto:"):
                continue
            destination = (skill_path.parent / link.split("#", 1)[0]).resolve()
            if not destination.exists():
                errors.append(f"{folder.name}: broken link {link!r}")

    expected = {
        "dyadic-security-scan",
        "dyadic-security-diff-scan",
        "dyadic-threat-model",
        "dyadic-finding-discovery",
        "dyadic-attack-path-analysis",
        "dyadic-finding-validation",
        "dyadic-vulnerability-writeup",
        "dyadic-fix-finding",
        "dyadic-verify-fix",
        "dyadic-security-hardening",
        "dyadic-security-policy",
        "dyadic-track-findings",
    }
    missing = expected - ids
    extra = ids - expected
    if missing:
        errors.append(f"missing expected skills: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"unexpected security skills: {', '.join(sorted(extra))}")

    schema = ROOT / "_shared" / "finding.schema.json"
    try:
        parsed_schema = json.loads(schema.read_text(encoding="utf-8"))
        if parsed_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append("finding schema is not Draft 2020-12")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid finding schema: {exc}")

    return errors


if __name__ == "__main__":
    found = validate()
    if found:
        for item in found:
            print(f"ERROR: {item}", file=sys.stderr)
        raise SystemExit(1)
    print("OK: 12 Dyadic security skills, manifests, shared schema, and local links")
