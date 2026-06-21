---
name: bob
description: >-
  Bob — the one workflow to run when building, extending, OR reorganizing a software
  project — start a feature, ship a module, add a subsystem, kick off a new app, or
  retrofit an existing messy codebase into a clean structure. Enforces senior-
  engineer discipline so work stays on track instead of drifting: recall prior
  context, capture intent as executable versioned specs (Spec-Driven Development),
  sharpen requirements, plan, execute test-first behind quality gates using cheaper
  sub-agents, then persist what was decided. Use this skill whenever the user types
  /bob, says "build me X", "let's add a feature", "start a new project",
  "implement <subsystem>", "reorganize/herorganiseer this project", "fix the
  structure", "ik ga een project bouwen", or any non-trivial coding task that
  deserves a real workflow rather than ad-hoc edits. It wires together project
  memory (context-memory-bank), local context contracts (dox / AGENTS.md),
  Spec-Driven Development (constitution + executable specs as permanent system
  memory), a two-tier plan-then-execute model strategy, and TDD with code review —
  all in one. Prefer this over jumping straight into code whenever the task is
  bigger than a one-line fix.
---

# bob — Senior-engineer build workflow, all in one

The failure mode this skill kills: starting to code before the goal is sharp,
drifting mid-task, re-deriving context the project already knew, burning expensive
tokens on work a cheaper model could do — and "vibe coding" where AI-generated code
works today but in six months nobody can explain *why* it works or *how* to maintain
it, because the prompts were temporary and the business context, architecture
choices, and logic scattered across chats instead of becoming part of the system.

You fix that by always running the same disciplined loop, by making intent
**executable and version-controlled** (specs, not prompts), and by leaning on
**sub-agents** and **persistent memory** to keep the main thread cheap, focused, and
informed.

Three ideas drive every phase:

- **Specs are the system's permanent memory.** Prompts evaporate. A constitution and
  versioned, executable specifications do not — they live in the repo, drive code
  generation/validation/tests/deploy, and answer "why" six months later. No code
  without an approved spec. Update the spec first, then generate code. (Full model:
  `references/spec-driven.md`.)
- **Memory before work, memory after work.** Recall what the project already decided
  (`context-memory-bank`) and read local contracts (`dox` / `AGENTS.md`) *before*
  touching code, so you never re-explain or re-discover. Persist new decisions
  *after*. Biggest lever on token cost — a 2-second recall beats re-reading the codebase.
- **Two-tier execution.** The expensive model (this session) thinks: specs,
  requirements, planning, review. Cheap sub-agents do the repetitive doing:
  scaffolding, tests, code from a precise spec+plan. Plan once at high quality,
  execute cheaply, review at high quality.

Run the phases in order. Track them with TodoWrite so drift is visible. Don't skip a
phase — if one genuinely doesn't apply, say why, don't silently drop it.

---

## Pick the mode first

- **New build** — greenfield project, new feature, or subsystem. → run Phases 0→5
  straight through. The constitution + specs are created in Phase 1.5.
- **Retrofit / reorganize** — an existing project that drifted: tangled structure,
  no specs, inconsistent conventions, unmaintainable "vibe-coded" pipelines. → run
  the **Retrofit track** in `references/retrofit-existing.md` first (it produces the
  constitution + specs *from the current code* and a safe migration plan), then
  rejoin the normal phases for any new work. Use this whenever the user says
  "reorganize", "herorganiseer", "fix the structure", or the codebase clearly has no
  durable memory.

When unsure which mode: if a coherent constitution/spec layer already exists →
new-build phases; if not and code already exists → retrofit.

---

## Phase 0 — Recall context (cheap, do it first)

1. **Recall project memory.** Invoke `context-memory-bank` with the task as query.
   Surface the 2–3 most relevant prior decisions/bugs/constraints and how they bear
   on this task. Empty bank → stay silent, continue.
