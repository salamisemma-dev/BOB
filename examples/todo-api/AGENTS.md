# examples/todo-api — the worked demo

## Purpose
A complete, valid BOB spec layer + conforming implementation + spec-traced tests.
Proof that the format and validator work end to end; also the tutorial's hands-on target.

## Ownership
Owns the demo's constitution, specs, code, and tests. Must always stay valid and green —
it's an integration check referenced by `../../tests/test_bob_validate.py`
(`test_todo_api_example_is_valid`) and by CI.

## Local Contracts
- `constitution.md` — the demo's supreme contract (stdlib only, in-memory, deterministic).
- `specs/<type>/<id>.md` — one approved spec per canonical type; all six represented.
- `src/todo.py` — implementation; every behavior traces to a spec.
- `tests/test_todo.py` — each test maps to a spec's Verification section.
- Invariant: changing a spec here means changing the matching code + test in the same edit.

## Work Guidance
Keep it tiny and dependency-free; it's a teaching example, not a product. If you add an
operation, follow `specs/ai-workflow/ai-workflow-add-endpoint.md` (spec → red → green →
refactor → validate).

## Verification
- `python -m unittest discover -s tests -v` (9 tests)
- `python ../../scripts/bob_validate.py .` → `OK: spec layer valid`
