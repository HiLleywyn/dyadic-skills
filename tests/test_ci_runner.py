"""Verify .lley/run.py rejects empty, zero-passed, skipped, failed, errored, malformed, and missing reports."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('lley_runner', ROOT / '.lley/run.py')
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class CiRunnerReportChecks(unittest.TestCase):
    def test_verify_junit_rejects_invalid_and_incomplete_reports(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'catalog.xml'
            with self.assertRaises(RuntimeError):
                RUNNER.verify_junit(p)
            for payload in (
                '',
                '<testsuite><',
                '<testsuite tests="0"/>',
                '<testsuite><testcase name="skip"><skipped/></testcase></testsuite>',
                '<testsuite><testcase name="ok"/><testcase name="skip"><skipped/></testcase></testsuite>',
                '<testsuite><testcase name="bad"><failure>fail</failure></testcase></testsuite>',
                '<testsuite><testcase name="err"><error>boom</error></testcase></testsuite>',
            ):
                p.write_text(payload, encoding='utf-8')
                with self.assertRaises(RuntimeError, msg=payload):
                    RUNNER.verify_junit(p)

            p.write_text('<testsuite><testcase name="ok"/></testsuite>', encoding='utf-8')
            self.assertEqual(RUNNER.verify_junit(p)['passed'], 1)
