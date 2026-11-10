"""Run every experiment for the paper and write CSV/JSON outputs plus the figure.

Usage:
  python experiments/run_all.py --repo /path/to/xfairmed-toolkit --v2 /path/to/v2-mirror --out results

Subjects
  real_v2           current XFAIR-MED (4 models, 5x5 nested CV); aggregate outputs only
  semi_synthetic    known-answer cohort audited with the earlier pipeline (3 models)
  real_v1           earlier pipeline on the real cohort (3 models); used for the history replay
                    and as a same-pipeline reference for the threshold sweep
Nothing here recomputes a fairness score.
"""
from __future__ import annotations

import argparse
import copy
import csv
import json
import shutil
import statistics
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from evidence_checker.adapters.xfairmed_v1 import build_bundle  # noqa: E402
from evidence_checker.adapters.xfairmed_v2 import build_bundle_v2  # noqa: E402
from evidence_checker.engine import run_checks  # noqa: E402
from evidence_checker.ledger import ledger_entry  # noqa: E402
from evidence_checker.mutate import alert_sigs, generate  # noqa: E402
from evidence_checker.report import to_markdown  # noqa: E402
from evidence_checker.rules import Finding  # noqa: E402

V1_MODELS = ["logistic_regression", "random_forest", "mlp"]
V2_MODELS = ["logistic_regression", "random_forest", "xgboost", "mlp"]
LABEL = {"logistic_regression": "LR", "random_forest": "RF", "xgboost": "XGB", "mlp": "MLP"}
STUDY = Path("studies/tcga_brca_model_agnostic_fairness/results")
POS_CTRL, NEG_CTRL = "audit_CDH1_ECadherin_disruption_status", "audit_method_control_status"
PAIRS = [["DF", "PP"], ["DF", "EXL_ASS"]]
PAIR_NAMES = ["DF~PP", "DF~EXL_ASS"]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def ratio(a, b):
    return None if b == 0 else a / b


# ---------------------------------------------------------------------------
def build_all(repo: Path, v2: Path, out: Path):
    """Return {(cohort, model): (bundle, artifact_root)}."""
    (out / "bundles").mkdir(parents=True, exist_ok=True)
    head = (v2 / "BRANCH_HEAD").read_text().strip()
    B = {}
    for m in V2_MODELS:
        B[("real_v2", m)] = (build_bundle_v2(v2, m, head), v2)
    for m in V1_MODELS:
        B[("semi_synthetic", m)] = (build_bundle(repo, repo / STUDY / "toy_validation/tables", m, "semi_synthetic",
                                                 "TCGA-BRCA-calibrated semi-synthetic v2 (seed 20260729)"), repo)
        B[("real_v1", m)] = (build_bundle(repo, repo / STUDY / "tables", m, "real_v1",
                                          "TCGA-BRCA multi-omics (brca_data_w_subtypes.csv)"), repo)
    for (c, m), (b, _) in B.items():
        (out / "bundles" / f"{c}__{m}.json").write_text(json.dumps(b, indent=1))
    return B


def exp_baseline(B, out):
    rows, counts = [], []
    (out / "reports").mkdir(exist_ok=True)
    for (c, m), (b, root) in B.items():
        res = run_checks(b, artifact_root=root)
        (out / "reports" / f"{c}__{m}.md").write_text(to_markdown(res))
        (out / "reports" / f"{c}__{m}.findings.json").write_text(json.dumps(res, indent=1))
        for f in res["findings"]:
            rows.append({"cohort": c, "model": LABEL[m], "rule": f["rule"], "outcome": f["outcome"],
                         "kind": f["kind"], "attribute": f["attribute"], "subgroup": f["subgroup"],
                         "key": f["key"], "message": f["message"]})
        for r in ("R1", "R2", "R3", "R4", "R5", "R6"):
            k = res["counts"].get(r, {})
            counts.append({"cohort": c, "model": LABEL[m], "rule": r, "INCOMPLETE": k.get("INCOMPLETE", 0),
                           "REVIEW": k.get("REVIEW", 0), "OBSERVED": k.get("OBSERVED", 0), "gate": res["gate"]})
    write_csv(out / "baseline_findings.csv", rows)
    write_csv(out / "baseline_counts.csv", counts)
    return counts


