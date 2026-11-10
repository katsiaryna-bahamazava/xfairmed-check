# Evidence bundle format and profiles

Evidence Checker does not read an audit toolkit's files directly. An **adapter**
maps the toolkit's aggregate outputs to an **evidence bundle** (one JSON file per
model and audit run), and a **profile** tells the rules where that toolkit keeps
its layer scores and tables. The rules themselves (`evidence_checker/rules.py`)
do not depend on any toolkit.

To support another audit toolkit you write:

1. an adapter that produces a bundle (see `evidence_checker/adapters/` for two examples), and
2. a profile (a JSON file or a dict; see `evidence_checker/profiles.py`).

`tests/test_generic_profile.py` shows a complete small example for an invented
toolkit with different layer names and three outcome classes.

## Bundle

| Part | Content | Required by the core |
|---|---|---|
| `model`, `cohort` | Identifiers used in reports and finding identifiers | yes |
| `I` | `dataset_id` (string), `n_samples` (integer > 0), `audited_attributes` (list) | yes |
| `M` | `model_id`, `metrics` (dict), `predictions`: a reference `{"artifact": ...}` or `{"withheld": true, "justification": "..."}` | yes |
| `G` | `support_policy` with `min_total` and `min_class`; `groups`: one record per subgroup | yes |
| `P` | Layer scores and per-attribute tables. Names and locations are given by the profile | by profile |
| `A` | Further metric sections (for example explanation metrics). Locations are given by the profile | by profile |
| `U` | `records`: uncertainty records keyed `"<metric>|<attribute>"`; optional `not_approved_methods` | if the contract requires uncertainty |
| `V` | Provenance fields, optional `claims` and `gates`, and `artifacts`: `{relative path: sha256}` for every file the bundle cites | yes |
| `contract` | What the audit declares it must provide (see below) | yes |

**Subgroup record** (`G.groups[]`): `attribute`, `group`, `total`, `ref`, optional
`declared_eligible`, and the class counts, either as `class_counts: {label: n}`
or as the count fields named in the profile (`class_count_fields`). The support
floor `min_class` is applied to the smallest class.

**References.** Any dict with an `artifact` key is a reference to a source file,
optionally with a `row` selector. Every referenced file must be listed in
`V.artifacts`. Values the audit did not record are stored as `null` with a
`note`, never defaulted.

**Metric entry** (in a metric section): `{"status": "computed", "value": ...}` or
`{"status": "not_applicable", "justification": "..."}`.

**Uncertainty record:** `n_attempted`, `n_valid`, `status`, optional `ref`.

## Contract

The contract is the audit's own declaration of what it must report. The rules
take their thresholds from here, not from the code.

| Field | Used by | Meaning |
|---|---|---|
| `required_metrics: {layer: [names]}` | R1, R3 | Metrics each layer must report |
| `allow_declared_not_applicable` | R3 | Whether a metric may be declared not applicable (with a justification) |
| `uncertainty: {required, min_attempted, min_valid_fraction}` | R2 | Quality gate for uncertainty records |
| `required_provenance: [fields]` | R5 | Provenance fields that must be recorded in `V` |

## Profile

| Key | Used by | Meaning |
|---|---|---|
| `required_fields: [[path, type]]` | R1 | The toolkit's layer scores and tables that must be present |
| `components: [{layer, path}]` | R1 | Where each layer's component metrics are stored |
| `unit_tables: [{name, path, field}]` | R1 | Per-attribute tables in which a missing value needs a documented reason |
| `class_count_fields` | R2 | Count fields of a subgroup record, if `class_counts` is not used |
| `comparison: {path, field, label}` | R2 | Table holding the between-subgroup comparison |
| `uncertainty_targets: [{path, metrics}]` | R2 | Reported metrics that need an uncertainty record |
| `interval_status_marker` | R2 | Text in a record's `status` that claims a confidence interval |
| `metric_sections: [{layer, label, metrics, scope, scope_source, reported_as}]` | R3 | Sections whose required metrics may be declared not applicable |
| `layers: {name: {path, field}}`, `default_pairs` | R4 | Per-attribute series that can be compared across layers |
| `open_gate_prefixes` | R5 | Status prefixes that mark a declared gate as open |

Field types: `str`, `pos_int`, `nonempty_list`, `nonempty_dict`, `dict`, `score`
(number in [0, 1]), `withholdable`, `enum:a|b`.

Select a profile with `--profile <name or file.json>` on the command line, or
with `"profile"` in the policy. The built-in default is `xfairmed`, the toolkit
audited in the accompanying study.

## Scope of the current implementation

The rule engine, review ledger, fingerprints, report and command line are
toolkit-independent. The two adapters and the built-in profile are for
XFAIR-MED. The mutation operators in `mutate.py` target the XFAIR-MED bundle
layout, except the required-field operators, which follow any profile.
Evidence Checker has been evaluated on one real toolkit only.
