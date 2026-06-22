# Spec governance — how specs evolve

Specs are permanent memory, not frozen stone. They change like code, through a defined
process, so they stay trustworthy.

## Change process
1. **Propose** — open a PR that edits the spec (specs are code; treat them as code).
2. **Review** — at least one senior engineer (or two reviewers) approves. The review
   checks: does Intent still hold? Are Business rules still true? Is Downstream impact
   listed and notified?
3. **Version** — bump per semver in the `version` field:
   - **major** — breaking contract change (renamed/removed field, changed semantics).
     Must update every `consumed_by` spec and note it.
   - **minor** — backward-compatible addition.
   - **patch** — clarification, typo, non-behavioral.
4. **Implement** — regenerate/adjust code to match. No code ahead of the approved spec.
5. **Validate** — CI runs `bob_validate.py`; green or it doesn't merge.

## Status lifecycle
`draft` → `approved` (gate before code) → `deprecated` (superseded; keep for history,
point to the replacement in Intent).

## Conflicts
On conflicting specs, the constitution wins; if the constitution is silent, the closer/
more specific spec wins and the conflict is resolved by amending one of them — never by
leaving both. Record the resolution in the amendment log / Intent.

## Fleet / multi-project governance
This file governs one project's specs. When BOB spans a **fleet** of projects sharing core
invariants, cross-project deviations need their own process so they don't become silent
drift — see `FLEET-GOVERNANCE.md` (deviation ratification, the core-owned `FLEET.md`
register, and the `bob_validate.py` "pending core ratification" gate).

## Tooling
- `python scripts/bob_validate.py .` — structural + reference integrity.
- `python scripts/bob_validate.py --strict .` — also fails on unratified fleet deviations.
- Spec diffs are plain `git diff` on Markdown — readable in any PR.
