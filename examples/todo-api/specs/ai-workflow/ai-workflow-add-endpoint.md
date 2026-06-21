---
id: ai-workflow-add-endpoint
type: ai-workflow
version: 1.0
status: approved
owner: BOB demo
depends_on: [schema-todo-item, transformation-create-todo, orchestration-todo-api]
consumed_by: []
---

## Intent
A reusable instruction block a sub-agent follows to add a new store operation. Captures
the repeatable "how we build one of these" so future work is consistent and cheap to
delegate to a cheaper model.

## Contract
Given a new operation `<name>` with input `<params>` and a referenced data spec:
1. Confirm or write the schema/validation/transformation spec it touches; get it approved.
2. Write the failing test in `tests/test_todo.py` first (red).
3. Implement the method on `TodoStore` in `src/todo.py` (green).
4. Refactor; keep methods small.
5. Run `python -m unittest` and `python ../../scripts/bob_validate.py .` — both must pass.

## Business rules
- No code before the relevant spec is approved.
- Every new operation gets at least one test tracing to a spec's Verification section.

## Downstream impact
None directly; governs how future operations are added.

## Verification
Process spec — verified by reviewer confirming the steps were followed and CI is green.
