# Review report: random_forest (semi_synthetic)

- Evidence snapshot: `snap-feb881c842c5`  
- Policy: `policy-v1`  
- Gate: **FAIL**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 20 |
| R5 | 3 | 0 | 0 |
| R6 | 0 | 3 | 0 |

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
