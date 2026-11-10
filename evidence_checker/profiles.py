"""Profiles: what is specific to one audit toolkit, kept out of the rules.

The rules in ``rules.py`` are toolkit-independent. A *profile* tells them where
a toolkit's bundle keeps its layer scores, per-attribute values, metric
sections and class counts, and which words the toolkit uses for intervals and
open gates. Supporting another toolkit means writing an adapter (see
``adapters/``) and a profile like the one below; see docs/BUNDLE_FORMAT.md.

Field types for ``required_fields``:
  str            non-empty string            pos_int        integer > 0
  nonempty_list  list with >= 1 item         nonempty_dict  dict with >= 1 key
  dict           any dict                    score          number in [0, 1]
  withholdable   an artifact reference, or withheld with a justification
  enum:a|b       one of the listed values
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

# Fields every bundle must carry, whatever the toolkit.
CORE_REQUIRED: list[list[str]] = [
    ["I.dataset_id", "str"],
    ["I.n_samples", "pos_int"],
    ["I.audited_attributes", "nonempty_list"],
    ["M.model_id", "str"],
    ["M.predictions", "withholdable"],
    ["M.metrics", "nonempty_dict"],
    ["G.support_policy.min_total", "pos_int"],
    ["G.support_policy.min_class", "pos_int"],
    ["G.groups", "nonempty_list"],
]

# Profile of the XFAIR-MED toolkit (three layers: DF, AMF, EXL; compound XCFS).
XFAIRMED: dict[str, Any] = {
    "name": "xfairmed",
    # Layer scores and per-attribute tables this toolkit must report (checked by R1).
    "required_fields": [
        ["P.DF.value", "score"],
        ["P.DF_units", "nonempty_dict"],
        ["P.AMF.value", "score"],
        ["P.parity_units", "nonempty_dict"],
        ["P.XCFS.value", "score"],
        ["P.XCFS.label", "str"],
        ["A.declared_scope", "enum:partial|complete"],
        ["A.metrics", "dict"],
        ["A.EXL.value", "score"],
    ],
    # Component metrics per layer; names come from contract.required_metrics[layer].
    "components": [
        {"layer": "DF", "path": "P.DF.components"},
        {"layer": "AMF", "path": "P.AMF.components"},
    ],
    # Per-attribute tables in which a missing value must carry a documented reason.
    "unit_tables": [
        {"name": "DF_units", "path": "P.DF_units", "field": "value"},
        {"name": "parity_units", "path": "P.parity_units", "field": "PP"},
    ],
    # Class-count fields of a subgroup record (a bundle may give `class_counts` instead).
    "class_count_fields": ["n_IDC", "n_ILC"],
    # Table that holds the between-subgroup comparison (R2 coverage findings).
    "comparison": {"path": "P.parity_units", "field": "PP", "label": "Model-layer parity"},
    # Reported per-attribute metrics that need an uncertainty record: table -> {metric: field}.
    "uncertainty_targets": [
        {"path": "P.parity_units", "metrics": {"PP": "PP", "RP": "RP"}},
        {"path": "A.ASS_units", "metrics": {"ASS": "value"}},
    ],
    # Substring of an uncertainty record's status that claims a confidence interval.
    "interval_status_marker": "95PCT_CI",
    # Metric sections whose required metrics may be declared not applicable (R3).
    "metric_sections": [
        {"layer": "EXL", "label": "explanation", "metrics": "A.metrics",
         "scope": "A.declared_scope", "scope_source": "A.declared_scope_source",
         "reported_as": "EXL/XCFS"},
    ],
    # Named per-attribute series that R4 can compare.
    "layers": {
        "DF": {"path": "P.DF_units", "field": "value"},
        "PP": {"path": "P.parity_units", "field": "PP"},
        "EXL_ASS": {"path": "A.ASS_units", "field": "value"},
    },
    "default_pairs": [["DF", "PP"], ["DF", "EXL_ASS"]],
    # Status prefixes that mark a declared provenance gate as still open (R5).
    "open_gate_prefixes": ["PENDING", "BLOCKED"],
}

PROFILES: dict[str, dict[str, Any]] = {"xfairmed": XFAIRMED}
DEFAULT_PROFILE = "xfairmed"  # the toolkit audited in the accompanying study


def resolve_profile(p: Any = None) -> dict[str, Any]:
    """Accept a profile name, a path to a JSON profile, a dict, or None (default)."""
    if p is None:
        p = DEFAULT_PROFILE
    if isinstance(p, dict):
        return copy.deepcopy(p)
    if isinstance(p, str) and p in PROFILES:
        return copy.deepcopy(PROFILES[p])
    path = Path(str(p))
    if path.exists():
        return json.loads(path.read_text())
    raise ValueError(f"Unknown profile: {p!r}")


def required_fields(profile: dict[str, Any]) -> list[list[str]]:
    """Core fields followed by the toolkit's own required fields."""
    return [list(x) for x in CORE_REQUIRED] + [list(x) for x in profile.get("required_fields", [])]
