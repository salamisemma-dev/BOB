# scripts — executable backbone

## Purpose
The scripts that make BOB's specs executable instead of decorative.

## Ownership
Owns the validator, runtime checker, ready gate, benchmark, and retrofit-scaffolder logic and their contracts. Test files live in `../tests/`; keep them in sync. The spec format these enforce is owned by `../docs/SPEC-FORMAT.md`.

## Local Contracts
- `bob_validate.py` — reads `*.md` only, never executes project code; exits 1 on any spec error, 0 otherwise; `--json` for machine output. `--strict` is CI-grade: traceability cannot be disabled and linked tests with no obvious assertion become errors. `--no-traceability` is diagnostic only and forbidden with `--strict`.
- `bob_runtime_check.py` — golden-file checks for `schema` specs: extracts the ```json schema from Contract, validates `golden/<spec-id>/valid|invalid/*.json` with a stdlib JSON-Schema subset. Exit 1 if a valid sample fails or an invalid one passes.
- `bob_ready.py` — adoption / fail-fast gate; composes strict validator + runtime check + file presence + real test execution into a 7-point readiness checklist. Exit 0 only if all pass. `--no-run-tests` is diagnostic only; CI must not use it. `--run-tests` is accepted as a backwards-compatible no-op because tests run by default.
- `bob_analyze.py` — retrofit scaffolder; dry-run by default, `--write` to create draft files; never overwrites an existing `constitution.md`; only writes under `constitution.md` and `specs/_drafts/`. Skips dependency/build/archive dirs and tolerates broken paths in brownfield repos.
- `bob_benchmark.py` — quality + footprint baseline; runs strict validator + tests + token count, writes a Markdown report, exit 0 only if both pass. `--json` for CI. tiktoken optional (exact tokens), stdlib heuristic otherwise.
- All scripts: Python 3.8+, standard library only. No required third-party imports.

## Work Guidance
Any change to validation rules requires a matching test and a doc update in the same change. Keep messages actionable (say how to fix). Do not weaken strict gates to make a project look ready.

## Verification
From the repo root:
- `python -m unittest discover -s tests -v` (tooling 55)
- `python scripts/bob_validate.py --strict examples/todo-api` -> OK
- `python scripts/bob_runtime_check.py examples/todo-api` -> OK
- `python scripts/bob_ready.py examples/todo-api` -> READY 7/7
