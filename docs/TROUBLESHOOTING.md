# Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `constitution.md missing` | No supreme contract at the root you pointed at. | `cp templates/constitution.template.md <root>/constitution.md`. |
| `missing required key 'X'` | Frontmatter incomplete. | Add the key; see `docs/SPEC-FORMAT.md`. |
| `type 'X' is not a canonical BOB spec type` | Typo / wrong type. | Use one of: schema, transformation, validation, orchestration, semantic, ai-workflow. |
| `section '## X' is empty but status is 'approved'` | Approved spec with a hollow section. | Fill it, or drop status back to `draft` until it's real. |
| `depends_on 'Y' does not resolve` | Upstream spec id wrong/absent. | Fix the id or create the upstream spec. |
| `duplicate spec id` | Two files share an id. | Ids are unique; rename one. |
| Validator exits 1 on the plugin repo root | Expected — the plugin itself isn't a spec project. | Point the validator at a project that has `constitution.md` + `specs/`. |
| Mojibake (`�`) in validator output on Windows | Console code page, not a bug. | Cosmetic; CI (Linux/UTF-8) is clean. Use `chcp 65001` for a UTF-8 console. |
| Sub-agent produced failing/drifting code | Normal Phase-3 event. | Don't accept; loop back with the failure, or fix the spec first. See `docs/SUB-AGENTS.md`. |
| A companion skill (dox / context-memory-bank) isn't found | Not installed. | BOB degrades to inline; install companions for the full experience. |
