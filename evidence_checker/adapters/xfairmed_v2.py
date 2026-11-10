"""Evidence bundle builder for XFAIR-MED v2 outputs (4 models, 5x5 nested CV).

Reads only aggregate outputs: the frozen subgroup-support manifest, per-attribute
PP/RP, DF components, the XCFS layer table, ASS/ERS summaries, bootstrap
uncertainty records and the cohort provenance record. Patient-level predictions
and attributions are protected assets and are recorded as withheld, with the
toolkit's own justification. No score is recomputed.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from .xfairmed_v1 import declared_scope
from ..ids import file_sha256

S = "studies/tcga_brca_xai_revision"
SRC = {
    "support": f"{S}/reports/xai_full5x5_20261027/frozen_subgroup_support.csv",
    "perf": f"{S}/reports/xai_full5x5_20261027/performance_summary.csv",
    "parity": f"{S}/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv",
    "df_sum": f"{S}/reports/xcfs_real_data_ablation_20261028/layer_reconstruction/original_df_components/data_fairness_layer_summary.csv",
    "df_attr": f"{S}/reports/xcfs_real_data_ablation_20261028/layer_reconstruction/original_df_components/data_fairness_layer_by_attribute.csv",
    "amf": f"{S}/paper_release_20261028/xcfs_ablation_20261028/DF_AMF_REAL_5X5_FOR_ABLATION.csv",
    "xcfs": f"{S}/paper_release_20261028/xcfs_ablation_20261028/FULL_XCFS_LAYER_ABLATION.csv",
    "ass": f"{S}/reports/xai_full5x5_explanations_v1/ASS_summary.csv",
    "intervals": f"{S}/reports/xai_full5x5_bootstrap_EXL_20261027/bootstrap_metric_intervals.csv",
    "ass_cal": f"{S}/reports/xai_uncertainty_integrated_FINAL_v2/ass_calibration_method_decisions.csv",
    "metric_spec": f"{S}/specs/SCIENTIFIC_METRIC_AUDIT_v0.1.0.md",
    "support_spec": f"{S}/specs/SUBGROUP_SUPPORT_AND_UNCERTAINTY_SPEC_v1.0.0.md",
    "provenance": f"{S}/configs/cohort_provenance_v2.0.0.json",
    "env": f"{S}/configs/environment_v2_requirements.txt",
    "protocol": f"{S}/configs/model_protocol_v2.0.0.json",
    "identity": f"{S}/reports/xai_full5x5_explanations_v1/explanation_run_identity.json",
    "manifest": f"{S}/reports/xai_full5x5_explanations_v1/results_manifest.json",
    "status": f"{S}/paper_release_20261028/PAPER_CANDIDATE_STATUS_20261028.json",
    "pyproject": "pyproject.toml",
}
METRIC_KEY = {"PP_balanced_accuracy": "PP", "RP_probability": "RP", "ASS": "ASS", "ERS": "ERS"}


def _f(x: Any) -> float | None:
    if x in (None, ""):
        return None
    try:
        return float(x)
    except ValueError:
        return None


class _R:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.artifacts: dict[str, str] = {}

    def path(self, key: str) -> Path:
        return self.root / SRC[key]

    def touch(self, key: str) -> bool:
        p = self.path(key)
        if p.exists():
            self.artifacts[SRC[key]] = file_sha256(p)
            return True
        return False

    def rows(self, key: str) -> list[dict[str, str]] | None:
        if not self.touch(key):
            return None
        with open(self.path(key), newline="", encoding="utf-8-sig") as fh:
            return list(csv.DictReader(fh))

    def json(self, key: str) -> dict | None:
        if not self.touch(key):
            return None
        return json.loads(self.path(key).read_text(encoding="utf-8-sig"))

    def text(self, key: str) -> str | None:
        if not self.touch(key):
            return None
        return self.path(key).read_text(encoding="utf-8-sig")

    @staticmethod
    def ref(key: str, **row) -> dict[str, Any]:
        r: dict[str, Any] = {"artifact": SRC[key]}
        if row:
            r["row"] = row
        return r


def build_bundle_v2(root: Path, model: str, code_commit: str | None,
                    dataset_id: str = "TCGA-BRCA multi-omics (brca_data_w_subtypes.csv)") -> dict[str, Any]:
    R = _R(root)

    # ---- G / I: frozen support manifest --------------------------------------
    sup = R.rows("support") or []
    groups = [{"attribute": r["audited_attribute"], "group": r["group"],
               "n_IDC": int(r["n_IDC"]), "n_ILC": int(r["n_ILC"]), "total": int(r["n"]),
               "declared_eligible": r.get("primary_eligible") == "True",
               "ref": R.ref("support", audited_attribute=r["audited_attribute"], group=r["group"])}
              for r in sup]
    attrs = list(dict.fromkeys(g["attribute"] for g in groups))
    first = [g for g in groups if g["attribute"] == attrs[0]] if attrs else []
    n_idc, n_ilc = sum(g["n_IDC"] for g in first), sum(g["n_ILC"] for g in first)
    spec = R.text("support_spec") or ""
    m_t = re.search(r"n_g >= (\d+)", spec)
    m_c = re.search(r"n_IDC,g >= (\d+)", spec)
    pol = {"min_total": int(m_t.group(1)) if m_t else None, "min_class": int(m_c.group(1)) if m_c else None,
           "ref": R.ref("support_spec")}
    I = {"dataset_id": dataset_id, "panel": "omics_leakage_safe", "task": "IDC vs ILC",
         "n_samples": n_idc + n_ilc if first else None,
         "class_counts": {"IDC": n_idc, "ILC": n_ilc} if first else None,
         "audited_attributes": attrs or None}
    G = {"support_policy": pol, "groups": groups or None}

    # ---- M ---------------------------------------------------------------------
    status = R.json("status") or {}
    withheld = status.get("protected_assets_excluded") or []
    perf = [r for r in (R.rows("perf") or []) if r["model"] == model]
    M = {"model_id": model,
         "predictions": ({"withheld": True,
                          "justification": "Protected asset excluded from release: " + ", ".join(withheld),
                          "ref": R.ref("status")} if "patient-level predictions" in withheld else None),
         "metrics": ({k: _f(v) for k, v in perf[0].items() if k.endswith("_mean")} if perf else None),
         "metrics_ref": R.ref("perf", model=model) if perf else None}

    # ---- P -----------------------------------------------------------------------
    P: dict[str, Any] = {"DF": None, "DF_units": None, "AMF": None, "parity_units": None, "XCFS": None}
    dfs = R.rows("df_sum")
    if dfs:
        r = dfs[0]
        P["DF"] = {"value": _f(r.get("DF")),
                   "components": {k: _f(r.get(f"{k}_mean")) for k in ("RES", "MIS", "FDS", "IBS")},
                   "ref": R.ref("df_sum")}
    dfa = R.rows("df_attr")
    if dfa:
        P["DF_units"] = {r["audit_unit"]: {"value": _f(r.get("DF_unit")),
                                           "ref": R.ref("df_attr", audit_unit=r["audit_unit"])} for r in dfa}
    amf = [r for r in (R.rows("amf") or []) if r["model"] == model]
    if amf:
        r = amf[0]
        P["AMF"] = {"value": _f(r.get("AMF")),
                    "components": {"PP": _f(r.get("PP_mean_six_supported")),
                                   "PR": _f(r.get("PR_full_fold_shared_1pct_perturbation")),
                                   "RP": _f(r.get("RP_mean_six_supported"))},
                    "n_supported_attributes": int(r["n_supported_attributes"]) if r.get("n_supported_attributes") else None,
                    "ref": R.ref("amf", model=model)}
    par = [r for r in (R.rows("parity") or []) if r["model"] == model]
    if par:
        units: dict[str, dict] = {}
        for r in par:
            a = r["audited_attribute"]
            u = units.setdefault(a, {"PP": None, "RP": None, "note": None,
                                     "groups_used": json.loads(r["frozen_required_groups_json"] or "[]"),
                                     "excluded_groups": [g["group"] for g in groups
                                                         if g["attribute"] == a and not g["declared_eligible"]],
                                     "ref": R.ref("parity", model=model, audited_attribute=a)})
            k = METRIC_KEY.get(r["metric"])
            if r["status"] == "VALID_ALL_REPEATS":
                u[k] = _f(r["mean_across_5_repeats"])
            else:
                u["note"] = (f"{r['status']}; frozen required groups: {r['n_frozen_required_groups']} "
                             f"(pairwise parity needs at least two).")
        P["parity_units"] = units
    xc = [r for r in (R.rows("xcfs") or []) if r["model"] == model]
    label_cols = []
    if xc:
        r = xc[0]
        # The toolkit's specification names this score XCFS_partial (column: XCFS_full_3_layers).
        label = ("XCFS_partial" if "XCFS_partial" in (R.text("metric_spec") or "")
                 else ("XCFS_full_3_layers" if "XCFS_full_3_layers" in r else None))
        label_cols.append(label or "")
        P["XCFS"] = {"value": _f(r.get("XCFS_full_3_layers")), "label": label,
                     "aggregation": "geometric_mean", "ref": R.ref("xcfs", model=model)}

    # ---- A -----------------------------------------------------------------------
    mspec = R.text("metric_spec") or ""
    na_just = ("audited attributes are excluded from the model inputs (leakage-safe cohort)"
               if "SAS and CSD are marked not applicable in the leakage-safe cohort" in mspec else "")
    A: dict[str, Any] = {"metrics": None, "EXL": None, "ASS_units": None}
    if xc:
        r = xc[0]
        A["metrics"] = {
            "ASS": {"status": "computed", "value": _f(r.get("ASS_mean_6_supported")), "ref": R.ref("xcfs", model=model)},
            "ERS": {"status": "computed", "value": _f(r.get("ERS_full1930")), "ref": R.ref("xcfs", model=model)},
            "SAS": {"status": "not_applicable", "justification": na_just, "ref": R.ref("metric_spec")},
            "CSD": {"status": "not_applicable", "justification": na_just, "ref": R.ref("metric_spec")},
        }
        A["EXL"] = {"value": _f(r.get("EXL_original_ASS_ERS")), "label": "EXL_original_ASS_ERS",
                    "ref": R.ref("xcfs", model=model)}
    # Scope is declared by the toolkit's metric specification, which names the compound score
    # XCFS_partial; the ablation column "XCFS_full_3_layers" means "all three layers included".
    if "XCFS_partial" in mspec:
        A["declared_scope"], A["declared_scope_source"] = "partial", "XCFS_partial (" + SRC["metric_spec"].split("/")[-1] + ")"
    else:
        A["declared_scope"], A["declared_scope_source"] = declared_scope([l for l in label_cols if l])
    ass = [r for r in (R.rows("ass") or []) if r["model"] == model]
    if ass:
        A["ASS_units"] = {r["audited_attribute"]: {"value": _f(r.get("ASS_mean_over_repetitions")),
                                                   "status": r.get("status"),
                                                   "ref": R.ref("ass", model=model, audited_attribute=r["audited_attribute"])}
                          for r in ass}

    # ---- U: uncertainty records --------------------------------------------------
    recs: dict[str, dict] = {}
    for r in (R.rows("intervals") or []):
        if r["model"] != model or r["metric"] not in METRIC_KEY:
            continue
        key = f"{METRIC_KEY[r['metric']]}|{r['audited_attribute']}" if r["audited_attribute"] else METRIC_KEY[r["metric"]]
        recs[key] = {"n_attempted": int(r["n_attempted"]), "n_valid": int(r["n_valid"]),
                     "status": r["interval_status"], "ci": [_f(r["ci_lower"]), _f(r["ci_upper"])],
                     "ref": R.ref("intervals", model=model, metric=r["metric"],
                                  audited_attribute=r["audited_attribute"])}
    cal = R.rows("ass_cal") or []
    not_approved = {}
    if cal and all(r["overall_recommendation"].startswith("NOT_APPROVED") for r in cal):
        not_approved["ASS"] = f"all {len(cal)} candidate interval methods failed calibration"
    U = {"records": recs, "not_approved_methods": not_approved, "not_approved_ref": R.ref("ass_cal")}

    # ---- V: provenance --------------------------------------------------------------
    prov = R.json("provenance") or {}
    ident = R.json("identity") or {}
    man = R.json("manifest") or {}
    proto = R.text("protocol") or ""
    R.touch("env")
    pyver = re.search(r'^version\s*=\s*"([^"]+)"', R.text("pyproject") or "", re.M)
    src_docs = prov.get("source_documentation") or []
    pub = next((d for d in src_docs if d.get("type", "").startswith("original")), {})
    dist = next((d for d in src_docs if d.get("type") == "distributor"), {})
    seed = re.search(r'"master_seed":\s*(\d+)', proto)
    V = {
        "xfairmed_version": (f"{pyver.group(1)} / protocol {prov.get('protocol_id')}" if pyver else None),
        "code_commit": code_commit,
        "run_script": ident.get("run_name"),
        "random_seed": int(seed.group(1)) if seed else None,
        "cv_folds": (f"{man.get('repetitions_analyzed')} repeats x {man.get('outer_folds_per_repetition')} outer folds"
                     if man.get("repetitions_analyzed") else None),
        "dataset_file": prov.get("input_file_repo_relative"),
        "dataset_release": (f"doi:{pub.get('doi')} via {dist.get('public_url')}" if pub.get("doi") else None),
        "dataset_sha256": prov.get("input_sha256_from_investigator_windows_get_filehash"),
        "environment_lock": SRC["env"] if (R.root / SRC["env"]).exists() else None,
        "protocol_sha256": ident.get("protocol_sha256_lf"),
        "claims": {k: v for k, v in (prov.get("claims") or {}).items() if isinstance(v, bool)},
        "gates": prov.get("gates") or {},
        "record_ref": R.ref("provenance"),
        # Each recorded provenance value cites the artifact it was read from.
        "refs": {"xfairmed_version": [R.ref("pyproject"), R.ref("provenance")],
                 "run_script": [R.ref("identity")], "protocol_sha256": [R.ref("identity")],
                 "random_seed": [R.ref("protocol")], "cv_folds": [R.ref("manifest")],
                 "dataset_file": [R.ref("provenance")], "dataset_release": [R.ref("provenance")],
                 "dataset_sha256": [R.ref("provenance")], "environment_lock": [R.ref("env")]},
    }
    V["artifacts"] = dict(sorted(R.artifacts.items()))

    contract = {
        "required_metrics": {"DF": ["RES", "MIS", "FDS", "IBS"], "AMF": ["PP", "PR", "RP"],
                             "EXL": ["ASS", "ERS", "SAS", "CSD"]},
        "allow_declared_not_applicable": True,
        "uncertainty": {"required": True, "min_attempted": 2000, "min_valid_fraction": 0.95,
                        "ref": {"artifact": SRC["support_spec"]}},
        "required_provenance": ["xfairmed_version", "code_commit", "run_script", "random_seed",
                                "cv_folds", "dataset_file", "dataset_release", "dataset_sha256",
                                "environment_lock"],
    }
    return {"bundle_version": "2.0", "cohort": "real_v2", "model": model,
            "I": I, "M": M, "G": G, "P": P, "A": A, "U": U, "V": V, "contract": contract}
