# Review report: logistic_regression (semi_synthetic)

- Evidence snapshot: `snap-0d4325531ffc`  
- Policy: `policy-v1`  
- Gate: **FAIL**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 20 |
| R5 | 3 | 0 | 0 |
| R6 | 0 | 3 | 0 |

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
