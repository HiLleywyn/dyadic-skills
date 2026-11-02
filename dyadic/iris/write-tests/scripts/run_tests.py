"""Run a project's tests in the sandbox, where pytest isn't installed.

Usage: run_tests.py [PATH ...] [-k WORD]

PATH is a folder (searched for test_*.py and *_test.py) or a test file; the
current folder when none is given. It runs unittest TestCase classes and
plain test_* functions written with assert, pytest style (without fixtures;
async ones too). -k keeps only tests whose name contains WORD. It prints one
line per test, then each failure with its traceback, then a summary, and
exits with 1 when anything failed.
"""
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import inspect
import os
import sys
import time
import traceback
import unittest

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "build", "dist"}


def test_files(paths: list[str]) -> list[str]:
    found: list[str] = []
    for path in paths:
        if os.path.isfile(path):
            found.append(path)
            continue
        for folder, dirs, files in os.walk(path):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            found += [os.path.join(folder, f) for f in sorted(files)
                      if f.endswith(".py") and (f.startswith("test_") or f.endswith("_test.py"))]
    return found


def load(path: str):
    folder = os.path.dirname(os.path.abspath(path))
    for entry in (os.getcwd(), folder):
        if entry not in sys.path:
            sys.path.insert(0, entry)
    name = "tests_" + os.path.relpath(path).replace(os.sep, "_").removesuffix(".py").replace(".", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description="Run tests without pytest.")
    parser.add_argument("paths", nargs="*", default=["."])
    parser.add_argument("-k", dest="word", default="")
    args = parser.parse_args()
    results: list[tuple[str, str, str]] = []  # (name, outcome, details)
    started = time.monotonic()
    for path in test_files(args.paths):
        try:
            module = load(path)
        except Exception:
            results.append((path, "ERROR", traceback.format_exc()))
            continue
        for name, item in sorted(vars(module).items()):
            if inspect.isclass(item) and issubclass(item, unittest.TestCase) and item.__module__ == module.__name__:
                suite = unittest.defaultTestLoader.loadTestsFromTestCase(item)
                for case in suite:
                    full = f"{path}::{item.__name__}::{case._testMethodName}"
                    if args.word and args.word not in full:
                        continue
                    outcome = unittest.TestResult()
                    case.run(outcome)
                    if outcome.skipped:
                        results.append((full, "SKIP", outcome.skipped[0][1]))
                    elif outcome.failures or outcome.errors:
                        kind = "FAIL" if outcome.failures else "ERROR"
                        results.append((full, kind, (outcome.failures or outcome.errors)[0][1]))
                    else:
                        results.append((full, "PASS", ""))
            elif name.startswith("test") and inspect.isfunction(item) and item.__module__ == module.__name__:
                full = f"{path}::{name}"
                if args.word and args.word not in full:
                    continue
                if inspect.signature(item).parameters:
                    results.append((full, "SKIP", "takes arguments (pytest fixtures aren't available here)"))
                    continue
                try:
                    if inspect.iscoroutinefunction(item):
                        asyncio.run(item())
                    else:
                        item()
                    results.append((full, "PASS", ""))
                except AssertionError:
                    results.append((full, "FAIL", traceback.format_exc()))
                except Exception:
                    results.append((full, "ERROR", traceback.format_exc()))
    for full, outcome, _details in results:
        print(f"{outcome:5} {full}")
    problems = [r for r in results if r[1] in ("FAIL", "ERROR")]
    for full, outcome, details in problems:
        print(f"\n---- {outcome}: {full}\n{details.rstrip()}")
    counts = {kind: sum(1 for r in results if r[1] == kind) for kind in ("PASS", "FAIL", "ERROR", "SKIP")}
    print(f"\n{counts['PASS']} passed, {counts['FAIL']} failed, {counts['ERROR']} errors, {counts['SKIP']} skipped "
          f"in {time.monotonic() - started:.2f}s")
    if not results:
        print("No tests found: name files test_*.py and functions test_*.")
    return 1 if problems or not results else 0


if __name__ == "__main__":
    sys.exit(main())
