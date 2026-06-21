# BOB in 30 minutes

A zero-to-working-spec-layer walkthrough.

## 0. Install (2 min)
```
/plugin marketplace add salamisemma-dev/BOB
/plugin install bob@bob-marketplace
```

## 1. See it work — run the demo (5 min)
```
cd examples/todo-api
python -m unittest discover -s tests        # 9 tests pass
python ../../scripts/bob_validate.py .       # OK: spec layer valid
```
Read `specs/schema/schema-todo-item.md` then `src/todo.py` — the code traces to the
spec; the spec explains *why*.

## 2. Start your own (10 min)
```
cp templates/constitution.template.md  <your-project>/constitution.md
# fill sections 1–5
mkdir -p <your-project>/specs/schema
cp templates/spec.template.md <your-project>/specs/schema/schema-myentity.md
# set id/type/status, fill Intent + Contract + the other sections
python scripts/bob_validate.py <your-project>
```
Set `status: approved` only when a section is real. Validator stays red until the
required sections are filled — that's the point.

## 3. Wire CI (3 min)
Copy `.github/workflows/bob-validate-template.yml` into your repo, vendor
`scripts/bob_validate.py`. Now spec drift fails the build.

## 4. Use the full workflow (10 min)
```
/bob "add a priority field to todos"
```
BOB recalls context → grills the requirement → updates the schema/validation specs
(approval gate) → plans → dispatches a cheap sub-agent TDD → reviews → persists. You
never get code ahead of an approved spec.

## Retrofit an existing project
```
python scripts/bob_analyze.py <project> --write   # draft constitution + spec stubs
```
Then fill the TODOs, add characterization tests, approve specs. Full track:
[`../skills/bob/references/retrofit-existing.md`](../skills/bob/references/retrofit-existing.md).