2. **Read local contracts + specs.** Invoke `dox`; walk the `AGENTS.md` tree
   root→target for paths you'll touch. Read any existing `constitution.md` and
   relevant files under `specs/`. No tree on a real project → offer to install DOX.
3. Report a one-paragraph "what we already know" so the user sees the starting state.

---

## Phase 1 — Sharpen requirements (expensive model, no code yet)

1. **Grill the request** like a senior engineer reviewing a ticket: scope in/out,
   inputs, outputs, error cases, constraints, acceptance criterion. Ask the questions
   whose answers change the design. (Use `superpowers:brainstorming` if open-ended.)
2. Flag technical debt this work will touch — note it, don't route around it.

Output: a short, testable definition of done.

---

## Phase 1.5 — Spec layer (Spec-Driven Development)

This is where intent becomes permanent system memory. The canonical, machine-checkable
format is `docs/SPEC-FORMAT.md` (copy-paste templates in `templates/`); the conceptual
model is `references/spec-driven.md`; a complete worked example is `examples/todo-api/`.
In short:

1. **Constitution.** If `constitution.md` doesn't exist at the project root, create it:
   technology standards, naming conventions, architecture rules, governance policy,
   and the cross-platform invariants that must stay consistent. This is the supreme
   contract; everything else conforms to it.
2. **Write/refresh the specs** the task needs, as versioned files under `specs/`:
   schema, transformation, validation, orchestration, semantic, and AI-workflow specs
   (only the ones this task touches). Each spec is **executable** — it drives codegen,
   validation, tests, and deploy — and records the **why**: business rules,
   assumptions, constraints, downstream dependencies, and intent behind choices.
3. **Approval gate.** Get the user's OK on the spec before any code. No code without
   an approved spec; when something must change, change the spec first, then regenerate.
4. **Validate.** Run `python scripts/bob_validate.py <project-root>` — it must pass
   before code. This is the executable check (also runs in CI), not a formality.
5. Commit the constitution + specs so they're version-controlled from the start.

---

## Phase 2 — Plan (expensive model writes it, once)

Derive the plan *from the approved specs*. Include:
- **Diagnosis** — current state of relevant code.
- **Tasks** — small units (~≤100 lines each), independently testable, with explicit
  file paths and the spec each task implements.
- **Test strategy** — TDD: the failing test (derived from the validation spec) first.
- **Sequencing** — dependency order; mark which tasks can run in parallel.

Save to `.claude/plans/plan_<YYYYMMDD-HHMMSS>.md`. Use `superpowers:writing-plans` if
present. A task a sub-agent can't execute from spec+plan alone is under-specified —
fix the spec/plan, don't paper over it.

---

## Phase 3 — Execute test-first behind quality gates (cheap sub-agents do the work)

For each task (respect sequencing; parallelize independent tasks):

1. **Dispatch a sub-agent** via the `Agent` tool (`coder`, `general-purpose`, or a
   `tester`-style role) with the exact task slice + the spec it implements. Instruct:
   red → green → refactor. Independent tasks → spawn in parallel in one message.
   Pass `model: "haiku"` (or `sonnet`) for routine implementation — the two-tier cost
   saving. Keep the expensive model for thinking and review.
2. **Quality gate after each task.** Review with the **expensive** model via the
   `superpowers:code-reviewer` agent or `reviewer`. Verify the code conforms to its
   spec and the constitution. Block on real findings; loop back to fix.
3. **Run the project's checks** (tests, lint, build, and spec validation). Don't
   declare a task done on unverified code — if checks fail, say so and fix.

### Sub-agent roles
`coder` / `general-purpose` — implement a spec'd task TDD. `tester` — coverage gaps.
`superpowers:code-reviewer` / `reviewer` — the quality gate. `Plan` — re-plan a slice
that grew. (Some swarm agents may be unavailable in a given session — fall back to
`general-purpose` or run inline.)

---

## Phase 4 — Persist decisions & update contracts (memory after work)

