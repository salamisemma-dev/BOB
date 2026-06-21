"""Tests for scripts/bob_validate.py — dependency-free, runnable with unittest.

Covers: a valid repo passes; each violation class is caught. Also validates the
shipped examples/todo-api as an integration check.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import bob_validate as bv  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

GOOD_SPEC = """---
id: schema-thing
type: schema
version: 1.0
status: approved
owner: me
depends_on: []
consumed_by: []
---

## Intent
why
## Contract
what
## Business rules
rules
## Downstream impact
impact
## Verification
test
"""


def write(root: Path, rel: str, content: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


class TestParse(unittest.TestCase):
    def test_frontmatter_lists(self):
        fm, body = bv.parse_frontmatter(GOOD_SPEC)
        self.assertEqual(fm["id"], "schema-thing")
        self.assertEqual(fm["depends_on"], [])
        self.assertIn("## Intent", body)

    def test_no_frontmatter(self):
        fm, body = bv.parse_frontmatter("no fences here")
        self.assertIsNone(fm)

    def test_sections(self):
        _, body = bv.parse_frontmatter(GOOD_SPEC)
        secs = bv.section_bodies(body)
        self.assertEqual(secs["Intent"], "why")


class TestValidate(unittest.TestCase):
    def _root(self):
        d = Path(tempfile.mkdtemp())
        write(d, "constitution.md", "# c")
        return d

    def test_valid_repo_passes(self):
        d = self._root()
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, _ = bv.validate(d)
        self.assertEqual(errors, [])

    def test_missing_constitution(self):
        d = Path(tempfile.mkdtemp())
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, _ = bv.validate(d)
        self.assertTrue(any("constitution.md" in e for e in errors))

    def test_bad_type(self):
        d = self._root()
        write(d, "specs/x/bad.md", GOOD_SPEC.replace("type: schema", "type: nonsense"))
        errors, _ = bv.validate(d)
        self.assertTrue(any("not a canonical" in e for e in errors))

    def test_missing_section(self):
        d = self._root()
        write(d, "specs/x/s.md", GOOD_SPEC.replace("## Verification\ntest\n", ""))
        errors, _ = bv.validate(d)
        self.assertTrue(any("Verification" in e for e in errors))

    def test_empty_section_when_approved(self):
        d = self._root()
        broken = GOOD_SPEC.replace("## Intent\nwhy", "## Intent\n")
        write(d, "specs/x/s.md", broken)
        errors, _ = bv.validate(d)
        self.assertTrue(any("empty" in e for e in errors))

    def test_duplicate_id(self):
        d = self._root()
        write(d, "specs/x/a.md", GOOD_SPEC)
        write(d, "specs/x/b.md", GOOD_SPEC)
        errors, _ = bv.validate(d)
        self.assertTrue(any("duplicate spec id" in e for e in errors))

    def test_dangling_depends_on(self):
        d = self._root()
        write(d, "specs/x/s.md", GOOD_SPEC.replace("depends_on: []", "depends_on: [missing-spec]"))
        errors, _ = bv.validate(d)
        self.assertTrue(any("does not resolve" in e for e in errors))

    def test_missing_required_key(self):
        d = self._root()
        write(d, "specs/x/s.md", GOOD_SPEC.replace("owner: me\n", ""))
        errors, _ = bv.validate(d)
        self.assertTrue(any("missing required key 'owner'" in e for e in errors))


class TestShippedExample(unittest.TestCase):
    def test_todo_api_example_is_valid(self):
        errors, _ = bv.validate(REPO_ROOT / "examples" / "todo-api")
        self.assertEqual(errors, [], f"shipped example invalid: {errors}")


if __name__ == "__main__":
    unittest.main()
