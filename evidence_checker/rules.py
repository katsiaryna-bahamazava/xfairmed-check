"""Rules R1-R5 of Evidence Checker (R6 lives in ledger.py).

The rules are toolkit-independent: thresholds come from the bundle's declared
policy and contract, and bundle locations and labels come from a profile
(see profiles.py).

Each rule reads an evidence bundle and returns findings f = (rule, outcome,
evidence, role, action). Rules never recompute fairness scores and never emit a
global fair/unfair verdict.

Outcomes:
  OBSERVED   evidence or a declared limitation recorded; no action required by policy
  REVIEW     a documented condition needs contextual human review
  INCOMPLETE required evidence is missing, invalid, undocumented or inconsistently declared
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from .ids import digest, file_sha256, logical_id
from .profiles import required_fields, resolve_profile

OBSERVED, REVIEW, INCOMPLETE = "OBSERVED", "REVIEW", "INCOMPLETE"

DEFAULT_ROLES = {
    "R1": "ML engineer (pipeline owner)",
    "R2": "Data steward + biostatistician",
    "R3": "Explainability owner",
    "R4": "Fairness reviewer + clinical domain expert",
    "R5": "ML engineer (pipeline owner)",
    "R6": "Responsibility lead (review owner)",
}


@dataclass
class Finding:
    rule: str
    outcome: str
    kind: str
    message: str
    model: str | None = None
    attribute: str | None = None
    subgroup: str | None = None
    key: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    refs: list[dict[str, Any]] = field(default_factory=list)
    role: str = ""
    action: str = ""
    finding_id: str = ""
    evidence_fp: str = ""

    def finalize(self, roles: dict[str, str], artifacts: dict[str, str],
                 fp_scope: str = "value") -> "Finding":
        """Assign stable id and evidence fingerprint.

        fp_scope="value":    fingerprint = the evidence values + row selectors the
                             finding rests on.
        fp_scope="artifact": additionally includes whole-file hashes of every
                             referenced artifact (conservative baseline).
        """
        self.role = self.role or roles.get(self.rule, "")
        self.finding_id = logical_id(self.rule, self.model, self.attribute, self.subgroup,
                                     f"{self.kind}:{self.key}")
        selectors = sorted([[r.get("artifact"), r.get("row")] for r in self.refs], key=str)
        parts: list = [self.evidence, selectors]
        if fp_scope == "artifact":
            parts.append(sorted({r.get("artifact"): artifacts.get(r.get("artifact"))
                                 for r in self.refs if r.get("artifact")}.items()))
        self.evidence_fp = digest(parts)
        return self

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ----------------------------------------------------------------------------
class _Missing:
    def __repr__(self):
        return "<missing>"


_MISSING = _Missing()


def _get(d: Any, path: str) -> Any:
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return _MISSING
        cur = cur[p]
    return cur


def _is_score(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and not math.isnan(x) and 0.0 <= x <= 1.0


def _predictions_ok(v: Any) -> bool:
    if not isinstance(v, dict):
        return False
    if "artifact" in v:
        return True
    return v.get("withheld") is True and bool((v.get("justification") or "").strip())


# R1: structure + values. Provenance is R5's job; metric coverage is R3's job.
def _validator(kind: str):
    if kind == "str":
        return lambda v: isinstance(v, str) and v != ""
    if kind == "pos_int":
        return lambda v: isinstance(v, int) and not isinstance(v, bool) and v > 0
    if kind == "nonempty_list":
        return lambda v: isinstance(v, list) and len(v) > 0
    if kind == "nonempty_dict":
        return lambda v: isinstance(v, dict) and len(v) > 0
    if kind == "dict":
        return lambda v: isinstance(v, dict)
    if kind == "score":
        return _is_score
    if kind == "withholdable":
        return _predictions_ok
    if kind.startswith("enum:"):
        allowed = tuple(kind[5:].split("|"))
        return lambda v: v in allowed
    raise ValueError(f"Unknown field type in profile: {kind!r}")


def _profile(ctx: dict) -> dict:
    p = ctx.get("profile")
    return p if isinstance(p, dict) else resolve_profile(None)


def class_counts(g: dict, profile: dict) -> dict[str, int]:
    """Class counts of a subgroup record: `class_counts`, or the profile's count fields."""
    cc = g.get("class_counts")
    if isinstance(cc, dict):
        return dict(cc)
    return {f[2:] if f.startswith("n_") else f: g[f] for f in profile.get("class_count_fields", []) if f in g}


