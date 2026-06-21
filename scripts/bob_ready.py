#!/usr/bin/env python3
"""bob ready — is this project BOB-ready? The adoption gate / fail-fast anti-vibe check.

Anti-vibe-coding only works if "build X" is *blocked* until the project has the
discipline in place. This script is that gate: it checks the concrete readiness
criteria and exits non-zero if any are missing, so CI (or the BOB workflow itself)
refuses to proceed on an un-specced project.

Criteria:
  1. constitution.md present (the supreme contract)
  2. at least one APPROVED spec
  3. validator passes (structure + spec-to-test traceability)
  4. runtime/golden checks pass (no errors)
  5. tests/ directory present
  6. AGENTS.md present (DOX context)

Usage:
    python bob_ready.py [PROJECT_ROOT] [--json]
Exit 0 only if every criterion passes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bob_validate as bv  # noqa: E402
import bob_runtime_check as rc  # noqa: E402


def _count_approved_specs(root: Path) -> int:
    specs = root / "specs"
    if not specs.is_dir():
        return 0
    n = 0
    for f in specs.rglob("*.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^status:\s*approved\s*$", text, re.MULTILINE):
            n += 1
    return n


def assess(root: Path):
    """Return a list of (criterion, passed, detail)."""
    results = []

    results.append(("constitution.md present", (root / "constitution.md").is_file(), ""))

    approved = _count_approved_specs(root)
    results.append(("at least one approved spec", approved >= 1, f"{approved} found"))

    v_errors, _ = bv.validate(root)
    results.append(("validator passes (structure + traceability)", not v_errors,
                    f"{len(v_errors)} error(s)"))

    r_errors, _ = rc.run(root)
    results.append(("runtime/golden checks pass", not r_errors, f"{len(r_errors)} error(s)"))

    results.append(("tests/ directory present", (root / "tests").is_dir(), ""))

    results.append(("AGENTS.md present (DOX)", (root / "AGENTS.md").is_file(), ""))

    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description="BOB adoption / readiness gate.")
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    results = assess(root)
    ready = all(p for _, p, _ in results)

    if args.json:
        print(json.dumps({
            "root": str(root), "ready": ready,
            "criteria": [{"name": n, "passed": p, "detail": d} for n, p, d in results],
        }, indent=2))
    else:
        print(f"BOB readiness: {root}\n")
        for name, passed, detail in results:
            mark = "[x]" if passed else "[ ]"
            tail = f"  ({detail})" if detail else ""
            print(f"  {mark} {name}{tail}")
        print(f"\n{'READY' if ready else 'NOT READY'} — "
              f"{sum(p for _, p, _ in results)}/{len(results)} criteria met.")
        if not ready:
            print("Fail-fast: do not generate code until every box is checked. "
                  "See docs/ADOPTION.md.")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
