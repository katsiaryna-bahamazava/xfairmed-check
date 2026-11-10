"""Stable identifiers and fingerprints.

logical_id     -- identifies *what* a finding is about (rule, model, attribute,
                  subgroup, key). Stable across runs, so dispositions can be
                  matched to later runs.
evidence_fp    -- fingerprint of the exact evidence values a finding depends on.
                  If it changes, an earlier human disposition is stale (R6).
snapshot_id    -- fingerprint of the whole evidence bundle + policy version.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any


def _norm(obj: Any) -> Any:
    """Normalise values so fingerprints ignore float noise and key order."""
    if isinstance(obj, float):
        if math.isnan(obj):
            return "NaN"
        return round(obj, 10)
    if isinstance(obj, dict):
        return {str(k): _norm(v) for k, v in sorted(obj.items(), key=lambda kv: str(kv[0]))}
    if isinstance(obj, (list, tuple)):
        return [_norm(v) for v in obj]
    return obj


def digest(obj: Any, n: int = 12) -> str:
    payload = json.dumps(_norm(obj), sort_keys=True, ensure_ascii=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:n]


def logical_id(rule: str, model: str | None, attribute: str | None,
               subgroup: str | None, key: str) -> str:
    return f"{rule}-" + digest([rule, model, attribute, subgroup, key], 10)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()
