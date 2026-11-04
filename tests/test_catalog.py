"""Executable collection checks; no bundled instructions/scripts are executed."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog', ROOT / 'tools/catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CollectionChecks(unittest.TestCase):
    def test_catalog_and_snapshot_integrity(self):
        self.assertTrue(catalog.check(ROOT)['entries'])

    def test_archive_reproducibility(self):
        a = catalog.archive({'second.txt': b'two', 'first.txt': b'one'})
        b = catalog.archive({'first.txt': b'one', 'second.txt': b'two'})
        self.assertEqual(a, b)
        with zipfile.ZipFile(io.BytesIO(a)) as z:
            self.assertEqual(z.namelist(), ['first.txt', 'second.txt'])
            self.assertEqual(z.read('second.txt'), b'two')

    def test_archive_rejects_escaping_paths(self):
        for path in ('../escape', '/absolute', 'C:/drive', 'back\\slash', 'nested/../escape', 'nested//empty'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                catalog.archive({path: b'bad'})

    def test_changed_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ('collection.json', 'catalog.json', 'provenance.json'):
                shutil.copyfile(ROOT / name, root / name)
            # Stop before materializing the collection: its inventory is unrelated
            # to the deliberately changed source byte tested here.
            changed = next(iter(catalog.read_json(ROOT / 'provenance.json')['files']))
            target = root / changed
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('unreviewed change', encoding='utf-8')
            with patch.object(catalog, 'inventory', return_value={'schema': 1, 'kind': 'skills', 'entries': []}):
                (root / 'catalog.json').write_bytes(catalog.dump(catalog.inventory(root)))
                with self.assertRaisesRegex(ValueError, 'snapshot changed'):
                    catalog.check(root)

    def test_complete_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            one, two = Path(temp) / 'one', Path(temp) / 'two'
            first = catalog.build(ROOT, one)
            second = catalog.build(ROOT, two)
            self.assertEqual(first, second)
            self.assertEqual((one / 'collection.zip').read_bytes(), (two / 'collection.zip').read_bytes())
            for name, record in first.items():
                body = (one / name).read_bytes()
                self.assertEqual(record, {'size': len(body), 'sha256': hashlib.sha256(body).hexdigest()})

    def test_primary_iris_is_not_a_delegate_export(self):
        if catalog.inventory(ROOT)['kind'] != 'agents':
            self.skipTest('Agent collection only')
        iris = next(i for i in catalog.inventory(ROOT)['entries'] if i['id'] == 'iris')
        with self.assertRaisesRegex(ValueError, 'primary'):
            catalog.agent_files(ROOT, iris)

    def test_dependency_changes_require_a_reviewed_lock(self):
        if catalog.inventory(ROOT)['kind'] != 'agents':
            self.skipTest('Agent collection only')
        item = next(i for i in catalog.inventory(ROOT)['entries'] if i['role'] == 'delegate')
        first = catalog.read_json(ROOT / item['path'] / 'agent.json')['skills'][0]
        with tempfile.TemporaryDirectory() as temp:
            dep = Path(temp) / first
            dep.mkdir()
            (dep / 'SKILL.md').write_text('Changed dependency', encoding='utf-8')
            with patch.object(catalog, 'check', return_value={'entries': [{'id': first, 'path': first}]}):
                with self.assertRaisesRegex(ValueError, 'dependency changed'):
                    catalog.agent_files(ROOT, item, Path(temp))

    def test_dependency_resources_are_locked_too(self):
        if catalog.inventory(ROOT)['kind'] != 'agents':
            self.skipTest('Agent collection only')
        item = next(i for i in catalog.inventory(ROOT)['entries'] if i['role'] == 'delegate')
        first = catalog.read_json(ROOT / item['path'] / 'agent.json')['skills'][0]
        originals = {'SKILL.md': b'unchanged entrypoint', 'reference.md': b'original resource'}
        locked = {'sha256': hashlib.sha256(originals['SKILL.md']).hexdigest(), 'bundle_sha256': hashlib.sha256(catalog.archive(originals)).hexdigest()}
        read_json = catalog.read_json
        def metadata(path):
            if path == ROOT / 'compatibility/skill-dependencies.json':
                return {'skills': {first: locked}}
            return read_json(path)
        with tempfile.TemporaryDirectory() as temp:
            dep = Path(temp) / first
            dep.mkdir()
            for name, body in originals.items():
                (dep / name).write_bytes(body)
            (dep / 'reference.md').write_bytes(b'changed supporting resource')
            with patch.object(catalog, 'check', return_value={'entries': [{'id': first, 'path': first}]}), patch.object(catalog, 'read_json', side_effect=metadata):
                with self.assertRaisesRegex(ValueError, 'dependency changed'):
                    catalog.agent_files(ROOT, item, Path(temp))


def package_case(item):
    def test(self):
        kind = catalog.inventory(ROOT)['kind']
        if kind == 'skills':
            files = catalog.skill_files(ROOT, item)
            self.assertIn('SKILL.md', files)
            metadata = catalog.yaml.safe_load(files['SKILL.md'].decode().split('---', 2)[1])
            self.assertEqual(metadata['name'], item['id'])
            if item['path'].startswith('dyadic/security/dyadic-'):
                self.assertNotIn(b'../_shared/', files['SKILL.md'])
                self.assertIn('references/standards/runtime-and-tools.md', files)
        elif kind == 'agents':
            if item['role'] == 'primary':
                self.assertTrue((ROOT / item['path'] / 'instructions.md').is_file())
                return
            files = catalog.agent_files(ROOT, item)
            manifest = json.loads(files['dyadic-package.json'])
            self.assertEqual(manifest['format'], 'dyadic.package')
            agent = manifest['agents'][0]
            self.assertEqual(agent['usage'], 'delegate')
            self.assertEqual(set(files), {'dyadic-package.json', agent['instructions']})
            self.assertTrue(files[agent['instructions']].strip())
            # Runtime-owned context is supplied by the parent, not requested as a
            # capability the delegated reader cannot exercise.
            self.assertFalse(set(agent['tools']) & {'runs.lookup', 'runs.read', 'runs.search'})
        else:
            files = catalog.folder_files(ROOT / item['path'])
            manifest = json.loads(files['plugin.json'])
            self.assertEqual(manifest['tool'], item['tool'])
            self.assertIn('README.md', files)
        body = catalog.archive(files)
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            self.assertEqual({name: archive.read(name) for name in archive.namelist()}, files)
    return test


if catalog.inventory(ROOT)['kind'] != 'agents':
    for name in ('test_primary_iris_is_not_a_delegate_export', 'test_dependency_changes_require_a_reviewed_lock', 'test_dependency_resources_are_locked_too'):
        delattr(CollectionChecks, name)

for item in catalog.inventory(ROOT)['entries']:
    setattr(CollectionChecks, 'test_package_' + item['id'].replace('-', '_'), package_case(item))


if __name__ == '__main__':
    unittest.main()
