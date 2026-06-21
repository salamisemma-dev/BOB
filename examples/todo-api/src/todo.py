"""Todo API demo — implementation that conforms to the specs in ../specs.

Each behavior traces to a spec; see the spec's Verification section for the test.
Standard library only, in-memory, deterministic (per the constitution).
"""
from __future__ import annotations

from datetime import datetime, timezone

# Canonical status values — defined by semantic-todo-status.
VALID_STATUSES = {"open", "done"}
DEFAULT_STATUS = "open"

# Allowed transitions — semantic-todo-status business rules.
_ALLOWED_TRANSITIONS = {("open", "done"), ("done", "open")}

# Item fields — schema-todo-item.
ITEM_FIELDS = ("id", "title", "status", "created_at")


def _now_iso() -> str:
    """Current time as UTC ISO-8601 (constitution invariant)."""
    return datetime.now(timezone.utc).isoformat()


def validate_input(title, status=None):
    """validation-todo-input: reject bad create-input at the boundary."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a non-empty string")
    if status is not None and status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")


class TodoStore:
    """orchestration-todo-api: synchronous, in-memory store."""

    def __init__(self):
        self._items = []
        self._counter = 0

    def create_todo(self, title, status=None):
        """transformation-create-todo: validated input -> stored item."""
        validate_input(title, status)
        self._counter += 1
        item = {
            "id": str(self._counter),
            "title": title.strip(),
            "status": status if status is not None else DEFAULT_STATUS,
            "created_at": _now_iso(),
        }
        self._items.append(item)
        return dict(item)

    def list_todos(self):
        """Return items in creation order; callers get copies, not internals."""
        return [dict(i) for i in self._items]

    def set_status(self, todo_id, status):
        """Apply an allowed status transition; KeyError on unknown id."""
        if status not in VALID_STATUSES:
            raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")
        for item in self._items:
            if item["id"] == todo_id:
                if (item["status"], status) not in _ALLOWED_TRANSITIONS and item["status"] != status:
                    raise ValueError(f"transition {item['status']} -> {status} not allowed")
                item["status"] = status
                return dict(item)
        raise KeyError(todo_id)
