# XFAIR-MED Check

Reproducibility artifacts for a software-engineering study of **evidence-to-review checks** over the outputs of the [XFAIR-MED toolkit](https://github.com/katsiaryna-bahamazava/xfairmed-toolkit).

The checker reads existing aggregate fairness-audit outputs, without recomputing fairness metrics. It produces three kinds of findings: `OBSERVED`, `REVIEW`, and `INCOMPLETE`. The CI-style gate fails only for defined **evidence defects**, not because a fairness score crosses an arbitrary threshold. Human decisions are maintained separately in a review ledger. A passing gate is **not** a fairness certification or clinical-deployment authorization.

## Repository contents

- `xfairmed_check/`: standalone Python checker, evidence bundle builders, six checking rules, fingerprints/review ledger, mutation operators and CLI.
- `tests/`: deterministic checker unit tests.
- `experiments/run_all.py`: research reproduction driver; `experiments/rubric.json`: the information-coverage rubric.
- `results/bundles/`: frozen aggregate evidence bundles for real and semi-synthetic cases.
- `results/reports/`: machine-readable findings and human-readable reports for each bundle.
- `results/`: mutation results, threshold sweeps, support-floor sensitivity, comparison data, history replay, figures and timing summaries.
- `results_before_fix/`: earlier mutation-test results, retained to document bugs uncovered before the repairs.
- `walkthrough/protocol.md`: planned informal walkthrough protocol; **not evidence of completed user testing**.

**The manuscript is intentionally not included.** This repository contains the implementation and associated experimental artifacts, not the old or current LaTeX draft.

## Run checker tests

Requires Python >=3.10. Tests run without the medical data and without the original toolkit source.

```bash
python -m pip install pytest
python -m pytest -q tests
```

## Check an archived bundle

```bash
python -m xfairmed_check.cli results/bundles/real_v2__xgboost.json \
  --out example_findings.json --report example_review.md
```

Archived result files include their own source-artifact references and snapshots. Checking source-file integrity or rebuilding the entire experimental results requires the original upstream audit artifact tree, which is **not embedded** in this repository. If only the frozen bundles are available, provenance checks referring to absent upstream source files may report `INCOMPLETE`; this is expected, not proof of a missing patient-level input.

## Re-run full research pipeline

```bash
python experiments/run_all.py --repo /path/to/xfairmed-toolkit \
  --v2 /path/to/v2-artifact-mirror --out results
```

`--repo` must be a full clone with Git history, used for the decision-continuity replay. `--v2` must contain the study-relative files listed in `xfairmed_check/bundle_v2.py` (including relevant locally stored aggregate reports), plus its `BRANCH_HEAD` record. The figure generation additionally requires `matplotlib`.

The frozen bundles and result tables are included to permit inspection of the evidence, calculations and records when the full upstream material is unavailable. Public TCGA-BRCA raw data, sample-level predictions, patient identifiers, protected clinical records, and private access credentials are not redistributed here.

## Scope and interpretation

The scripts and stored results address six responsibilities: schema validity (R1), subgroup support and uncertainty declarations (R2), explanation-scope declarations (R3), cross-layer divergence (R4), provenance (R5), and review continuity (R6). The findings do **not** establish discrimination, clinical safety or ethical acceptability. Deterministic fixture conformance does not establish usefulness in real engineering teams; a practitioner study is not claimed.


