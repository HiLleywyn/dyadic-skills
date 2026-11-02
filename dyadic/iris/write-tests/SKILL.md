---
name: "write-tests"
description: "Write focused, readable tests for code and run them in the sandbox. List the behaviours and cases first (usual, edge, failure), write one small test per behaviour named for what it proves, replace networks, clocks and randomness with fakes, run them with scripts/run_tests.py, and report honestly. Use when someone asks for tests, a test plan, more coverage, or a regression test for a bug."
---

# Write Tests

A good test proves one behaviour, fails for one reason, and tells the reader
what broke from its name alone. Write fewer, sharper tests rather than many
that check the same path.

## 1. Know what the code promises

Read the code and anything that describes it (docstring, README, the
request). Write the promises down as sentences before writing any test:

```
apply_discount(price, code):
- "SAVE10" takes 10% off.
- An unknown code leaves the price unchanged.
- The price never goes below 0.
- A negative price is an error (ValueError).
```

If a promise is unclear (what should happen for an expired code?), ask the
user, or test the current behaviour and say that you did.

## 2. Pick the cases

For each promise, choose cases from these groups:

- **Usual:** the common input.
- **Edges:** empty, zero, one item, the largest allowed, a boundary on each
  side (9, 10, 11 when 10 is the limit), unicode, time zones.
- **Failures:** bad input, a missing file, a service that errors or times
  out. Check the error type and message, not just that "something" failed.

## 3. Write them

- One behaviour per test, named for it:
  `test_unknown_code_leaves_price_unchanged`, not `test_discount_2`.
- Arrange, act, assert, in that order, with a blank line between.
- Assert exact values. For floats, compare with a tolerance
  (`abs(a - b) < 1e-9` or `assertAlmostEqual`).
- No network, real clock or randomness: pass in a fake, a fixed time or a
  seeded `random.Random(7)`. Tests must give the same result every run.
- Use invented data (a product called "Blue Kettle", a customer called
  "Rowan Vale"), never real people's details.
- Follow the project's existing test style and folder if it has one.

```python
import unittest
from shop.pricing import apply_discount


class ApplyDiscount(unittest.TestCase):
    def test_save10_takes_ten_percent_off(self):
        self.assertEqual(apply_discount(50.0, "SAVE10"), 45.0)

    def test_unknown_code_leaves_price_unchanged(self):
        self.assertEqual(apply_discount(50.0, "NOPE"), 50.0)

    def test_negative_price_is_refused(self):
        with self.assertRaises(ValueError):
            apply_discount(-1.0, "SAVE10")
```

Plain functions with `assert` work too:

```python
def test_price_never_goes_below_zero():
    assert apply_discount(0.5, "MINUS1") == 0
```

## 4. Run them

The sandbox has Python and its standard library, not pytest. Save the tests
in the workspace (for example `tests/test_pricing.py`), then run them with
`workspace.python` and this code:

```python
import runpy, sys
sys.argv = ["run_tests.py", "tests"]
runpy.run_path("/mnt/skills/write-tests/scripts/run_tests.py", run_name="__main__")
```

It runs unittest classes and plain `test_*` functions (async ones too),
prints a line per test, each failure's traceback, and a summary. Add `"-k",
"discount"` to the arguments to run only matching tests.

A test you write for a bug must fail before the fix and pass after it: run
it both ways when you can.

For a language the sandbox can't run, write the tests in the project's own
framework and say clearly that they were not run.

## 5. Report

- Which behaviours are covered, in a short list.
- The run: "9 passed, 0 failed" with anything skipped and why.
- What you didn't test and why (needs a database, needs the network).
- Any test that fails because the code is wrong: say so, and don't change the
  test to make it pass.
