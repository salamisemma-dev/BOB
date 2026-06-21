#!/usr/bin/env python3
"""BOB Benchmark Harness — measure quality and footprint of a spec-driven project.

What it measures:
- Validator: does the spec layer pass `bob_validate.py`? (spec<->format integrity)
- Tests: does the project's unittest suite pass? how long? how many passed/failed?
- Footprint: token count of specs + code as a proxy for maintenance load.

It does NOT yet measure with-vs-without-BOB ROI (tokens/time saved). That needs a
controlled comparison harness; this is the repeatable quality+footprint baseline it
builds on. See docs/BENCHMARK.md.

Usage:
    python scripts/bob_benchmark.py [--demo examples/todo-api] [--output report.md] [--json]

Exit code: 0 if validator AND tests pass, else 1.

Dependency-free by default: token counting uses a stdlib heuristic (~chars/4). If the
optional `tiktoken` package is installed, exact cl100k_base counts are used instead and
the report says so. Staying runnable without third-party deps is a repo invariant.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "bob_validate.py"

try:
    import tiktoken  # type: ignore

    _ENC = tiktoken.get_encoding("cl100k_base")
    HAVE_TIKTOKEN = True
except Exception:  # ImportError, or model data fetch failure
    _ENC = None
    HAVE_TIKTOKEN = False


def run_cmd(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """Run a command; return (returncode, stdout, stderr). Never raises on non-zero."""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return result.returncode, result.stdout, result.stderr


def measure_validator(demo_path: Path) -> Dict:
    start = time.perf_counter()
    rc, out, err = run_cmd([sys.executable, str(VALIDATOR), str(demo_path)])
    return {
        "success": rc == 0,
        "returncode": rc,
        "stdout": out,
        "stderr": err,
        "time": time.perf_counter() - start,
    }


def parse_unittest(output: str) -> Tuple[int, int, int]:
    """Parse unittest output into (ran, passed, failed).

    unittest writes its summary to stderr: a 'Ran N tests' line, then 'OK' or
    'FAILED (failures=X, errors=Y)'. Counting bare 'OK'/'FAIL' substrings is unreliable
    (they appear inside other words and the verbose stream), so parse the summary.
    """
    ran = 0
    m = re.search(r"Ran (\d+) test", output)
    if m:
        ran = int(m.group(1))
    failed = 0
    for label in ("failures", "errors"):
        fm = re.search(rf"{label}=(\d+)", output)
        if fm:
            failed += int(fm.group(1))
    passed = max(ran - failed, 0)
    return ran, passed, failed


def measure_tests(demo_path: Path) -> Dict:
    test_dir = demo_path / "tests"
    if not test_dir.exists():
        return {"success": False, "error": "tests/ directory not found", "time": 0,
                "ran": 0, "passed": 0, "failed": 0}
    start = time.perf_counter()
    rc, out, err = run_cmd(
        [sys.executable, "-m", "unittest", "discover", "-s", str(test_dir), "-v"]
    )
    elapsed = time.perf_counter() - start
    ran, passed, failed = parse_unittest(out + "\n" + err)
    return {
        "success": rc == 0,
        "returncode": rc,
        "stdout": out,
        "stderr": err,
        "time": elapsed,
        "ran": ran,
        "passed": passed,
        "failed": failed,
    }


def count_tokens(text: str) -> int:
    """Exact via tiktoken if available, else a stdlib heuristic (~chars/4)."""
    if HAVE_TIKTOKEN and _ENC is not None:
        return len(_ENC.encode(text))
    return (len(text) + 3) // 4


def count_tokens_in_dir(directory: Path, pattern: str) -> int:
    total = 0
    if not directory.exists():
        return 0
    for path in directory.rglob(pattern):
        if path.is_file():
            total += count_tokens(path.read_text(encoding="utf-8", errors="replace"))
    return total


def measure_footprint(demo_path: Path) -> Dict:
    spec_tokens = count_tokens_in_dir(demo_path / "specs", "*.md")
    constitution = demo_path / "constitution.md"
    if constitution.is_file():
        spec_tokens += count_tokens(constitution.read_text(encoding="utf-8", errors="replace"))
    code_tokens = count_tokens_in_dir(demo_path / "src", "*.py")
    return {
        "spec_tokens": spec_tokens,
        "code_tokens": code_tokens,
        "total_tokens": spec_tokens + code_tokens,
        "exact": HAVE_TIKTOKEN,
    }


def _tail(text: str, n: int = 10) -> List[str]:
    lines = text.splitlines()
    return lines[-n:] if len(lines) > n else lines


def generate_report(demo_path: Path, val: Dict, tests: Dict, fp: Dict, output_file: Path) -> None:
    method = "tiktoken cl100k_base (exact)" if fp["exact"] else "stdlib heuristic (~chars/4, approximate)"
    lines = [
        "# BOB Benchmark Report",
        "",
        f"**Project:** `{demo_path}`",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Validator | {'PASS' if val['success'] else 'FAIL'} ({val['time']:.3f}s) |",
        f"| Tests | {'PASS' if tests['success'] else 'FAIL'} — {tests['passed']}/{tests['ran']} passed, {tests['failed']} failed ({tests['time']:.3f}s) |",
        f"| Spec tokens | {fp['spec_tokens']} |",
        f"| Code tokens | {fp['code_tokens']} |",
        f"| Total tokens | {fp['total_tokens']} |",
        f"| Token method | {method} |",
        "",
        "## Validator output (tail)",
        "```",
        *_tail(val["stdout"] or val["stderr"]),
        "```",
        "",
        "## Test output (tail)",
        "```",
        *_tail(tests.get("stderr", "") or tests.get("stdout", "")),
        "```",
        "",
        "---",
        "_Generated by `scripts/bob_benchmark.py`. Token counts are a footprint proxy, "
        "not a with/without-BOB ROI measurement (see docs/BENCHMARK.md)._",
    ]
    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="BOB benchmark harness")
    parser.add_argument("--demo", default="examples/todo-api",
                        help="path to the project to benchmark (default: examples/todo-api)")
    parser.add_argument("--output", default="benchmark-report.md",
                        help="markdown report path (default: benchmark-report.md)")
    parser.add_argument("--json", action="store_true", help="also print a JSON summary to stdout")
    args = parser.parse_args(argv)

    demo_path = Path(args.demo).resolve()
    if not demo_path.exists():
        print(f"ERROR demo path not found: {demo_path}")
        return 1

    print(f"Benchmarking {demo_path} ...")
    val = measure_validator(demo_path)
    print(f"  validator: {'PASS' if val['success'] else 'FAIL'} ({val['time']:.3f}s)")
    tests = measure_tests(demo_path)
    print(f"  tests: {'PASS' if tests['success'] else 'FAIL'} "
          f"{tests['passed']}/{tests['ran']} ({tests['time']:.3f}s)")
    fp = measure_footprint(demo_path)
    print(f"  footprint: {fp['total_tokens']} tokens "
          f"({'exact' if fp['exact'] else 'approx'})")

    out_path = Path(args.output)
    generate_report(demo_path, val, tests, fp, out_path)
    print(f"Report written to {out_path}")

    if args.json:
        print(json.dumps({
            "validator_pass": val["success"],
            "tests_pass": tests["success"],
            "ran": tests["ran"], "passed": tests["passed"], "failed": tests["failed"],
            "spec_tokens": fp["spec_tokens"], "code_tokens": fp["code_tokens"],
            "total_tokens": fp["total_tokens"], "token_exact": fp["exact"],
        }, indent=2))

    return 0 if (val["success"] and tests["success"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
