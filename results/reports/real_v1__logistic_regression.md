# Review report: logistic_regression (real_v1)

- Evidence snapshot: `snap-5a6b828abc70`  
- Policy: `policy-v1`  
- Gate: **FAIL**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R2 | 0 | 9 | 0 |
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 18 |
| R5 | 3 | 0 | 0 |
| R6 | 0 | 12 | 0 |

### [INCOMPLETE] R5 missing_provenance `R5-e87c22cc42`
Provenance field `dataset_release` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `f99b975cb8e0`

### [INCOMPLETE] R5 missing_provenance `R5-03aac4ce2d`
Provenance field `dataset_sha256` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `9fc9a0281d13`

### [INCOMPLETE] R5 missing_provenance `R5-8c5ee7b7f6`
Provenance field `environment_lock` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `179c7c4a864a`

### [REVIEW] R2 parity_not_computable `R2-50b804fb79`
Model-layer parity for `audit_CDH1_ECadherin_disruption_status` was not computed: Less than two supported groups available. Excluded: CDH1_Ecadherin_not_disrupted_proxy.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `de2316b0508c`

### [REVIEW] R2 low_support `R2-78e2006424`
Subgroup `audit_CDH1_ECadherin_disruption_status=CDH1_Ecadherin_not_disrupted_proxy` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status, group=CDH1_Ecadherin_not_disrupted_proxy]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `9ca363cf3c9b`

### [REVIEW] R2 low_support `R2-f3883ac7fe`
Subgroup `audit_ER_Status=Negative` has insufficient support (minority class 3 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_ER_Status, group=Negative]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_ER_Status]`
- Evidence fingerprint: `9159b09e931a`

### [REVIEW] R2 parity_not_computable `R2-d4aa4b1630`
Model-layer parity for `audit_GATA3_mut_status` was not computed: Less than two supported groups available. Excluded: GATA3_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `1c3d9e073eca`

### [REVIEW] R2 low_support `R2-d3d7704844`
Subgroup `audit_GATA3_mut_status=GATA3_mut` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_GATA3_mut_status, group=GATA3_mut]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `2ef2daedbf69`

### [REVIEW] R2 low_support `R2-b0cbaa034c`
Subgroup `audit_HER2_Final_Status=Positive` has insufficient support (minority class 2 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_HER2_Final_Status, group=Positive]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_HER2_Final_Status]`
- Evidence fingerprint: `420c314afd77`

### [REVIEW] R2 low_support `R2-3bae68d595`
Subgroup `audit_PR_Status=Negative` has insufficient support (minority class 9 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_PR_Status, group=Negative]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_PR_Status]`
- Evidence fingerprint: `8e9a0ac61a94`

### [REVIEW] R2 parity_not_computable `R2-9814eb81c8`
Model-layer parity for `audit_TP53_mut_status` was not computed: Less than two supported groups available. Excluded: TP53_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `70ede1860fa0`

### [REVIEW] R2 low_support `R2-11d77c1c6a`
Subgroup `audit_TP53_mut_status=TP53_mut` has insufficient support (minority class 8 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_TP53_mut_status, group=TP53_mut]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_logistic_regression_oof_omics_leakage_safe.csv [audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `05e7caf826fd`

### [REVIEW] R6 unresolved `R6-f8e09c342e`
R5 finding `R5-e87c22cc42` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `9ca39836b38b`

### [REVIEW] R6 unresolved `R6-fb6853b172`
R5 finding `R5-03aac4ce2d` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `70e34bcb6cb7`

### [REVIEW] R6 unresolved `R6-45167cea02`
R5 finding `R5-8c5ee7b7f6` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `a547d2e8dbe1`

### [REVIEW] R6 unresolved `R6-38b1698ad7`
R2 finding `R2-50b804fb79` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `177aa67963e2`

### [REVIEW] R6 unresolved `R6-b0051c2fc8`
R2 finding `R2-78e2006424` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `108cd8b7dc4f`

### [REVIEW] R6 unresolved `R6-9165aef8ad`
R2 finding `R2-f3883ac7fe` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `1133af31b4a0`

### [REVIEW] R6 unresolved `R6-ebb63a23f1`
R2 finding `R2-d4aa4b1630` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `2020de2670ae`

### [REVIEW] R6 unresolved `R6-a5e5827cca`
R2 finding `R2-d3d7704844` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `cc8d8ead06cf`

### [REVIEW] R6 unresolved `R6-c3d5659cde`
R2 finding `R2-b0cbaa034c` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `f97aa68ae010`

### [REVIEW] R6 unresolved `R6-9e1b27a11c`
R2 finding `R2-3bae68d595` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `ee473d9c7846`

### [REVIEW] R6 unresolved `R6-8048158675`
R2 finding `R2-9814eb81c8` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `6dcfd4b9bde4`

### [REVIEW] R6 unresolved `R6-586c4095d1`
R2 finding `R2-11d77c1c6a` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `d0a7e2522384`
