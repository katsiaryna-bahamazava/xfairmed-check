"""Unit tests on a small hand-written bundle (no dependency on the toolkit repo)."""
import copy

from xfairmed_check.engine import run_checks
from xfairmed_check.ledger import ledger_entry
from xfairmed_check.rules import Finding


def bundle():
    ref = {"artifact": "t.csv"}
    return {
        "bundle_version": "1.0", "cohort": "unit", "model": "m",
        "I": {"dataset_id": "d", "n_samples": 100, "audited_attributes": ["a"]},
        "M": {"model_id": "m", "predictions": {"artifact": "t.csv"}, "metrics": {"acc": 0.9}, "metrics_ref": ref},
        "G": {"support_policy": {"min_total": 35, "min_class": 10},
              "groups": [{"attribute": "a", "group": "g1", "n_IDC": 50, "n_ILC": 40, "total": 90, "ref": ref},
                         {"attribute": "a", "group": "g2", "n_IDC": 8, "n_ILC": 2, "total": 10, "ref": ref}]},
        "P": {"DF": {"value": 0.5, "components": {"RES": .5, "MIS": .5, "FDS": .5, "IBS": .5}, "ref": ref},
              "DF_units": {"a": {"value": 0.5, "ref": ref}},
              "AMF": {"value": 0.9, "components": {"PP": .9, "PR": .9, "RP": .9}, "ref": ref},
              "parity_units": {"a": {"PP": None, "RP": None, "note": "Less than two supported groups available.",
                                     "excluded_groups": ["g2"], "groups_used": ["g1"], "ref": ref}},
              "XCFS": {"value": 0.7, "label": "XCFS_partial", "aggregation": "geometric_mean", "ref": ref}},
        "A": {"declared_scope": "partial",
              "metrics": {"ASS": {"status": "computed", "value": .9, "ref": ref},
                          "ERS": {"status": "computed", "value": .9, "ref": ref},
                          "SAS": {"status": "not_applicable", "justification": "attrs not predictors", "ref": ref},
                          "CSD": {"status": "not_applicable", "justification": "attrs not predictors", "ref": ref}},
              "EXL": {"value": 0.9, "ref": ref}, "ASS_units": {"a": {"value": 0.9, "ref": ref}}},
        "V": {"xfairmed_version": "0.1", "code_commit": "abc", "run_script": "r.py", "random_seed": 1,
              "cv_folds": 5, "dataset_file": "d.csv", "dataset_release": "r1", "dataset_sha256": "x",
              "environment_lock": "uv.lock", "artifacts": {"t.csv": "h"}},
        "contract": {"required_metrics": {"EXL": ["ASS", "ERS", "SAS", "CSD"]},
                     "allow_declared_not_applicable": True,
                     "required_provenance": ["xfairmed_version", "code_commit", "dataset_release"]},
    }


def kinds(res, rule=None, outcome=None):
    return sorted(f["kind"] for f in res["findings"]
                  if (rule is None or f["rule"] == rule) and (outcome is None or f["outcome"] == outcome))


def test_valid_partial_audit_has_no_incomplete():  # S8
    res = run_checks(bundle())
    assert kinds(res, outcome="INCOMPLETE") == []
    assert kinds(res, "R3") == ["declared_limitation", "declared_limitation"]
    assert res["gate"] == "PASS"


def test_r2_low_support_and_amf_gap():  # S3
    res = run_checks(bundle())
    assert kinds(res, "R2", "REVIEW") == ["low_support", "parity_not_computable"]


def test_r3_scope_mismatch():  # S4
    b = bundle()
    b["A"]["declared_scope"] = "complete"
    assert kinds(run_checks(b), "R3", "INCOMPLETE") == ["scope_mismatch", "scope_mismatch"]


def test_r4_no_threshold_no_review():  # S5
    res = run_checks(bundle())
    assert "divergence" not in kinds(res, "R4")


def test_r4_threshold():
    res = run_checks(bundle(), {"r4": {"pairs": [["DF", "EXL_ASS"]], "delta": 0.3}})
    assert kinds(res, "R4", "REVIEW") == ["divergence"]


def test_r2_uncertainty_and_eligibility():
    b = bundle()
    b["P"]["parity_units"]["a"].update({"PP": 0.9, "RP": 0.9})
    b["contract"]["uncertainty"] = {"required": True, "min_attempted": 2000, "min_valid_fraction": 0.95}
    b["U"] = {"records": {"PP|a": {"n_attempted": 2000, "n_valid": 1800, "status": "PROVISIONAL_95PCT_CI"}}}
    b["G"]["groups"][0]["declared_eligible"] = False
    k = kinds(run_checks(b), "R2", "INCOMPLETE")
    assert k == ["eligibility_mismatch", "interval_gate_violation", "uncertainty_missing", "uncertainty_missing"]  # RP and ASS records missing


def test_r5_declared_gates_and_claims():
    b = bundle()
    b["V"]["claims"] = {"barcodes_verified": False, "rows_ok": True}
    b["V"]["gates"] = {"traceability": "PENDING_X", "panel": "PASS"}
    res = run_checks(b)
    assert kinds(res, "R5", "OBSERVED") == ["declared_unverified"]
    assert kinds(res, "R5", "REVIEW") == ["open_gate"]


def test_withheld_predictions_need_justification():
    b = bundle()
    b["M"]["predictions"] = {"withheld": True, "justification": "protected asset"}
    assert kinds(run_checks(b), "R1") == []
    b["M"]["predictions"]["justification"] = ""
    assert kinds(run_checks(b), "R1", "INCOMPLETE") == ["invalid_field"]


def test_r5_missing_and_r1_undocumented_gap():  # S2, S6
    b = bundle()
    b["V"]["dataset_release"] = None
    b["P"]["parity_units"]["a"].pop("note")
    res = run_checks(b)
    assert kinds(res, "R5", "INCOMPLETE") == ["missing_provenance"]
    assert kinds(res, "R1", "INCOMPLETE") == ["undocumented_gap"]


def _ledger(res):
    out = []
    for f in res["findings"]:
        if f["rule"] != "R6" and f["outcome"] != "OBSERVED":
            ff = Finding(f["rule"], f["outcome"], f["kind"], f["message"], model=f["model"])
            ff.finding_id, ff.evidence_fp = f["finding_id"], f["evidence_fp"]
            out.append(ledger_entry(ff, "rev", "accepted_limitation", "test", "2026-11-01T00:00:00Z"))
    return out


def test_r6_dispose_and_stale():  # S7
    b = bundle()
    led = _ledger(run_checks(b))
    assert kinds(run_checks(b, ledger=led), "R6", "REVIEW") == []
    b2 = copy.deepcopy(b)
    b2["G"]["groups"][1]["n_IDC"] += 1
    b2["G"]["groups"][1]["total"] += 1
    assert kinds(run_checks(b2, ledger=led), "R6", "REVIEW") == ["stale"]
    # editing a different row does not reopen the decision (value scope)
    b3 = copy.deepcopy(b)
    b3["G"]["groups"][0]["n_IDC"] += 1
    assert kinds(run_checks(b3, ledger=led), "R6", "REVIEW") == []
    assert kinds(run_checks(b, ledger=led[1:]), "R6", "REVIEW") == ["unresolved"]


def test_deterministic():
    assert run_checks(bundle()) == run_checks(bundle())
