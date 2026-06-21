# Security

## Threat model
BOB is Markdown instructions + two small, dependency-free Python scripts
(`bob_validate.py`, `bob_analyze.py`). Neither executes project code, makes network
calls, or writes outside the target tree:
- `bob_validate.py` only **reads** `*.md` files and prints a report.
- `bob_analyze.py` only reads source paths and, with `--write`, creates draft Markdown
  under `constitution.md` / `specs/_drafts/`. Dry-run by default.

The execution risk in the BOB *workflow* is the sub-agents (Phase 3), which generate
and run code in your environment — the same trust boundary as any AI coding session.

## Practices
- **Secrets**: never put credentials in specs or the constitution; they're committed.
  Specs describe contracts, not values. Keep secrets in a vault / env, referenced by name.
- **Review gate**: Phase 3's code-review gate is also a security gate — review generated
  code before it runs against real data or credentials.
- **Sub-agent scope**: dispatch sub-agents with least context needed; don't hand them
  secrets to "make it work".
- **Supply chain**: the scripts have no third-party deps, so no transitive risk from
  BOB itself. Audit any deps your generated code introduces.
- **CI**: `bob_validate.py` runs untrusted repo Markdown but only parses it as text —
  no eval, no import of repo code.

## Reporting
Open an issue (omit sensitive detail) or contact the maintainer privately for anything
exploitable.
