"""Tests for scripts/bob_validate.py — dependency-free, runnable with unittest."""
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
See `tests/test_thing.py::test_it`.
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
        write(d, "tests/test_thing.py", "def test_it():\n    assert True\n")
        return d

    def test_specs_agents_md_is_ignored(self):
        d = self._root()
        write(d, "specs/AGENTS.md", "# local contract\n")
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, _ = bv.validate(d)
        self.assertEqual(errors, [])

    def test_valid_repo_passes(self):
        d = self._root()
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, _ = bv.validate(d, strict=True)
        self.assertEqual(errors, [])

    def test_typescript_test_reference_passes(self):
        d = self._root()
        write(d, "src/__tests__/thing.test.ts", "import { test, expect } from 'vitest';\ntest('handlesThing', () => { expect(true).toBe(true); });\n")
        spec = GOOD_SPEC.replace("tests/test_thing.py::test_it", "src/__tests__/thing.test.ts::handlesThing")
        write(d, "specs/schema/schema-thing.md", spec)
        errors, _ = bv.validate(d, strict=True)
        self.assertEqual(errors, [])

    def test_typescript_missing_test_name_fails(self):
        d = self._root()
        write(d, "src/__tests__/thing.test.ts", "import { test, expect } from 'vitest';\ntest('otherThing', () => { expect(true).toBe(true); });\n")
        spec = GOOD_SPEC.replace("tests/test_thing.py::test_it", "src/__tests__/thing.test.ts::handlesThing")
        write(d, "specs/schema/schema-thing.md", spec)
        errors, _ = bv.validate(d)
        self.assertTrue(any("handlesThing" in e for e in errors))

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
        write(d, "specs/x/s.md", GOOD_SPEC.replace("## Verification\nSee `tests/test_thing.py::test_it`.\n", ""))
        errors, _ = bv.validate(d)
        self.assertTrue(any("Verification" in e for e in errors))

    def test_empty_section_when_approved(self):
        d = self._root()
        write(d, "specs/x/s.md", GOOD_SPEC.replace("## Intent\nwhy", "## Intent\n"))
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

    def test_fleet_deviation_marker_warns_by_default(self):
        d = self._root()
        write(d, "constitution.md", "# c\n\nDeviation: pending core ratification\n")
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, warnings = bv.validate(d)
        self.assertEqual(errors, [])
        self.assertTrue(any("pending core ratification" in w for w in warnings))

    def test_fleet_deviation_marker_fails_under_strict(self):
        d = self._root()
        write(d, "constitution.md", "# c\n")
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC + "\nPending Core Ratification\n")
        errors, warnings = bv.validate(d, strict=True)
        self.assertTrue(any("pending core ratification" in e for e in errors))
        self.assertEqual(warnings, [])


class TestTraceability(unittest.TestCase):
    def _root(self):
        d = Path(tempfile.mkdtemp())
        write(d, "constitution.md", "# c")
        return d

    def test_missing_test_reference_fails(self):
        d = self._root()
        spec = GOOD_SPEC.replace("See `tests/test_thing.py::test_it`.", "manual review only")
        write(d, "specs/x/s.md", spec)
        errors, _ = bv.validate(d)
        self.assertTrue(any("no test reference" in e for e in errors))

    def test_broken_test_file_fails(self):
        d = self._root()
        spec = GOOD_SPEC.replace("tests/test_thing.py::test_it", "tests/missing.py::test_x")
        write(d, "specs/x/s.md", spec)
        errors, _ = bv.validate(d)
        self.assertTrue(any("does not" in e and "exist" in e for e in errors))

    def test_missing_test_function_fails(self):
        d = self._root()
        write(d, "tests/test_thing.py", "def test_other():\n    assert True\n")
        write(d, "specs/x/s.md", GOOD_SPEC)
        errors, _ = bv.validate(d)
        self.assertTrue(any("not found in" in e for e in errors))

    def test_ai_workflow_exempt(self):
        d = self._root()
        spec = GOOD_SPEC.replace("type: schema", "type: ai-workflow").replace("id: schema-thing", "id: ai-workflow-thing").replace("See `tests/test_thing.py::test_it`.", "reviewer confirms steps")
        write(d, "specs/x/s.md", spec)
        errors, _ = bv.validate(d, strict=True)
        self.assertEqual(errors, [])

    def test_verification_manual_exempt(self):
        d = self._root()
        spec = GOOD_SPEC.replace("owner: me", "owner: me\nverification: manual").replace("See `tests/test_thing.py::test_it`.", "manual check")
        write(d, "specs/x/s.md", spec)
        errors, _ = bv.validate(d, strict=True)
        self.assertEqual(errors, [])

    def test_flag_disables_gate_in_non_strict_mode(self):
        d = self._root()
        spec = GOOD_SPEC.replace("See `tests/test_thing.py::test_it`.", "manual review only")
        write(d, "specs/x/s.md", spec)
        errors, _ = bv.validate(d, traceability=False)
        self.assertEqual(errors, [])

    def test_strict_rejects_no_traceability_escape(self):
        d = self._root()
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, _ = bv.validate(d, traceability=False, strict=True)
        self.assertTrue(any("--strict cannot be combined" in e for e in errors))

    def test_strict_fails_assertionless_test_file(self):
        d = self._root()
        write(d, "tests/test_thing.py", "def test_it():\n    pass\n")
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, warnings = bv.validate(d, strict=True)
        self.assertTrue(any("no obvious" in e for e in errors))
        self.assertEqual(warnings, [])

    def test_non_strict_warns_on_assertionless_test_file(self):
        d = self._root()
        write(d, "tests/test_thing.py", "def test_it():\n    pass\n")
        write(d, "specs/schema/schema-thing.md", GOOD_SPEC)
        errors, warnings = bv.validate(d)
        self.assertEqual(errors, [])
        self.assertTrue(any("no obvious" in w for w in warnings))

    def test_draft_spec_not_gated(self):
        d = self._root()
        spec = GOOD_SPEC.replace("status: approved", "status: draft").replace("See `tests/test_thing.py::test_it`.", "tbd")
        write(d, "specs/x/s.md", spec)
        errors, _ = bv.validate(d, strict=True)
        self.assertEqual(errors, [])


class TestShippedExample(unittest.TestCase):
    def test_todo_api_example_is_valid(self):
        errors, _ = bv.validate(REPO_ROOT / "examples" / "todo-api", strict=True)
        self.assertEqual(errors, [], f"shipped example invalid: {errors}")


if __name__ == "__main__":
    unittest.main()
