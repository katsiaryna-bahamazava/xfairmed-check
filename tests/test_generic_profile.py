"""The rules are toolkit-independent: a bundle from a different (invented) audit
toolkit, with other layer names, three outcome classes and its own profile, is
checked without any change to the rules."""
import copy

from evidence_checker.engine import run_checks

REF = {"artifact": "report.csv"}

PROFILE = {
    "name": "two-layer-demo",
    "required_fields": [["P.model_gap.value", "score"], ["P.calibration.value", "score"]],
    "components": [{"layer": "model_gap", "path": "P.model_gap.components"}],
    "unit_tables": [{"name": "gap_by_attribute", "path": "P.gap_by_attribute", "field": "tpr_gap"}],
    "comparison": {"path": "P.gap_by_attribute", "field": "tpr_gap", "label": "TPR gap"},
    "uncertainty_targets": [{"path": "P.gap_by_attribute", "metrics": {"TPR_GAP": "tpr_gap"}}],
    "interval_status_marker": "CI95",
    "metric_sections": [{"layer": "calibration", "label": "calibration", "metrics": "P.calibration.metrics",
                         "scope": "P.calibration.scope"}],
    "layers": {"GAP": {"path": "P.gap_by_attribute", "field": "tpr_gap"},
               "CAL": {"path": "P.cal_by_attribute", "field": "value"}},
    "default_pairs": [["GAP", "CAL"]],
    "open_gate_prefixes": ["TODO"],
}


def bundle():
    return {
        "model": "m", "cohort": "demo",
        "I": {"dataset_id": "d", "n_samples": 300, "audited_attributes": ["sex"]},
        "M": {"model_id": "m", "predictions": {"withheld": True, "justification": "protected"},
              "metrics": {"auc": 0.8}},
        "G": {"support_policy": {"min_total": 30, "min_class": 5},
              "groups": [
                  {"attribute": "sex", "group": "F", "total": 150, "ref": REF,
                   "class_counts": {"low": 60, "mid": 50, "high": 40}},
                  {"attribute": "sex", "group": "M", "total": 150, "ref": REF,
                   "class_counts": {"low": 100, "mid": 47, "high": 3}}]},
        "P": {"model_gap": {"value": 0.9, "components": {"tpr": 0.9, "fpr": 0.95}},
              "calibration": {"value": 0.8, "scope": "partial",
                              "metrics": {"ece": {"status": "computed", "value": 0.8},
                                          "brier_by_group": {"status": "not_applicable",
                                                             "justification": "too few events"}}},
              "gap_by_attribute": {"sex": {"tpr_gap": 0.9, "ref": REF}},
              "cal_by_attribute": {"sex": {"value": 0.5, "ref": REF}}},
        "U": {"records": {"TPR_GAP|sex": {"n_attempted": 1000, "n_valid": 990, "status": "CI95"}}},
        "V": {"code_commit": "abc", "gates": {"external_validation": "TODO: not started"},
              "artifacts": {"report.csv": "0" * 64}},
        "contract": {"required_metrics": {"model_gap": ["tpr", "fpr"], "calibration": ["ece", "brier_by_group"]},
                     "allow_declared_not_applicable": True,
                     "uncertainty": {"required": True, "min_attempted": 1000, "min_valid_fraction": 0.95},
                     "required_provenance": ["code_commit"]},
    }


def kinds(res, rule):
    return sorted((f["outcome"], f["kind"]) for f in res["findings"] if f["rule"] == rule)


def run(b, **pol):
    return run_checks(b, {"profile": PROFILE, **pol})


def test_other_toolkit_passes_with_review_items():
    res = run(bundle())
    assert res["gate"] == "PASS"
    assert kinds(res, "R1") == []
    # third class of group M is below the floor of 5
    low = [f for f in res["findings"] if f["kind"] == "low_support"]
    assert len(low) == 1 and low[0]["subgroup"] == "M"
    assert low[0]["evidence"]["n_high"] == 3
    assert kinds(res, "R3") == [("OBSERVED", "declared_limitation")]
    assert kinds(res, "R5") == [("REVIEW", "open_gate")]
    assert kinds(res, "R4") == [("OBSERVED", "gap_recorded")]


def test_other_toolkit_defects_block():
    b = copy.deepcopy(bundle())
    del b["P"]["calibration"]["value"]                      # required layer score dropped
    del b["P"]["model_gap"]["components"]["fpr"]            # contracted component dropped
    b["P"]["calibration"]["scope"] = "complete"            # overstated scope
    b["U"]["records"]["TPR_GAP|sex"]["n_valid"] = 500      # below the declared gate
    res = run(b)
    assert res["gate"] == "FAIL"
    assert ("INCOMPLETE", "missing_field") in kinds(res, "R1")
    assert ("INCOMPLETE", "invalid_component") in kinds(res, "R1")
    assert ("INCOMPLETE", "scope_mismatch") in kinds(res, "R3")
    assert ("INCOMPLETE", "interval_gate_violation") in kinds(res, "R2")


def test_other_toolkit_cross_layer_threshold():
    res = run(bundle(), r4={"delta": 0.3})
    assert kinds(res, "R4") == [("REVIEW", "divergence")]
