# Adoption gate & fail-fast anti-vibe mode

BOB only prevents vibe-coding if it *blocks* work on an un-disciplined project instead
of politely suggesting specs. This is the enforceable gate.

## When is a project BOB-ready?

A project is BOB-ready when all six hold (checked by `scripts/bob_ready.py`):

1. `constitution.md` present — the supreme contract.
2. At least one **approved** spec.
3. Validator passes — structure **and** spec-to-test traceability.
4. Runtime/golden checks pass — schema specs verified against sample data.
5. `tests/` directory present.
6. `AGENTS.md` present — DOX context.

```
python scripts/bob_ready.py <project>     # exit 0 only if all six pass
python scripts/bob_ready.py <project> --json
```

## Fail-fast anti-vibe rule

When someone says "build X" / "add feature Y" on a project, BOB must refuse to generate
code until the chain exists for that work:

- **No spec** for the thing being built → stop, write the spec (Phase 1.5).
- **Spec not approved** → stop, get approval.
- **Validator/traceability failing** → stop, fix the spec layer.
- **No test plan** (the spec's Verification names no test) → stop, define it.

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
