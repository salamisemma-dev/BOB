---
id: transformation-create-todo
type: transformation
version: 1.0
status: approved
owner: BOB demo
depends_on: [schema-todo-item, semantic-todo-status, validation-todo-input]
consumed_by: [orchestration-todo-api]
---

## Intent
Define the business logic that turns validated input into a stored Todo item. This is
the "what actually happens" layer; keeping it specced means the mapping from request
to record is explicit and testable, not buried in handler code.

## Contract
`create_todo(title, status=None) -> item`:
1. Validate input per `validation-todo-input`.
2. Trim `title`.
3. `status` defaults to `open` (per `semantic-todo-status`) when omitted.
4. Assign a unique string `id` (monotonic counter as a string).
5. Set `created_at` to current UTC ISO-8601.
6. Return an item conforming to `schema-todo-item`.

## Business rules
- Ids are assigned by the store and increase; they are never reused.
- Creation never mutates existing items.

## Downstream impact
Consumed by `orchestration-todo-api`. Changing the id scheme or default status is a
breaking behavior change.

## Verification
`tests/test_todo.py::test_create_returns_conforming_item` and `test_ids_unique`.
