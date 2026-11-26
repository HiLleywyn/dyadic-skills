"""Inventory, validate and package one of the three lley.cat collections.

Requires PyYAML for skill frontmatter. Does not execute bundled resources, contact
services or change accounts. The same helper is maintained in all three repos.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def text(path):
    return path.read_text(encoding='utf-8')


def dump(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def frontmatter(path):
    parts = text(path).split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f'{path}: missing frontmatter')
    value = yaml.safe_load(parts[1])
    if not isinstance(value, dict):
        raise ValueError(f'{path}: frontmatter must be an object')
    return value


def safe_file(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative or any(p in ('', '.', '..') for p in relative.split('/')):
        raise ValueError(f'Unsafe collection path: {relative!r}')
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()) or any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError(f'Collection path escapes its root: {relative}')
    return path


def inventory(root):
    kind = read_json(root / 'collection.json')['kind']
    if kind == 'skills':
        manifests = sorted(p for p in root.rglob('SKILL.md') if not set(p.relative_to(root).parts) & {'.git', 'dist', 'reports', '__pycache__'})
    elif kind == 'agents':
        manifests = sorted([*root.glob('agents/*/agent.json'), *root.glob('subagents/*/agent.json')])
    elif kind == 'plugins':
        manifests = sorted(root.glob('dyadic/*/plugin.json'))
    else:
        raise ValueError('Unknown collection kind')
    entries = []
    for path in manifests:
        data = frontmatter(path) if kind == 'skills' else read_json(path)
        meta_path = path.with_name('skill.json')
        display = read_json(meta_path) if kind == 'skills' and meta_path.exists() else data
        entries.append({'id': data.get('name') if kind == 'skills' else data.get('id'),
                        'name': display.get('name'), 'description': data.get('description') or display.get('description') or 'Dyadic’s built-in primary assistant.',
                        'path': path.parent.relative_to(root).as_posix(),
                        **({'role': 'primary' if path.parent.parent.name == 'agents' else 'delegate'} if kind == 'agents' else {}),
                        **({'tool': data.get('tool')} if kind == 'plugins' else {})})
    return {'schema': 1, 'kind': kind, 'entries': entries}


def check(root):
    actual = inventory(root)
    if actual != read_json(root / 'catalog.json'):
        raise ValueError('catalog.json is stale; run python tools/catalog.py index')
    ids = set()
    for item in actual['entries']:
        key = item['id']
        if not isinstance(key, str) or not re.fullmatch('[a-z0-9][a-z0-9-]{0,63}', key) or key in ids:
            raise ValueError(f'Invalid or duplicate ID: {key}')
        ids.add(key)
        folder = safe_file(root, item['path'])
        if folder.name != key:
            raise ValueError(f'ID must match its folder: {key}')
        if not item['description'] or not item['name']:
            raise ValueError(f'Missing description/name: {key}')
        if actual['kind'] != 'skills' and not (folder / 'README.md').is_file():
            raise ValueError(f'Missing navigable README: {key}')
        if actual['kind'] == 'agents':
            if not text(folder / 'instructions.md').strip():
                raise ValueError(f'Empty agent instructions: {key}')
            if item['role'] == 'delegate':
                policy = read_json(folder / 'import.json')
                tools = policy['tools']
                known = read_json(root / 'compatibility/native-tools.json')['tools']
                if not isinstance(tools, list) or len(set(tools)) != len(tools) or set(tools) - set(known):
                    raise ValueError(f'Unknown or duplicate import tools: {key}')
                deps = read_json(root / 'compatibility/skill-dependencies.json')['skills']
                agent = read_json(folder / 'agent.json')
                if set(agent.get('skills', [])) - set(deps):
                    raise ValueError(f'Unresolved skill dependency: {key}')
        if actual['kind'] == 'plugins':
            manifest = read_json(folder / 'plugin.json')
            if not re.fullmatch(r'[a-z_]+\.(?:[a-z_]+|\*)', manifest['tool']):
                raise ValueError(f'Invalid plugin switch: {key}')
            if manifest['changes'][0]['version'] != manifest['version']:
                raise ValueError(f'Plugin version/change mismatch: {key}')
    provenance = read_json(root / 'provenance.json')
    for path, record in provenance['files'].items():
        body = safe_file(root, path).read_bytes().replace(b'\r\n', b'\n')
        if hashlib.sha256(body).hexdigest() != record['sha256']:
            raise ValueError(f'Source snapshot changed without a provenance update: {path}')
    # Navigation is authored documentation, not example links embedded in skills.
    for page in root.rglob('README.md'):
        if set(page.relative_to(root).parts) & {'.git', 'dist', 'reports', '__pycache__'}:
            continue
        body = re.sub(r'```.*?```', '', text(page), flags=re.S)
        for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            if '://' in href or href.startswith(('#', 'mailto:')):
                continue
            target = href.split('#', 1)[0]
            if target and not (page.parent / target).exists():
                raise ValueError(f'{page.relative_to(root)}: broken navigation link {href}')
    return actual


def folder_files(folder):
    files = {}
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Cannot package a symlink: {path}')
        if path.is_file():
            relative = path.relative_to(folder).as_posix()
            if set(path.relative_to(folder).parts) & {'.git', '__pycache__'}:
                continue
            safe_file(folder, relative)
            files[relative] = path.read_bytes().replace(b'\r\n', b'\n') if path.suffix in {'.md', '.json', '.py', '.yaml', '.yml', '.txt', '.html', '.ps1', '.sh'} else path.read_bytes()
    return files


def skill_files(root, item):
    folder = safe_file(root, item['path'])
    files = folder_files(folder)
    # Security standards are maintained once in source and included in each ZIP.
    # Rewrite only their documented link prefix; never edit the source skill.
    if item['path'].startswith('dyadic/security/dyadic-'):
        shared = folder_files(folder.parent / '_shared')
        files.update({'references/standards/' + p: b for p, b in shared.items()})
        files['SKILL.md'] = files['SKILL.md'].replace(b'../_shared/', b'references/standards/')
    return files


def bundle_digest(files):
    """SHA-256 over the uncompressed, sorted file set, independent of the local zlib build."""
    h = hashlib.sha256()
    for name, body in sorted(files.items()):
        encoded = name.encode()
        h.update(len(encoded).to_bytes(4, 'big') + encoded + len(body).to_bytes(8, 'big') + body)
    return h.hexdigest()


def archive(files):
    if len(files) > 2000 or sum(map(len, files.values())) > 100 * 1024 * 1024:
        raise ValueError('Package exceeds file/expanded size limits')
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, body in sorted(files.items()):
            safe_file(Path('/package-root'), name)
            z.writestr(zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0)), body, zipfile.ZIP_DEFLATED)
    if out.tell() > 50 * 1024 * 1024:
        raise ValueError('Package exceeds upload size limit')
    return out.getvalue()


def agent_files(root, item, skills_root=None):
    if item['role'] != 'delegate':
        raise ValueError('Iris is a built-in primary definition, not an installable primary-agent package')
    folder = safe_file(root, item['path'])
    agent = read_json(folder / 'agent.json')
    policy = read_json(folder / 'import.json')
    name = 'instructions/' + item['id'] + '.md'
    files = {name: (folder / 'instructions.md').read_bytes().replace(b'\r\n', b'\n')}
    skills, wanted = [], []
    if skills_root is not None:
        available = {s['id']: s for s in check(skills_root)['entries']}
        expected = read_json(root / 'compatibility/skill-dependencies.json')['skills']
        for key in agent.get('skills', []):
            if key not in available:
                raise ValueError(f'Missing dependency: {key}')
            bundled = skill_files(skills_root, available[key])
            digest = hashlib.sha256(bundled['SKILL.md']).hexdigest()
            bundled_digest = bundle_digest(bundled)
            if digest != expected[key]['sha256'] or bundled_digest != expected[key]['bundle_sha256']:
                raise ValueError(f'Skill dependency changed; review the lock: {key}')
            target = 'skills/' + key
            files.update({target + '/' + p: b for p, b in bundled.items()})
            skills.append({'key': key, 'folder': target})
            wanted.append(key)
    if len(skills) > 10:
        raise ValueError('A native package allows at most ten skills')
    declaration = {'key': item['id'], 'name': agent['name'], 'description': agent['description'],
                   'instructions': name, 'model': 'iris', 'usage': 'delegate',
                   'icon': agent['icon'], 'color': agent['color'], 'tools': policy['tools'], 'skills': wanted,
                   'requirements': {'tools': policy['tools'], 'skills': agent.get('skills', [])}}
    files['dyadic-package.json'] = dump({'format': 'dyadic.package', 'version': 1, 'name': agent['name'],
                                      'release': agent['version'], 'agents': [declaration], 'skills': skills})
    return files


def build(root, output, skills_root=None):
    catalog = check(root)
    output.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for item in catalog['entries']:
        if catalog['kind'] == 'skills':
            files = skill_files(root, item)
        elif catalog['kind'] == 'agents':
            if item['role'] != 'delegate':
                continue
            files = agent_files(root, item, skills_root)
        else:
            files = folder_files(safe_file(root, item['path']))
        outputs[item['id'] + '.zip'] = archive(files)
    hashes = {name: {'sha256': hashlib.sha256(body).hexdigest(), 'size': len(body)} for name, body in outputs.items()}
    for name, body in outputs.items():
        (output / name).write_bytes(body)
    (output / 'checksums.json').write_bytes(dump(hashes))
    outputs['checksums.json'] = dump(hashes)
    outputs['README.md'] = ('# ' + catalog['kind'].title() + ' packages\n\n' +
        ('These are plugin catalog descriptors, not executable plugin installs.\n' if catalog['kind'] == 'plugins' else
         'Extract this collection, then review/import one individual ZIP at a time in Dyadic.\n') +
        'See the repository README for permissions and runtime limits.\n').encode()
    (output / 'collection.zip').write_bytes(archive(outputs))
    return hashes


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['index', 'check', 'build'])
    p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--output', type=Path)
    p.add_argument('--skills', type=Path, help='Optionally bundle reviewed skill dependencies from the skills checkout')
    args = p.parse_args()
    try:
        if args.command == 'index':
            (args.root / 'catalog.json').write_bytes(dump(inventory(args.root)))
        elif args.command == 'check':
            value = check(args.root)
            print(f"Validated {len(value['entries'])} {value['kind']}")
        else:
            hashes = build(args.root, args.output or args.root / 'dist', args.skills)
            print(f'Built {len(hashes)} packages')
    except (ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        sys.exit(str(exc))


if __name__ == '__main__':
    main()
