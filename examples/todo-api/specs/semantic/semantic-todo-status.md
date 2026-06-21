---
id: semantic-todo-status
type: semantic
version: 1.0
status: approved
owner: BOB demo
depends_on: []
consumed_by: [schema-todo-item, transformation-create-todo]
---

## Intent
Pin the shared meaning of "status" so every component uses the same vocabulary. When
a business term is defined in one place, you avoid the classic bug where two modules
disagree on what "done" means.

## Contract
Canonical status values and their meaning:
- `open` — created, not yet completed. Default on creation.
- `done` — completed.
There are no other valid values.

## Business rules
- New todos start as `open`.
- Transitions allowed: `open → done` and `done → open` (re-open). No others.

## Downstream impact
Consumed by `schema-todo-item` (status field domain) and `transformation-create-todo`
(sets the default). Adding/removing a value is a breaking change.

## Verification
`tests/test_todo.py::test_default_status` asserts a new todo is `open`;
`test_invalid_status_rejected` asserts unknown values are refused.
