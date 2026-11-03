"""Run the policy pi over an evidence bundle E: C_pi(E) = {f_1..f_k}."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .ids import digest
from .ledger import rule_r6_continuity
from .rules import DEFAULT_ROLES, RULES, Finding

DEFAULT_POLICY: dict[str, Any] = {
    "version": "policy-v1",
    "rules": ["R1", "R2", "R3", "R4", "R5", "R6"],
    "r4": {"pairs": [["DF", "PP"], ["DF", "EXL_ASS"]], "delta": None},
    "r6": {"fp_scope": "value"},
    "fail_on": ["INCOMPLETE"],
    "roles": DEFAULT_ROLES,
}


def snapshot_id(bundle: dict, policy: dict) -> str:
    return "snap-" + digest([bundle.get("V", {}).get("artifacts"), bundle.get("model"),
                             bundle.get("cohort"), policy.get("version"), policy.get("r4")], 12)


def run_checks(bundle: dict, policy: dict | None = None, ledger: list | None = None,
               artifact_root: Path | None = None) -> dict[str, Any]:
    pol = copy.deepcopy(DEFAULT_POLICY)
    if policy:
        for k, v in policy.items():
            pol[k] = copy.deepcopy(v)
    ctx = {"policy": pol, "artifact_root": artifact_root}
    artifacts = bundle.get("V", {}).get("artifacts") if isinstance(bundle.get("V"), dict) else {}
    artifacts = artifacts if isinstance(artifacts, dict) else {}
    findings: list[Finding] = []
    for r in pol["rules"]:
        if r in RULES:
            findings.extend(RULES[r](bundle, ctx))
    scope = pol.get("r6", {}).get("fp_scope", "value")
    for f in findings:
        f.finalize(pol["roles"], artifacts, scope)
    if "R6" in pol["rules"]:
        r6 = rule_r6_continuity(findings, ledger or [], bundle.get("model"))
        for f in r6:
            f.finalize(pol["roles"], artifacts, scope)
        findings.extend(r6)
    sid = snapshot_id(bundle, pol)
    counts: dict[str, dict[str, int]] = {}
    for f in findings:
        counts.setdefault(f.rule, {}).setdefault(f.outcome, 0)
        counts[f.rule][f.outcome] += 1
    failed = any(f.outcome in pol["fail_on"] for f in findings)
    return {"snapshot_id": sid, "policy_version": pol["version"], "model": bundle.get("model"),
            "cohort": bundle.get("cohort"), "counts": counts, "gate": "FAIL" if failed else "PASS",
            "gate_note": "PASS means the configured technical checks found no blocking condition. "
                         "It is not a fairness certification or deployment approval.",
            "findings": [f.to_dict() for f in findings]}
