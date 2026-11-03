"""R6 Review continuity: the human-decision ledger and dependency-scoped reassessment.

The ledger is a separate, human-authored record. The checker never writes a
decision into it; it only reads it and reports which findings are
  * unresolved  (REVIEW: no disposition yet),
  * stale       (REVIEW: the evidence the decision rested on has changed),
  * disposed    (OBSERVED: decision recorded and evidence unchanged),
  * orphaned    (OBSERVED: decision refers to a finding that no longer occurs).

Staleness is scoped to each finding's own evidence fingerprint, so a change to
one table only reopens decisions that actually depended on it.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .rules import Finding, OBSERVED, REVIEW

DECISIONS = {"accepted_limitation", "action_required", "fixed", "not_a_problem", "deferred"}
LEDGER_FIELDS = ("finding_id", "evidence_fp", "assignee", "decision", "rationale", "timestamp")


def load_ledger(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not Path(path).exists():
        return []
    return json.loads(Path(path).read_text()).get("entries", [])


def rule_r6_continuity(findings: list[Finding], ledger: list[dict[str, Any]],
                       model: str | None) -> list[Finding]:
    by_id: dict[str, dict[str, Any]] = {}
    for e in ledger:
        by_id[e.get("finding_id")] = e  # last entry wins (append-only log)
    out: list[Finding] = []
    actionable = [f for f in findings if f.outcome in (REVIEW,) or f.outcome == "INCOMPLETE"]
    live_ids = {f.finding_id for f in actionable}
    for f in actionable:
        e = by_id.get(f.finding_id)
        base = dict(model=f.model, attribute=f.attribute, subgroup=f.subgroup, key=f.finding_id)
        if e is None or e.get("decision") not in DECISIONS or not e.get("assignee"):
            out.append(Finding("R6", REVIEW, "unresolved",
                               f"{f.rule} finding `{f.finding_id}` has no recorded disposition.",
                               evidence={"target": f.finding_id, "target_fp": f.evidence_fp},
                               action="Assign an owner and record a decision with rationale.", **base))
        elif e.get("evidence_fp") != f.evidence_fp:
            out.append(Finding("R6", REVIEW, "stale",
                               f"Decision `{e.get('decision')}` on `{f.finding_id}` by {e.get('assignee')} "
                               f"rested on evidence {e.get('evidence_fp')}; evidence is now {f.evidence_fp}.",
                               evidence={"target": f.finding_id, "target_fp": f.evidence_fp,
                                         "decided_fp": e.get("evidence_fp"), "decision": e.get("decision")},
                               action="Reassess: the earlier decision does not carry over automatically.", **base))
        else:
            out.append(Finding("R6", OBSERVED, "disposed",
                               f"`{f.finding_id}` disposed as `{e['decision']}` by {e['assignee']}.",
                               evidence={"target": f.finding_id, "target_fp": f.evidence_fp,
                                         "decision": e["decision"]},
                               action="None; disposition current.", **base))
    for fid, e in by_id.items():
        if fid not in live_ids and (model is None or e.get("model") in (None, model)):
            out.append(Finding("R6", OBSERVED, "orphaned",
                               f"Ledger decision on `{fid}` no longer matches a live finding.",
                               model=model, key=fid,
                               evidence={"target": fid, "decision": e.get("decision")},
                               action="Confirm the condition is truly resolved, then close the entry."))
    return out


def ledger_entry(f: Finding, assignee: str, decision: str, rationale: str,
                 timestamp: str) -> dict[str, Any]:
    assert decision in DECISIONS
    return {"finding_id": f.finding_id, "evidence_fp": f.evidence_fp, "model": f.model,
            "rule": f.rule, "assignee": assignee, "decision": decision,
            "rationale": rationale, "timestamp": timestamp}
