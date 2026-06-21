# BOB benchmark harness

`scripts/bob_benchmark.py` is a repeatable quality + footprint baseline for a
spec-driven project. It runs the validator, runs the test suite, counts the
spec+code token footprint, and writes a Markdown report.

```
python scripts/bob_benchmark.py [--demo <project>] [--output report.md] [--json]
```
Exit code 0 only if validator AND tests pass — so it doubles as a gate.

## What it measures (and what it doesn't)

Measures: validator pass/fail + time, tests pass/fail/count + time, spec+code token
footprint (proxy for maintenance load).

Does **not** measure with-vs-without-BOB ROI (tokens/time saved versus ad-hoc "vibe
coding"). That needs a controlled comparison running the same task both ways and
logging the API traffic — a separate harness. This is the foundation it builds on:
once footprint and quality are tracked per commit, drift and bloat become visible.

## Token counting

Default is a **stdlib heuristic** (~chars/4) so the harness runs with zero
third-party deps (a repo invariant). If `pip install tiktoken` is present, exact
`cl100k_base` counts are used and the report labels the method. The heuristic is a
trend indicator, not an exact billing figure — fine for "is our footprint growing?".

---

## PvA — benchmark harness: pros, cons, fix per con

### Pros
| # | Pro |
|---|-----|
| V1 | Repeatable quality gate (validator + tests) in one command. |
| V2 | Footprint trend — catch spec/code bloat per commit. |
| V3 | Zero-dependency by default; exact mode when tiktoken is available. |
| V4 | Machine-readable (`--json`) for CI dashboards. |
| V5 | Honest scoping — clearly states it's a baseline, not ROI proof. |

### Cons + fix (each fix is shipped)
| # | Con | Fix | Where |
|---|-----|-----|-------|
| N1 | Original draft parsed `out.count("OK")` — unittest writes to **stderr**; counts were wrong. | Parse the `Ran N` / `FAILED (failures=,errors=)` summary from combined stdout+stderr. | `parse_unittest`, tested 3 ways |
| N2 | Spec token count used default `*.py` glob → specs are `.md` → always 0. | Specs counted with `*.md` (+constitution), code with `*.py`. | `measure_footprint` |
| N3 | `Path \| None` type hint requires Python 3.10+, repo invariant is 3.8+. | `Optional[Path]` + `from __future__ import annotations`. | top of file |
| N4 | Relative `scripts/bob_validate.py` broke unless run from repo root. | Resolve `REPO_ROOT`/`VALIDATOR` from `__file__`; absolute paths. | module constants |
| N5 | tiktoken-only → no number without a third-party dep (breaks stdlib-only rule). | stdlib heuristic fallback always returns a count; tiktoken optional + labeled. | `count_tokens` |
| N6 | Token count is not exact billing. | Documented as a proxy; exact mode via tiktoken; report states the method. | this doc + report |
| N7 | Report file could be committed by accident. | `benchmark-report.md` in `.gitignore`. | `.gitignore` |
| N8 | Real ROI (with/without BOB) still unmeasured. | Explicitly scoped as the next harness; this is the baseline. Open on the roadmap. | this doc, `docs/PVA.md` |

### Open (roadmap)
- N8 comparison harness: run a fixed task with and without the BOB workflow via the
  Claude API, log tokens/time/iterations, publish a case study. Requires consent +
  prompt anonymization (see SECURITY.md).

## Verification
`python -m unittest tests.test_bob_benchmark -v` (7 tests) — parsing, token heuristic,
end-to-end green on the demo, missing-demo handling.
