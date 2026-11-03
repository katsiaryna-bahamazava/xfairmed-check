# Review report: random_forest (real_v1)

- Evidence snapshot: `snap-cdb618a0956b`  
- Policy: `policy-v1`  
- Gate: **FAIL**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R2 | 0 | 9 | 0 |
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 18 |
| R5 | 3 | 0 | 0 |
| R6 | 0 | 12 | 0 |

### [INCOMPLETE] R5 missing_provenance `R5-4cd49c3689`
Provenance field `dataset_release` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `f99b975cb8e0`

### [INCOMPLETE] R5 missing_provenance `R5-82027eb462`
Provenance field `dataset_sha256` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `9fc9a0281d13`

### [INCOMPLETE] R5 missing_provenance `R5-3c7c53e329`
Provenance field `environment_lock` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `179c7c4a864a`

### [REVIEW] R2 parity_not_computable `R2-58bb7ba403`
Model-layer parity for `audit_CDH1_ECadherin_disruption_status` was not computed: Less than two supported groups available. Excluded: CDH1_Ecadherin_not_disrupted_proxy.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `3925268cd4ef`

### [REVIEW] R2 low_support `R2-f028f4205d`
Subgroup `audit_CDH1_ECadherin_disruption_status=CDH1_Ecadherin_not_disrupted_proxy` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status, group=CDH1_Ecadherin_not_disrupted_proxy]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `d35330a8d1bc`

### [REVIEW] R2 low_support `R2-265b9a6a5a`
Subgroup `audit_ER_Status=Negative` has insufficient support (minority class 3 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_ER_Status, group=Negative]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_ER_Status]`
- Evidence fingerprint: `e3246049660a`

### [REVIEW] R2 parity_not_computable `R2-d98b14d9c7`
Model-layer parity for `audit_GATA3_mut_status` was not computed: Less than two supported groups available. Excluded: GATA3_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `3579c3c3d4c9`

### [REVIEW] R2 low_support `R2-73a7b42ab6`
Subgroup `audit_GATA3_mut_status=GATA3_mut` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_GATA3_mut_status, group=GATA3_mut]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `71fd706b4746`

### [REVIEW] R2 low_support `R2-41528c0a58`
Subgroup `audit_HER2_Final_Status=Positive` has insufficient support (minority class 2 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_HER2_Final_Status, group=Positive]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_HER2_Final_Status]`
- Evidence fingerprint: `ce937b52d909`

### [REVIEW] R2 low_support `R2-385046dfdb`
Subgroup `audit_PR_Status=Negative` has insufficient support (minority class 9 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_PR_Status, group=Negative]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_PR_Status]`
- Evidence fingerprint: `1cf8cf24b143`

### [REVIEW] R2 parity_not_computable `R2-7d9cc3fef8`
Model-layer parity for `audit_TP53_mut_status` was not computed: Less than two supported groups available. Excluded: TP53_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `15901894d8ab`

### [REVIEW] R2 low_support `R2-386731302d`
Subgroup `audit_TP53_mut_status=TP53_mut` has insufficient support (minority class 8 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_TP53_mut_status, group=TP53_mut]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_random_forest_oof_omics_leakage_safe.csv [audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `2490a0234e06`

### [REVIEW] R6 unresolved `R6-fff9107764`
R5 finding `R5-4cd49c3689` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `2e141efd751c`

### [REVIEW] R6 unresolved `R6-51731ac782`
R5 finding `R5-82027eb462` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `0b3bcdd030c7`

### [REVIEW] R6 unresolved `R6-275ba47fd4`
R5 finding `R5-3c7c53e329` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `c4fb0f7227b4`

### [REVIEW] R6 unresolved `R6-f350537e9a`
R2 finding `R2-58bb7ba403` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `75522de8cbea`

### [REVIEW] R6 unresolved `R6-88a787bcbc`
R2 finding `R2-f028f4205d` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `3d2ba514bf2f`

### [REVIEW] R6 unresolved `R6-ca33956d9a`
R2 finding `R2-265b9a6a5a` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `57eb154bee06`

### [REVIEW] R6 unresolved `R6-8ee81af8f5`
R2 finding `R2-d98b14d9c7` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `9593ab6ca435`

### [REVIEW] R6 unresolved `R6-f1108b64f3`
R2 finding `R2-73a7b42ab6` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `b4bf7168f6eb`

### [REVIEW] R6 unresolved `R6-c3be36a891`
R2 finding `R2-41528c0a58` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `3322f60f0c8b`

### [REVIEW] R6 unresolved `R6-461b3987f2`
R2 finding `R2-385046dfdb` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `5fd76eab9a33`

### [REVIEW] R6 unresolved `R6-c0efc8dcdf`
R2 finding `R2-7d9cc3fef8` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `04f8120b1a00`

### [REVIEW] R6 unresolved `R6-eef4ed7213`
R2 finding `R2-386731302d` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `151ef8552d73`
