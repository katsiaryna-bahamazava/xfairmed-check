# Review report: mlp (semi_synthetic)

- Evidence snapshot: `snap-332a75a19074`  
- Policy: `policy-v1`  
- Gate: **FAIL**. PASS means the configured technical checks found no blocking condition. It is not a fairness certification or deployment approval.

| Rule | INCOMPLETE | REVIEW | OBSERVED |
|---|---|---|---|
| R3 | 0 | 0 | 2 |
| R4 | 0 | 0 | 20 |
| R5 | 3 | 0 | 0 |
| R6 | 0 | 3 | 0 |

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
