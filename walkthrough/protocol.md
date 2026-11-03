# Pilot walkthrough: Condition B vs Condition C (RQ3, practical validity)

**Goal.** Check, informally and before submission, whether reviewers can locate and act on review-relevant conditions faster and more completely with the checker report (C) than with the raw XFAIR-MED tables (B). This is a formative pilot (2–4 colleagues), not a controlled user study, and the paper must say so.

**Ethics.** An informal walkthrough with colleagues is usually low risk, but check whether your institution (UL) requires ethics review for collecting opinions from staff. If in doubt, collect no personal data, ask for verbal consent, and report only aggregated observations.

## Participants
2–4 colleagues with ML or clinical-informatics background who did **not** build XFAIR-MED Check. Record only role and years of experience.

## Materials (real cohort, current XFAIR-MED version, XGBoost or LR)
- **B:** the toolkit's own outputs for the study `studies/tcga_brca_xai_revision/`: `reports/xai_full5x5_20261027/frozen_subgroup_support.csv`, `reports/xai_full5x5_20261027/fairness_PP_RP_5x5.csv`, `paper_release_20261028/xcfs_ablation_20261028/FULL_XCFS_LAYER_ABLATION.csv`, `specs/SCIENTIFIC_METRIC_AUDIT_v0.1.0.md`, `configs/cohort_provenance_v2.0.0.json`, `reports/xai_uncertainty_integrated_FINAL_v2/ass_calibration_method_decisions.csv`.
- **C:** `results/reports/real_v2__xgboost.md` (checker report).

Counterbalance: half the participants start with B, half with C. Use the RF model for the second condition so answers cannot be copied (the conditions are the same for LR and RF).

## Tasks (≈10 min per condition)
1. Which audited attributes are **not** covered by the AMF score, and why?
2. Which subgroups have too little support to interpret? What threshold defines "too little"?
3. Is the explanation-fairness score complete? If not, is that a defect or a declared limitation?
4. Is there anything you would need before you could reproduce this audit?
5. For one of your answers above: who should act on it, and what should they do?

## Record per task
- Correct / partially correct / incorrect (answer key below)
- Time to answer (rough, minutes)
- Where the participant looked (file / section)

## Short debrief questions (5 min)
- What in C was useful that B did not give you? What was missing or misleading?
- Would you trust a PASS gate? What would you expect it to mean?
- Would this fit into your team's code review or CI? What would stop it?

## Answer key (current version, any model)
1. TP53 mutation status, GATA3 mutation status and the CDH1/E-cadherin disruption proxy: each has only one eligible group, so pairwise parity (PP/RP) is undefined and AMF summarizes the other six attributes.
2. Six subgroups (ER-negative, PR-negative, HER2-positive, TP53-mutant, GATA3-mutant, CDH1/E-cadherin-not-disrupted); rule: at least 35 cases and at least 10 of each class.
3. Partial: ASS and ERS are computed; SAS and CSD are declared not applicable because audited attributes are not model inputs, and the toolkit's specification names the compound score XCFS_partial. This is a declared limitation, not a defect.
4. Two provenance gates are open (bitwise traceability to the distributed source file; definitive training blocked), and four provenance claims are declared unverified (e.g., patient identity at row level).
5. Any reasonable owner/action (e.g., data steward to record the low-support subgroups as a limitation; pipeline owner to close the traceability gate).

## Reporting in the paper
Report as: "In an informal pilot walkthrough with N colleagues (roles…), participants answered k/5 tasks correctly with B and m/5 with C…", plus 2–3 short paraphrased observations. Name it a pilot, list it as a threat to validity, and do not compute statistics on N ≤ 4.
