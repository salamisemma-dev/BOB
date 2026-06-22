# <FLEET NAME> Fleet — BOB-proof register

The core's authoritative view of every project's anti-vibe status and any approved
deviations from the shared invariants (constitution §5). A deviation is **drift** until it
appears here as **ratified**. Update whenever a project is retrofitted or a deviation is
raised/ratified. See `docs/FLEET-GOVERNANCE.md`.

Last reviewed: <DATE> · Owner: <WHO>

## Status

| Project | Repo / path | Constitution | Specs | Validator | Tests | CI | Verdict |
|---------|-------------|--------------|-------|-----------|-------|----|---------|
| <core>  | <repo>      | ✅ v1.0      | 0     | ✅        | 0     | ✅ | BOB-proof |
| <proj>  | <repo>      | ✅           | 0     | ✅        | 0     | ✅ | BOB-proof |

## Ratified deviations from core invariants

| Invariant | Project(s) | Deviation | Condition | Status |
|-----------|-----------|-----------|-----------|--------|
| <§x.y>    | <proj>    | <what>    | <mandatory mitigation / bound> | **Ratified** (constitution v<x>, <date>) |

## Open / unratified

| Invariant | Project | Issue | Action |
|-----------|---------|-------|--------|
| <§x.y>    | <proj>  | <what's vague or unverified> | <pin a value / ratify / conform> |

## Governance rule (how a deviation gets here)

1. Project documents the deviation in its own constitution + marks "pending core ratification".
2. Deviation raised against the core constitution.
3. Core ratifies (amend core constitution + add a row above) or rejects (project conforms).
4. Until then, the project's validator WARNs (ERROR under `--strict`).