1. **Update specs first** if anything changed — specs lead code, always.
2. **Remember.** `context-memory-bank` (`/remember`): durable non-obvious facts —
   decisions + *why*, bugs + root cause, edge cases, dependency choices. One atomic
   note per fact. Skip what's in code/git.
3. **Update DOX.** `dox` maintenance: owning `AGENTS.md` + affected indexes for
   anything that changed scope/contracts/workflow/structure. Remove stale text.
4. **Commit** specs + code together (if a git repo / the user wants a commit), clear
   message describing the why.

---

## Phase 5 — Close out

1. Summarize: tasks done, real test/build/spec-validation results (not "should
   pass"), files touched, spec + memory + contract updates.
2. Surface remaining tech debt / follow-ups. Name any architecture concern; offer to
   address now rather than deferring vaguely.

---

## CI/CD integration

Specs are meant to be enforced automatically, not by goodwill. When the project has
(or wants) CI: wire a job that validates every spec and fails the build on drift
between spec and code — schema mismatch, missing validation rule, constitution
violation. Generate as much implementation as possible from the specs. Ship
`scripts/bob_validate.py` + `templates/github-actions/bob-validate.yml` into the
project; details in `docs/SPEC-FORMAT.md` and `references/spec-driven.md`.

---

## Anti-drift / anti-excuse table

| Excuse | Reality |
|--------|---------|
| "Task's too small for the full workflow." | Run it *light* — recall + a tiny spec + a 3-line plan + review. Strategy is cheap; drift is not. |
| "I don't need context, it's obvious." | You forget across sessions; the project knows things you don't. `/recall` + the AGENTS.md/spec chain costs seconds and prevents blind edits. |
| "I'll skip the spec and just code." | Then in 6 months nobody knows why it works. The spec IS the memory. Spec first, always. |
| "I'll skip the plan and just code." | No plan = no contract for sub-agents = expensive model does cheap work and drifts. Plan once, execute cheap. |
| "I'll skip review to go faster." | Unreviewed code is slower once it breaks. Run the reviewer gate after each task. |
| "I'll use the big model for everything." | Routine implementation on the expensive model is wasted money. Cheap sub-agents do the doing. |
| "We'll document/remember it later." | Later never comes; context evaporates at session end. `/remember` + DOX + spec update happen in Phase 4, every time. |
| "This existing project is too messy to spec." | That's exactly when you retrofit — `references/retrofit-existing.md`. Specs extracted from messy code are how you stop the mess growing. |

---

## Why this saves tokens & survives 6 months

- Recall (Phase 0) replaces re-reading/re-explaining the project every session.
- Specs (Phase 1.5) make intent permanent and machine-checkable — humans *and* future
  AI agents read the spec instead of reverse-engineering code.
- Two-tier execution (Phase 3) moves bulk token volume to cheap sub-agents.
- Persisted memory + specs (Phase 4) compound: every session starts from accumulated
  context, not cold.

## Reference files
- `references/spec-driven.md` — SDD model, constitution, 6 spec types + templates, CI/CD.
- `references/retrofit-existing.md` — reorganize an existing/drifted project safely.
- `references/sdd-pva.md` — plan van aanpak: pros, cons, and a fix for each con.

## Tooling (in the plugin repo)
- `scripts/bob_validate.py` — dependency-free spec validator; run it in Phase 1.5 and CI.
- `scripts/bob_analyze.py` — retrofit scaffolder: drafts constitution + spec stubs from code.
- `templates/` — constitution + spec templates. `docs/SPEC-FORMAT.md` — the format spec.
- `examples/todo-api/` — a complete, validating reference project.

## Dependencies
Calls (via `Skill`): `context-memory-bank`, `dox`, optionally
`superpowers:brainstorming`, `superpowers:writing-plans`. Dispatches sub-agents (via
`Agent`): `coder`, `general-purpose`, `tester`, `superpowers:code-reviewer`,
`reviewer`, `Plan`. All degrade gracefully — if one isn't present, do that phase
inline and continue.

