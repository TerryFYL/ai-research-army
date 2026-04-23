# Influenza Vaccination Coverage and Excess Pneumonia-and-Influenza Mortality in US Jurisdictions: a pre-COVID primary ecological analysis with COVID-era sensitivity extensions

**Author**: Yilou Feng  
**Affiliation**: Independent Researcher, Shanghai, China  
**Correspondence**: fyltzx@gmail.com

Target journal: BMJ Open

## Abstract

**Objectives:** To estimate whether higher state-season influenza vaccination coverage was associated with lower excess pneumonia-and-influenza (P&I) mortality in public jurisdiction-season surveillance data, treating the pre-COVID 2015-16 to 2019-20 seasons as the primary inferential era because COVID-era outcome generation materially changed after 2020, and secondarily to assess whether any exploratory hinge remained stable.

**Design:** Ecological repeated panel observational analysis using official CDC/NCHS and CDC FluView public data; no individual participants were enrolled or followed.

**Setting and units of analysis:** A universe of 408 possible state-season cells across 51 reporting jurisdictions (50 states plus the District of Columbia) and eight influenza seasons; 333 retained observations from 48 jurisdictions entered analysis.

**Exposures:** Primary exposure was cumulative December influenza vaccination coverage among persons aged >=6 months from CDC FluVaxView.

**Main outcome measure:** Seasonal net excess P&I deaths, expressed as percentage of NCHS expected P&I deaths, aggregated across MMWR weeks 40-20.

**Results:** Mean December all-age vaccination coverage was 41.9% (range 27.4% to 58.8%). Mean state-season excess P&I mortality was -0.6% of expected deaths. In the pre-COVID primary weighted fixed-effects linear model, each 10 percentage-point higher December coverage was associated with -3.1 percentage points lower excess P&I mortality, but the estimate was imprecise and the 95% CI crossed the null (-9.9 to 3.7; p=0.376). In the pooled eight-season weighted model, the corresponding slope was -0.9 (95% CI -4.0 to 2.1; p=0.552). A pooled era-interaction sensitivity estimated a post-2020 slope change of 2.3 per 10 percentage points, but season-clustered and two-way-clustered uncertainty intervals crossed the null. Unweighted, ACS proxy-adjusted, and availability-IPW linear sensitivities remained qualitatively null. Exploratory threshold analyses did not yield a stable hinge across bootstrap, leave-one-season-out, split-sample, and weighting checks.

**Conclusions:** In the pre-COVID primary analysis, we did not detect a statistically significant ecological association between higher December influenza vaccination coverage and lower excess P&I mortality; the 95% CI crossed the null. Pooled all-era estimates were further limited by COVID-era heterogeneity. Exploratory threshold signals were unstable and model-dependent; the most defensible contribution is a transparent demonstration of what current public surveillance data can and cannot support.

## Strengths and Limitations

- This analysis uses official, programmatically downloadable CDC/NCHS and CDC FluView sources with raw files and code retained [1-5].
- The analysis does not fabricate CDC WONDER outputs. CDC WONDER was replaced by a transparent NCHS/FluView open-data mortality table because the interactive endpoint did not yield stable machine-readable output during execution [1,5].
- The primary inferential result is the pre-COVID weighted fixed-effects linear model; pooled eight-season and era-interaction estimates are reported to show how COVID-era outcome heterogeneity changes the estimand.
- The threshold analysis is secondary, explicitly post hoc, and reported descriptively; its instability is checked with bootstrap, leave-one-season-out, split-sample, and weighting comparisons [17,21].
- State and season fixed effects reduce, but do not eliminate, confounding by jurisdictional reporting, health-system differences, epidemic timing, and season severity [18,19].
- P&I mortality is a surveillance proxy, not laboratory-confirmed influenza mortality; pneumonia deaths during COVID-era seasons can reflect SARS-CoV-2 and other respiratory pathogens [4,5].
- Vaccination coverage is ecological and survey-derived; the analysis cannot estimate individual-level vaccine effectiveness.

