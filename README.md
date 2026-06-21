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
├── .claude-plugin/         # plugin.json + marketplace.json (installable)
├── commands/bob.md         # /bob slash command
├── skills/bob/             # the skill + references (SDD, retrofit, PvA)
├── scripts/
│   ├── bob_validate.py     # dependency-free spec validator (CI-enforced)
│   └── bob_analyze.py      # retrofit scaffolder for existing projects
├── templates/              # constitution + spec templates (copy-paste)
├── examples/todo-api/      # complete, validating demo: specs + code + tests
├── tests/                  # validator unit tests (12)
├── docs/                   # SPEC-FORMAT, SUB-AGENTS, GOVERNANCE, TUTORIAL, etc.
├── .github/workflows/      # CI: spec validation + tests
└── AGENTS.md               # DOX context tree
```

## The spec layer is real (not just prose)

BOB ships the executable backbone the workflow promises:

- **Canonical spec format** — [`docs/SPEC-FORMAT.md`](docs/SPEC-FORMAT.md) + copy-paste
  [`templates/`](templates/). Markdown + YAML frontmatter; the *Contract* section embeds
  the formal artifact per type (JSON Schema, DDL, rules).
- **Validator** — `python scripts/bob_validate.py <project>` fails on missing
  constitution, bad spec type, empty approved sections, dangling `depends_on`, duplicate
  ids. Tested (12 cases).
- **CI** — [`.github/workflows/bob-validate.yml`](.github/workflows/bob-validate.yml)
  turns spec drift into a red build.
- **Worked demo** — [`examples/todo-api/`](examples/todo-api/): all six spec types,
  conforming code, 9 spec-traced tests, validates clean.
- **Retrofit tooling** — `python scripts/bob_analyze.py <project> --write` drafts a
  constitution + spec stubs from existing code.
- **Benchmark harness** — `python scripts/bob_benchmark.py` runs validator + tests +
  token-footprint and writes a report; exit 0 only if green. stdlib-only (exact tokens
  if `tiktoken` is installed). Doc + PvA: [`docs/BENCHMARK.md`](docs/BENCHMARK.md).
- **Honest trade-offs** — [`docs/PVA.md`](docs/PVA.md): every review criticism with the
  fix that shipped, and the one gap (with/without-BOB ROI) left open on purpose.

Quick verify:
```
python -m unittest tests.test_bob_validate -v        # validator: 12
python -m unittest tests.test_bob_benchmark -v       # benchmark: 7
python -m unittest discover -s examples/todo-api/tests -v   # demo: 9
python scripts/bob_validate.py examples/todo-api
python scripts/bob_benchmark.py --json
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

