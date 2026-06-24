# Minimal by default — the laziness ladder inside BOB

BOB makes you build the *right* thing (spec + tests + gate). This file makes you build
the *least* of it. Spec rigor can quietly license over-engineering — a big spec feels
like it deserves a big implementation. It doesn't. The spec defines what must be true;
the code should be the smallest thing that makes the spec's tests pass.

Adapted from [ponytail](https://github.com/DietrichGebert/ponytail) (MIT) — "the best
code is the code never written" — kept compatible with BOB: minimality shortens the
*solution*, never the *guarantees*.

## The ladder (stop at the first rung that holds)

1. **Does it need to exist?** Speculative need → skip it, say so in one line (YAGNI).
   Best handled in Phase 1 before a spec is even written.
2. **Already in this codebase?** A helper, util, type, or pattern a few files over →
   reuse it. Re-implementing what already exists is the most common slop.
3. **Stdlib does it?** Use it.
4. **Native platform feature?** `<input type="date">` over a picker lib, CSS over JS,
   a DB constraint over app code.
5. **Already-installed dependency?** Use it. Never add a new dep for what a few lines do.
6. **One line?** One line.
7. **Only then** the minimum code that works.

Two rungs work → take the higher one and move on. The first lazy solution that passes
the spec's tests is the right one — *once you actually understand the change*.

## Where it lives in the BOB phases
- **Phase 1** — question whether the feature should exist at all before speccing it.
- **Phase 3** — sub-agents climb the ladder; the review gate rejects over-engineering
  (one-impl interface, factory for one product, new dep for a few lines, "for later"
  scaffolding) as a real finding.

## Bug fixes: root cause, not symptom
A ticket names a symptom. Before editing, find every caller of the function you'll
touch. One guard in the shared function is a smaller diff than a guard in every caller —
and it actually fixes the siblings the ticket didn't mention. The lazy fix IS the
root-cause fix.

## Mark deliberate shortcuts
A known-ceiling simplification gets a comment so a reader sees intent, not ignorance:
`# bob: global lock; per-account locks if throughput matters`. This is the same "capture
the why" ethos as specs, at the line level. (A `ponytail:` comment means the same thing.)

## Never be lazy about (hard boundary — this is where BOB overrides)
- The spec, its Verification test, or the validator/runtime gates. Minimality never
  removes a test or weakens a contract.
- Input validation at trust boundaries, error handling that prevents data loss,
  security, accessibility basics, anything the user explicitly asked for.
- Understanding the problem. The ladder shortens the solution, never the reading —
  a tiny diff in the wrong place is a second bug, not laziness.

The shortest path that keeps every guarantee is the right path.
