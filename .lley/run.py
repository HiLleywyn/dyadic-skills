"""Run offline collection tests and emit real JUnit cases for lley.cat Actions."""
from pathlib import Path
import sys
import time
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Results(unittest.TextTestResult):
    def startTest(self, test):
        self.started = time.perf_counter()
        super().startTest(test)

    def addSuccess(self, test):
        self.record(test)
        super().addSuccess(test)

    def addFailure(self, test, err):
        self.record(test, 'failure', self._exc_info_to_string(err, test))
        super().addFailure(test, err)

    def addError(self, test, err):
        self.record(test, 'error', self._exc_info_to_string(err, test))
        super().addError(test, err)

    def addSkip(self, test, reason):
        self.record(test, 'skipped', reason)
        super().addSkip(test, reason)

    def addSubTest(self, test, subtest, err):
        if err:
            self.record(subtest, 'failure', self._exc_info_to_string(err, test))
        super().addSubTest(test, subtest, err)

    def record(self, test, status=None, message=''):
        case = ET.SubElement(suite_xml, 'testcase', name=test.id().split('.')[-1], classname=test.__class__.__name__, time=f'{time.perf_counter() - self.started:.6f}')
        if status:
            ET.SubElement(case, status, message=message.splitlines()[-1][:400] if message else status).text = message


suite_xml = ET.Element('testsuite', name='Collection')
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
result = unittest.TextTestRunner(verbosity=2, resultclass=Results).run(suite)
suite_xml.set('tests', str(len(suite_xml)))
suite_xml.set('failures', str(len(result.failures)))
suite_xml.set('errors', str(len(result.errors)))
suite_xml.set('skipped', str(len(result.skipped)))
reports = ROOT / 'reports'
reports.mkdir(exist_ok=True)
ET.ElementTree(suite_xml).write(reports / 'catalog.xml', encoding='utf-8', xml_declaration=True)
sys.exit(not result.wasSuccessful())