# ---------------------------------------------------------------------------
def exp_mutation(B, out, delta=0.3, cohorts=("real_v2", "semi_synthetic")):
    per, agg, fam, ops = [], defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int)), \
        defaultdict(lambda: defaultdict(int))
    for (c, m), (b, root) in B.items():
        if c not in cohorts:
            continue
        base0 = alert_sigs(run_checks(b, artifact_root=root))
        base4 = alert_sigs(run_checks(b, {"r4": {"pairs": PAIRS, "delta": delta}}, artifact_root=root))
        for mu in generate(b, delta_for_r4=delta):
            got = alert_sigs(run_checks(mu.bundle, mu.policy, artifact_root=root))
            base = base4 if mu.policy else base0
            ep, ea = set(mu.expect_present), set(mu.expect_absent)
            tp, fn, tn, fpa = ep & got, ep - got, ea - got, ea & got
            unexpected = (got - base) - ep - ea
            masked = (base - got) - ea
            for s in tp:
                agg[s[0]]["tp"] += 1
            for s in fn:
                agg[s[0]]["fn"] += 1
            for s in tn:
                agg[s[0]]["tn"] += 1
            for s in fpa | unexpected:
                agg[s[0]]["fp"] += 1
            ok = not fn and not (fpa | unexpected)
            fam[mu.family]["mutants"] += 1
            fam[mu.family]["correct"] += int(ok)
            fam[mu.family]["masked"] += len(masked)
            okey = (mu.target_rule, mu.operator, mu.polarity)
            ops[okey]["n"] += 1
            ops[okey]["correct"] += int(ok)
            ops[okey]["masked"] += len(masked)
            per.append({"mutant": mu.mid, "cohort": c, "model": LABEL[m], "family": mu.family,
                        "operator": mu.operator, "target_rule": mu.target_rule, "polarity": mu.polarity,
                        "tp": len(tp), "fn": len(fn), "tn": len(tn), "fp": len(fpa | unexpected),
                        "masked": len(masked), "correct": ok,
                        "fn_sigs": "|".join(map(str, sorted(fn, key=str))),
                        "fp_sigs": "|".join(map(str, sorted(fpa | unexpected, key=str))),
                        "masked_sigs": "|".join(map(str, sorted(masked, key=str)))})
    write_csv(out / "mutants.csv", per)
    rr = [{"rule": r, "TP": agg[r]["tp"], "FN": agg[r]["fn"], "FP": agg[r]["fp"], "TN": agg[r]["tn"],
           "precision": ratio(agg[r]["tp"], agg[r]["tp"] + agg[r]["fp"]),
           "recall": ratio(agg[r]["tp"], agg[r]["tp"] + agg[r]["fn"]),
           "specificity": ratio(agg[r]["tn"], agg[r]["tn"] + agg[r]["fp"])} for r in ("R1", "R2", "R3", "R4", "R5")]
    write_csv(out / "mutation_by_rule.csv", rr)
    fr = [{"family": k, **v} for k, v in sorted(fam.items())]
    write_csv(out / "mutation_by_family.csv", fr)
    write_csv(out / "mutation_by_operator.csv",
              [{"rule": k[0], "operator": k[1], "polarity": k[2], **v} for k, v in sorted(ops.items())])
    return per, rr, fr


