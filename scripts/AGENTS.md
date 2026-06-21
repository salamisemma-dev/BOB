# scripts — executable backbone

## Purpose
The two scripts that make BOB's specs "executable" instead of decorative.

## Ownership
Owns the validator and retrofit-scaffolder logic and their contracts. Test files live
in `../tests/` (validator) — keep them in sync. The spec *format* these enforce is
owned by `../docs/SPEC-FORMAT.md`.

## Local Contracts
- `bob_validate.py` — reads `*.md` only, never executes project code; exits 1 on any
  spec error, 0 otherwise; `--json` for machine output. Allowed spec types and required
  sections are constants at the top — change them here AND in `../docs/SPEC-FORMAT.md`
  AND add a test in `../tests/test_bob_validate.py`.
- `bob_analyze.py` — retrofit scaffolder; dry-run by default, `--write` to create draft
  files; never overwrites an existing `constitution.md`; only writes under
  `constitution.md` and `specs/_drafts/`.
- Both: Python 3.8+, standard library only. No third-party imports.

## Work Guidance
Any change to validation rules requires a matching test and a doc update in the same
change. Keep messages actionable (say how to fix).

## Verification
`python -m unittest tests.test_bob_validate -v` from the repo root (12 tests).
