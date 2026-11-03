# Review report: xgboost (real_v2)

- Evidence snapshot: `snap-c951b06d3db2`  
- Policy: `policy-v1`  
- Gate: **PASS**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R2 | 0 | 9 | 1 |
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 18 |
| R5 | 0 | 2 | 4 |
| R6 | 0 | 11 | 0 |

### [REVIEW] R2 parity_not_computable `R2-59b54f8a16`
Model-layer parity for `audit_CDH1_ECadherin_disruption_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: CDH1_Ecadherin_not_disrupted_proxy.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `c24f77a0a11e`

### [REVIEW] R2 low_support `R2-5d4c857e22`
Subgroup `audit_CDH1_ECadherin_disruption_status=CDH1_Ecadherin_not_disrupted_proxy` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status, group=CDH1_Ecadherin_not_disrupted_proxy]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `6532427202a1`

### [REVIEW] R2 low_support `R2-b2f3d87ce0`
Subgroup `audit_ER_Status=Negative` has insufficient support (minority class 3 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_ER_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_ER_Status]`
- Evidence fingerprint: `67c4ffe569d7`

### [REVIEW] R2 parity_not_computable `R2-df3e8affc6`
Model-layer parity for `audit_GATA3_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: GATA3_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `41b576ac83df`

### [REVIEW] R2 low_support `R2-01fb57d0e5`
Subgroup `audit_GATA3_mut_status=GATA3_mut` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_GATA3_mut_status, group=GATA3_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `5872cb4bbca0`

### [REVIEW] R2 low_support `R2-60a28f9b0f`
Subgroup `audit_HER2_Final_Status=Positive` has insufficient support (minority class 2 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_HER2_Final_Status, group=Positive]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_HER2_Final_Status]`
- Evidence fingerprint: `44ddd28e8c10`

### [REVIEW] R2 low_support `R2-7cdbaa3fa6`
Subgroup `audit_PR_Status=Negative` has insufficient support (minority class 9 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_PR_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_PR_Status]`
- Evidence fingerprint: `0f3a4810a865`

### [REVIEW] R2 parity_not_computable `R2-7a6e1c9e40`
Model-layer parity for `audit_TP53_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: TP53_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `a6816912487c`

### [REVIEW] R2 low_support `R2-ad434d3194`
Subgroup `audit_TP53_mut_status=TP53_mut` has insufficient support (minority class 8 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_TP53_mut_status, group=TP53_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=xgboost, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `e0c7c8f86af2`

### [REVIEW] R5 open_gate `R5-598729f043`
Provenance gate `definitive_training` is open: BLOCKED_PENDING_UPSTREAM_PROVENANCE_REVIEW_AND_V2_TRAINING_ENVIRONMENT_WEIGHTING_AND_RUNNER_TESTS.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `4f110c4647bf`

### [REVIEW] R5 open_gate `R5-08b20282ab`
Provenance gate `source_to_local_bitwise_traceability` is open: PENDING_NO_ORIGINAL_KAGGLE_HASH_AVAILABLE.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `201f23094000`

### [REVIEW] R6 unresolved `R6-45365f77aa`
R5 finding `R5-598729f043` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `b77b7f88529c`

### [REVIEW] R6 unresolved `R6-8161865713`
R5 finding `R5-08b20282ab` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `f419be627a1e`

### [REVIEW] R6 unresolved `R6-0c38b1145f`
R2 finding `R2-59b54f8a16` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `2d3104013230`

### [REVIEW] R6 unresolved `R6-b7e831d0a5`
R2 finding `R2-5d4c857e22` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `6d1fade7a7a4`

### [REVIEW] R6 unresolved `R6-f445d0b915`
R2 finding `R2-b2f3d87ce0` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `1bb14f245ca2`

### [REVIEW] R6 unresolved `R6-01d14fe356`
R2 finding `R2-df3e8affc6` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `9c509e423fd6`

### [REVIEW] R6 unresolved `R6-de423bc09a`
R2 finding `R2-01fb57d0e5` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `d6b2560be38d`

### [REVIEW] R6 unresolved `R6-47f2b435fc`
R2 finding `R2-60a28f9b0f` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `e7b455887d49`

### [REVIEW] R6 unresolved `R6-623f7e8d10`
R2 finding `R2-7cdbaa3fa6` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `92b8944930dd`

### [REVIEW] R6 unresolved `R6-233e01f268`
R2 finding `R2-7a6e1c9e40` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `85dc40fa3643`

### [REVIEW] R6 unresolved `R6-1bf62b6bb2`
R2 finding `R2-ad434d3194` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `70bd81d0af74`
