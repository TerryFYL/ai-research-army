# CDC WONDER Replacement Protocol

## Original Requirement
The initial brief named CDC WONDER mortality extraction for influenza-related mortality.

## Failure Condition Observed
During execution on 2026-04-23, the CDC WONDER interactive path did not yield a stable machine-readable export suitable for reproducible scripted analysis. Under the project's hard rules, this blocked any honest attempt to derive jurisdiction-season mortality counts directly from WONDER without manual copying or unverifiable transformation.

## Predefined Replacement Rule
If CDC WONDER did not provide a stable programmatic extract, replace it only with:
1. an official CDC/NCHS public table,
2. a source that can be downloaded programmatically,
3. a source whose row-level provenance can be retained under `data/raw/`, and
4. a source whose changed estimand is explicitly disclosed in the manuscript and data audit.

## Replacement Chosen
- Mortality outcome: NCHS Weekly Counts of Death by Jurisdiction and Select Causes of Death (`u6jv-9ijr`)
- Exposure: CDC FluVaxView (`vh55-3he6`)
- Virology descriptors: CDC FluView WHO/NREVSS downloads

## Consequence For Interpretation
This replacement changes the paper from a CDC WONDER-derived mortality study to a programmatic ecological surveillance analysis using weekly jurisdiction-level P&I mortality benchmarks. The study therefore does **not** claim WONDER-derived death counts, influenza-specific mortality, or causal vaccine-effectiveness inference.

## Public Verification
The manuscript, harmonised dataset, public reproduction script, STROBE checklist, and reproducibility manifest are mirrored at https://github.com/TerryFYL/ai-research-army/tree/main/public_release/C052.
