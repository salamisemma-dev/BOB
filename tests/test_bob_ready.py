"""Tests for scripts/bob_ready.py — stdlib only."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import bob_ready as br  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO = REPO_ROOT / "examples" / "todo-api"


def write(root: Path, rel: str, content: str = ""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


class TestReady(unittest.TestCase):
    def test_demo_is_ready(self):
        rc = br.main(["--json", str(DEMO)])
        self.assertEqual(rc, 0, "shipped demo should be BOB-ready")

    def test_empty_dir_not_ready(self):
        with tempfile.TemporaryDirectory() as d:
            rc = br.main([str(d)])
            self.assertEqual(rc, 1)

    def test_assess_reports_each_criterion(self):
        with tempfile.TemporaryDirectory() as d:
            results = br.assess(Path(d))
            self.assertEqual(len(results), 6)
            by_name = {n: p for n, p, _ in results}
            # File-presence + approved-spec criteria must be False on an empty dir.
            self.assertFalse(by_name["constitution.md present"])
            self.assertFalse(by_name["at least one approved spec"])
            self.assertFalse(by_name["test suite present"])
            self.assertFalse(by_name["AGENTS.md present (DOX)"])

    def test_detects_vitest_style_src_tests(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "src" / "__tests__").mkdir(parents=True)
            ok, detail = br._has_test_suite(root)
            self.assertTrue(ok)
            self.assertEqual(detail, "src/__tests__/")

    def test_detects_common_test_file_patterns(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write(root, "src/services/foo.spec.ts", "")
            ok, detail = br._has_test_suite(root)
            self.assertTrue(ok)
            self.assertEqual(detail, "src/services/foo.spec.ts")

    def test_ignores_dependency_test_files(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write(root, "node_modules/pkg/foo.test.ts", "")
            ok, _ = br._has_test_suite(root)
            self.assertFalse(ok)

    def test_run_tests_adds_criterion_and_passes_on_green(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write(root, "tests/test_ok.py",
                  "import unittest\n"
                  "class T(unittest.TestCase):\n"
                  "    def test_ok(self):\n        self.assertTrue(True)\n")
            results = br.assess(root, run_tests=True)
            names = [n for n, _, _ in results]
            self.assertIn("test suite passes (--run-tests)", names)
            passed = {n: p for n, p, _ in results}["test suite passes (--run-tests)"]
            self.assertTrue(passed)

    def test_run_tests_fails_on_red_suite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write(root, "tests/test_bad.py",
                  "import unittest\n"
                  "class T(unittest.TestCase):\n"
                  "    def test_bad(self):\n        self.fail('boom')\n")
            passed, _ = br._run_tests(root)
            self.assertFalse(passed)

    def test_run_tests_no_command_detected(self):
        with tempfile.TemporaryDirectory() as d:
            passed, detail = br._run_tests(Path(d))
            self.assertFalse(passed)
            self.assertIn("no runnable test command", detail)


if __name__ == "__main__":
    unittest.main()
