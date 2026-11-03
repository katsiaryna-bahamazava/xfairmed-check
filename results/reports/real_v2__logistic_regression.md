# Review report: logistic_regression (real_v2)

- Evidence snapshot: `snap-5ea548765e1e`  
- Policy: `policy-v1`  
- Gate: **PASS**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R2 | 0 | 9 | 1 |
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 18 |
| R5 | 0 | 2 | 4 |
| R6 | 0 | 11 | 0 |

### [REVIEW] R2 parity_not_computable `R2-50b804fb79`
Model-layer parity for `audit_CDH1_ECadherin_disruption_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: CDH1_Ecadherin_not_disrupted_proxy.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `7bda7b0bbc10`

### [REVIEW] R2 low_support `R2-78e2006424`
Subgroup `audit_CDH1_ECadherin_disruption_status=CDH1_Ecadherin_not_disrupted_proxy` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status, group=CDH1_Ecadherin_not_disrupted_proxy]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `df3baedd51ee`

### [REVIEW] R2 low_support `R2-f3883ac7fe`
Subgroup `audit_ER_Status=Negative` has insufficient support (minority class 3 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_ER_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_ER_Status]`
- Evidence fingerprint: `4aa0ff740fe5`

### [REVIEW] R2 parity_not_computable `R2-d4aa4b1630`
Model-layer parity for `audit_GATA3_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: GATA3_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `aa2577e5e123`

### [REVIEW] R2 low_support `R2-d3d7704844`
Subgroup `audit_GATA3_mut_status=GATA3_mut` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_GATA3_mut_status, group=GATA3_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `ab207b32213f`

### [REVIEW] R2 low_support `R2-b0cbaa034c`
Subgroup `audit_HER2_Final_Status=Positive` has insufficient support (minority class 2 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_HER2_Final_Status, group=Positive]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_HER2_Final_Status]`
- Evidence fingerprint: `75cbf1bebb9d`

### [REVIEW] R2 low_support `R2-3bae68d595`
Subgroup `audit_PR_Status=Negative` has insufficient support (minority class 9 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_PR_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_PR_Status]`
- Evidence fingerprint: `d14e982a4afe`

### [REVIEW] R2 parity_not_computable `R2-9814eb81c8`
Model-layer parity for `audit_TP53_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: TP53_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `9ba25c714c03`

### [REVIEW] R2 low_support `R2-11d77c1c6a`
Subgroup `audit_TP53_mut_status=TP53_mut` has insufficient support (minority class 8 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_TP53_mut_status, group=TP53_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=logistic_regression, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `de47c3f73dca`

### [REVIEW] R5 open_gate `R5-d2aa88ad4b`
Provenance gate `definitive_training` is open: BLOCKED_PENDING_UPSTREAM_PROVENANCE_REVIEW_AND_V2_TRAINING_ENVIRONMENT_WEIGHTING_AND_RUNNER_TESTS.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `4f110c4647bf`

### [REVIEW] R5 open_gate `R5-0691ae1282`
Provenance gate `source_to_local_bitwise_traceability` is open: PENDING_NO_ORIGINAL_KAGGLE_HASH_AVAILABLE.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `201f23094000`

### [REVIEW] R6 unresolved `R6-b41baf6a95`
R5 finding `R5-d2aa88ad4b` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `85f7b5139d90`

### [REVIEW] R6 unresolved `R6-3476a8face`
R5 finding `R5-0691ae1282` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `e9dce7d291c5`

### [REVIEW] R6 unresolved `R6-38b1698ad7`
R2 finding `R2-50b804fb79` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `20bff0f63187`

### [REVIEW] R6 unresolved `R6-b0051c2fc8`
R2 finding `R2-78e2006424` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `c85409650070`

### [REVIEW] R6 unresolved `R6-9165aef8ad`
R2 finding `R2-f3883ac7fe` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `9915bb4eae21`

### [REVIEW] R6 unresolved `R6-ebb63a23f1`
R2 finding `R2-d4aa4b1630` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `0b95eb687f74`

### [REVIEW] R6 unresolved `R6-a5e5827cca`
R2 finding `R2-d3d7704844` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `2279dd040438`

### [REVIEW] R6 unresolved `R6-c3d5659cde`
R2 finding `R2-b0cbaa034c` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `3cdb19f06b6a`

### [REVIEW] R6 unresolved `R6-9e1b27a11c`
R2 finding `R2-3bae68d595` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `a946869dc81b`

### [REVIEW] R6 unresolved `R6-8048158675`
R2 finding `R2-9814eb81c8` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `4b90c0bceca2`

### [REVIEW] R6 unresolved `R6-586c4095d1`
R2 finding `R2-11d77c1c6a` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `cbe331877c3b`
