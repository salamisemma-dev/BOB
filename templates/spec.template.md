---
id: <type>-<stable-unique-slug>
type: schema   # one of: schema | transformation | validation | orchestration | semantic | ai-workflow
version: 0.1
status: draft  # draft | approved | deprecated
owner: <name>
depends_on: []         # upstream spec ids this relies on
consumed_by: []        # downstream spec ids / components affected by changes here
---

## Intent
WHY this exists. The decision and its rationale — the part that is expensive to
rediscover six months from now. This is permanent memory; never let it live only in
a prompt.

## Contract
The executable part: the precise, checkable definition. Depending on type:
- schema → field names, types, nullability, keys (e.g. a JSON Schema or a table DDL).
- transformation → the input→output mapping / business logic.
- validation → the quality rules / assertions that make output correct.
- orchestration → when/how it runs: schedule, DAG, retries, backoff, dependencies.
- semantic → the canonical definition of a business term or metric.
- ai-workflow → the reusable, parameterized instruction block handed to a sub-agent.

## Business rules
Assumptions, constraints, edge cases — the context that used to live in prompts.

## Downstream impact
What breaks if this changes; who/what must be notified. List consumed_by here in prose.

## Verification
How CI / a test proves code conforms to this spec. Be concrete: name the test, the
schema check, or the assertion.
