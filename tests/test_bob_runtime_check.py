"""Tests for scripts/bob_runtime_check.py — stdlib only."""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import bob_runtime_check as rc  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO = REPO_ROOT / "examples" / "todo-api"

SCHEMA = {
    "type": "object",
    "required": ["id", "title", "status"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string", "minLength": 1},
        "status": {"type": "string", "enum": ["open", "done"]},
    },
    "additionalProperties": False,
}


class TestSchemaChecker(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(rc.json_schema_check(SCHEMA, {"id": "1", "title": "x", "status": "open"}), [])

    def test_missing_required(self):
        errs = rc.json_schema_check(SCHEMA, {"id": "1", "status": "open"})
        self.assertTrue(any("missing required" in e for e in errs))

    def test_min_length(self):
        errs = rc.json_schema_check(SCHEMA, {"id": "1", "title": "", "status": "open"})
        self.assertTrue(any("minLength" in e for e in errs))

    def test_additional_property(self):
        errs = rc.json_schema_check(SCHEMA, {"id": "1", "title": "x", "status": "open", "z": 1})
        self.assertTrue(any("additional property" in e for e in errs))

    def test_enum(self):
        errs = rc.json_schema_check(SCHEMA, {"id": "1", "title": "x", "status": "archived"})
        self.assertTrue(any("enum" in e for e in errs))

    def test_wrong_type_and_bool_not_int(self):
        errs = rc.json_schema_check(SCHEMA, {"id": 1, "title": "x", "status": "open"})
        self.assertTrue(any("expected type" in e for e in errs))
        # bool must not satisfy integer
        self.assertNotEqual(rc.json_schema_check({"type": "integer"}, True), [])


class TestExtractSchema(unittest.TestCase):
    def test_extract(self):
        text = "## Contract\n```json\n{\"type\": \"object\"}\n```\n"
        self.assertEqual(rc.extract_schema(text), {"type": "object"})

    def test_no_block(self):
        self.assertIsNone(rc.extract_schema("no json here"))


class TestShippedDemo(unittest.TestCase):
    def test_demo_golden_passes(self):
        errors, _ = rc.run(DEMO)
        self.assertEqual(errors, [], f"demo golden runtime check failed: {errors}")


if __name__ == "__main__":
    unittest.main()
