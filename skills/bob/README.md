# bob

Bob — one skill that runs your whole build like a senior engineer — no drift, no
re-explaining, lower token cost.

## What it does

When you start any non-trivial coding work, `bob` runs a fixed loop:

| Phase | What | Model | Why |
|------|------|-------|-----|
| 0 | Recall project memory + read AGENTS.md/specs | cheap | don't rebuild what the project already knows |
| 1 | Sharpen requirements (grill the task) | expensive | a sharp goal = no drift |
| 1.5 | **Spec layer (SDD)** — constitution + executable specs | expensive | intent becomes permanent system memory |
| 2 | Write the plan from the specs (small testable tasks) | expensive | one contract for executors |
| 3 | Execute TDD via sub-agents + review gate | cheap exec / expensive review | bulk work goes to cheap models |
| 4 | Update specs + remember decisions + DOX | cheap | next session starts informed |
| 5 | Close out: summary, test/spec-validation results | — | honest reporting |

## Two modes

- **New build** — greenfield/feature/subsystem → run all phases.
- **Retrofit / reorganize** — existing drifted project → runs `references/retrofit-existing.md`
  first: extracts a constitution + specs *from the current code*, then migrates to a
  clean structure behind characterization tests, then rejoins the normal phases.
  Triggers on "reorganize", "herorganiseer", "fix the structure".

## Spec-Driven Development (the anti-vibe-coding core)

Prompts are temporary; specs are permanent. The skill captures intent —
business rules, architecture choices, validation logic — as **executable,
version-controlled specifications** (constitution + schema/transformation/validation/
orchestration/semantic/AI-workflow specs). No code without an approved spec; change
the spec first, then regenerate. CI validates spec-vs-code and fails the build on
drift. Result: in 6 months a human *or* an AI agent reads the spec instead of
reverse-engineering the code. Full model in `references/spec-driven.md`; trade-offs
(pros/cons + a fix for every con) in `references/sdd-pva.md`.

## How to use

```
/bob "add a rate limiter to the API"
```

or just say "I'm going to build X" / "ik ga een project bouwen" — it triggers on
any real build task.

## How it cuts token cost

- **Recall before work** — a 2-second memory lookup replaces re-reading the codebase.
- **Two-tier** — cheap sub-agents (Haiku/Sonnet) do scaffolding/coding; the expensive
  model only plans and reviews.
- **Persistent memory** — context compounds across sessions instead of starting cold.

## Wires together

- `context-memory-bank` — persistent `/remember` + `/recall` project brain.
- `dox` — hierarchical `AGENTS.md` contracts read before editing, updated after.
- Sub-agents — `sparc-coder`, `coder`, `tdd-london-swarm`, `tester`, `code-reviewer`.
- Two-tier plan→execute strategy (shadcn/improve pattern), built into Phases 2–3.

All dependencies degrade gracefully: if a skill or agent isn't installed, that phase
runs inline.

## The anti-drift rule

The skill carries an anti-excuse table. The short version: never skip recall, never
skip the plan, never skip review, never use the big model for routine doing, always
persist what you decided. Small task? Run it light — but run all phases.
