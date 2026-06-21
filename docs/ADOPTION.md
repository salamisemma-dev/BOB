# Adoption gate & fail-fast anti-vibe mode

BOB only prevents vibe-coding if it *blocks* work on an undisciplined project instead
of politely suggesting specs. This is the enforceable gate.

## When is a project BOB-ready?

A project is BOB-ready when all seven hold (checked by `scripts/bob_ready.py`):

1. `constitution.md` present — the supreme contract.
2. At least one **approved** spec.
3. Strict validator passes — structure, spec-to-test traceability, and assertion evidence.
4. Runtime/golden checks pass — schema specs verified against sample data.
5. A test suite is present: `tests/`, `src/__tests__/`, or common `*.test` / `*.spec` files.
6. The test command passes. `bob_ready.py` runs tests by default.
7. `AGENTS.md` present — DOX context.

```bash
python scripts/bob_validate.py --strict <project>
python scripts/bob_runtime_check.py <project>
python scripts/bob_ready.py <project>     # strict + tests by default
python scripts/bob_ready.py <project> --json
```

`--no-run-tests` on `bob_ready.py` is diagnostic only. Do not use it in CI.
`--no-traceability` on `bob_validate.py` is forbidden with `--strict`.

## Branch protection

CI is not enforcement until branch protection requires the green check. For GitHub:

```bash
bash templates/enable-branch-protection.sh owner/repo main bob-validate
```

This requires GitHub CLI auth (`gh auth login`) or an equivalent authenticated REST call.
Without branch protection, a red BOB workflow is only advice.

## Fail-fast anti-vibe rule

When someone says "build X" / "add feature Y" on a project, BOB must refuse to generate
code until the chain exists for that work:

- **No spec** for the thing being built → stop, write the spec (Phase 1.5).
- **Spec not approved** → stop, get approval.
- **Strict validator/traceability failing** → stop, fix the spec layer.
- **No test plan** (the spec's Verification names no test) → stop, define it.
- **Test command fails** → stop, fix the implementation or the test contract.

This is not bureaucracy for a one-line fix — run it *light* for tiny tasks (a mini-spec
+ one test reference). But the gate is never skipped: a spec that isn't tied to a test
is exactly how "looks valid, behaves wrong" sneaks in.

## Sub-agent rule (anti-drift)

A sub-agent may only work from a **spec id + explicit acceptance criteria** (the spec's
Contract + Verification). No "go build the whole feature" prompts — that's where drift
starts. One spec slice per agent.

## Memory/DOX policy (anti-noise)

Persist only: decisions + rationale, risks, spec paths, and verification results. Not
transient chatter. Keeps the memory bank and AGENTS.md signal-dense.

## Pilot (the real test)

The demo proves the happy path. The honest next step is a **pilot on one real,
messy repo**: run `bob_analyze.py` to draft specs, fill + approve them, wire the
validator + runtime checks into CI, get `bob_ready.py` to green, and record before/after
structure + open risks. Point BOB at such a repo to do this — it can't be faked on a
clean demo.