## Introduction

Seasonal influenza vaccination is a core public-health intervention, but translating individual protection and population coverage into jurisdiction-level mortality patterns is methodologically difficult. US public surveillance systems provide repeated measures of influenza vaccination, virologic intensity, and mortality outcomes, yet these systems were designed for monitoring rather than causal inference [1-5]. CDC burden-estimation resources and prior peer-reviewed influenza burden studies show why P&I mortality, laboratory surveillance, vaccination coverage, and hospitalization-based estimates are complementary but non-interchangeable data streams [7-10,13-16].

The original project question specified CDC WONDER mortality data. During execution, the CDC WONDER interactive endpoint did not provide a stable programmatic extract. To avoid fabricating WONDER-derived counts, this study used the official CDC/NCHS weekly jurisdiction-level P&I mortality table and CDC FluView/FluVaxView programmatic sources [1-5]. The resulting design is an ecological repeated panel in which the unit of analysis is a jurisdiction-season, not an individual participant or cohort member [19].

This framing matters because vaccination analyses can easily drift from surveillance association into individual vaccine-effectiveness claims. Individual protection, prevented outcomes, and population-level mortality all require different denominators, confounding structures, and outcome definitions [13-16]. The fixed-effects linear association remained the core model throughout the project, but the pre-COVID 2015-16 to 2019-20 era is now treated as the primary inferential window because pneumonia coding, pathogen mix, and surveillance behaviour changed after the emergence of SARS-CoV-2. Threshold detection was added during iterative review as a post hoc exploratory stress test, not as a preregistered confirmatory objective [17-19,21]. Journal and reporting-guideline resources were reviewed to keep the manuscript aligned with observational reporting requirements and public-data reproducibility expectations [6,11,12].

## Methods

### Data Sources

Mortality data came from the NCHS "Weekly Counts of Death by Jurisdiction and Select Causes of Death" public dataset (`u6jv-9ijr`) [1]. The outcome used the "Influenza and pneumonia" cause subgroup. Vaccination coverage came from CDC FluVaxView (`vh55-3he6`) [2]. Virologic descriptors came from CDC FluView WHO/NREVSS national clinical and public-health laboratory downloads [3,4]. Post-review proxy-confounder sensitivities merged annual state-level ACS measures of age structure, median household income, and poverty from the Census API [22]. Because 2020 ACS 1-year estimates were not released, 2020 proxy values were linearly interpolated from 2019 and 2021 for sensitivity analysis only. All sources were accessed on 2026-04-23, and raw downloaded files are retained in `data/raw/`.

### Study Design, Units, and Time Window

Complete influenza seasons were defined as MMWR weeks 40 through 20, spanning 2015-16 through 2022-23. The unit of analysis was a jurisdiction-season, and no individuals were followed longitudinally. The sampling universe was 51 reporting jurisdictions (50 states plus the District of Columbia) across eight seasons, yielding 408 possible state-season cells. Jurisdiction-season observations were retained when both mortality and vaccination data were available and the NCHS benchmark-based excess outcome could be computed. Non-state or unmatched NCHS jurisdictions, including New York City and Puerto Rico, were excluded. Forty-eight jurisdictions contributed at least one retained analytic cell. New York was retained in the primary analysis and excluded in a sensitivity analysis because NYC is a separately reported mortality jurisdiction but not a separate FluVaxView vaccination geography.

### Exposure

The primary exposure was cumulative December influenza vaccination coverage among persons aged >=6 months. December coverage was selected because it precedes much of the winter mortality peak while still reflecting early-season uptake. Sensitivity analyses used May all-age coverage and December coverage among adults aged >=65 years.

### Outcome

