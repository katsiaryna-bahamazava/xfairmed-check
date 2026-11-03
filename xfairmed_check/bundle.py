"""Build an evidence bundle E = (I, M, G, P, A, V) from XFAIR-MED result tables.

The builder only *reads* existing XFAIR-MED outputs. It never recomputes a
fairness score. Every value carries a reference (artifact path, sha256, row
selector) so a reviewer can trace it back to the table it came from.
Anything the audit did not record is stored as ``None`` so the checker can
report it, rather than being silently filled in.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from .ids import file_sha256

SUFFIX = "oof_omics_leakage_safe"
# Expansions verified against xfairmed/{data,model,explanation}_fairness.py and modeling.py
METRIC_EXPANSION = {
    "RES": "Representation Evenness Score (Simpson evenness)",
    "MIS": "Max Independence Score (1 - max Cramer's V with target)",
    "FDS": "Feature-Distribution Similarity",
    "IBS": "Intersectional Balance Score",
    "PP": "Performance Parity (1 - subgroup balanced-accuracy gap)",
    "PR": "Perturbation Robustness (global, not subgroup-specific)",
    "RP": "Residual Parity (1 - subgroup error-rate gap)",
    "ASS": "Attribution Similarity Score",
    "ERS": "Explanation Robustness Score",
    "SAS": "Sensitive Attribution Score",
    "CSD": "Counterfactual Sensitive Dependence",
}


def _rows(path: Path) -> list[dict[str, str]]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def _f(x: str | None) -> float | None:
    if x is None or x == "":
        return None
    try:
        return float(x)
    except ValueError:
        return None


class _Reader:
    """Reads tables relative to a results dir and records artifact hashes."""

    def __init__(self, tables_dir: Path, root: Path):
        self.tables_dir = tables_dir
        self.root = root
        self.artifacts: dict[str, str] = {}

    def rel(self, name: str) -> str:
        return str((self.tables_dir / name).relative_to(self.root))

    def read(self, name: str) -> list[dict[str, str]] | None:
        p = self.tables_dir / name
        if not p.exists():
            return None
        self.artifacts[self.rel(name)] = file_sha256(p)
        return _rows(p)

    def ref(self, name: str, **row) -> dict[str, Any]:
        r = {"artifact": self.rel(name)}
        if row:
            r["row"] = row
        return r


def _commit_of(repo_root: Path) -> str | None:
    head = repo_root / ".git" / "HEAD"
    if not head.exists():
        return None
    txt = head.read_text().strip()
    if txt.startswith("ref:"):
        ref = repo_root / ".git" / txt.split(" ", 1)[1]
        if ref.exists():
            return ref.read_text().strip()
        packed = repo_root / ".git" / "packed-refs"
        if packed.exists():
            for line in packed.read_text().splitlines():
                if line.endswith(txt.split(" ", 1)[1]):
                    return line.split(" ")[0]
        return None
    return txt


def _scan_provenance(repo_root: Path) -> dict[str, Any]:
    """Extract only provenance that the repository actually records."""
    prov: dict[str, Any] = {
        "xfairmed_version": None, "code_commit": None, "run_script": None,
        "random_seed": None, "cv_folds": None, "dataset_file": None,
        "dataset_release": None, "dataset_sha256": None, "environment_lock": None,
    }
    pp = repo_root / "pyproject.toml"
    if pp.exists():
        m = re.search(r'^version\s*=\s*"([^"]+)"', pp.read_text(), re.M)
        prov["xfairmed_version"] = m.group(1) if m else None
    prov["code_commit"] = _commit_of(repo_root)
    sdir = repo_root / "studies" / "tcga_brca_model_agnostic_fairness" / "scripts"
    run = sdir / "run_tcga_brca_paper.py"
    if run.exists():
        prov["run_script"] = str(run.relative_to(repo_root))
        src = run.read_text()
        seeds = set(re.findall(r"random_state\s*=\s*(\d+)", src))
        folds = set(re.findall(r"n_splits\s*=\s*(\d+)", src))
        prov["random_seed"] = int(seeds.pop()) if len(seeds) == 1 else None
        prov["cv_folds"] = int(folds.pop()) if len(folds) == 1 else None
    setup = sdir / "tcga_brca_setup.py"
    if setup.exists():
        m = re.search(r'DATA_PATH\s*=\s*Path\("([^"]+)"\)', setup.read_text())
        prov["dataset_file"] = m.group(1) if m else None
    for lock in ("requirements.lock", "poetry.lock", "uv.lock", "environment.yml", "conda-lock.yml"):
        if (repo_root / lock).exists():
            prov["environment_lock"] = lock
    return prov


def _support_policy(repo_root: Path) -> dict[str, Any]:
    setup = repo_root / "studies" / "tcga_brca_model_agnostic_fairness" / "scripts" / "tcga_brca_setup.py"
    pol = {"min_total": None, "min_class": None,
           "source": "studies/tcga_brca_model_agnostic_fairness/scripts/tcga_brca_setup.py::flag_low_support_subgroups"}
    if setup.exists():
        src = setup.read_text()
        a = re.search(r"min_total:\s*int\s*=\s*(\d+)", src)
        b = re.search(r"min_class_count:\s*int\s*=\s*(\d+)", src)
        pol["min_total"] = int(a.group(1)) if a else None
        pol["min_class"] = int(b.group(1)) if b else None
    return pol


def declared_scope(labels: list[str]) -> tuple[str | None, str | None]:
    """'complete' if any label claims full scope, else 'partial' if any says partial."""
    for l in labels:
        if "full" in l.lower():
            return "complete", l
    for l in labels:
        if "partial" in l.lower():
            return "partial", l
    return None, None


def build_bundle(repo_root: Path, tables_dir: Path, model: str, cohort: str,
                 dataset_id: str) -> dict[str, Any]:
    """Assemble one evidence bundle for one model on one cohort."""
    repo_root, tables_dir = Path(repo_root), Path(tables_dir)
    R = _Reader(tables_dir, repo_root)
    mid = model

    # ---- I: input / dataset -------------------------------------------------
    support_rows = R.read("low_support_subgroups.csv") or []
    attrs = list(dict.fromkeys(r["audited_attribute"] for r in support_rows))
    first_attr = attrs[0] if attrs else None
    n_idc = sum(int(r["IDC_count"]) for r in support_rows if r["audited_attribute"] == first_attr)
    n_ilc = sum(int(r["ILC_count"]) for r in support_rows if r["audited_attribute"] == first_attr)
    I = {"dataset_id": dataset_id, "panel": "omics_leakage_safe", "task": "IDC vs ILC",
         "n_samples": n_idc + n_ilc if support_rows else None,
         "class_counts": {"IDC": n_idc, "ILC": n_ilc} if support_rows else None,
         "audited_attributes": attrs or None}

    # ---- M: model + predictions --------------------------------------------
    pred_name = f"oof_predictions_{model}_omics_leakage_safe.csv"
    has_pred = (tables_dir / pred_name).exists()
    if has_pred:
        R.artifacts[R.rel(pred_name)] = file_sha256(tables_dir / pred_name)
    met_name = f"oof_metrics_{model}_omics_leakage_safe.csv"
    met = R.read(met_name)
    metrics = None
    if met:
        metrics = {k: _f(v) for k, v in met[0].items() if k not in ("panel", "model")}
    M = {"model_id": mid,
         "predictions": {"artifact": R.rel(pred_name)} if has_pred else None,
         "metrics": metrics, "metrics_ref": R.ref(met_name) if met else None}

    # ---- G: groups + support -------------------------------------------------
    groups = [{"attribute": r["audited_attribute"], "group": r["group"],
               "n_IDC": int(r["IDC_count"]), "n_ILC": int(r["ILC_count"]),
               "total": int(r["total"]),
               "ref": R.ref("low_support_subgroups.csv", audited_attribute=r["audited_attribute"], group=r["group"])}
              for r in support_rows]
    G = {"support_policy": _support_policy(repo_root), "groups": groups or None}  # v1 declares no eligibility flags

    # ---- P: data + model fairness -----------------------------------------
    P: dict[str, Any] = {"DF": None, "DF_units": None, "AMF": None, "parity_units": None, "XCFS": None}
    dfs = R.read("data_fairness_layer_summary.csv")
    if dfs:
        r = dfs[0]
        P["DF"] = {"value": _f(r.get("DF")), "components": {k: _f(r.get(f"{k}_mean")) for k in ("RES", "MIS", "FDS", "IBS")},
                   "ref": R.ref("data_fairness_layer_summary.csv")}
    dfu = R.read("data_fairness_layer_by_attribute.csv")
    if dfu:
        P["DF_units"] = {r["audit_unit"]: {"value": _f(r.get("DF_unit")),
                                           "ref": R.ref("data_fairness_layer_by_attribute.csv", audit_unit=r["audit_unit"])}
                         for r in dfu}
    amf_name = f"amf_layer_summary_{model}_{SUFFIX}.csv"
    amf = R.read(amf_name)
    if amf:
        r = amf[0]
        P["AMF"] = {"value": _f(r.get("AMF")),
                    "components": {"PP": _f(r.get("PP_mean")), "PR": _f(r.get("PR")), "RP": _f(r.get("RP_mean"))},
                    "use_only_supported_groups": r.get("use_only_supported_groups") == "True",
                    "ref": R.ref(amf_name)}
    amfu_name = f"amf_layer_by_attribute_{model}_{SUFFIX}.csv"
    amfu = R.read(amfu_name)
    if amfu:
        P["parity_units"] = {
            r["audited_attribute"]: {
                "PP": _f(r.get("PP")), "RP": _f(r.get("RP")), "AMF_unit": _f(r.get("AMF_unit")),
                "groups_used": [g for g in (r.get("groups_used") or "").split(";") if g],
                "excluded_groups": [g for g in (r.get("excluded_low_support_groups") or "").split(";") if g],
                "note": r.get("note") or None,
                "ref": R.ref(amfu_name, audited_attribute=r["audited_attribute"])}
            for r in amfu}
    x_name = f"xcfs_partial_{model}_{SUFFIX}.csv"
    x = R.read(x_name)
    if x:
        r = x[0]
        P["XCFS"] = {"value": _f(r.get("XCFS_partial")), "label": r.get("status"),
                     "aggregation": r.get("aggregation"), "ref": R.ref(x_name)}

    # ---- A: explanations ----------------------------------------------------
    # LR files have no "model_agnostic" infix; RF/MLP do.
    infix = "" if model == "logistic_regression" else "model_agnostic_"
    exl_name = f"exl_layer_summary_partial_{model}_{SUFFIX}.csv"
    exl = R.read(exl_name)
    ass_name = f"exl_ass_{infix}{model}_{SUFFIX}.csv"
    ass = R.read(ass_name)
    A: dict[str, Any] = {"declared_scope": None, "metrics": None, "EXL": None, "ASS_units": None}
    if exl:
        r = exl[0]
        metrics_a = {"ASS": {"status": "computed", "value": _f(r.get("ASS_mean")), "ref": R.ref(exl_name)},
                     "ERS": {"status": "computed", "value": _f(r.get("ERS")), "ref": R.ref(exl_name)}}
        for k in ("SAS", "CSD"):
            st = r.get(f"{k}_status", "")
            if st.startswith("not_applicable"):
                metrics_a[k] = {"status": "not_applicable",
                                "justification": st.replace("not_applicable_", "").replace("_", " "),
                                "ref": R.ref(exl_name)}
            elif st:
                metrics_a[k] = {"status": st, "ref": R.ref(exl_name)}
            else:
                metrics_a[k] = {"status": "missing"}
        A["metrics"] = metrics_a
        A["EXL"] = {"value": _f(r.get("EXL_partial_ASS_ERS")), "label": "EXL_partial(ASS,ERS)", "ref": R.ref(exl_name)}
    if ass:
        A["ASS_units"] = {r["audited_attribute"]: {"value": _f(r.get("ASS")),
                                                   "ref": R.ref(ass_name, audited_attribute=r["audited_attribute"])}
                          for r in ass}

    # Declared scope comes from the labels the audit itself attaches to its outputs.
    labels = [l for l in ((P.get("XCFS") or {}).get("label"),) if l]
    if exl:
        labels.append(exl_name)
    A["declared_scope"], A["declared_scope_source"] = declared_scope(labels)

    # ---- V: provenance ------------------------------------------------------
    V = _scan_provenance(repo_root)
    V["artifacts"] = dict(sorted(R.artifacts.items()))

    contract = {
        "required_metrics": {"DF": ["RES", "MIS", "FDS", "IBS"], "AMF": ["PP", "PR", "RP"],
                             "EXL": ["ASS", "ERS", "SAS", "CSD"]},
        "allow_declared_not_applicable": True,
        "uncertainty": {"required": False},
        "required_provenance": ["xfairmed_version", "code_commit", "run_script", "random_seed",
                                "cv_folds", "dataset_file", "dataset_release", "dataset_sha256",
                                "environment_lock"],
    }
    return {"bundle_version": "1.0", "cohort": cohort, "model": mid,
            "I": I, "M": M, "G": G, "P": P, "A": A, "V": V, "contract": contract}


def save(bundle: dict, path: Path) -> None:
    Path(path).write_text(json.dumps(bundle, indent=1, sort_keys=False))
