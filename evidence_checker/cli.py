"""Command line entry point, suitable for a CI step.

  python -m evidence_checker.cli bundle.json --policy policy.json \
      --ledger review_ledger.json --artifact-root . --out findings.json --report report.md

Exit code 1 when a finding matches policy.fail_on (default: INCOMPLETE), else 0.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import run_checks
from .ledger import load_ledger
from .report import to_markdown


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="evidence-checker")
    ap.add_argument("bundle", type=Path)
    ap.add_argument("--policy", type=Path)
    ap.add_argument("--profile", help="profile name or path to a JSON profile (default: built-in)")
    ap.add_argument("--ledger", type=Path)
    ap.add_argument("--artifact-root", type=Path)
    ap.add_argument("--out", type=Path, default=Path("findings.json"))
    ap.add_argument("--report", type=Path, default=Path("review_report.md"))
    a = ap.parse_args(argv)
    bundle = json.loads(a.bundle.read_text())
    policy = json.loads(a.policy.read_text()) if a.policy else None
    if a.profile:
        policy = {**(policy or {}), "profile": a.profile}
    res = run_checks(bundle, policy, load_ledger(a.ledger), a.artifact_root)
    a.out.write_text(json.dumps(res, indent=1))
    a.report.write_text(to_markdown(res))
    print(f"{res['model']}: gate={res['gate']} counts={res['counts']}")
    return 1 if res["gate"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