The primary outcome was seasonal net excess P&I deaths as a percentage of expected P&I deaths. Within each jurisdiction-week, the NCHS table supplies both observed P&I deaths (`number_of_deaths`) and an expected benchmark count (`average_number_of_deaths`) in the same surveillance extract [1,25]. Weekly excess was calculated as observed minus expected deaths; observed and expected values were then summed over weeks 40-20 within each jurisdiction-season, and the primary outcome was defined as `100 * (sum(observed) - sum(expected)) / sum(expected)`. We therefore preserved the table's internal observed-versus-expected benchmark contrast rather than reconstructing a separate counterfactual mortality model. The resulting outcome should be interpreted as a surveillance benchmark contrast rather than an age-standardised causal estimand [4,5,25].

### Variables, bias, and study size

The confirmatory exposure was December all-age influenza vaccination coverage, and the confirmatory outcome was net excess P&I mortality as a percentage of expected deaths. Additional linear sensitivities used May all-age coverage, December older-adult coverage, ACS proxies for age structure, median household income, and poverty, plus availability-IPW reweighting. The principal bias threats were ecological confounding, nonrandom row availability, New York/NYC geographic mismatch, and structural differences between pre-COVID and COVID-era P&I outcome generation. Study size was fixed by the available public surveillance universe of 408 possible jurisdiction-season cells; no formal sample-size calculation was applicable because the analysis used the complete observable public panel rather than prospectively enrolled units.

### Statistical Analysis

The primary inferential model was a weighted jurisdiction and season fixed-effects linear regression fit only in the pre-COVID 2015-16 to 2019-20 subset:

`excess_pct = beta1 * coverage + jurisdiction FE + season FE + error`.

The pooled eight-season weighted linear model was retained as a surveillance-oriented sensitivity, and a pooled era-interaction model tested whether the coverage slope changed after 2020:

`excess_pct = beta1 * coverage + jurisdiction FE + season FE + error`.

`excess_pct = beta1 * coverage + beta2 * covid_era + beta3 * coverage_x_covid_era + jurisdiction FE + season FE + error`.

A secondary exploratory threshold model added a hinge term:

`excess_pct = beta1 * coverage + beta2 * max(coverage - k, 0) + jurisdiction FE + season FE + error`.

The primary estimand was the expected-deaths-weighted within-season, across-jurisdiction association between coverage and excess P&I mortality in pre-COVID seasons. The weighting scheme was chosen to upweight jurisdiction-seasons contributing more expected P&I deaths; pooled eight-season, unweighted, ACS proxy-adjusted, and availability-IPW linear models were reported as sensitivities. Candidate thresholds from 20% through 60% were scanned, and the threshold minimizing BIC was retained only as a descriptive exploratory hinge [17]. Because the threshold is selected from the data, hinge coefficients, confidence intervals, and p-values are descriptive and should not be read as post-selection-corrected hypothesis tests [21]. Threshold uncertainty was summarised using jurisdiction bootstrap resampling, leave-one-season-out re-estimation, and random split-sample validation in which threshold discovery and hinge evaluation were separated across jurisdictions. All reported linear and threshold models converged with jurisdiction-clustered robust standard errors; the coded HC3 fallback was not needed for reported estimates. Sensitivity analyses excluded New York, used only jurisdictions with complete eight-season availability, reported an unweighted threshold model, used May coverage, used older-adult coverage, and fit a virus-adjusted model without season fixed effects. Additional post-review linear sensitivities added ACS proxy covariates for age structure, income, and poverty, and an availability-IPW model that reweighted retained rows using observed retention propensity across the full 408-cell universe. The retention model included December coverage, ACS age-65+, income, poverty, and season indicators; predicted retention probabilities were clipped to 0.05-0.99 before weighting, and positivity plus balance diagnostics are provided in supplementary tables. Alternative uncertainty estimators for the primary slope and pooled era-interaction term also used HC3, season-clustered, and two-way clustered covariance estimators to probe residual panel dependence. The threshold scan was not preregistered and was added after initial model fitting during iterative review; no external protocol registry was maintained for this manuscript. The virus-adjusted sensitivity model targets a different estimand because national virologic covariates vary by season and therefore cannot coexist with season fixed effects in the same specification. Potential ecological confounders that were considered but not directly adjusted included comorbidity burden, health-care access, socioeconomic context beyond the ACS proxies, and vaccine strain match; these remain residual limitations rather than resolved covariates. Analyses were implemented in Python with `statsmodels` [20].

