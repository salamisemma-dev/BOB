#!/usr/bin/env python3
"""bob validate — dependency-free validator for BOB Spec-Driven Development repos.

Enforces the canonical BOB spec format so "executable, version-controlled specs"
are actually checkable in CI instead of being voluntary documentation. Exits non-zero
on any violation, so a broken spec layer turns the build red.

Usage:
    python bob_validate.py [PROJECT_ROOT]      # default: current dir
    python bob_validate.py --json [ROOT]       # machine-readable report

What it checks (see docs/SPEC-FORMAT.md for the full contract):
    - constitution.md exists at the project root.
    - every specs/**/*.md has valid frontmatter with required keys.
    - type is one of the six canonical spec types.
    - status is draft | approved | deprecated.
    - required body sections are present (and non-empty for approved specs).
    - spec ids are unique.
    - depends_on ids resolve to existing specs (hard error).
    - consumed_by ids that look like specs resolve (soft warning otherwise).

No third-party dependencies — a tiny frontmatter parser handles the YAML subset the
templates use, so the validator runs anywhere Python 3.8+ runs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SPEC_TYPES = {
    "schema",
    "transformation",
    "validation",
    "orchestration",
    "semantic",
    "ai-workflow",
}
STATUSES = {"draft", "approved", "deprecated"}
REQUIRED_KEYS = ["id", "type", "version", "status", "owner"]
REQUIRED_SECTIONS = [
    "Intent",
    "Contract",
    "Business rules",
    "Downstream impact",
    "Verification",
]


def parse_frontmatter(text: str):
    """Return (frontmatter_dict, body_str). Frontmatter is the block between the
    first pair of `---` fences. Supports `key: value` and inline `[a, b]` lists —
    the subset the BOB templates use. Returns (None, text) if no frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    fm = {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    for raw in lines[1:end]:
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
            fm[key] = items
        else:
            fm[key] = val.strip("'\"")
    body = "\n".join(lines[end + 1 :])
    return fm, body


def section_bodies(body: str):
    """Map H2 heading text -> its content (until the next H2). Used to check that
    required sections exist and (for approved specs) carry real content."""
    out = {}
    current = None
    buf = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def validate(root: Path, traceability: bool = True, strict: bool = False):
    """Return (errors, warnings) lists of human-readable strings.

    traceability=True also enforces the spec-to-test gate (see check_traceability).
    strict=True promotes the 'referenced test asserts nothing' warning to a hard error
    (and traceability is forced on)."""
    if strict:
        traceability = True
    errors = []
    warnings = []

    if not (root / "constitution.md").is_file():
        errors.append(
            "constitution.md missing at project root — every BOB project needs its "
            "supreme contract. Create it from templates/constitution.template.md."
        )

    specs_dir = root / "specs"
    if not specs_dir.is_dir():
        warnings.append(
            "no specs/ directory found — nothing to validate. Add specs before "
            "generating code (no code without an approved spec)."
        )
        return errors, warnings

    spec_files = sorted(f for f in specs_dir.rglob("*.md") if f.name != "AGENTS.md")
    ids = {}
    records = []

    for f in spec_files:
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: missing YAML frontmatter block (--- ... ---).")
            continue

        for key in REQUIRED_KEYS:
            if not fm.get(key):
                errors.append(f"{rel}: frontmatter missing required key '{key}'.")

        stype = fm.get("type")
        if stype and stype not in SPEC_TYPES:
            errors.append(
                f"{rel}: type '{stype}' is not a canonical BOB spec type "
                f"({', '.join(sorted(SPEC_TYPES))})."
            )

        status = fm.get("status")
        if status and status not in STATUSES:
            errors.append(
                f"{rel}: status '{status}' invalid (use {', '.join(sorted(STATUSES))})."
            )

        sid = fm.get("id")
        if sid:
            if sid in ids:
                errors.append(
                    f"{rel}: duplicate spec id '{sid}' (also in {ids[sid]}). Ids must "
                    "be unique — they are the stable handle other specs reference."
                )
            else:
                ids[sid] = rel

        secs = section_bodies(body)
        for sec in REQUIRED_SECTIONS:
            if sec not in secs:
                errors.append(f"{rel}: missing required section '## {sec}'.")
            elif status == "approved" and not secs[sec]:
                errors.append(
                    f"{rel}: section '## {sec}' is empty but status is 'approved'. "
                    "Approved specs must carry real content (esp. Intent + Business "
                    "rules — that's the permanent memory)."
                )

        records.append((rel, fm, secs))

    # Cross-reference integrity (after collecting all ids).
    for rel, fm, _secs in records:
        for dep in fm.get("depends_on", []) or []:
            if dep not in ids:
                errors.append(
                    f"{rel}: depends_on '{dep}' does not resolve to any spec id "
                    "(dangling upstream dependency)."
                )
        for cons in fm.get("consumed_by", []) or []:
            # consumed_by may name a component, not a spec; only warn when it looks
            # like a spec id (one of the type prefixes) but isn't found.
            looks_like_spec = any(cons.startswith(t) for t in SPEC_TYPES)
            if looks_like_spec and cons not in ids:
                warnings.append(
                    f"{rel}: consumed_by '{cons}' looks like a spec id but no such "
                    "spec exists — fix the reference or rename it."
                )

    if not spec_files:
        warnings.append("specs/ exists but contains no .md spec files.")

    if traceability:
        t_errors, t_warnings = check_traceability(root, records, strict=strict)
        errors.extend(t_errors)
        warnings.extend(t_warnings)

    return errors, warnings


# Matches a test file path with an optional ::test_name. Supports Python and
# common JS/TS test runners, e.g. tests/test_x.py::test_y or
# src/__tests__/thing.test.ts::handlesThing.
_TEST_REF_RE = re.compile(
    r"([\w./\\-]+\.(?:py|js|mjs|cjs|ts|tsx|jsx))(?:::(\w+))?"
)


def parse_test_refs(verification_text: str):
    """Return [(path, test_name_or_None)] for Python/JS/TS test references."""
    return [(m.group(1).replace("\\", "/"), m.group(2)) for m in _TEST_REF_RE.finditer(verification_text)]


# Tokens that signal a test actually asserts something (Python + common JS/TS runners).
_ASSERTION_TOKENS = (
    "assert", "expect(", "toBe", "toEqual", "toThrow", ".should", "chai",
    "t.is(", "t.deepEqual", "self.assert",
)


def _looks_like_real_test(content: str) -> bool:
    return any(tok in content for tok in _ASSERTION_TOKENS)


def check_traceability(root, records, strict=False):
    """Anti-vibe gate: every APPROVED spec must tie to a real test, so a spec can't
    just 'look valid' while nothing exercises the behavior. A spec satisfies this when
    its Verification section names at least one test file that exists (and, if a
    ::test_name is given, that the test is defined in that file).

    Hard errors block (missing reference / missing file / missing test name). A
    referenced test file that contains no recognizable assertions is flagged as a
    *warning* — a test that asserts nothing can't prove the spec, but assertion styles
    vary across runners, so we surface rather than block to avoid false positives. Under
    strict=True that assertionless case is promoted to a hard error.

    Exempt: type 'ai-workflow' (process/instruction specs) and any spec with frontmatter
    `verification: manual` — those are reviewed by a human, not a unit test.

    Returns (errors, warnings).
    """
    errors = []
    warnings = []
    for rel, fm, secs in records:
        if fm.get("status") != "approved":
            continue
        if fm.get("type") == "ai-workflow":
            continue
        if str(fm.get("verification", "")).lower() == "manual":
            continue
        ver = secs.get("Verification", "") or ""
        refs = parse_test_refs(ver)
        if not refs:
            errors.append(
                f"{rel}: approved spec has no test reference in its Verification section. "
                "Tie it to a real test (e.g. `tests/x.py::test_y`), or — for a process "
                "spec — use type 'ai-workflow' or add frontmatter `verification: manual`."
            )
            continue
        for path, name in refs:
            target = (root / path)
            if not target.is_file():
                errors.append(
                    f"{rel}: Verification references test file '{path}' which does not "
                    "exist. The spec-to-test link is broken (green CI would be a lie)."
                )
                continue
            content = target.read_text(encoding="utf-8", errors="replace")
            if name and f"def {name}" not in content and name not in content:
                errors.append(
                    f"{rel}: Verification references test '{name}' not found in "
                    f"'{path}'. Rename the reference or add the test."
                )
            if not _looks_like_real_test(content):
                msg = (
                    f"{rel}: referenced test '{path}' contains no recognizable assertions "
                    "(expect/assert/...). A test that asserts nothing can't prove the spec — "
                    "verify it really exercises the behavior."
                )
                (errors if strict else warnings).append(msg)
    return errors, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate a BOB spec-driven repo.")
    ap.add_argument("root", nargs="?", default=".", help="project root (default: .)")
    ap.add_argument("--json", action="store_true", help="emit JSON report")
    ap.add_argument("--no-traceability", action="store_true",
                    help="skip the spec-to-test gate (structural checks only)")
    ap.add_argument("--strict", action="store_true",
                    help="promote the 'test asserts nothing' warning to an error; forces "
                         "traceability on (ignores --no-traceability). Use in CI.")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    traceability = not args.no_traceability
    if args.strict and args.no_traceability:
        print("note: --strict overrides --no-traceability (traceability forced on).")
    errors, warnings = validate(root, traceability=traceability, strict=args.strict)

    if args.json:
        print(json.dumps({"root": str(root), "errors": errors, "warnings": warnings}, indent=2))
    else:
        for w in warnings:
            print(f"WARN  {w}")
        for e in errors:
            print(f"ERROR {e}")
        if errors:
            print(f"\nFAIL: {len(errors)} error(s), {len(warnings)} warning(s).")
        else:
            print(f"OK: spec layer valid ({len(warnings)} warning(s)).")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())



