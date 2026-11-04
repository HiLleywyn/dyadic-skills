"""Verify the complete adopted Dyadic skill snapshot against its recorded source hashes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def verify(root: Path = ROOT) -> list[str]:
    receipt = json.loads((root / 'dyadic/catalog-source.json').read_text(encoding='utf-8'))
    errors = []
    if not re.fullmatch(r'[0-9a-f]{40}', receipt.get('revision', '')):
        errors.append('Source revision is not a full Git commit')
    files = receipt.get('files', {})
    if not files:
        errors.append('Receipt contains no files')
    packages = set()
    for name, expected in files.items():
        path = (root / name).resolve()
        parts = Path(name).parts
        if len(parts) < 4 or parts[:2] not in {('dyadic', 'iris'), ('dyadic', 'security')} or not path.is_relative_to(root.resolve()):
            errors.append(f'Invalid mirror path: {name}')
            continue
        packages.add(Path(*parts[:3]))
        if not path.is_file():
            errors.append(f'Missing: {name}')
            continue
        data = path.read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8')
        if hashlib.sha256(data).hexdigest() != expected:
            errors.append(f'Changed: {name}')
    for package in packages:
        for path in (root / package).rglob('*'):
            if path.is_file() and path.relative_to(root).as_posix() not in files:
                errors.append(f'Unrecorded: {path.relative_to(root).as_posix()}')
    return errors


if __name__ == '__main__':
    errors = verify()
    if errors:
        print('\n'.join(errors))
    else:
        print('Dyadic catalog mirror matches its source receipt')
    raise SystemExit(bool(errors))
