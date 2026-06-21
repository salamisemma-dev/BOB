# Project Constitution — Todo API (BOB demo)

Version: 1.0 · Last updated: 2026-06-21 · Owner: BOB demo

Supreme contract for the demo. Shows a real, valid spec layer that BOB's validator
passes. Small on purpose.

## 1. Technology standards
- Language / runtime: Python 3.8+, standard library only (no third-party deps).
- Tests: stdlib `unittest`, runnable with `python -m unittest`.
- No network or persistent storage — in-memory store, deterministic.

## 2. Naming conventions
- Files / modules: `snake_case.py`.
- Spec ids: `<type>-<slug>` (e.g. `schema-todo-item`).
- Public functions: verbs (`create_todo`, `list_todos`).

## 3. Architecture rules & boundaries
- `src/` holds implementation; `tests/` holds tests; `specs/` is the source of truth.
- Implementation conforms to specs; specs change first, code follows.
- No business rule lives only in code — it must trace to a spec.

## 4. Governance
- Spec approval: a spec must be `status: approved` before its code is written.
- Versioning: semver per spec; major = breaking contract change.
- Breaking change: bump major, update consumed_by specs, note in amendment log.

## 5. Invariants (must hold platform-wide)
- All ids are strings; todo ids are unique within a store.
- Status is one of the canonical values defined in `semantic-todo-status`.
- Titles are non-empty after trimming whitespace.

## 6. Amendment log
- 2026-06-21 — created. Why: demonstrate a complete, valid BOB spec layer.
