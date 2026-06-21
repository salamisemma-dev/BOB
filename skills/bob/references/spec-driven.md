# Spec-Driven Development (SDD) — the spec layer

The point: turn temporary prompts, business rules, and validation logic into
**executable, version-controlled specifications** that act as the system's permanent
memory. Six months from now a human or an AI agent reads the spec to understand
*why* the system works and *how* to change it safely — instead of reverse-engineering
generated code or hunting through old chat logs.

Golden rule: **no code without an approved spec; change the spec before the code.**

---

## Where it lives

```
<project-root>/
├── constitution.md              # supreme contract — standards, conventions, governance
├── specs/
│   ├── schema/                  # structural compatibility
│   ├── transformation/          # business logic
│   ├── validation/              # quality / data-quality rules
│   ├── orchestration/           # execution behavior (scheduling, retries, DAG)
│   ├── semantic/                # shared business definitions / glossary
│   └── ai-workflow/             # reusable implementation instructions for AI agents
└── .claude/                     # plans, context_memory (handled by other phases)
```

Everything under `specs/` is version-controlled and reviewed like code. The
constitution and specs are committed *before or with* the code they govern.

---

## The constitution

`constitution.md` is the project's supreme, slow-changing contract. Everything else
conforms to it. It defines:

- **Technology standards** — languages, runtimes, frameworks, allowed/forbidden deps.
- **Naming conventions** — files, modules, tables, columns, jobs, env vars.
- **Architecture rules** — layering, boundaries, allowed dependency directions,
  data-flow rules, what may talk to what.
- **Governance policy** — who/what approves specs, how breaking changes are handled,
  versioning scheme, deprecation policy.
- **Cross-platform invariants** — the few rules that must stay consistent everywhere
  (e.g. "all timestamps UTC ISO-8601", "every table has a surrogate key", "no PII in
  logs").

Keep it short and durable. If it changes weekly it's not a constitution — push that
detail down into a spec.

### Constitution skeleton
```markdown
# Project Constitution — <name>
Version: <x.y> · Last updated: <date> · Owner: <who>

## 1. Technology standards
## 2. Naming conventions
## 3. Architecture rules & boundaries
## 4. Governance (spec approval, versioning, breaking-change policy)
## 5. Invariants (must hold platform-wide)
## 6. Amendment log   # every change: date, what, why
```

---

## The six spec types

Each spec is **executable** (drives codegen / validation / tests / deploy) and
records the **why** (business rules, assumptions, constraints, downstream impact).

| Spec type | Answers | Drives |
|-----------|---------|--------|
| **Schema** | What's the shape of the data/interface? | structural validation, type/contract generation, compatibility checks |
| **Transformation** | What business logic maps input→output? | transform code generation, unit tests |
| **Validation** | What makes data/output correct? | quality gates, test assertions, runtime checks |
| **Orchestration** | When/how does it run? | scheduler config, DAG, retry/backoff, dependencies |
| **Semantic** | What do the business terms mean? | shared glossary, metric definitions, consistency across components |
| **AI-workflow** | How should an AI agent implement this kind of thing? | reusable, parameterized build instructions for sub-agents |

### Common spec frontmatter (every spec file)
```yaml
---
id: <stable-unique-id>
type: schema | transformation | validation | orchestration | semantic | ai-workflow
version: <x.y>            # bump on every change
status: draft | approved | deprecated
owner: <who>
depends_on: [<spec-ids>]  # upstream specs
consumed_by: [<spec-ids or components>]  # downstream — impact surface
---
```

### Spec body — required sections
```markdown
## Intent          # WHY this exists, the decision and its rationale
## Contract        # the executable part: schema/rules/logic, precise & checkable
## Business rules  # assumptions, constraints, edge cases, the "context that used to live in prompts"
## Downstream impact  # what breaks if this changes; who must be notified
## Verification    # how CI proves code conforms to this spec
```

The **Intent** + **Business rules** sections are the permanent memory — the part
that's expensive to rediscover. Never let them live only in a prompt.

---

## Executable, not decorative

A spec is executable when something automated reads it and acts:

- **Schema spec** → generate types/DDL/validators; CI fails on structural drift.
- **Validation spec** → generated test assertions + runtime data-quality checks.
- **Transformation spec** → scaffold the transform + its unit tests.
- **Orchestration spec** → generate/validate scheduler/DAG config.
- **Semantic spec** → single source for metric/term definitions; lint references.
- **AI-workflow spec** → the exact instruction block handed to a sub-agent in Phase 3.

If a spec can't drive *any* automation, tighten it until it can, or it's just a doc
that will rot.

---

## Iterative workflow

1. Write/refresh the spec. 2. Get approval (the gate). 3. Generate code/tests from
the spec (cheap sub-agents). 4. CI validates code-vs-spec. 5. Change needed? Back to
step 1 — spec first, never patch code around an unchanged spec.

---

## CI/CD integration

Specs are enforced by the pipeline, not by goodwill. Minimum viable wiring:

```
on: [pull_request]
jobs:
  spec-validate:
    - check every specs/**/* has valid frontmatter, status, version
    - validate code against schema specs (structural drift = fail)
    - run generated validation-spec assertions
    - check constitution invariants (naming, boundaries, forbidden deps)
    - fail the build on any spec/code drift
  generate:
    - regenerate artifacts that are derived from specs; fail if working tree differs
```

Goal: drift between intent and implementation becomes a red build, caught in minutes,
not a six-month mystery.
