# Stage 5 Analysis Plan — C046 (Public Archive Copy)

This file is a cleaned public-archive copy of the local planning document used in project `C046`.

It preserves the substantive analysis specification while removing one unverified OSF placeholder that was present in the local file.

## Cleaned note

The local file contained the line:

- `Pre-registration: OSF osf.io/r9j3k 2026-03-22`

That identifier could not be verified via the public OSF API on `2026-04-24`, so it is omitted here rather than treated as a valid registration record.

## Preserved local timestamp

- Source file timestamp: `2026-04-23 21:58:20 +0800`

## Analysis specification

Design: Cross-sectional complex-sample analysis with NHANES MEC weights

Exposure categories:

- normal (ferritin >=30 M or >=15 F)
- iron deficiency without anemia (low ferritin, normal Hb)
- iron deficiency anemia (both)

Primary outcome:

- estimated VO2max (NHANES submaximal treadmill protocol with ACSM equation)

Primary model:

- survey-weighted linear regression `VO2max ~ iron_status + age + sex + BMI + race + PA_level + smoking`

SE:

- Taylor-series linearization accounting for MEC design strata and PSU

Sensitivity analyses:

- alternative ferritin cutoffs
- log-ferritin continuous
- exclude elevated CRP (inflammation)

Subgroups:

- pre-menopausal women
- post-menopausal women
- men
