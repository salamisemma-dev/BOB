# DOX framework

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

- Output language to the user: Dutch (the maintainer works in Dutch).
- Keep scripts dependency-free (stdlib only) — portability is a hard requirement.
- No code/spec change merges without passing `scripts/bob_validate.py` and the test suites.

## Project Overview

BOB is a Claude Code / Cowork plugin: a senior-engineer build workflow built on
Spec-Driven Development. The repo root doubles as the plugin root (`.claude-plugin/`
at top level) so it installs directly. The repo is NOT itself a BOB spec project, so
`bob_validate.py .` failing at the root is expected — the validator targets downstream
projects and the `examples/` demo.

## Verification

- `python -m unittest tests.test_bob_validate -v` (validator: 12 tests)
- `python -m unittest discover -s examples/todo-api/tests -v` (demo: 9 tests)
- `python scripts/bob_validate.py examples/todo-api` → must print OK

## Child DOX Index

- [scripts/AGENTS.md](scripts/AGENTS.md) — the executable backbone: spec validator + retrofit scaffolder. Dependency-free, tested.
- [examples/todo-api/AGENTS.md](examples/todo-api/AGENTS.md) — the worked demo: a complete, validating spec layer + conforming code + spec-traced tests.
- Other top-level paths (no child doc needed yet):
  - `.claude-plugin/` — plugin + marketplace manifests (JSON; keep valid).
  - `skills/bob/` — the skill itself; SKILL.md is the workflow contract, `references/` the deep docs.
  - `templates/` — copy-paste spec + constitution templates.
  - `docs/` — SPEC-FORMAT, SUB-AGENTS, GOVERNANCE, TUTORIAL, TROUBLESHOOTING, PVA.
  - `.github/workflows/` — CI that runs the verification above.
  - `commands/` — the `/bob` slash command.