def _iter_refs(obj: Any):
    """Every dict carrying an `artifact` key is an evidence reference, whatever its parent key."""
    if isinstance(obj, dict):
        if isinstance(obj.get("artifact"), str):
            yield obj
        for k, v in obj.items():
            if k == "artifacts":  # the manifest itself, not a reference
                continue
            yield from _iter_refs(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _iter_refs(v)


def rule_r1_schema(b: dict, ctx: dict) -> list[Finding]:
    out: list[Finding] = []
    model = b.get("model")
    prof = _profile(ctx)
    for path, kind in required_fields(prof):
        ok = _validator(kind)
        v = _get(b, path)
        if v is _MISSING or v is None:
            out.append(Finding("R1", INCOMPLETE, "missing_field", f"Required field `{path}` is absent.",
                               model=model, key=path, evidence={"field": path, "value": None},
                               action="Restore the artifact/field or document why it is withheld or not applicable."))
        elif not ok(v):
            out.append(Finding("R1", INCOMPLETE, "invalid_field", f"Field `{path}` has an invalid value ({v!r}).",
                               model=model, key=path, evidence={"field": path, "value": v},
                               action="Correct the value at its source table and re-export the bundle."))
    for c in prof.get("components", []):
        comp_path = c["path"]
        names = _get(b, f"contract.required_metrics.{c['layer']}")
        names = names if isinstance(names, list) else c.get("default", [])
        comps = _get(b, comp_path)
        if isinstance(comps, dict):
            for n in names:
                v = comps.get(n, _MISSING)
                if v is _MISSING or not _is_score(v):
                    out.append(Finding("R1", INCOMPLETE, "invalid_component",
                                       f"Contracted metric `{n}` in `{comp_path}` is missing or out of [0,1].",
                                       model=model, key=f"{comp_path}.{n}",
                                       evidence={"field": f"{comp_path}.{n}", "value": None if v is _MISSING else v},
                                       action="Recompute or restore the component metric."))
    # Per-attribute units: a missing value must be explained (explicit incompleteness).
    for t in prof.get("unit_tables", []):
        layer, field_ = t["name"], t["field"]
        units = _get(b, t["path"])
        if isinstance(units, dict):
            for attr, u in units.items():
                u = u if isinstance(u, dict) else {}
                v = u.get(field_)
                ref = [u["ref"]] if "ref" in u else []
                if v is None and not u.get("note"):
                    out.append(Finding("R1", INCOMPLETE, "undocumented_gap",
                                       f"{layer} value for `{attr}` is missing with no documented reason.",
                                       model=model, attribute=attr, key=layer, evidence={"value": None},
                                       refs=ref, action="Record why the unit was not computed, or compute it."))
                elif v is not None and not _is_score(v):
                    out.append(Finding("R1", INCOMPLETE, "invalid_field",
                                       f"{layer} value for `{attr}` is out of [0,1] ({v!r}).",
                                       model=model, attribute=attr, key=layer, evidence={"value": v},
                                       refs=ref, action="Correct the value at its source table."))
    declared = _get(b, "V.artifacts")
    declared = set(declared) if isinstance(declared, dict) else set()
    for ref in _iter_refs(b):
        a = ref.get("artifact")
        if a and a not in declared:
            out.append(Finding("R1", INCOMPLETE, "dangling_ref",
                               f"Evidence reference `{a}` is not declared in the artifact manifest.",
                               model=model, key=a, evidence={"artifact": a},
                               action="Declare the artifact (with hash) or fix the reference."))
    return out


# ----------------------------------------------------------------------------
def rule_r2_support(b: dict, ctx: dict) -> list[Finding]:
    """Subgroup support, parity coverage and uncertainty records."""
    out: list[Finding] = []
    model = b.get("model")
    pol = _get(b, "G.support_policy")
    groups = _get(b, "G.groups")
    prof = _profile(ctx)
    cmp_ = prof.get("comparison") or {}
    cmp_field, cmp_label = cmp_.get("field", "value"), cmp_.get("label", "Subgroup comparison")
    units = _get(b, cmp_["path"]) if cmp_.get("path") else {}
    units = units if isinstance(units, dict) else {}
    if isinstance(pol, dict) and isinstance(groups, list) and \
            isinstance(pol.get("min_total"), int) and isinstance(pol.get("min_class"), int):
        mt, mc = pol["min_total"], pol["min_class"]
        for g in groups:
            counts = class_counts(g, prof)
            n_ev = {f"n_{k}": v for k, v in counts.items()}
            minority = min(counts.values())
            low_total, low_class = g["total"] < mt, minority < mc
            eligible_by_policy = not (low_total or low_class)
            u = units.get(g["attribute"], {})
            # Consistency: the toolkit's own eligibility declaration must match its policy.
            declared = g.get("declared_eligible")
            if declared is not None and bool(declared) != eligible_by_policy:
                out.append(Finding(
                    "R2", INCOMPLETE, "eligibility_mismatch",
                    f"Subgroup `{g['attribute']}={g['group']}` is declared "
                    f"{'eligible' if declared else 'ineligible'} but the support policy says otherwise.",
                    model=model, attribute=g["attribute"], subgroup=g["group"], key="eligibility",
                    evidence={"declared_eligible": declared, "eligible_by_policy": eligible_by_policy,
                              **n_ev, "total": g["total"]},
                    refs=[g["ref"]], action="Re-derive the frozen eligibility manifest from the declared policy."))
            if eligible_by_policy:
                continue
            excluded = g["group"] in (u.get("excluded_groups") or [])
            why = []
            if low_total:
                why.append(f"total {g['total']} < {mt}")
            if low_class:
                why.append(f"minority class {minority} < {mc}")
            out.append(Finding(
                "R2", REVIEW, "low_support",
                f"Subgroup `{g['attribute']}={g['group']}` has insufficient support ({'; '.join(why)})."
                + (" It is excluded from the parity comparison." if excluded else ""),
                model=model, attribute=g["attribute"], subgroup=g["group"], key="support",
                evidence={**n_ev, "total": g["total"],
                          "min_total": mt, "min_class": mc, "excluded_from_parity": excluded},
                refs=[g["ref"]] + ([u["ref"]] if "ref" in u else []),
                action="Inspect counts and uncertainty; decide whether subgroup results are interpretable, "
                       "need pooling, more data, or an explicit limitation."))
    for attr, u in units.items():
        if u.get(cmp_field) is None and u.get("note"):
            out.append(Finding(
                "R2", REVIEW, "parity_not_computable",
                f"{cmp_label} for `{attr}` was not computed: {u['note']} "
                f"Excluded: {', '.join(u.get('excluded_groups') or []) or 'n/a'}.",
                model=model, attribute=attr, key="parity_coverage",
                evidence={"note": u["note"], "excluded_groups": u.get("excluded_groups"),
                          "groups_used": u.get("groups_used")},
                refs=[u["ref"]] if "ref" in u else [],
                action="Do not read the aggregate model-fairness score as covering this attribute; "
                       "record the coverage gap."))
    # Uncertainty records (only when the contract requires them).
    req = _get(b, "contract.uncertainty")
    if not isinstance(req, dict) or not req.get("required"):
        return out
    U = _get(b, "U")
    U = U if isinstance(U, dict) else {}
    recs = U.get("records") if isinstance(U.get("records"), dict) else {}
    min_b, min_frac = req.get("min_attempted", 2000), req.get("min_valid_fraction", 0.95)
    marker = prof.get("interval_status_marker", "CI")
    targets = []
    for t in prof.get("uncertainty_targets", []):
        table = _get(b, t["path"])
        for attr, u in (table.items() if isinstance(table, dict) else []):
            for m, fld in t["metrics"].items():
                if isinstance(u, dict) and u.get(fld) is not None:
                    targets.append((f"{m}|{attr}", attr, m))
    for key, attr, metric in targets:
        r = recs.get(key)
        if not isinstance(r, dict):
            out.append(Finding("R2", INCOMPLETE, "uncertainty_missing",
                               f"No uncertainty record for {metric} on `{attr}`.",
                               model=model, attribute=attr, key=f"U:{metric}",
                               evidence={"metric": metric, "record": None},
                               action="Report the bootstrap record (attempted, valid, status) for this metric."))
            continue
        ref = [r["ref"]] if "ref" in r else []
        claims_ci = marker in (r.get("status") or "")
        att, val = r.get("n_attempted"), r.get("n_valid")
        if claims_ci and (not isinstance(att, int) or not isinstance(val, int)
                          or att < min_b or val < min_frac * att):
            out.append(Finding("R2", INCOMPLETE, "interval_gate_violation",
                               f"{metric} interval for `{attr}` is labelled `{r.get('status')}` but "
                               f"{val}/{att} replicates do not meet the declared gate "
                               f"({min_b} attempted, {min_frac:.0%} valid).",
                               model=model, attribute=attr, key=f"U:{metric}",
                               evidence={"metric": metric, "n_attempted": att, "n_valid": val,
                                         "status": r.get("status")}, refs=ref,
                               action="Withhold the interval or rerun the bootstrap to the declared gate."))
    na = U.get("not_approved_methods") or {}
    for metric, why in sorted(na.items()):
        out.append(Finding("R2", OBSERVED, "interval_not_approved",
                           f"{metric} intervals are declared not approved for confidence-interval "
                           f"reporting ({why}); point estimates are descriptive only.",
                           model=model, key=f"U:{metric}:not_approved",
                           evidence={"metric": metric, "reason": why},
                           refs=[U["not_approved_ref"]] if "not_approved_ref" in U else [],
                           action="Report point estimates only; do not present these intervals as CIs."))
    return out


# ----------------------------------------------------------------------------
def rule_r3_coverage(b: dict, ctx: dict) -> list[Finding]:
    """Metric coverage: required metrics are computed, or declared not applicable with a reason."""
    out: list[Finding] = []
    for sec in _profile(ctx).get("metric_sections", []):
        out.extend(_r3_section(b, sec))
    return out


def _r3_section(b: dict, sec: dict) -> list[Finding]:
    out: list[Finding] = []
    model = b.get("model")
    layer, label = sec["layer"], sec.get("label", sec["layer"])
    Label, reported_as = label[:1].upper() + label[1:], sec.get("reported_as", layer)
    metrics = _get(b, sec["metrics"])
    scope = _get(b, sec["scope"]) if sec.get("scope") else _MISSING
    scope_src = _get(b, sec["scope_source"]) if sec.get("scope_source") else _MISSING
    contract = _get(b, f"contract.required_metrics.{layer}")
    allow_na = _get(b, "contract.allow_declared_not_applicable") is True
    if not isinstance(metrics, dict) or not isinstance(contract, list):
        return out
    for m in contract:
        e = metrics.get(m)
        ref = [e["ref"]] if isinstance(e, dict) and "ref" in e else []
        if e is None or e.get("status") in (None, "missing"):
            out.append(Finding("R3", INCOMPLETE, "missing_metric",
                               f"Required {label} metric `{m}` is absent.",
                               model=model, key=m, evidence={"metric": m, "status": None}, refs=ref,
                               action="Compute the metric or declare it not applicable with a justification."))
            continue
        st = e.get("status")
        if st == "computed":
            if not _is_score(e.get("value")):
                out.append(Finding("R3", INCOMPLETE, "invalid_metric",
                                   f"{Label} metric `{m}` is marked computed but has no valid value.",
                                   model=model, key=m, evidence={"metric": m, "value": e.get("value")}, refs=ref,
                                   action="Restore the computed value."))
        elif st == "not_applicable":
            just = (e.get("justification") or "").strip()
            if not allow_na or not just:
                out.append(Finding("R3", INCOMPLETE, "unjustified_na",
                                   f"`{m}` is declared not applicable without an accepted justification.",
                                   model=model, key=m, evidence={"metric": m, "justification": just or None},
                                   refs=ref, action="Add a justification or compute the metric."))
            elif scope == "complete":
                out.append(Finding("R3", INCOMPLETE, "scope_mismatch",
                                   f"The audit output declares a complete scope"
                                   + (f" (`{scope_src}`)" if isinstance(scope_src, str) else "")
                                   + f" but `{m}` was not computed ({just}).",
                                   model=model, key=m, evidence={"metric": m, "declared_scope": scope,
                                                                 "declared_by": scope_src if isinstance(scope_src, str) else None},
                                   refs=ref, action="Label the compound score as partial, or compute the metric."))
            else:
                out.append(Finding("R3", OBSERVED, "declared_limitation",
                                   f"`{m}` not computed by declaration: {just}. {layer} is reported as partial.",
                                   model=model, key=m, evidence={"metric": m, "justification": just,
                                                                 "declared_scope": scope},
                                   refs=ref, action=f"Keep the limitation visible wherever {reported_as} is reported."))
        else:
            out.append(Finding("R3", INCOMPLETE, "unknown_status",
                               f"{Label} metric `{m}` has unrecognised status `{st}`.",
                               model=model, key=m, evidence={"metric": m, "status": st}, refs=ref,
                               action="Use one of: computed, not_applicable (with justification)."))
    return out


# ----------------------------------------------------------------------------
def _layer_units(b: dict, layer: str, profile: dict) -> dict[str, dict]:
    spec = (profile.get("layers") or {}).get(layer)
    if not spec:
        return {}
    u = _get(b, spec["path"])
    if not isinstance(u, dict):
        return {}
    fld = spec.get("field", "value")
    if fld == "value":
        return u
    return {k: {"value": v.get(fld), "ref": v.get("ref")} for k, v in u.items()}


def rule_r4_cross_layer(b: dict, ctx: dict) -> list[Finding]:
    """Per-attribute cross-layer comparison; REVIEW only above a pre-registered delta."""
    out: list[Finding] = []
    model = b.get("model")
    pol = ctx.get("policy", {}).get("r4", {})
    delta = pol.get("delta")
    prof = _profile(ctx)
    for a, c in (pol.get("pairs") or prof.get("default_pairs") or []):
        ua, uc = _layer_units(b, a, prof), _layer_units(b, c, prof)
        for attr in sorted(set(ua) | set(uc)):
            va = (ua.get(attr) or {}).get("value")
            vc = (uc.get(attr) or {}).get("value")
            refs = [x["ref"] for x in (ua.get(attr), uc.get(attr)) if x and x.get("ref")]
            if va is None or vc is None:
                out.append(Finding("R4", OBSERVED, "not_comparable",
                                   f"{a} vs {c} for `{attr}` not comparable: one layer has no value.",
                                   model=model, attribute=attr, key=f"{a}~{c}",
                                   evidence={a: va, c: vc}, refs=refs,
                                   action="See R2/R1 findings for why the unit is missing."))
                continue
            gap = abs(va - vc)
            ev = {a: round(va, 6), c: round(vc, 6), "gap": round(gap, 6), "delta": delta}
            if delta is not None and gap > delta:
                out.append(Finding("R4", REVIEW, "divergence",
                                   f"{a}={va:.3f} vs {c}={vc:.3f} for `{attr}` (|gap|={gap:.3f} > delta={delta}).",
                                   model=model, attribute=attr, key=f"{a}~{c}", evidence=ev, refs=refs,
                                   action="Inspect layer-specific metrics and their measurement context "
                                          "before drawing any fairness conclusion."))
            else:
                out.append(Finding("R4", OBSERVED, "gap_recorded",
                                   f"{a}={va:.3f} vs {c}={vc:.3f} for `{attr}` (|gap|={gap:.3f}"
                                   + (f" <= delta={delta})." if delta is not None else "; no pre-registered threshold)."),
                                   model=model, attribute=attr, key=f"{a}~{c}", evidence=ev, refs=refs,
                                   action="None required by policy; evidence preserved."))
    return out


# ----------------------------------------------------------------------------
def rule_r5_provenance(b: dict, ctx: dict) -> list[Finding]:
    out: list[Finding] = []
    model = b.get("model")
    V = _get(b, "V")
    open_prefixes = tuple(_profile(ctx).get("open_gate_prefixes", ["PENDING", "BLOCKED"]))
    required = _get(b, "contract.required_provenance")
    if not isinstance(V, dict):
        return [Finding("R5", INCOMPLETE, "missing_provenance", "Provenance section `V` is absent.",
                        model=model, key="V", evidence={"field": "V"},
                        action="Restore provenance or repeat the evaluation with documented inputs.")]
    for f in (required if isinstance(required, list) else []):
        if V.get(f) in (None, ""):
            out.append(Finding("R5", INCOMPLETE, "missing_provenance",
                               f"Provenance field `{f}` is not recorded.",
                               model=model, key=f, evidence={"field": f, "value": None},
                               action="Record the value in the run manifest or repeat the run with it documented."))
    # Declared provenance claims and gates (explicit incompleteness, as in R3).
    pref = [V["record_ref"]] if isinstance(V.get("record_ref"), dict) else []
    for claim, val in sorted((V.get("claims") or {}).items()):
        if val is False:
            out.append(Finding("R5", OBSERVED, "declared_unverified",
                               f"Provenance claim `{claim}` is declared unverified.",
                               model=model, key=f"claim:{claim}", evidence={"claim": claim, "value": False},
                               refs=pref, action="Keep the limitation visible in any report that relies on it."))
    for gate, val in sorted((V.get("gates") or {}).items()):
        if isinstance(val, str) and val.startswith(open_prefixes):
            out.append(Finding("R5", REVIEW, "open_gate",
                               f"Provenance gate `{gate}` is open: {val}.",
                               model=model, key=f"gate:{gate}", evidence={"gate": gate, "status": val},
                               refs=pref, action="Assign an owner to close the gate or accept it as a limitation."))
    arts = V.get("artifacts")
    if not isinstance(arts, dict) or not arts:
        out.append(Finding("R5", INCOMPLETE, "missing_provenance", "Artifact manifest is empty.",
                           model=model, key="artifacts", evidence={"field": "artifacts"},
                           action="Regenerate the bundle with artifact hashes."))
        return out
    root = ctx.get("artifact_root")
    if root is not None:
        for rel, h in sorted(arts.items()):
            p = Path(root) / rel
            if not p.exists():
                out.append(Finding("R5", INCOMPLETE, "artifact_unavailable",
                                   f"Artifact `{rel}` cannot be found.", model=model, key=rel,
                                   evidence={"artifact": rel, "declared_sha256": h},
                                   action="Restore the artifact or regenerate the bundle."))
            elif file_sha256(p) != h:
                out.append(Finding("R5", INCOMPLETE, "hash_mismatch",
                                   f"Artifact `{rel}` differs from the hash recorded in the bundle.",
                                   model=model, key=rel, evidence={"artifact": rel, "declared_sha256": h},
                                   action="Re-export the bundle from the current artifacts or restore the original."))
    return out


rule_r3_explanations = rule_r3_coverage  # backward-compatible name

RULES = {"R1": rule_r1_schema, "R2": rule_r2_support, "R3": rule_r3_coverage,
         "R4": rule_r4_cross_layer, "R5": rule_r5_provenance}
