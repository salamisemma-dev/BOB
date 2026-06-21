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
            self.assertFalse(by_name["tests/ directory present"])
            self.assertFalse(by_name["AGENTS.md present (DOX)"])


if __name__ == "__main__":
    unittest.main()
