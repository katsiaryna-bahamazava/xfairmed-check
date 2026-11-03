# Review report: random_forest (real_v2)

- Evidence snapshot: `snap-c4796c52c545`  
- Policy: `policy-v1`  
- Gate: **PASS**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R2 | 0 | 9 | 1 |
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 18 |
| R5 | 0 | 2 | 4 |
| R6 | 0 | 11 | 0 |

### [REVIEW] R2 parity_not_computable `R2-58bb7ba403`
Model-layer parity for `audit_CDH1_ECadherin_disruption_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: CDH1_Ecadherin_not_disrupted_proxy.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `7acd048cfad2`

### [REVIEW] R2 low_support `R2-f028f4205d`
Subgroup `audit_CDH1_ECadherin_disruption_status=CDH1_Ecadherin_not_disrupted_proxy` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status, group=CDH1_Ecadherin_not_disrupted_proxy]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `46527a39be1c`

### [REVIEW] R2 low_support `R2-265b9a6a5a`
Subgroup `audit_ER_Status=Negative` has insufficient support (minority class 3 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_ER_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_ER_Status]`
- Evidence fingerprint: `923438b7e64a`

### [REVIEW] R2 parity_not_computable `R2-d98b14d9c7`
Model-layer parity for `audit_GATA3_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: GATA3_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `5ad5345011fe`

### [REVIEW] R2 low_support `R2-73a7b42ab6`
Subgroup `audit_GATA3_mut_status=GATA3_mut` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_GATA3_mut_status, group=GATA3_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `6dce235fb2b5`

### [REVIEW] R2 low_support `R2-41528c0a58`
Subgroup `audit_HER2_Final_Status=Positive` has insufficient support (minority class 2 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_HER2_Final_Status, group=Positive]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_HER2_Final_Status]`
- Evidence fingerprint: `26994dc93157`

### [REVIEW] R2 low_support `R2-385046dfdb`
Subgroup `audit_PR_Status=Negative` has insufficient support (minority class 9 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_PR_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_PR_Status]`
- Evidence fingerprint: `444fd6ccfec0`

### [REVIEW] R2 parity_not_computable `R2-7d9cc3fef8`
Model-layer parity for `audit_TP53_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: TP53_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `5843ea174087`

### [REVIEW] R2 low_support `R2-386731302d`
Subgroup `audit_TP53_mut_status=TP53_mut` has insufficient support (minority class 8 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_TP53_mut_status, group=TP53_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=random_forest, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `5b52565e913d`

### [REVIEW] R5 open_gate `R5-f49299bfcd`
Provenance gate `definitive_training` is open: BLOCKED_PENDING_UPSTREAM_PROVENANCE_REVIEW_AND_V2_TRAINING_ENVIRONMENT_WEIGHTING_AND_RUNNER_TESTS.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `4f110c4647bf`

### [REVIEW] R5 open_gate `R5-efa6069d6e`
Provenance gate `source_to_local_bitwise_traceability` is open: PENDING_NO_ORIGINAL_KAGGLE_HASH_AVAILABLE.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `201f23094000`

### [REVIEW] R6 unresolved `R6-755e0e5c9c`
R5 finding `R5-f49299bfcd` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `1877f8976f9e`

### [REVIEW] R6 unresolved `R6-38d4ee6334`
R5 finding `R5-efa6069d6e` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `640c3e503cc0`

### [REVIEW] R6 unresolved `R6-f350537e9a`
R2 finding `R2-58bb7ba403` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `284e7b62485b`

### [REVIEW] R6 unresolved `R6-88a787bcbc`
R2 finding `R2-f028f4205d` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `bd56bb34c31c`

### [REVIEW] R6 unresolved `R6-ca33956d9a`
R2 finding `R2-265b9a6a5a` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `9bbbd3885e2f`

### [REVIEW] R6 unresolved `R6-8ee81af8f5`
R2 finding `R2-d98b14d9c7` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `b59833829310`

### [REVIEW] R6 unresolved `R6-f1108b64f3`
R2 finding `R2-73a7b42ab6` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `3891fecb2d74`

### [REVIEW] R6 unresolved `R6-c3be36a891`
R2 finding `R2-41528c0a58` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `0fc74178ab4a`

### [REVIEW] R6 unresolved `R6-461b3987f2`
R2 finding `R2-385046dfdb` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `dd4c33cbd91d`

### [REVIEW] R6 unresolved `R6-c0efc8dcdf`
R2 finding `R2-7d9cc3fef8` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `23dee24d9d9b`

### [REVIEW] R6 unresolved `R6-eef4ed7213`
R2 finding `R2-386731302d` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `7324eff202cb`
