---
description: Run the Bob senior-engineer build workflow (SDD + memory + sub-agents + TDD/review) on a task or project.
argument-hint: "<task description>"   e.g. "add a rate limiter to the API" or "reorganize this pipeline"
---

Invoke the `bob` skill and run its full workflow for the following task.

Task: $ARGUMENTS

Follow the bob SKILL.md exactly: pick the mode (new build vs retrofit), then run the
phases in order (Phase 0 recall → 1 sharpen → 1.5 spec layer → 2 plan → 3 execute via
sub-agents behind review gates → 4 persist specs/memory/DOX → 5 close out). Do not skip
phases; if one doesn't apply, say why.
