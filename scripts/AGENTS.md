# scripts — executable backbone

## Purpose
The five scripts that make BOB's specs "executable" instead of decorative.

## Ownership
Owns the validator and retrofit-scaffolder logic and their contracts. Test files live
in `../tests/` (validator) — keep them in sync. The spec *format* these enforce is
owned by `../docs/SPEC-FORMAT.md`.

## Local Contracts
- `bob_validate.py` — reads `*.md` only, never executes project code; exits 1 on any
  spec error, 0 otherwise; `--json` for machine output; `--no-traceability` for
  structural-only. Enforces structure AND the spec-to-test traceability gate (every
  approved non-`ai-workflow` spec must reference an existing test in Verification, unless
  frontmatter `verification: manual`). Traceability supports Python and JS/TS test
  references (`.py/.js/.mjs/.cjs/.ts/.tsx/.jsx`, optional `::name`); `specs/AGENTS.md`
  (DOX) is not treated as a spec. Allowed spec types and required sections are
  constants at the top — change them here AND in `../docs/SPEC-FORMAT.md` AND add a test
  in `../tests/test_bob_validate.py`.
- `bob_runtime_check.py` — golden-file checks for `schema` specs: extracts the ```json
  schema from Contract, validates `golden/<spec-id>/valid|invalid/*.json` with a stdlib
  JSON-Schema subset. Exit 1 if a valid sample fails or an invalid one passes. Tests:
  `../tests/test_bob_runtime_check.py`.
- `bob_ready.py` — adoption / fail-fast gate; composes validator + runtime check + file
  presence into a 6-point readiness checklist. Exit 0 only if all pass. Recognizes
  Python and JS/TS test suites (`tests/`, `src/__tests__/`, or `*.(test|spec).*`).
  Tests: `../tests/test_bob_ready.py`. Doc: `../docs/ADOPTION.md`.
- `bob_analyze.py` — retrofit scaffolder; dry-run by default, `--write` to create draft
  files; never overwrites an existing `constitution.md`; only writes under
  `constitution.md` and `specs/_drafts/`. Crash-safe `os.walk` traversal that skips
  `node_modules/_archive/dist/.git/...` and tolerates broken paths. Tests:
  `../tests/test_bob_analyze.py`.
- `bob_benchmark.py` — quality + footprint baseline; runs validator + tests + token
  count, writes a Markdown report, exit 0 only if both pass. `--json` for CI. tiktoken
  optional (exact tokens), stdlib heuristic otherwise. Tests in
  `../tests/test_bob_benchmark.py`; doc + PvA in `../docs/BENCHMARK.md`.
- All: Python 3.8+, standard library only. No required third-party imports
  (tiktoken is an optional enhancement).

## Work Guidance
Any change to validation rules requires a matching test and a doc update in the same
change. Keep messages actionable (say how to fix).

## Verification
From the repo root:
- `python -m unittest discover -s tests` → 46 tests, OK
- `python scripts/bob_validate.py examples/todo-api` → OK
- `python scripts/bob_runtime_check.py examples/todo-api` → OK
- `python scripts/bob_ready.py examples/todo-api` → READY 6/6
