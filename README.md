# Bob — plugin

Bob is a senior-engineer build workflow packaged as a Claude Code / Cowork plugin, so
you can use it in any workspace, not just where it was created.

**What Bob does:** one disciplined loop for building or reorganizing software — recall
project memory, capture intent as executable versioned specs (Spec-Driven
Development), sharpen requirements, plan, execute test-first via cheap sub-agents
behind code-review gates, then persist decisions. Anti-vibe-coding, anti-drift, lower
token cost. Full details: [`skills/bob/SKILL.md`](skills/bob/SKILL.md) and
[`skills/bob/README.md`](skills/bob/README.md).

---

## What's inside

```
bob-plugin/
├── .claude-plugin/
│   ├── plugin.json         # plugin manifest
│   └── marketplace.json    # marketplace listing (so it's installable)
├── commands/
│   └── bob.md              # /bob slash command
└── skills/
    └── bob/                # the skill itself + references (SDD, retrofit, PvA)
```

## Install

### Option A — local folder (this machine, any workspace)

```
/plugin marketplace add C:/Users/Lenovo/Documents/claude/bob-plugin
/plugin install bob@bob-marketplace
```

Bob is now available globally in Claude Code — `/bob "..."` works in every project.

### Option B — share via GitHub (other machines / Cowork)

1. Push this `bob-plugin/` folder to a GitHub repo (it's the repo root — the
   `.claude-plugin/` folder must sit at the top level).
2. On any machine / in Cowork:
   ```
   /plugin marketplace add <your-username>/<your-repo>
   /plugin install bob@bob-marketplace
   ```

### Cowork notes

Cowork uses the same plugin format (`.claude-plugin/plugin.json` + `skills/`). Install
via the GitHub method above, or add the plugin through Cowork's plugin manager pointing
at the repo. Bob's sub-agents fall back to `general-purpose` and run phases inline if a
specialized agent or helper skill isn't present, so it works in a fresh Cowork
environment without extra setup.

## Use

```
/bob "add a rate limiter to the API"        # new build
/bob "reorganize this messy data pipeline"  # retrofit / fix structure
```

Or just say "I'm going to build X" / "ik ga een project bouwen" — the skill triggers
on any real build or reorganize task.

## Optional companions

Bob calls these if present, and degrades gracefully if not:
- `context-memory-bank` — persistent `/remember` + `/recall` project memory.
- `dox` — hierarchical `AGENTS.md` contracts.
- `superpowers` skills/agents — brainstorming, writing-plans, code-reviewer.

To get the full experience on another machine, install those alongside Bob.
