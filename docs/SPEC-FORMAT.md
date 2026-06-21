# BOB canonical spec format

This is the concrete, enforced format the critique demanded. It's deliberately
**Markdown + a tiny YAML frontmatter subset** — readable by humans, diffable in PRs,
and machine-checkable by `scripts/bob_validate.py` with zero third-party deps. The
*Contract* section embeds the right formal artifact per type (JSON Schema, DDL,
Gherkin-style rules, etc.), so you get portability without inventing a new DSL.

## Files & layout
```
<project-root>/
├── constitution.md          # required — supreme contract
└── specs/
    ├── schema/        <id>.md
    ├── transformation/<id>.md
    ├── validation/    <id>.md
    ├── orchestration/ <id>.md
    ├── semantic/      <id>.md
    └── ai-workflow/   <id>.md
```
Folder names are convention; the validator keys off the `type` field, not the path.

## Frontmatter (required keys)
```yaml
---
id: <type>-<slug>      # unique across the repo; stable handle others reference
type: schema | transformation | validation | orchestration | semantic | ai-workflow
version: <semver>      # major = breaking contract change
status: draft | approved | deprecated
owner: <name>
depends_on: [<spec-ids>]   # upstream; validator fails on dangling ids
consumed_by: [<spec-ids or components>]  # downstream impact surface
---
```

## Required body sections (all six spec types)
`## Intent` · `## Contract` · `## Business rules` · `## Downstream impact` ·
`## Verification`. For `status: approved`, every section must be non-empty — the
**Intent** and **Business rules** are the permanent memory.

## What the validator enforces
- constitution.md present at root.
- frontmatter present with all required keys; `type` and `status` from the allowed sets.
- all required sections present; non-empty when approved.
- unique ids; `depends_on` ids resolve (hard error); spec-shaped `consumed_by` ids
  resolve (warning).

Run it: `python scripts/bob_validate.py <project-root>` (exit 1 on any error).
JSON report: add `--json`.

## The rule
No code without an approved spec. Change the spec first, then regenerate code. CI
(`.github/workflows/bob-validate.yml`) makes drift a red build. Worked example that
passes: [`../examples/todo-api/`](../examples/todo-api/).
