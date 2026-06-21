---
id: validation-todo-input
type: validation
version: 1.0
status: approved
owner: BOB demo
depends_on: [schema-todo-item, semantic-todo-status]
consumed_by: [transformation-create-todo]
---

## Intent
Define what makes create-input correct, so bad data is rejected at the boundary rather
than corrupting the store. Validation rules are the quality gate; encoding them as a
spec lets tests and runtime checks share one source of truth.

## Contract
For `create_todo(title, status=None)`:
- `title` must be a string and non-empty after `str.strip()` → else `ValueError`.
- `status`, if provided, must be a value from `semantic-todo-status` → else `ValueError`.
- nothing else is accepted as input.

## Business rules
- Whitespace-only titles are invalid (trim then check).
- Omitted status is not an error — it defaults (see transformation spec).

## Downstream impact
Consumed by `transformation-create-todo`, which must call this validation before
building an item. Loosening a rule here weakens the store's guarantees.

## Verification
`tests/test_todo.py::test_empty_title_rejected` and `test_invalid_status_rejected`.