This public aggregate-data analysis used deidentified state-season surveillance tables without individual identifiers or contact with human participants. Under the Common Rule and OHRP guidance, activities that do not obtain data through intervention or interaction with living individuals and do not obtain identifiable private information do not involve human subjects [23,24]. The work was conducted by an independent researcher without institutional affiliation; therefore no institutional review board submission channel or formal determination letter was available for this draft, and none is claimed here. The ethics statement is offered as a data-characteristics rationale rather than an institutional exemption letter. Reporting follows STROBE principles [6].

## Results

The final analytic dataset contained 333 jurisdiction-season observations from 48 jurisdictions. The sampling universe comprised 408 possible state-season cells from 51 reporting jurisdictions (50 states plus the District of Columbia) across eight influenza seasons. 333 cells were retained for analysis, 74 lacked mortality data in the NCHS table, 0 lacked vaccination data, 0 lacked both sources, and 1 failed benchmark-based outcome construction. Missingness was concentrated in 2020-21 (18 missing), 2021-22 (14 missing), 2015-16 (9 missing), with the highest jurisdictional gaps in Alaska (8 missing), District of Columbia (8 missing), Wyoming (8 missing). December all-age vaccination coverage averaged 41.9%, with a range from 27.4% to 58.8%. Mean excess P&I mortality was -0.6% of expected deaths, with a range from -31.4% to 35.9%.

In the pre-COVID primary weighted fixed-effects linear model, the point estimate for each 10 percentage-point higher December coverage was -3.1 percentage points lower excess P&I mortality (95% CI -9.9 to 3.7; p=0.376). The pooled eight-season weighted model was attenuated at -0.9 (95% CI -4.0 to 2.1; p=0.552). In the pooled era-interaction model, the pre-COVID slope remained -2.7 per 10 percentage points (95% CI -6.6 to 1.3; p=0.183), while the post-2020 slope changed by 2.3 (95% CI 0.5 to 4.1; interaction p=0.011). Unweighted, ACS proxy-adjusted, and availability-IPW linear sensitivities remained qualitatively null. Alternative uncertainty estimators for the pre-COVID primary slope all included the null, including HC3 (95% CI -11.7 to 5.6) and two-way clustering by jurisdiction and season (95% CI -9.3 to 3.2). For the pooled era-interaction term, the jurisdiction-clustered interval excluded the null (0.5 to 4.1), but the season-clustered and two-way-clustered intervals crossed the null (-2.5 to 7.0 and -2.0 to 6.6), so post-2020 slope heterogeneity should be read as suggestive rather than confirmatory.

Exploratory threshold analyses were unstable rather than confirmatory. One weighted grid search selected a mid-30% hinge candidate, but bootstrap thresholds ranged 28%-50%, leave-one-season-out thresholds ranged 34% to 41%, and split-sample validation did not provide consistent support. Across threshold specifications, nominal hinge significance appeared in the unweighted model but not in the primary weighted model, indicating specification dependence rather than a stable operational cut point.

Figure 1 shows season-level trends in mean state excess P&I mortality and vaccination coverage. Figure 4 summarizes national FluView virologic intensity and dominant subtype by season. Supplementary Figures S1-S2 retain the threshold scatter and BIC-scan diagnostics for transparency, but these figures are descriptive appendices rather than main-result graphics.

### Sensitivity Analyses