# ---------------------------------------------------------------------------
def exp_delta_sweep(B, out):
    deltas = [round(0.025 * i, 3) for i in range(0, 25)]
    gaps, rows, calib = [], [], []
    for (c, m), (b, _) in B.items():
        res = run_checks(b, {"r4": {"pairs": PAIRS, "delta": None}})
        for f in res["findings"]:
            if f["rule"] == "R4" and f["kind"] == "gap_recorded":
                gaps.append({"cohort": c, "model": LABEL[m], "pair": f["key"], "attribute": f["attribute"],
                             "gap": f["evidence"]["gap"]})
    write_csv(out / "r4_unit_gaps.csv", gaps)
    for d in deltas:
        for (c, m), (b, _) in B.items():
            res = run_checks(b, {"r4": {"pairs": PAIRS, "delta": d}})
            for pair in PAIR_NAMES:
                fs = [f for f in res["findings"] if f["rule"] == "R4" and f["key"] == pair and f["kind"] != "not_comparable"]
                rev = [f for f in fs if f["outcome"] == "REVIEW"]
                rows.append({"delta": d, "cohort": c, "model": LABEL[m], "pair": pair,
                             "comparable_units": len(fs), "review": len(rev),
                             "pos_ctrl_flagged": any(f["attribute"] == POS_CTRL for f in rev),
                             "neg_ctrl_flagged": any(f["attribute"] == NEG_CTRL for f in rev)})
    write_csv(out / "r4_delta_sweep.csv", rows)
    for m in V1_MODELS:
        for pair in PAIR_NAMES:
            ok = [r["delta"] for r in rows if r["cohort"] == "semi_synthetic" and r["model"] == LABEL[m]
                  and r["pair"] == pair and r["pos_ctrl_flagged"] and not r["neg_ctrl_flagged"]]
            g = {x["attribute"]: x["gap"] for x in gaps if x["cohort"] == "semi_synthetic"
                 and x["model"] == LABEL[m] and x["pair"] == pair}
            calib.append({"model": LABEL[m], "pair": pair, "pos_gap": g.get(POS_CTRL), "neg_gap": g.get(NEG_CTRL),
                          "window_lo": min(ok) if ok else None, "window_hi": max(ok) if ok else None})
    write_csv(out / "r4_known_answer_window.csv", calib)
    return rows, calib, gaps


