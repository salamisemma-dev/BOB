# Retrofit track — reorganize an existing / drifted project

Use when code already exists but there's no durable memory: tangled structure,
no specs, inconsistent conventions, "vibe-coded" pipelines nobody dares touch. Goal:
extract a constitution + specs *from the current reality*, then migrate to a clean
structure **without breaking what works**. Specs come before re-structuring so you
capture intent before you move anything.

Run this track first, then rejoin the normal `project-build` phases for new work.

---

## Guardrails (read before touching anything)

- **Never reorganize on a dirty tree.** Commit or stash first; work on a branch.
- **Characterize before you change.** If behavior isn't covered by tests, add
  characterization tests that pin current behavior *before* moving code. You can't
  call a refactor safe if nothing proves behavior is unchanged.
- **Document-then-move.** Extract intent into specs first; restructure second. Moving
  code you don't understand just relocates the mystery.
- **Small reversible steps.** One coherent move per commit; checks green between each.

---

## Step 1 — Inventory & map (read-only)

Dispatch an `Explore` / `general-purpose` sub-agent (read-only) to map the repo:
entry points, modules, data flows, external deps, build/test/deploy scripts, dead
code, and the worst drift hotspots (duplicated logic, inconsistent naming, god files,
untested pipelines). Produce a one-page map. Don't edit yet.

## Step 2 — Extract the constitution (from what IS, then what SHOULD BE)

Read the actual conventions in use and write `constitution.md` capturing the *good*
existing patterns as standards, and explicitly naming the inconsistencies to converge
on (e.g. "two date formats exist; standard is UTC ISO-8601; migrate the rest"). Get
the user's sign-off — this is where impractical structure becomes a decision, not an
accident.

## Step 3 — Extract specs from current behavior

For each meaningful component, write the spec that describes what it *actually does*
plus the intent you can recover (`references/spec-driven.md` for types/templates).
Mark unknowns as open questions instead of inventing rationale. These specs become
the permanent memory the project never had. Approve, then commit.

## Step 4 — Target structure & migration plan

Design the clean layout that conforms to the constitution (the `specs/` tree +
sensible source layout). Write a migration plan as small steps, each:
- one move/rename/dedup,
- the characterization tests that must stay green,
- the spec it aligns to,
- rollback note.
Save to `.claude/plans/`. Sequence safest-first; isolate any genuinely risky moves.

## Step 5 — Execute migration behind gates

Per step: dispatch a cheap sub-agent to perform the move/refactor; keep the
characterization tests + lint + build green; review with the expensive model
(`superpowers:code-reviewer`); commit. Stop and report if a step reveals behavior the
specs didn't capture — update the spec first.

## Step 6 — Wire anti-drift so it can't rot again

- Add the CI spec-validation job (`references/spec-driven.md`) so future drift = red build.
- Install/refresh DOX (`AGENTS.md` tree) so local contracts are read before edits.
- `/remember` the migration decisions and the *why* behind the new structure.

---

## What this prevents

Drift, impractical structure, and unmaintainable workflow recur because intent lived
in prompts/heads, not the system. After retrofit: intent is in specs, structure is in
the constitution, local rules are in AGENTS.md, decisions are in memory, and CI
enforces all of it. New work re-enters the normal phases and stays clean by default.
