# Contributing to BOB

BOB eats its own dog food: changes follow the BOB workflow.

## Ground rules
- **Spec or behavior change → update docs/specs in the same PR.** No drift.
- **Tests required.** Changes to `scripts/bob_validate.py` need a case in
  `tests/test_bob_validate.py`. Changes to the demo need a test in
  `examples/todo-api/tests/`.
- **Green CI.** `python -m unittest tests.test_bob_validate` and the demo tests must
  pass; `python scripts/bob_validate.py examples/todo-api` must say OK.
- **Dependency-free.** Scripts stay stdlib-only so they run anywhere.

## Local check (run before pushing)
```
python -m unittest tests.test_bob_validate -v
python -m unittest discover -s examples/todo-api/tests -v
python scripts/bob_validate.py examples/todo-api
```

## Layout
See [`AGENTS.md`](AGENTS.md) for the per-folder contracts (read before editing).

## Issues / discussion
Known gaps and roadmap live in the issue tracker. Limitations are documented honestly
in `docs/PVA.md` — if you hit one, file it.
