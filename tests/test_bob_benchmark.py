"""Tests for scripts/bob_benchmark.py — stdlib only, runnable with unittest."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import bob_benchmark as bb  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO = REPO_ROOT / "examples" / "todo-api"


class TestParseUnittest(unittest.TestCase):
    def test_all_pass(self):
        out = "test_x ... ok\n\nRan 9 tests in 0.01s\n\nOK\n"
        ran, passed, failed = bb.parse_unittest(out)
        self.assertEqual((ran, passed, failed), (9, 9, 0))

    def test_failures_and_errors(self):
        out = "Ran 10 tests in 0.1s\n\nFAILED (failures=2, errors=1)\n"
        ran, passed, failed = bb.parse_unittest(out)
        self.assertEqual((ran, passed, failed), (10, 7, 3))

    def test_no_summary(self):
        self.assertEqual(bb.parse_unittest("garbage"), (0, 0, 0))


class TestTokens(unittest.TestCase):
    def test_heuristic_nonzero(self):
        # Even without tiktoken, a non-empty string yields a positive count.
        self.assertGreater(bb.count_tokens("hello world this is text"), 0)

    def test_empty(self):
        self.assertEqual(bb.count_tokens(""), 0)


class TestEndToEnd(unittest.TestCase):
    def test_demo_runs_green_and_reports(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "report.md"
            rc = bb.main(["--demo", str(DEMO), "--output", str(out)])
            self.assertEqual(rc, 0, "benchmark should be green on the shipped demo")
            self.assertTrue(out.is_file())
            text = out.read_text(encoding="utf-8")
            self.assertIn("# BOB Benchmark Report", text)
            self.assertIn("Validator | PASS", text)

    def test_missing_demo_returns_1(self):
        rc = bb.main(["--demo", "does/not/exist", "--output", "x.md"])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
