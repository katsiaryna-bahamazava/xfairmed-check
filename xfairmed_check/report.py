"""Human-readable review report (Markdown) from a check result."""
from __future__ import annotations

from typing import Any

ORDER = {"INCOMPLETE": 0, "REVIEW": 1, "OBSERVED": 2}


def _refs(f: dict[str, Any]) -> str:
    parts = []
    for r in f.get("refs", []):
        s = r.get("artifact", "")
        if r.get("row"):
            s += " [" + ", ".join(f"{k}={v}" for k, v in r["row"].items()) + "]"
        parts.append(f"`{s}`")
    return "; ".join(parts) or "-"


def to_markdown(result: dict[str, Any], include_observed: bool = False) -> str:
    L = [f"# Review report: {result['model']} ({result['cohort']})", "",
         f"- Evidence snapshot: `{result['snapshot_id']}`  ",
         f"- Policy: `{result['policy_version']}`  ",
         f"- Gate: **{result['gate']}**. {result['gate_note']}", "",
         "| Rule | INCOMPLETE | REVIEW | OBSERVED |", "|---|---|---|---|"]
    for r in sorted(result["counts"]):
        c = result["counts"][r]
        L.append(f"| {r} | {c.get('INCOMPLETE', 0)} | {c.get('REVIEW', 0)} | {c.get('OBSERVED', 0)} |")
    L.append("")
    fs = [f for f in result["findings"] if include_observed or f["outcome"] != "OBSERVED"]
    fs.sort(key=lambda f: (ORDER[f["outcome"]], f["rule"], f.get("attribute") or "", f.get("subgroup") or ""))
    for f in fs:
        L += [f"### [{f['outcome']}] {f['rule']} {f['kind']} `{f['finding_id']}`",
              f"{f['message']}", "",
              f"- Owner role: {f['role']}",
              f"- Suggested action: {f['action']}",
              f"- Evidence: {_refs(f)}",
              f"- Evidence fingerprint: `{f['evidence_fp']}`", ""]
    return "\n".join(L)