| name                                                       | n   | covariate        | slope_per_10pp | ci_low | ci_high | p_value | adj_r2 | se_type              |
| ---------------------------------------------------------- | --- | ---------------- | -------------- | ------ | ------- | ------- | ------ | -------------------- |
| Primary inferential model: pre-COVID weighted linear model | 221 | coverage_m12_all | -3.074         | -9.883 | 3.736   | 0.376   | 0.673  | cluster_jurisdiction |
| Sensitivity: pooled eight-season weighted linear model     | 333 | coverage_m12_all | -0.922         | -3.962 | 2.118   | 0.552   | 0.694  | cluster_jurisdiction |
| Sensitivity: unweighted linear model                       | 333 | coverage_m12_all | -0.661         | -3.63  | 2.308   | 0.662   | 0.555  | cluster_jurisdiction |
| Sensitivity: ACS proxy-adjusted weighted linear model      | 333 | coverage_m12_all | -0.377         | -4.048 | 3.295   | 0.841   | 0.691  | cluster_jurisdiction |
| Sensitivity: availability-IPW weighted linear model        | 333 | coverage_m12_all | -0.687         | -3.453 | 2.078   | 0.626   | 0.684  | cluster_jurisdiction |

Linear sensitivities did not rescue a precise protective association. The pooled all-era estimate was closer to the null than the pre-COVID primary estimate. The availability-IPW retention model was fit on 405 of 408 possible cells using December coverage, ACS age-65+, income, poverty, and season indicators. Predicted retention probabilities ranged from 0.270 to 0.979 at the 95th percentile after clipping to 0.05-0.99, and resulting IPW weights ranged from 0.824 to 3.018. The largest retained-versus-missing standardized difference fell from 0.797 before weighting to 0.660 after IPW, so the weighting reduced but did not eliminate observable selection imbalance. Threshold diagnostics were also specification-dependent: the unweighted threshold model crossed a nominal p<0.05 boundary whereas the primary weighted threshold model did not, reinforcing that the hinge behaves as a post hoc diagnostic rather than a stable finding.

## Figure Legends

![Figure 1. State-season trends in excess P&I mortality and December vaccination coverage.](figures/figure1_state_season_trends.png)

![Supplementary Figure S1. Exploratory threshold scatter between December all-age vaccination coverage and excess P&I mortality.](figures/figure2_threshold_scatter.png)

![Supplementary Figure S2. Exploratory BIC threshold scan from 20% to 60% December all-age coverage.](figures/figure3_threshold_scan.png)

![Figure 4. FluView virologic intensity and dominant subtype by season.](figures/figure4_fluview_virology.png)

## Discussion

This study asked a narrower question than vaccine-effectiveness research: do publicly available jurisdiction-season surveillance tables show a robust ecological association between higher influenza vaccination coverage and lower excess P&I mortality? On the evidence generated here, the answer remains no precise association detected. In the pre-COVID primary model the point estimate suggested lower excess P&I mortality at higher coverage, but the 95% CI crossed the null and remained compatible with both a meaningful protective association and a much smaller or null relationship. That uncertainty persisted, and the pooled eight-season estimate was further attenuated.

The pooled era-interaction result shows why the pre-COVID model is the more interpretable inferential summary. After 2020, pneumonia coding, respiratory-pathogen mix, and surveillance behaviour changed enough that a single pooled slope averages across structurally different outcome-generation regimes. The pooled estimate is therefore best read as a surveillance-era summary, not a single mechanism-preserving effect estimate. The interaction direction is informative, but alternative season-clustered and two-way-clustered uncertainty intervals crossed the null, so the post-2020 difference should not be overstated.

The threshold scan is informative only as a secondary diagnostic, not as support for a coverage target. The candidate hinge changed across bootstrap and leave-one-season-out re-estimation, split-sample validation did not produce consistent hinge support, and nominal statistical significance depended on whether weighting was used. A post-selection hinge may still be a hypothesis-generating surveillance feature, but it is not an implementation-ready or confirmatory threshold.

