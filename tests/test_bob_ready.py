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
            rc = br.main([str(d), "--no-run-tests"])
            self.assertEqual(rc, 1)

    def test_assess_reports_each_criterion(self):
        with tempfile.TemporaryDirectory() as d:
            results = br.assess(Path(d), run_tests=False)
            self.assertEqual(len(results), 7)
            by_name = {n: p for n, p, _ in results}
            self.assertFalse(by_name["constitution.md present"])
            self.assertFalse(by_name["at least one approved spec"])
            self.assertFalse(by_name["test suite present"])
            self.assertTrue(by_name["test command passes"])
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

    def test_run_tests_failure_blocks_readiness(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write(root, "package.json", '{"scripts":{"test":"node missing-test-file.js"}}')
            ok, detail = br._run_tests(root)
            self.assertFalse(ok)
            self.assertTrue("FAILED" in detail or "not found" in detail or "could not run" in detail)

    def test_no_supported_test_command_fails(self):
        with tempfile.TemporaryDirectory() as d:
            ok, detail = br._run_tests(Path(d))
            self.assertFalse(ok)
            self.assertIn("no supported test command", detail)


if __name__ == "__main__":
    unittest.main()
