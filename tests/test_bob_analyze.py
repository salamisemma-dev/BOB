"""Tests for scripts/bob_analyze.py — stdlib only."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import bob_analyze as ba  # noqa: E402


class TestAnalyze(unittest.TestCase):
    def test_scan_skips_archives_and_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "src").mkdir()
            (root / "src" / "app.ts").write_text("export const ok = true;\n", encoding="utf-8")
            (root / "_archive" / "old" / "node_modules" / "pkg").mkdir(parents=True)
            (root / "_archive" / "old" / "node_modules" / "pkg" / "ignored.ts").write_text("", encoding="utf-8")
            (root / "node_modules" / "pkg").mkdir(parents=True)
            (root / "node_modules" / "pkg" / "ignored.js").write_text("", encoding="utf-8")

            languages, modules, components = ba.scan(root)

            self.assertEqual(languages, ["ts"])
            self.assertEqual(modules, ["src"])
            self.assertEqual(components, ["src/app.ts"])

    def test_dry_run_main_handles_basic_project(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "src").mkdir()
            (root / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
            self.assertEqual(ba.main([str(root)]), 0)


if __name__ == "__main__":
    unittest.main()