The manuscript's secondary contribution is reproducibility rather than causal attribution. The analysis shows how to replace an unusable CDC WONDER interaction path with transparent official alternatives, preserve raw files, and expose the exact workflow, harmonised dataset, and hash-pinned bundled release for inspection. That transparency matters because it makes the inferential limits visible instead of hiding them behind unverifiable extracted counts. At the same time, the epidemiologic limitations remain substantial: exposure timing changed model behaviour, missingness clustered in a subset of seasons and jurisdictions, and COVID-era seasons make P&I outcomes especially difficult to interpret because pneumonia deaths can reflect multiple respiratory pathogens and coding changes [4,5].

## Limitations

This analysis has major limitations. The design is ecological and cannot estimate individual vaccine effectiveness [19]. P&I deaths are not equivalent to laboratory-confirmed influenza deaths. The `average_number_of_deaths` field is an NCHS surveillance benchmark supplied with the dataset rather than a bespoke age-standardised counterfactual model [1,25]. Vaccination coverage is survey-derived and may vary in measurement error by jurisdiction. Although ACS proxy covariates for age structure, income, and poverty were added in sensitivity analyses, they are incomplete substitutes for age-standardised denominators, comorbidity burden, health-care access, vaccine strain match, and other time-varying ecological confounders. The 2020 ACS proxy values were interpolated because 2020 ACS 1-year estimates were not released, which is acceptable for a sensitivity analysis but not a full solution to confounding. National virologic subtype data cannot be cleanly separated from season fixed effects in the primary specification. The analysis window begins in 2015-16 because the selected programmatic mortality source supports complete-season construction from that point. New York reporting is imperfect because New York City appears as a separate mortality jurisdiction, and this is handled through sensitivity analysis rather than fully resolved.

The public-health interpretation is also bounded by the outcome definition and missingness structure. P&I mortality has long been used in influenza mortality modelling, including historical estimates of influenza-associated mortality and broader respiratory disease burden [13-15]. However, P&I is neither pathogen-specific nor age-standardised in this ecological panel, and the benchmarked outcome inherits the limits of the underlying NCHS surveillance reference. Several jurisdiction-season cells were unavailable because the NCHS table did not provide usable mortality records for them, and these gaps were concentrated in a limited number of jurisdictions and seasons rather than being uniformly distributed. The availability-IPW retention model was fit on 405 of 408 possible cells using December coverage, ACS age-65+, income, poverty, and season indicators. Predicted retention probabilities ranged from 0.270 to 0.979 at the 95th percentile after clipping to 0.05-0.99, and resulting IPW weights ranged from 0.824 to 3.018. The largest retained-versus-missing standardized difference fell from 0.797 before weighting to 0.660 after IPW, so the weighting reduced but did not eliminate observable selection imbalance. During and after the emergence of SARS-CoV-2, pneumonia coding and respiratory-virus testing patterns changed enough that COVID-era estimates should be considered surveillance signals rather than influenza-specific mortality estimates [4,5]. For this reason, the pre-COVID sensitivity analysis is part of the core interpretation rather than a peripheral appendix.

Finally, the threshold analysis inherits post-selection uncertainty. The candidate hinge was chosen by BIC from a grid, no formal post-selection correction was attempted, and the split-sample validation results were not consistent with a stable confirmatory threshold signal. The study therefore supports at most the claim that public surveillance data may contain an unstable inverse coverage-mortality signal worthy of further investigation, not that a stable vaccination threshold has been established.

## Conclusions

In public jurisdiction-season surveillance data, we did not detect a statistically significant ecological association between higher December influenza vaccination coverage and lower excess P&I mortality in the pre-COVID primary analysis, and the 95% CI crossed the null. Pooled all-era estimates were additionally limited by COVID-era heterogeneity. Exploratory threshold signals were unstable and model-dependent. The most defensible contribution of this work is therefore a transparent, fully inspectable demonstration of the inferential limits of current programmatic CDC/NCHS, FluVaxView, and FluView data rather than a causal or implementation-ready vaccination target.

## Patient and Public Involvement

Patients and the public were not involved in the design, conduct, reporting, or dissemination planning of this study because the analysis used only publicly released aggregate surveillance tables.

