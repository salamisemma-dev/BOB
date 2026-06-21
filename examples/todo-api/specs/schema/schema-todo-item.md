---
id: schema-todo-item
type: schema
version: 1.0
status: approved
owner: BOB demo
depends_on: []
consumed_by: [transformation-create-todo, validation-todo-input]
---

## Intent
Define the structural shape of a Todo item so every component agrees on field names
and types. Structure drift (a renamed field, a wrong type) is the most common silent
breakage in pipelines; pinning it in a schema spec makes that drift a failed check.

## Contract
A Todo item is an object with:
- `id`: string, required, unique within a store.
- `title`: string, required, non-empty after trim.
- `status`: string, required, one of the values in `semantic-todo-status`.
- `created_at`: string, required, UTC ISO-8601.

JSON Schema (the executable contract):
```json
{
  "type": "object",
  "required": ["id", "title", "status", "created_at"],
  "properties": {
    "id": {"type": "string"},
    "title": {"type": "string", "minLength": 1},
    "status": {"type": "string"},
    "created_at": {"type": "string"}
  },
  "additionalProperties": false
}
```

## Business rules
- `id` is server-assigned, never supplied by the client.
- `title` is trimmed before storage; empty-after-trim is rejected (see validation spec).

## Downstream impact
Consumed by `transformation-create-todo` (builds items) and `validation-todo-input`.
Renaming or retyping any field is a breaking change → bump major, update both.

## Verification
`tests/test_todo.py::test_item_shape` asserts a created item has exactly these keys
with these types.
