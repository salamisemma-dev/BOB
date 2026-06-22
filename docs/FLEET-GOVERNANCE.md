# Fleet governance — invariants, deviations & drift across many projects

`GOVERNANCE.md` covers how a *single* project's specs evolve. This covers the harder
problem when BOB is applied to a **fleet** of related projects that share core
invariants: stopping each project from quietly diverging from the shared contract while
nobody tracks it.

This was added after a real 5-project audit (the SALAMIS fleet) found two services had
widened an HMAC freshness window from the core's 60s to 300s — documented locally, but
never ratified in the core, so the core was blind to it.

## The one rule

**A deviation from a shared invariant is DRIFT until the core ratifies it.**

Projects inherit the core invariants *literally* (`templates/constitution.template.md`
§5). If a project genuinely must differ:

1. Document it in the project's own constitution and mark it
   **"pending core ratification"**. `bob_validate.py` emits a WARN on this marker (and an
   ERROR under `--strict`), so the deviation stays visible in CI instead of hiding.
2. Raise it against the **core** constitution.
3. The core decides:
   - **Ratify** (optionally with conditions) → amend the core constitution's amendment
     log + add a row to the core's `FLEET.md` deviations table; remove the "pending"
     marker downstream.
   - **Reject** → the project conforms to the invariant.
4. Until step 3, treat the deviation as provisional.

## The fleet register (core-owned)

The core repo keeps a `FLEET.md` (from `templates/FLEET.template.md`): every project's
BOB-proof status + every ratified deviation with its condition. The core is
authoritative — a deviation that lives only in a downstream constitution and never reaches
the register is exactly the drift BOB exists to prevent.

## Worked example — tiered HMAC TTL (SALAMIS fleet)

- **Symptom:** two services used a 300s HMAC freshness window; the core invariant said 60s.
  A third used 600s, exceeding even that.
- **Mitigation already present:** all three enforced single-use **nonce/replay stores**,
  which neutralise the replay risk a wider window otherwise opens.
- **Ratified:** the core constitution now allows **up to 300s service-to-service IFF a
  nonce/replay store with TTL ≥ window exists**; 60s stays the single-process default. The
  600s service was narrowed to the 300s cap so the whole fleet sits at one ceiling.
- **Recorded** in the core `FLEET.md` deviations table. Drift → ratified, bounded policy.

The lesson generalises: ratify a deviation as a *bounded, conditioned* policy (here: a cap
plus a mandatory mitigation), never as an open-ended per-project exception.

## CI

Run `python scripts/bob_validate.py --strict .` in each project. With `--strict`, an
unratified deviation marker fails the build — governance becomes enforceable, not goodwill.
