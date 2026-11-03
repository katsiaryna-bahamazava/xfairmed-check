# Review report: mlp (real_v1)

- Evidence snapshot: `snap-18344c149d72`  
- Policy: `policy-v1`  
- Gate: **FAIL**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R2 | 0 | 9 | 0 |
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 18 |
| R5 | 3 | 0 | 0 |
| R6 | 0 | 12 | 0 |

### [INCOMPLETE] R5 missing_provenance `R5-3b82d19c9b`
Provenance field `dataset_release` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `f99b975cb8e0`

### [INCOMPLETE] R5 missing_provenance `R5-3bb70c7031`
Provenance field `dataset_sha256` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `9fc9a0281d13`

### [INCOMPLETE] R5 missing_provenance `R5-02145f2b7d`
Provenance field `environment_lock` is not recorded.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Record the value in the run manifest or repeat the run with it documented.
- Evidence: -
- Evidence fingerprint: `179c7c4a864a`

### [REVIEW] R2 parity_not_computable `R2-bc4aef2541`
Model-layer parity for `audit_CDH1_ECadherin_disruption_status` was not computed: Less than two supported groups available. Excluded: CDH1_Ecadherin_not_disrupted_proxy.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `f75def717459`

### [REVIEW] R2 low_support `R2-dc7f2ccf06`
Subgroup `audit_CDH1_ECadherin_disruption_status=CDH1_Ecadherin_not_disrupted_proxy` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status, group=CDH1_Ecadherin_not_disrupted_proxy]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `899f461fbdf9`

### [REVIEW] R2 low_support `R2-8b28782259`
Subgroup `audit_ER_Status=Negative` has insufficient support (minority class 3 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_ER_Status, group=Negative]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_ER_Status]`
- Evidence fingerprint: `5e2695ab8d2b`

### [REVIEW] R2 parity_not_computable `R2-6ffb9b2742`
Model-layer parity for `audit_GATA3_mut_status` was not computed: Less than two supported groups available. Excluded: GATA3_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `73304fb23c53`

### [REVIEW] R2 low_support `R2-3950c539fb`
Subgroup `audit_GATA3_mut_status=GATA3_mut` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_GATA3_mut_status, group=GATA3_mut]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `d9cda7dfab32`

### [REVIEW] R2 low_support `R2-16740d9473`
Subgroup `audit_HER2_Final_Status=Positive` has insufficient support (minority class 2 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_HER2_Final_Status, group=Positive]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_HER2_Final_Status]`
- Evidence fingerprint: `fd5c33a02026`

### [REVIEW] R2 low_support `R2-55e3a58f43`
Subgroup `audit_PR_Status=Negative` has insufficient support (minority class 9 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_PR_Status, group=Negative]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_PR_Status]`
- Evidence fingerprint: `204e6aee5138`

### [REVIEW] R2 parity_not_computable `R2-3d3ec43e70`
Model-layer parity for `audit_TP53_mut_status` was not computed: Less than two supported groups available. Excluded: TP53_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `1fed7cecc38d`

### [REVIEW] R2 low_support `R2-737f71a6be`
Subgroup `audit_TP53_mut_status=TP53_mut` has insufficient support (minority class 8 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_model_agnostic_fairness/results/tables/low_support_subgroups.csv [audited_attribute=audit_TP53_mut_status, group=TP53_mut]`; `studies/tcga_brca_model_agnostic_fairness/results/tables/amf_layer_by_attribute_mlp_oof_omics_leakage_safe.csv [audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `4c363853eb60`

### [REVIEW] R6 unresolved `R6-ad001cbc63`
R5 finding `R5-3b82d19c9b` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `b093df9d4bea`

### [REVIEW] R6 unresolved `R6-805fb957c3`
R5 finding `R5-3bb70c7031` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `c10db8e18592`

### [REVIEW] R6 unresolved `R6-3bddec0571`
R5 finding `R5-02145f2b7d` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `e0db7faa4c3c`

### [REVIEW] R6 unresolved `R6-af954285c1`
R2 finding `R2-bc4aef2541` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `9dd4a608f1a0`

### [REVIEW] R6 unresolved `R6-927c3b2d9a`
R2 finding `R2-dc7f2ccf06` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `f9032033ce5b`

### [REVIEW] R6 unresolved `R6-2eda94f3a4`
R2 finding `R2-8b28782259` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `f92397370162`

### [REVIEW] R6 unresolved `R6-96d2efd720`
R2 finding `R2-6ffb9b2742` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `3272f5847fb0`

### [REVIEW] R6 unresolved `R6-3f7d487dcd`
R2 finding `R2-3950c539fb` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `c9a3c7c88613`

### [REVIEW] R6 unresolved `R6-349c9ae65b`
R2 finding `R2-16740d9473` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `d3530aa4fd46`

### [REVIEW] R6 unresolved `R6-c3ead62983`
R2 finding `R2-55e3a58f43` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `c2ba7ba8e33e`

### [REVIEW] R6 unresolved `R6-080021c1cd`
R2 finding `R2-3d3ec43e70` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `67f29ee30c17`

### [REVIEW] R6 unresolved `R6-2623eee645`
R2 finding `R2-737f71a6be` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `779f6c4912fa`
