# C052 Public Review Mirror

This directory is the open-access review mirror referenced in the manuscript's Data Availability Statement.

- Repository: `TerryFYL/ai-research-army`
- Public URL: https://github.com/TerryFYL/ai-research-army/tree/main/public_release/C052
- Public script URL: https://github.com/TerryFYL/ai-research-army/blob/main/public_release/C052/reproduce_main_analysis.py
- Public source-data note: see the CDC/NCHS, FluVaxView, FluView, and Census API URLs cited in `manuscript.md`

## Included files

- `manuscript.md`
- `reproduce_main_analysis.py`
- `reproducibility_manifest.json`
- `cdc_wonder_replacement_protocol.md`
- `strobe_checklist.md`
- `table2_primary_linear_model.csv`
- `table10_linear_sensitivity_models.csv`
- `table11_era_interaction_model.csv`
- `table12_availability_ipw_diagnostics.csv`
- `table13_availability_balance_diagnostics.csv`
- `table14_alternative_inference_sensitivity.csv`
- `table15_outcome_construction.csv`

## Interpretation notes

- The pre-COVID weighted fixed-effects linear model is the primary inferential result.
- The pooled era-interaction estimate is exploratory and becomes less decisive under season-clustered and two-way clustered uncertainty estimators.
- Threshold results are post hoc, unstable across validation checks, and are not presented as implementation-ready targets.
- No CDC WONDER-derived mortality counts are claimed in this release.

## Versioning

The public mirror is paired with the manuscript-specific frozen peer-review bundle in `submission_package/`, which contains `analysis_ready.csv` and the full package-build script.
`reproducibility_manifest.json` records SHA-256 hashes for the mirrored manuscript-specific files.
