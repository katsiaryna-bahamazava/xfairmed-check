"""Mutation testing of audit evidence.

Each operator copies a real evidence bundle, applies one controlled defect (or
one controlled *repair*), and states its oracle from the operator semantics
only:

  expect_present  alerts that must appear   (positive mutants -> TP / FN)
  expect_absent   alerts that must not occur (negative mutants -> TN / FP)

Any alert that is new relative to the unmutated baseline and not listed in
expect_present counts as a false positive. Alerts that disappear without being
listed in expect_absent are counted separately as "masked" (a downstream rule
can no longer evaluate because its input was removed).

Only audit artifacts are mutated, never patient-level data.
An alert is a REVIEW or INCOMPLETE finding of R1-R5. R6 is evaluated separately.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator

from .rules import R1_REQUIRED

Sig = tuple  # (rule, outcome, kind, attribute, subgroup, key)


def sig(rule, outcome, kind, attribute=None, subgroup=None, key=""):
    return (rule, outcome, kind, attribute, subgroup, key)


def alert_sigs(result: dict) -> set[Sig]:
    return {sig(f["rule"], f["outcome"], f["kind"], f.get("attribute"), f.get("subgroup"), f.get("key", ""))
            for f in result["findings"]
            if f["rule"] in ("R1", "R2", "R3", "R4", "R5") and f["outcome"] in ("REVIEW", "INCOMPLETE")}


@dataclass
class Mutant:
    mid: str
    family: str          # S-family from the scenario table
    operator: str
    target_rule: str
    bundle: dict
    expect_present: list = field(default_factory=list)
    expect_absent: list = field(default_factory=list)
    policy: dict | None = None
    polarity: str = "positive"  # positive: must raise an alert; negative: must not


def _set(d: dict, path: str, value: Any) -> None:
    ks = path.split(".")
    for k in ks[:-1]:
        d = d[k]
    d[ks[-1]] = value


def _del(d: dict, path: str) -> None:
    ks = path.split(".")
    for k in ks[:-1]:
        d = d[k]
    del d[ks[-1]]


def _has(d: dict, path: str) -> bool:
    for k in path.split("."):
        if not isinstance(d, dict) or k not in d:
            return False
        d = d[k]
    return True


SCORE_PATHS = [p for p, _ in R1_REQUIRED if p.endswith(".value")]
BAD_SCORES = [("above_one", 1.7), ("negative", -0.2), ("nan", float("nan")), ("string", "high")]


def generate(base: dict, delta_for_r4: float = 0.3) -> Iterator[Mutant]:
    model = base["model"]
    tag = f"{base['cohort']}/{model}"
    n = 0

    def mk(**kw) -> Mutant:
        nonlocal n
        n += 1
        return Mutant(mid=f"{tag}#{n:04d}", **kw)

    # S1/S8 identity: no new alert.
    yield mk(family="S1/S8", operator="identity", target_rule="-", bundle=copy.deepcopy(base),
             polarity="negative")

    # ---- R1: required fields (S2) ------------------------------------------
    for path, _ in R1_REQUIRED:
        if not _has(base, path):
            continue
        b = copy.deepcopy(base)
        _del(b, path)
        yield mk(family="S2", operator="drop_required_field", target_rule="R1", bundle=b,
                 expect_present=[sig("R1", "INCOMPLETE", "missing_field", key=path)])
    for path in SCORE_PATHS:
        if not _has(base, path):
            continue
        for name, val in BAD_SCORES:
            b = copy.deepcopy(base)
            _set(b, path, val)
            yield mk(family="S2", operator=f"invalid_score:{name}", target_rule="R1", bundle=b,
                     expect_present=[sig("R1", "INCOMPLETE", "invalid_field", key=path)])
    pred = base["M"].get("predictions") or {}
    if pred.get("withheld"):
        b = copy.deepcopy(base)
        b["M"]["predictions"]["justification"] = ""
        yield mk(family="S2", operator="unjustified_withholding", target_rule="R1", bundle=b,
                 expect_present=[sig("R1", "INCOMPLETE", "invalid_field", key="M.predictions")])
    for comp_path, names in (("P.DF.components", ("RES", "MIS", "FDS", "IBS")),
                             ("P.AMF.components", ("PP", "PR", "RP"))):
        for nm in names:
            b = copy.deepcopy(base)
            del b["P"][comp_path.split(".")[1]]["components"][nm]
            yield mk(family="S2", operator="drop_contract_metric", target_rule="R1", bundle=b,
                     expect_present=[sig("R1", "INCOMPLETE", "invalid_component", key=f"{comp_path}.{nm}")])
    for layer, fld in (("DF_units", "value"), ("parity_units", "PP")):
        for attr, u in (base["P"].get(layer) or {}).items():
            b = copy.deepcopy(base)
            b["P"][layer][attr][fld] = None
            b["P"][layer][attr].pop("note", None)
            yield mk(family="S2", operator="undocumented_unit_gap", target_rule="R1", bundle=b,
                     expect_present=[sig("R1", "INCOMPLETE", "undocumented_gap", attribute=attr, key=layer)])
    for rel in sorted(base["V"]["artifacts"]):
        b = copy.deepcopy(base)
        del b["V"]["artifacts"][rel]
        yield mk(family="S2", operator="undeclared_artifact", target_rule="R1", bundle=b,
                 expect_present=[sig("R1", "INCOMPLETE", "dangling_ref", key=rel)])

    # ---- R2: support, eligibility, uncertainty (S3) -------------------------
    pol = base["G"]["support_policy"]
    mt, mc = pol["min_total"], pol["min_class"]
    for i, g in enumerate(base["G"]["groups"]):
        minority_key = "n_IDC" if g["n_IDC"] <= g["n_ILC"] else "n_ILC"
        flagged = g["total"] < mt or min(g["n_IDC"], g["n_ILC"]) < mc
        s = sig("R2", "REVIEW", "low_support", attribute=g["attribute"], subgroup=g["group"], key="support")
        has_decl = g.get("declared_eligible") is not None
        mism = sig("R2", "INCOMPLETE", "eligibility_mismatch", attribute=g["attribute"], subgroup=g["group"],
                   key="eligibility")
        # Count changes that cross the policy also contradict a declared eligibility flag.
        cross = [mism] if has_decl else []
        if not flagged:
            b = copy.deepcopy(base)
            gg = b["G"]["groups"][i]
            gg["total"] -= gg[minority_key] - (mc - 1)
            gg[minority_key] = mc - 1
            yield mk(family="S3", operator="inject_low_class_support", target_rule="R2", bundle=b,
                     expect_present=[s] + cross)
            b = copy.deepcopy(base)
            gg = b["G"]["groups"][i]
            if gg[minority_key] >= mc:
                gg["total"] -= gg[minority_key] - mc
                gg[minority_key] = mc
                if gg["total"] >= mt:
                    yield mk(family="S3", operator="boundary_class_support_ok", target_rule="R2", bundle=b,
                             expect_absent=[s] + ([mism] if has_decl else []), polarity="negative")
            b = copy.deepcopy(base)
            gg = b["G"]["groups"][i]
            other = "n_ILC" if minority_key == "n_IDC" else "n_IDC"
            if gg[minority_key] < mt - 1:
                gg[other] = mt - 1 - gg[minority_key]
                gg["total"] = mt - 1
                yield mk(family="S3", operator="inject_low_total_support", target_rule="R2", bundle=b,
                         expect_present=[s] + cross)
        else:
            b = copy.deepcopy(base)
            gg = b["G"]["groups"][i]
            gg[minority_key] = max(gg[minority_key], mc)
            gg["total"] = max(gg["n_IDC"] + gg["n_ILC"], mt)
            yield mk(family="S3", operator="repair_support", target_rule="R2", bundle=b,
                     expect_absent=[s], expect_present=cross, polarity="positive" if cross else "negative")
        if has_decl:
            b = copy.deepcopy(base)
            b["G"]["groups"][i]["declared_eligible"] = not g["declared_eligible"]
            yield mk(family="S3", operator="flip_declared_eligibility", target_rule="R2", bundle=b,
                     expect_present=[mism])
    U = base.get("U") or {}
    req = (base.get("contract") or {}).get("uncertainty") or {}
    if req.get("required"):
        for key, r in sorted((U.get("records") or {}).items()):
            if "|" not in key:
                continue
            metric, attr = key.split("|", 1)
            defined = (metric in ("PP", "RP") and ((base["P"]["parity_units"] or {}).get(attr) or {}).get(metric) is not None) \
                or (metric == "ASS" and ((base["A"].get("ASS_units") or {}).get(attr) or {}).get("value") is not None)
            if not defined:
                continue
            b = copy.deepcopy(base)
            del b["U"]["records"][key]
            yield mk(family="S3", operator="drop_uncertainty_record", target_rule="R2", bundle=b,
                     expect_present=[sig("R2", "INCOMPLETE", "uncertainty_missing", attribute=attr, key=f"U:{metric}")])
            if "95PCT_CI" in (r.get("status") or ""):
                b = copy.deepcopy(base)
                b["U"]["records"][key]["n_valid"] = int(req.get("min_valid_fraction", 0.95) * r["n_attempted"]) - 1
                yield mk(family="S3", operator="interval_below_gate", target_rule="R2", bundle=b,
                         expect_present=[sig("R2", "INCOMPLETE", "interval_gate_violation", attribute=attr, key=f"U:{metric}")])
                b = copy.deepcopy(base)
                b["U"]["records"][key]["n_valid"] = int(req.get("min_valid_fraction", 0.95) * r["n_attempted"])
                yield mk(family="S3", operator="interval_at_gate", target_rule="R2", bundle=b,
                         expect_absent=[sig("R2", "INCOMPLETE", "interval_gate_violation", attribute=attr, key=f"U:{metric}")],
                         polarity="negative")

    # ---- R3: explanation coverage (S4, S8) ----------------------------------
    metrics = base["A"]["metrics"] or {}
    na = [m for m, e in metrics.items() if e.get("status") == "not_applicable"]
    mismatch = [sig("R3", "INCOMPLETE", "scope_mismatch", key=m) for m in na]
    if na and base["A"].get("declared_scope") == "partial":
        b = copy.deepcopy(base)
        b["A"]["declared_scope"] = "complete"
        yield mk(family="S4", operator="misdeclare_exl_complete", target_rule="R3", bundle=b,
                 expect_present=mismatch)
    if na and base["A"].get("declared_scope") == "complete":
        b = copy.deepcopy(base)
        b["A"]["declared_scope"] = "partial"
        b["A"]["declared_scope_source"] = "XCFS_partial"
        yield mk(family="S4", operator="relabel_scope_partial", target_rule="R3", bundle=b,
                 expect_absent=mismatch, polarity="negative")
    for m in na:
        b = copy.deepcopy(base)
        b["A"]["metrics"][m]["justification"] = ""
        yield mk(family="S4", operator="remove_na_justification", target_rule="R3", bundle=b,
                 expect_present=[sig("R3", "INCOMPLETE", "unjustified_na", key=m)],
                 expect_absent=[sig("R3", "INCOMPLETE", "scope_mismatch", key=m)])
    if na:
        b = copy.deepcopy(base)
        b["contract"]["allow_declared_not_applicable"] = False
        yield mk(family="S4", operator="contract_forbids_na", target_rule="R3", bundle=b,
                 expect_present=[sig("R3", "INCOMPLETE", "unjustified_na", key=x) for x in na],
                 expect_absent=mismatch)
    for m in metrics:
        b = copy.deepcopy(base)
        del b["A"]["metrics"][m]
        yield mk(family="S4", operator="drop_exl_metric", target_rule="R3", bundle=b,
                 expect_present=[sig("R3", "INCOMPLETE", "missing_metric", key=m)],
                 expect_absent=[sig("R3", "INCOMPLETE", "scope_mismatch", key=m)])
        b = copy.deepcopy(base)
        b["A"]["metrics"][m]["status"] = "todo"
        yield mk(family="S4", operator="unknown_exl_status", target_rule="R3", bundle=b,
                 expect_present=[sig("R3", "INCOMPLETE", "unknown_status", key=m)],
                 expect_absent=[sig("R3", "INCOMPLETE", "scope_mismatch", key=m)])
    for m, e in metrics.items():
        if e.get("status") == "computed":
            b = copy.deepcopy(base)
            b["A"]["metrics"][m]["value"] = None
            yield mk(family="S4", operator="computed_without_value", target_rule="R3", bundle=b,
                     expect_present=[sig("R3", "INCOMPLETE", "invalid_metric", key=m)])

    # ---- R4: pre-registered divergence policy, boundary mutants (S5) --------
    r4pol = {"r4": {"pairs": [["DF", "PP"], ["DF", "EXL_ASS"]], "delta": delta_for_r4}}

    def other_value(b, comp, attr):
        if comp == "PP":
            return ((b["P"].get("parity_units") or {}).get(attr) or {}).get("PP")
        return ((b["A"].get("ASS_units") or {}).get(attr) or {}).get("value")

    for c in ("PP", "EXL_ASS"):
        units = base["P"].get("parity_units") if c == "PP" else base["A"].get("ASS_units")
        for attr in sorted(units or {}):
            vc = other_value(base, c, attr)
            if vc is None or (base["P"].get("DF_units") or {}).get(attr) is None:
                continue
            s = sig("R4", "REVIEW", "divergence", attribute=attr, key=f"DF~{c}")
            oc = "EXL_ASS" if c == "PP" else "PP"
            for eps, pol_ in ((+0.01, "positive"), (-0.01, "negative")):
                gap = delta_for_r4 + eps
                new_df = vc - gap if vc - gap >= 0 else vc + gap
                if not 0 <= new_df <= 1:
                    continue
                b = copy.deepcopy(base)
                b["P"]["DF_units"][attr]["value"] = new_df
                ov = other_value(b, oc, attr)
                osig = sig("R4", "REVIEW", "divergence", attribute=attr, key=f"DF~{oc}")
                oexp = [] if ov is None else ([osig] if abs(new_df - ov) > delta_for_r4 else [])
                oabs = [] if ov is None else ([] if abs(new_df - ov) > delta_for_r4 else [osig])
                if pol_ == "positive":
                    yield mk(family="S5", operator="r4_gap_above_delta", target_rule="R4", bundle=b,
                             policy=r4pol, expect_present=[s] + oexp, expect_absent=oabs)
                else:
                    yield mk(family="S5", operator="r4_gap_below_delta", target_rule="R4", bundle=b,
                             policy=r4pol, expect_present=oexp, expect_absent=[s] + oabs, polarity="negative")

    # ---- R5: provenance (S6) -------------------------------------------------
    for f in base["contract"]["required_provenance"]:
        if base["V"].get(f) not in (None, ""):
            b = copy.deepcopy(base)
            b["V"][f] = None
            yield mk(family="S6", operator="drop_provenance_field", target_rule="R5", bundle=b,
                     expect_present=[sig("R5", "INCOMPLETE", "missing_provenance", key=f)])
        else:
            b = copy.deepcopy(base)
            b["V"][f] = "recorded-for-test"
            yield mk(family="S6", operator="supply_provenance_field", target_rule="R5", bundle=b,
                     expect_absent=[sig("R5", "INCOMPLETE", "missing_provenance", key=f)], polarity="negative")
    for gate, val in sorted((base["V"].get("gates") or {}).items()):
        gs = sig("R5", "REVIEW", "open_gate", key=f"gate:{gate}")
        b = copy.deepcopy(base)
        if isinstance(val, str) and val.startswith(("PENDING", "BLOCKED")):
            b["V"]["gates"][gate] = "PASS_CLOSED_FOR_TEST"
            yield mk(family="S6", operator="close_open_gate", target_rule="R5", bundle=b,
                     expect_absent=[gs], polarity="negative")
        else:
            b["V"]["gates"][gate] = "PENDING_REOPENED_FOR_TEST"
            yield mk(family="S6", operator="reopen_gate", target_rule="R5", bundle=b, expect_present=[gs])
    for rel in sorted(base["V"]["artifacts"]):
        b = copy.deepcopy(base)
        b["V"]["artifacts"][rel] = "0" * 64
        yield mk(family="S6", operator="corrupt_artifact_hash", target_rule="R5", bundle=b,
                 expect_present=[sig("R5", "INCOMPLETE", "hash_mismatch", key=rel)])


def score(baseline: set[Sig], mutant_alerts: set[Sig], m: Mutant) -> dict[str, Any]:
    exp_p, exp_a = set(m.expect_present), set(m.expect_absent)
    tp = exp_p & mutant_alerts
    fn = exp_p - mutant_alerts
    fp_absent = exp_a & mutant_alerts
    tn = exp_a - mutant_alerts
    new = mutant_alerts - baseline
    unexpected = new - exp_p - exp_a
    masked = (baseline - mutant_alerts) - exp_a
    return {"tp": len(tp), "fn": len(fn), "fp": len(fp_absent) + len(unexpected), "tn": len(tn),
            "masked": len(masked),
            "fn_sigs": sorted(map(str, fn)), "fp_sigs": sorted(map(str, fp_absent | unexpected)),
            "masked_sigs": sorted(map(str, masked)),
            "killed": len(fn) == 0 and len(fp_absent | unexpected) == 0}
