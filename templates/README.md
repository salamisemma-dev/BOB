# BOB spec templates

Copy-paste starting points for the BOB spec layer. Canonical format and rules:
[`../docs/SPEC-FORMAT.md`](../docs/SPEC-FORMAT.md). Validate with
`python ../scripts/bob_validate.py <project-root>`.

- `constitution.template.md` → copy to `<project-root>/constitution.md`.
- `spec.template.md` → copy to `specs/<type>/<id>.md`, set `type` to one of the six
  canonical types: schema, transformation, validation, orchestration, semantic,
  ai-workflow.

A worked, passing example lives in [`../examples/todo-api/`](../examples/todo-api/).
