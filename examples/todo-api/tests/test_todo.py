"""Tests for the Todo API demo. Each test traces to a spec Verification section."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from todo import TodoStore, ITEM_FIELDS  # noqa: E402


class TestTodo(unittest.TestCase):
    def setUp(self):
        self.store = TodoStore()

    # schema-todo-item
    def test_item_shape(self):
        item = self.store.create_todo("buy milk")
        self.assertEqual(set(item.keys()), set(ITEM_FIELDS))
        self.assertIsInstance(item["id"], str)
        self.assertIsInstance(item["title"], str)

    # semantic-todo-status
    def test_default_status(self):
        item = self.store.create_todo("task")
        self.assertEqual(item["status"], "open")

    def test_invalid_status_rejected(self):
        with self.assertRaises(ValueError):
            self.store.create_todo("task", status="archived")

    # validation-todo-input
    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.store.create_todo("   ")

    # transformation-create-todo
    def test_create_returns_conforming_item(self):
        item = self.store.create_todo("  trimmed  ")
        self.assertEqual(item["title"], "trimmed")
        self.assertEqual(item["status"], "open")

    def test_ids_unique(self):
        a = self.store.create_todo("a")
        b = self.store.create_todo("b")
        self.assertNotEqual(a["id"], b["id"])

    # orchestration-todo-api
    def test_list_order(self):
        self.store.create_todo("first")
        self.store.create_todo("second")
        titles = [i["title"] for i in self.store.list_todos()]
        self.assertEqual(titles, ["first", "second"])

    def test_set_status_transition(self):
        item = self.store.create_todo("task")
        updated = self.store.set_status(item["id"], "done")
        self.assertEqual(updated["status"], "done")

    def test_set_status_unknown_id(self):
        with self.assertRaises(KeyError):
            self.store.set_status("999", "done")


if __name__ == "__main__":
    unittest.main()
