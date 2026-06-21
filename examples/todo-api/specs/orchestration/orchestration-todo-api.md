---
id: orchestration-todo-api
type: orchestration
version: 1.0
status: approved
owner: BOB demo
depends_on: [transformation-create-todo]
consumed_by: []
---

## Intent
Define execution behavior — how the store is exercised end to end — so the runtime
wiring is intentional. Even a tiny demo benefits from stating the operations and their
order explicitly.

## Contract
The `TodoStore` exposes:
- `create_todo(title, status=None) -> item` (per transformation spec).
- `list_todos() -> list[item]` returning items in creation order.
- `set_status(id, status) -> item` applying an allowed transition.
Operations are synchronous, in-memory, single-process. No retries/backoff needed.

## Business rules
- `set_status` on an unknown id raises `KeyError`.
- `list_todos` returns a copy; callers cannot mutate internal state.

## Downstream impact
Top of the chain; nothing consumes it. Changing the operation set changes the public
API.

## Verification
`tests/test_todo.py::test_list_order` and `test_set_status_transition`.