def plot_sweep(rows, calib, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 7, "font.family": "serif"})
    fig, axes = plt.subplots(1, 2, figsize=(3.5, 2.0), sharey=True)
    styles = {"LR": "-", "RF": "--", "XGB": "-.", "MLP": ":"}
    for ax, pair in zip(axes, PAIR_NAMES):
        for coh, color, models in (("real_v2", "black", ["LR", "RF", "XGB", "MLP"]),
                                   ("semi_synthetic", "0.6", ["LR", "RF", "MLP"])):
            for lab in models:
                rs = [r for r in rows if r["cohort"] == coh and r["model"] == lab and r["pair"] == pair]
                if not rs or not rs[0]["comparable_units"]:
                    continue
                tot = rs[0]["comparable_units"]
                ax.plot([r["delta"] for r in rs], [r["review"] / tot for r in rs], styles[lab], color=color,
                        lw=0.9, label=f"{lab} ({'real' if coh == 'real_v2' else 'synth.'})")
        lo = [c["window_lo"] for c in calib if c["pair"] == pair and c["window_lo"] is not None]
        hi = [c["window_hi"] for c in calib if c["pair"] == pair and c["window_hi"] is not None]
        if lo and hi and len(lo) == 3 and len(hi) == 3 and max(lo) <= min(hi):
            if max(lo) < min(hi):
                ax.axvspan(max(lo), min(hi), color="0.85", lw=0, zorder=0)
            else:
                ax.axvline(max(lo), color="0.6", lw=2.5, zorder=0)
        ax.set_title("DF vs PP" if pair == "DF~PP" else "DF vs ASS", fontsize=7)
        ax.set_xlabel(r"threshold $\delta$")
        ax.set_xlim(0, 0.6)
        ax.grid(alpha=0.25, lw=0.4)
    axes[0].set_ylabel("share of units\nflagged REVIEW")
    h, l = axes[0].get_legend_handles_labels()
    fig.tight_layout(pad=0.3, w_pad=0.8)
    fig.subplots_adjust(bottom=0.38)
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=5.3, frameon=False, bbox_to_anchor=(0.55, -0.02))
    fig.savefig(out / "fig_delta_sweep.pdf", bbox_inches="tight")
    fig.savefig(out / "fig_delta_sweep.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
def _dispose_all(result: dict) -> list[dict]:
    led = []
    for f in result["findings"]:
        if f["rule"] != "R6" and f["outcome"] in ("REVIEW", "INCOMPLETE"):
            ff = Finding(f["rule"], f["outcome"], f["kind"], f["message"], model=f["model"])
            ff.finding_id, ff.evidence_fp = f["finding_id"], f["evidence_fp"]
            led.append(ledger_entry(ff, "replay-reviewer (synthetic)", "accepted_limitation",
                                    "Synthetic disposition used to exercise R6; not a real review decision.",
                                    "2026-11-01T00:00:00Z"))
    return led


def _r6(res):
    c = defaultdict(int)
    for f in res["findings"]:
        if f["rule"] == "R6":
            c[f["kind"]] += 1
    return c


def exp_r6_controlled(B, out):
    rows = []
    for (c, m), (b, _) in B.items():
        if c != "real_v2":
            continue
        for scope in ("value", "artifact"):
            pol = {"r6": {"fp_scope": scope}}
            led = _dispose_all(run_checks(b, pol))
            n = len(led)
            k = _r6(run_checks(b, pol, led))
            rows.append({"model": LABEL[m], "scope": scope, "scenario": "identity", "actionable": n,
                         "mutants": 1, "correct_mutants": int(k["unresolved"] == 0 and k["stale"] == 0)})
            ok = sum(int(_r6(run_checks(b, pol, led[:i] + led[i + 1:]))["unresolved"] == 1) for i in range(n))
            rows.append({"model": LABEL[m], "scope": scope, "scenario": "drop_each_disposition",
                         "actionable": n, "mutants": n, "correct_mutants": ok})
            groups = b["G"]["groups"]
            mc = b["G"]["support_policy"]["min_class"]
            low = [i for i, g in enumerate(groups) if min(g["n_IDC"], g["n_ILC"]) < mc]
            for scen, idxs, expect in (("edit_one_low_support_row", low, 1),
                                       ("edit_unrelated_row_same_table",
                                        [i for i in range(len(groups)) if i not in low], 0)):
                okc, over = 0, []
                for i in idxs:
                    bb = copy.deepcopy(b)
                    g = bb["G"]["groups"][i]
                    key = ("n_IDC" if g["n_IDC"] > g["n_ILC"] else "n_ILC") if expect else "n_IDC"
                    g[key] += 1
                    g["total"] += 1
                    rel = g["ref"]["artifact"]
                    bb["V"]["artifacts"][rel] = "edited-" + bb["V"]["artifacts"][rel][:20]
                    st = _r6(run_checks(bb, pol, led))["stale"]
                    okc += int(st == expect)
                    over.append(st - expect)
                rows.append({"model": LABEL[m], "scope": scope, "scenario": scen, "actionable": n,
                             "mutants": len(idxs), "correct_mutants": okc,
                             "mean_unnecessary_reopenings": statistics.mean(over) if over else 0})
    write_csv(out / "r6_controlled.csv", rows)
    return rows


def exp_r6_history(repo: Path, v2: Path, out: Path, scratch: Path):
    """Replay R6 over every commit that changed v1 result tables, then the v1 -> v2 transition."""
    log = subprocess.run(["git", "-C", str(repo), "log", "--reverse", "--format=%h|%cs|%s", "main", "--",
                          str(STUDY / "tables")], capture_output=True, text=True, check=True).stdout.strip()
    commits = [ln.split("|", 2) for ln in log.splitlines()]
    root = scratch / "history"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    states = []
    for h, date, subj in commits:
        wt = root / h
        wt.mkdir()
        paths = [p for p in ("pyproject.toml", str(STUDY / "tables"), "studies/tcga_brca_model_agnostic_fairness/scripts")
                 if subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{h}:{p}"], capture_output=True).returncode == 0]
        arch = subprocess.run(["git", "-C", str(repo), "archive", h, *paths], capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(wt)], input=arch.stdout, check=True)
        bs = {}
        for m in V1_MODELS:
            if (wt / STUDY / "tables" / f"amf_layer_summary_{m}_oof_omics_leakage_safe.csv").exists():
                b = build_bundle(wt, wt / STUDY / "tables", m, "real", "TCGA-BRCA multi-omics (brca_data_w_subtypes.csv)")
                b["V"]["code_commit"] = h
                bs[m] = b
        states.append((h, date, subj, "v1", bs))
    head = (v2 / "BRANCH_HEAD").read_text().strip()
    states.append((head[:7], "2026-10-28", "Toolkit v2: tuned 4-model 5x5 nested CV", "v2",
                   {m: build_bundle_v2(v2, m, head) for m in V2_MODELS}))
    rows = []
    for (h0, _, _, _, b0), (h1, d1, s1, ver, b1) in zip(states, states[1:]):
        for m, b in b1.items():
            if m not in b0:
                continue
            for scope in ("value", "artifact"):
                pol = {"r6": {"fp_scope": scope}}
                led = _dispose_all(run_checks(b0[m], pol))
                k = _r6(run_checks(b, pol, led))
                rows.append({"commit": h1, "date": d1, "subject": s1, "version": ver, "model": LABEL[m],
                             "scope": scope, "prior_decisions": len(led), "carried_over": k["disposed"],
                             "reopened_stale": k["stale"], "new_unresolved": k["unresolved"], "orphaned": k["orphaned"]})
    write_csv(out / "r6_history.csv", rows)
    return rows


# ---------------------------------------------------------------------------
RUBRIC_PRESENT = {  # fields supplied by conditions A and B (see experiments/rubric.json)
    "A": {},
    "B": {"low_support": {"f1", "f2", "f3"}, "parity_not_computable": {"f1", "f2", "f3"},
          "exl_scope": {"f2", "f3"}, "provenance": {"f2", "f3"}, "uncertainty": {"f2", "f3"}},
}
APPLICABLE = {"low_support": ["f1", "f2", "f3", "f4", "f5", "f6"],
              "parity_not_computable": ["f1", "f2", "f3", "f4", "f5", "f6"],
              "exl_scope": ["f2", "f3", "f4", "f5", "f6"], "provenance": ["f2", "f3", "f4", "f5", "f6"],
              "uncertainty": ["f2", "f3", "f4", "f5", "f6"]}


def _item_kind(f):
    if f["rule"] == "R2" and f["kind"] in ("low_support", "parity_not_computable"):
        return f["kind"]
    if f["rule"] == "R2" and f["kind"] == "interval_not_approved":
        return "uncertainty"
    if f["rule"] == "R3" and f["kind"] in ("declared_limitation", "scope_mismatch"):
        return "exl_scope"
    if f["rule"] == "R5" and f["kind"] in ("missing_provenance", "open_gate", "declared_unverified"):
        return "provenance"
    return None


def exp_coverage(B, out):
    rows = []
    for (c, m), (b, root) in B.items():
        if c != "real_v2":
            continue
        res = run_checks(b, artifact_root=root)
        declared = set(b["V"]["artifacts"])
        t = {x: [0, 0] for x in "ABC"}
        n_items = defaultdict(int)
        for f in res["findings"]:
            k = _item_kind(f)
            if not k:
                continue
            n_items[k] += 1
            app = APPLICABLE[k]
            for cond in "AB":
                have = RUBRIC_PRESENT[cond].get(k, set())
                t[cond][0] += sum(1 for x in app if x in have)
                t[cond][1] += len(app)
            refs_ok = all(r.get("artifact") in declared for r in f["refs"])
            pres = {"f1": bool(f["attribute"]), "f2": bool(f["refs"]) and refs_ok, "f3": bool(f["message"]),
                    "f4": bool(f["role"]), "f5": bool(f["action"]),
                    "f6": bool(res["snapshot_id"] and f["finding_id"] and f["evidence_fp"])}
            t["C"][0] += sum(1 for x in app if pres[x])
            t["C"][1] += len(app)
        row = {"model": LABEL[m], "items": sum(n_items.values()), **{f"n_{k}": v for k, v in n_items.items()}}
        for cond in "ABC":
            row[f"T_{cond}"], row[f"valid_{cond}"], row[f"applicable_{cond}"] = ratio(*t[cond]), *t[cond]
        rows.append(row)
    write_csv(out / "coverage_abc.csv", rows)
    return rows


def exp_floor_sensitivity(B, out):
    b = B[("real_v2", "logistic_regression")][0]
    groups, attrs = b["G"]["groups"], b["I"]["audited_attributes"]
    mt = b["G"]["support_policy"]["min_total"]
    rows = []
    for mc in (5, 10, 15, 20, 30):
        flagged = [g for g in groups if g["total"] < mt or min(g["n_IDC"], g["n_ILC"]) < mc]
        no_cov = [a for a in attrs if sum(1 for g in groups if g["attribute"] == a and g not in flagged) < 2]
        rows.append({"min_class": mc, "min_total": mt, "under_supported": len(flagged), "attributes_without_parity": len(no_cov)})
    write_csv(out / "support_floor_sensitivity.csv", rows)
    return rows


def exp_timing(B, out, reps=30):
    rows = []
    for (c, m), (b, root) in B.items():
        if c != "real_v2":
            continue
        p = out / "bundles" / f"{c}__{m}.json"
        tb, tc = [], []
        for _ in range(reps):
            t0 = time.perf_counter()
            json.loads(p.read_text())
            tb.append(time.perf_counter() - t0)
            t0 = time.perf_counter()
            r = run_checks(json.loads(p.read_text()), artifact_root=root)
            to_markdown(r)
            tc.append(time.perf_counter() - t0)
        same = json.dumps(run_checks(b, artifact_root=root), sort_keys=True) == \
            json.dumps(run_checks(json.loads(p.read_text()), artifact_root=root), sort_keys=True)
        rows.append({"model": LABEL[m], "bundle_bytes": p.stat().st_size, "artifacts": len(b["V"]["artifacts"]),
                     "t_B_ms_median": 1000 * statistics.median(tb), "t_C_ms_median": 1000 * statistics.median(tc),
                     "delta_t_ms_median": 1000 * (statistics.median(tc) - statistics.median(tb)),
                     "t_C_ms_p95": 1000 * sorted(tc)[int(0.95 * reps) - 1], "identical_output": same})
    write_csv(out / "timing.csv", rows)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--v2", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=HERE.parent / "results")
    ap.add_argument("--scratch", type=Path, default=Path("/tmp/evidence_checker_scratch"))
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    B = build_all(a.repo, a.v2, a.out)
    s = {"baseline": exp_baseline(B, a.out)}
    _, s["mutation_by_rule"], s["mutation_by_family"] = exp_mutation(B, a.out)
    sweep, s["r4_window"], _ = exp_delta_sweep(B, a.out)
    plot_sweep(sweep, s["r4_window"], a.out)
    s["r6_controlled"] = exp_r6_controlled(B, a.out)
    s["r6_history"] = exp_r6_history(a.repo, a.v2, a.out, a.scratch)
    s["coverage"] = exp_coverage(B, a.out)
    s["floor"] = exp_floor_sensitivity(B, a.out)
    s["timing"] = exp_timing(B, a.out)
    (a.out / "summary.json").write_text(json.dumps(s, indent=1, default=str))
    print("done")


if __name__ == "__main__":
    main()
