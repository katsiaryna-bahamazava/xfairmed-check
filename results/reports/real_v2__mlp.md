# Review report: mlp (real_v2)

- Evidence snapshot: `snap-1929c763cdc9`  
- Policy: `policy-v1`  
- Gate: **PASS**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R2 | 0 | 9 | 1 |
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 18 |
| R5 | 0 | 2 | 4 |
| R6 | 0 | 11 | 0 |

### [REVIEW] R2 parity_not_computable `R2-bc4aef2541`
Model-layer parity for `audit_CDH1_ECadherin_disruption_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: CDH1_Ecadherin_not_disrupted_proxy.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `82eaefa9e110`

### [REVIEW] R2 low_support `R2-dc7f2ccf06`
Subgroup `audit_CDH1_ECadherin_disruption_status=CDH1_Ecadherin_not_disrupted_proxy` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_CDH1_ECadherin_disruption_status, group=CDH1_Ecadherin_not_disrupted_proxy]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_CDH1_ECadherin_disruption_status]`
- Evidence fingerprint: `337dad648812`

### [REVIEW] R2 low_support `R2-8b28782259`
Subgroup `audit_ER_Status=Negative` has insufficient support (minority class 3 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_ER_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_ER_Status]`
- Evidence fingerprint: `74888068073b`

### [REVIEW] R2 parity_not_computable `R2-6ffb9b2742`
Model-layer parity for `audit_GATA3_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: GATA3_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `a5be63d65b14`

### [REVIEW] R2 low_support `R2-3950c539fb`
Subgroup `audit_GATA3_mut_status=GATA3_mut` has insufficient support (minority class 6 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_GATA3_mut_status, group=GATA3_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_GATA3_mut_status]`
- Evidence fingerprint: `3d6580625365`

### [REVIEW] R2 low_support `R2-16740d9473`
Subgroup `audit_HER2_Final_Status=Positive` has insufficient support (minority class 2 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_HER2_Final_Status, group=Positive]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_HER2_Final_Status]`
- Evidence fingerprint: `eedd3e04355f`

### [REVIEW] R2 low_support `R2-55e3a58f43`
Subgroup `audit_PR_Status=Negative` has insufficient support (minority class 9 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_PR_Status, group=Negative]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_PR_Status]`
- Evidence fingerprint: `e03a2640792c`

### [REVIEW] R2 parity_not_computable `R2-3d3ec43e70`
Model-layer parity for `audit_TP53_mut_status` was not computed: UNDEFINED_AT_LEAST_ONE_REPEAT; frozen required groups: 1 (pairwise parity needs at least two). Excluded: TP53_mut.

- Owner role: Data steward + biostatistician
- Suggested action: Do not read the aggregate model-fairness score as covering this attribute; record the coverage gap.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `296e1578d305`

### [REVIEW] R2 low_support `R2-737f71a6be`
Subgroup `audit_TP53_mut_status=TP53_mut` has insufficient support (minority class 8 < 10). It is excluded from the parity comparison.

- Owner role: Data steward + biostatistician
- Suggested action: Inspect counts and uncertainty; decide whether subgroup results are interpretable, need pooling, more data, or an explicit limitation.
- Evidence: `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/frozen_subgroup_support.csv [audited_attribute=audit_TP53_mut_status, group=TP53_mut]`; `studies/tcga_brca_xai_revision/reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv [model=mlp, audited_attribute=audit_TP53_mut_status]`
- Evidence fingerprint: `cb545d3223b6`

### [REVIEW] R5 open_gate `R5-08184599c7`
Provenance gate `definitive_training` is open: BLOCKED_PENDING_UPSTREAM_PROVENANCE_REVIEW_AND_V2_TRAINING_ENVIRONMENT_WEIGHTING_AND_RUNNER_TESTS.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `4f110c4647bf`

### [REVIEW] R5 open_gate `R5-169a7e437d`
Provenance gate `source_to_local_bitwise_traceability` is open: PENDING_NO_ORIGINAL_KAGGLE_HASH_AVAILABLE.

- Owner role: ML engineer (pipeline owner)
- Suggested action: Assign an owner to close the gate or accept it as a limitation.
- Evidence: `studies/tcga_brca_xai_revision/configs/cohort_provenance_v2.0.0.json`
- Evidence fingerprint: `201f23094000`

### [REVIEW] R6 unresolved `R6-5bf6ca2e77`
R5 finding `R5-08184599c7` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `240b0f862705`

### [REVIEW] R6 unresolved `R6-eca6068b65`
R5 finding `R5-169a7e437d` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `9a5eb194dab0`

### [REVIEW] R6 unresolved `R6-af954285c1`
R2 finding `R2-bc4aef2541` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `2bb24fac5337`

### [REVIEW] R6 unresolved `R6-927c3b2d9a`
R2 finding `R2-dc7f2ccf06` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `a5d62aba3971`

### [REVIEW] R6 unresolved `R6-2eda94f3a4`
R2 finding `R2-8b28782259` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `ff3d90650b74`

### [REVIEW] R6 unresolved `R6-96d2efd720`
R2 finding `R2-6ffb9b2742` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `8395809b82b8`

### [REVIEW] R6 unresolved `R6-3f7d487dcd`
R2 finding `R2-3950c539fb` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `07ea23739bb6`

### [REVIEW] R6 unresolved `R6-349c9ae65b`
R2 finding `R2-16740d9473` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `01df6ade6c2e`

### [REVIEW] R6 unresolved `R6-c3ead62983`
R2 finding `R2-55e3a58f43` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `6ec533bba596`

### [REVIEW] R6 unresolved `R6-080021c1cd`
R2 finding `R2-3d3ec43e70` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `12d2588abb92`

### [REVIEW] R6 unresolved `R6-2623eee645`
R2 finding `R2-737f71a6be` has no recorded disposition.

- Owner role: Responsibility lead (review owner)
- Suggested action: Assign an owner and record a decision with rationale.
- Evidence: -
- Evidence fingerprint: `51c1d3671a24`