## Data Availability

All source data are public and programmatically accessible from CDC/NCHS, CDC FluView, and the Census API [1-5,22]. A journal-facing public review mirror is available at GitHub repository `TerryFYL/ai-research-army`, directory `public_release/C052` (https://github.com/TerryFYL/ai-research-army/tree/main/public_release/C052). Public files include `reproduce_main_analysis.py`, `reproducibility_manifest.json`, `strobe_checklist.md`, `cdc_wonder_replacement_protocol.md`, and key supplementary result tables. The manuscript-specific frozen review bundle accompanying this submission in `submission_package/` contains the harmonised analytic dataset `analysis_ready.csv`, `manuscript.md`, `acs_state_covariates.csv`, the full package-build script `build_c052_package.py`, peer-review DOCX files, and the SHA-256 provenance manifest.

## Code Availability

A compact public reproduction script for the primary and interaction linear models is available at https://github.com/TerryFYL/ai-research-army/blob/main/public_release/C052/reproduce_main_analysis.py. The full manuscript-packaging script `build_c052_package.py` is duplicated inside `submission_package/`. Manuscript-specific version provenance, SHA-256 hashes, and the parent repository commit are recorded in `reproducibility_manifest.json`.

## Ethics Statement

The study used public aggregate surveillance data without individual identifiers, interaction with human participants, or access to non-public records. Under the Common Rule and OHRP guidance, this activity was treated as not human-subjects research because no identifiable private information was obtained [23,24]. The work was conducted by an independent researcher without institutional affiliation, so no institutional IRB submission channel or formal determination letter was available for this draft; no institutional exemption letter is claimed here. The statement is therefore a description of the data characteristics and review context rather than an institutional ethics determination. Informed consent was not applicable.

## Funding

No external funding was used.

## Competing Interests

The author declares no competing interests.

## References

1. Centers for Disease Control and Prevention. Weekly Counts of Death by Jurisdiction and Select Causes of Death. Data.CDC.gov dataset u6jv-9ijr. Accessed 2026-04-23. https://data.cdc.gov/NCHS/Weekly-Counts-of-Death-by-Jurisdiction-and-Select-/u6jv-9ijr
2. Centers for Disease Control and Prevention. Influenza Vaccination Coverage for All Ages 6 Months and Older. Data.CDC.gov dataset vh55-3he6. Accessed 2026-04-23. https://data.cdc.gov/Flu-Vaccinations/Influenza-Vaccination-Coverage-for-All-Ages-6-Mont/vh55-3he6
3. Centers for Disease Control and Prevention. FluView Interactive: National, Regional, and State Level Outpatient Illness and Viral Surveillance. Accessed 2026-04-23. https://www.cdc.gov/fluview/overview/fluview-interactive.html
4. Centers for Disease Control and Prevention. U.S. Influenza Surveillance: Purpose and Methods. Accessed 2026-04-23. https://www.cdc.gov/fluview/overview/index.html
5. Centers for Disease Control and Prevention. National Center for Health Statistics Mortality Surveillance System. Accessed 2026-04-23. https://gis.cdc.gov/grasp/fluview/mortality.html
6. STROBE Initiative. STROBE checklists for observational studies. Accessed 2026-04-23. https://www.strobe-statement.org/checklists/
7. Centers for Disease Control and Prevention. FluView weekly influenza surveillance reports. Accessed 2026-04-23. https://www.cdc.gov/fluview/
8. National Center for Health Statistics. Vital Statistics Rapid Release and provisional mortality data resources. Accessed 2026-04-23. https://www.cdc.gov/nchs/nvss/vsrr/
9. Centers for Disease Control and Prevention. Flu vaccination coverage, United States, historical seasonal reports. Accessed 2026-04-23. https://www.cdc.gov/flu/fluvaxview/
10. Centers for Disease Control and Prevention. National Respiratory and Enteric Virus Surveillance System overview. Accessed 2026-04-23. https://www.cdc.gov/surveillance/nrevss/
11. BMJ Open. Instructions for authors: observational studies and reporting guidelines. Accessed 2026-04-23. https://bmjopen.bmj.com/pages/authors/
12. Equator Network. Reporting guidelines for observational studies. Accessed 2026-04-23. https://www.equator-network.org/
13. Thompson WW, Shay DK, Weintraub E, Brammer L, Cox N, Anderson LJ, Fukuda K. Mortality associated with influenza and respiratory syncytial virus in the United States. JAMA. 2003;289:179-186. doi: 10.1001/jama.289.2.179. https://pubmed.ncbi.nlm.nih.gov/12517228/
14. Rolfes MA, Foppa IM, Garg S, Flannery B, Brammer L, Singleton JA, et al. Annual estimates of the burden of seasonal influenza in the United States: a tool for strengthening influenza surveillance and preparedness. Influenza Other Respir Viruses. 2018;12:132-137. doi: 10.1111/irv.12486. https://pmc.ncbi.nlm.nih.gov/articles/PMC5818346/
15. Reed C, Chaves SS, Daily Kirley P, Emerson R, Aragon D, Hancock EB, et al. Estimating influenza disease burden from population-based surveillance data in the United States. PLoS One. 2015;10:e0118369. doi: 10.1371/journal.pone.0118369. https://pmc.ncbi.nlm.nih.gov/articles/PMC4349859/
16. Rolfes MA, Flannery B, Chung JR, O'Halloran A, Garg S, Belongia EA, et al. Effects of influenza vaccination in the United States during the 2017-2018 influenza season. Clin Infect Dis. 2019;69:1845-1853. doi: 10.1093/cid/ciz075. https://pubmed.ncbi.nlm.nih.gov/30715278/
17. Muggeo VMR. Estimating regression models with unknown break-points. Stat Med. 2003;22:3055-3071. doi: 10.1002/sim.1545. https://doi.org/10.1002/sim.1545
18. Arellano M. Computing robust standard errors for within-groups estimators. Oxf Bull Econ Stat. 1987;49:431-434. doi: 10.1111/j.1468-0084.1987.mp49004006.x. https://doi.org/10.1111/j.1468-0084.1987.mp49004006.x
19. Morgenstern H. Ecologic studies in epidemiology: concepts, principles, and methods. Annu Rev Public Health. 1995;16:61-81. doi: 10.1146/annurev.pu.16.050195.000425. https://doi.org/10.1146/annurev.pu.16.050195.000425
20. Seabold S, Perktold J. Statsmodels: Econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference. 2010:92-96. doi: 10.25080/MAJORA-92BF1922-011. https://conference.scipy.org.s3-website-us-east-1.amazonaws.com/proceedings/scipy2010/pdfs/seabold.pdf
21. Taylor J, Tibshirani RJ. Statistical learning and selective inference. Proc Natl Acad Sci U S A. 2015;112:7629-7634. doi: 10.1073/pnas.1507583112. https://pubmed.ncbi.nlm.nih.gov/26100887/
22. U.S. Census Bureau. American Community Survey 1-year tables accessed via the Census API. Accessed 2026-04-23. https://api.census.gov/data.html
23. U.S. Department of Health and Human Services, Office for Human Research Protections. 45 CFR 46. Accessed 2026-04-23. https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/index.html
24. U.S. Department of Health and Human Services, Office for Human Research Protections. Coded Private Information or Specimens Use in Research, Guidance (2008). Accessed 2026-04-23. https://www.hhs.gov/ohrp/regulations-and-policy/guidance/research-involving-coded-private-information/index.html
25. Centers for Disease Control and Prevention. CDC FluView: Pneumonia, Influenza, and COVID-19 Mortality Surveillance Data, Application Quick Reference Guide. Accessed 2026-04-23. https://gis.cdc.gov/grasp/fluview/FluViewPhase7QuickReferenceGuide.pdf
