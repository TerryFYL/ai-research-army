# Influenza Vaccination Coverage and Excess Pneumonia-and-Influenza Mortality in US Jurisdictions During the 2015-16 to 2022-23 Influenza Seasons: an ecological repeated panel analysis

TerryFengYilou

Target journal: BMJ Open

## Abstract

**Objectives:** To estimate the primary ecological association between state-season influenza vaccination coverage and excess pneumonia-and-influenza (P&I) mortality, and secondarily to assess whether public surveillance data suggested an exploratory coverage threshold.

**Design:** Ecological repeated panel observational analysis using official CDC/NCHS and CDC FluView public data; no individual participants were enrolled or followed.

**Setting and units of analysis:** 333 jurisdiction-season observations from 48 US jurisdictions across complete influenza seasons 2015-16 through 2022-23.

**Exposures:** Primary exposure was cumulative December influenza vaccination coverage among persons aged >=6 months from CDC FluVaxView.

**Main outcome measure:** Seasonal net excess P&I deaths, expressed as percentage of NCHS expected P&I deaths, aggregated across MMWR weeks 40-20.

**Results:** Mean December all-age vaccination coverage was 41.9% (range 27.4% to 58.8%). Mean state-season excess P&I mortality was -0.6% of expected deaths. In the primary weighted fixed-effects linear model, the point estimate for each 10 percentage-point higher December coverage was -0.9 percentage points lower excess P&I mortality, but the 95% CI crossed the null (-4.0 to 2.1; p=0.552). A secondary, model-dependent grid search suggested a candidate hinge region in the mid-30% range; bootstrap thresholds ranged 28%-50%, leave-one-season-out thresholds ranged 34%-41%, and split-sample validation did not provide consistent hinge support.

**Conclusions:** Programmatic CDC/NCHS and FluView data can support transparent ecological surveillance analyses of vaccination coverage and excess P&I mortality. In this ecological repeated panel, the primary linear association was imprecise and the candidate threshold was model-dependent, post-selection, and suitable only as a surveillance signal rather than a causal or implementation-ready target.

## Strengths and Limitations

- This analysis uses official, programmatically downloadable CDC/NCHS and CDC FluView sources with raw files and code retained [1-5].
- The analysis does not fabricate CDC WONDER outputs. CDC WONDER was replaced by a transparent NCHS/FluView open-data mortality table because the interactive endpoint did not yield stable machine-readable output during execution [1,5].
- The primary estimand is the expected-deaths-weighted within-season, across-jurisdiction association per 10 percentage-point higher coverage; an unweighted sensitivity analysis is reported alongside it.
- The threshold analysis is secondary and explicitly post-selection; its uncertainty is described with bootstrap, leave-one-season-out, and split-sample validation checks [17,21].
- State and season fixed effects reduce, but do not eliminate, confounding by jurisdictional reporting, health-system differences, epidemic timing, and season severity [18,19].
- P&I mortality is a surveillance proxy, not laboratory-confirmed influenza mortality; pneumonia deaths during COVID-era seasons can reflect SARS-CoV-2 and other respiratory pathogens [4,5].
- Vaccination coverage is ecological and survey-derived; the analysis cannot estimate individual-level vaccine effectiveness.

## Introduction

Seasonal influenza vaccination is a core public-health intervention, but translating individual protection and population coverage into jurisdiction-level mortality patterns is methodologically difficult. US public surveillance systems provide repeated measures of influenza vaccination, virologic intensity, and mortality outcomes, yet these systems were designed for monitoring rather than causal inference [1-5]. CDC burden-estimation resources and prior peer-reviewed influenza burden studies show why P&I mortality, laboratory surveillance, vaccination coverage, and hospitalization-based estimates are complementary but non-interchangeable data streams [7-10,13-16].

The original project question specified CDC WONDER mortality data. During execution, the CDC WONDER interactive endpoint did not provide a stable programmatic extract. To avoid fabricating WONDER-derived counts, this study used the official CDC/NCHS weekly jurisdiction-level P&I mortality table and CDC FluView/FluVaxView programmatic sources [1-5]. The resulting design is an ecological repeated panel in which the unit of analysis is a jurisdiction-season, not an individual participant or cohort member [19].

This framing matters because vaccination analyses can easily drift from surveillance association into individual vaccine-effectiveness claims. Individual protection, prevented outcomes, and population-level mortality all require different denominators, confounding structures, and outcome definitions [13-16]. The primary estimand in this study is therefore the adjusted burden-weighted change in excess P&I mortality associated with a 10 percentage-point higher December vaccination coverage. Threshold detection is a secondary exploratory analysis intended to stress-test whether a candidate hinge is visible in public surveillance data, not to declare an actionable coverage cut point [17-19,21]. Journal and reporting-guideline resources were reviewed to keep the manuscript aligned with observational reporting requirements and public-data reproducibility expectations [6,11,12].

## Methods

### Data Sources

Mortality data came from the NCHS "Weekly Counts of Death by Jurisdiction and Select Causes of Death" public dataset (`u6jv-9ijr`) [1]. The outcome used the "Influenza and pneumonia" cause subgroup. Vaccination coverage came from CDC FluVaxView (`vh55-3he6`) [2]. Virologic descriptors came from CDC FluView WHO/NREVSS national clinical and public-health laboratory downloads [3,4]. All sources were accessed on 2026-04-23, and raw downloaded files are retained in `data/raw/`.

### Study Design, Units, and Time Window

Complete influenza seasons were defined as MMWR weeks 40 through 20, spanning 2015-16 through 2022-23. The unit of analysis was a jurisdiction-season, and no individuals were followed longitudinally. Jurisdiction-season observations were retained when both mortality and vaccination data were available and the NCHS benchmark-based excess outcome could be computed. Non-state or unmatched NCHS jurisdictions, including New York City and Puerto Rico, were excluded. New York was retained in the primary analysis and excluded in a sensitivity analysis because NYC is a separately reported mortality jurisdiction but not a separate FluVaxView vaccination geography.

### Exposure

The primary exposure was cumulative December influenza vaccination coverage among persons aged >=6 months. December coverage was selected because it precedes much of the winter mortality peak while still reflecting early-season uptake. Sensitivity analyses used May all-age coverage and December coverage among adults aged >=65 years.

### Outcome

The primary outcome was seasonal net excess P&I deaths as a percentage of expected P&I deaths. Weekly excess was calculated as observed P&I deaths minus the dataset-provided NCHS expected benchmark count (`average_number_of_deaths`); weekly values were summed over weeks 40-20 and divided by summed expected deaths. We used the official benchmark distributed with the surveillance table and did not reconstruct a separate counterfactual mortality model. The resulting excess outcome should therefore be interpreted as a surveillance benchmark contrast rather than an age-standardised causal estimand [4,5].

### Statistical Analysis

The primary model was a weighted jurisdiction and season fixed-effects linear regression:

`excess_pct = beta1 * coverage + jurisdiction FE + season FE + error`.

A secondary exploratory threshold model added a hinge term:

`excess_pct = beta1 * coverage + beta2 * max(coverage - k, 0) + jurisdiction FE + season FE + error`.

The primary estimand was the expected-deaths-weighted within-season, across-jurisdiction association between coverage and excess P&I mortality. The weighting scheme was chosen to upweight jurisdiction-seasons contributing more expected P&I deaths; an unweighted linear model was reported as a sensitivity analysis to show whether this burden weighting altered qualitative interpretation.

Candidate thresholds from 20% through 60% were scanned, and the threshold minimizing BIC was retained as a descriptive candidate hinge [17]. Because the threshold is selected from the data, hinge coefficients, confidence intervals, and p-values are descriptive and should not be read as post-selection-corrected hypothesis tests [21]. Threshold uncertainty was summarised using jurisdiction bootstrap resampling, leave-one-season-out re-estimation, and random split-sample validation in which threshold discovery and hinge evaluation were separated across jurisdictions. Cluster-robust standard errors by jurisdiction were used when estimable [18]. Sensitivity analyses restricted to pre-COVID seasons, excluded New York, used only jurisdictions with complete eight-season availability, reported an unweighted threshold model, used May coverage, used older-adult coverage, and fit a virus-adjusted model without season fixed effects. The virus-adjusted sensitivity model targets a different estimand because national virologic covariates vary by season and therefore cannot coexist with season fixed effects in the same specification. Potential ecological confounders that were considered but not directly adjusted included age structure, comorbidity burden, health-care access, socioeconomic context, and vaccine strain match; these were not consistently available at the required jurisdiction-season resolution and are therefore treated as residual limitations rather than resolved covariates. Analyses were implemented in Python with `statsmodels` [20].

This public aggregate-data analysis used deidentified surveillance tables and did not require institutional review board review. Reporting follows STROBE principles [6].

## Results

The final analytic dataset contained 333 jurisdiction-season observations from 48 jurisdictions. Of 408 possible jurisdiction-season cells, 333 were retained, 74 lacked mortality data in the NCHS table, 0 lacked vaccination data, 0 lacked both sources, and 1 had incomplete benchmark fields after merging. Missingness was concentrated in 2020-21 (18 missing), 2021-22 (14 missing), 2015-16 (9 missing), with the highest jurisdictional gaps in Alaska (8 missing), District of Columbia (8 missing), Wyoming (8 missing). December all-age vaccination coverage averaged 41.9%, with a range from 27.4% to 58.8%. Mean excess P&I mortality was -0.6% of expected deaths, with a range from -31.4% to 35.9%.

In the primary weighted fixed-effects linear model, the point estimate for each 10 percentage-point higher December coverage was -0.9 percentage points lower excess P&I mortality (95% CI -4.0 to 2.1; p=0.552). The unweighted linear sensitivity was similar in direction and remained imprecise at -0.7 (95% CI -3.6 to 2.3; p=0.662).

The exploratory threshold scan identified a model-dependent hinge region centered in the mid-30% range; one best-scoring grid point occurred at 34%, but no post-selection-corrected confirmatory threshold inference was attempted. At that grid point, the below-threshold descriptive slope was -16.5 percentage points of excess P&I mortality per 10 percentage points higher coverage (95% CI -36.2 to 3.2), the corresponding hinge p-value was 0.121, bootstrap thresholds were wide with median 34%, IQR 33%-39%, and range 28%-50%, and leave-one-season-out thresholds ranged from 34% to 41%. In 200 random split-sample validations, discovery thresholds had median 36% (IQR 34%-41%), the median validation hinge p-value was 0.372, and only 16.5% of validation splits had p<0.05. These results indicate a surveillance signal rather than confirmatory threshold evidence.

Figure 1 shows season-level trends in mean state excess P&I mortality and vaccination coverage. Figure 2 displays the ecological state-season association with the selected threshold. Figure 3 presents the BIC scan. Figure 4 summarizes national FluView virologic intensity and dominant subtype by season.

### Sensitivity Analyses

| name                                                           | n   | covariate              | below_slope_per_10pp | below_ci_low | below_ci_high | above_slope_per_10pp | above_ci_low | above_ci_high | p_hinge |
| -------------------------------------------------------------- | --- | ---------------------- | -------------------- | ------------ | ------------- | -------------------- | ------------ | ------------- | ------- |
| Primary: all complete seasons, December all-age coverage       | 333 | coverage_m12_all       | -16.522              | -36.241      | 3.197         | -0.432               | -3.466       | 2.601         | 0.121   |
| Sensitivity: pre-COVID seasons only                            | 221 | coverage_m12_all       | -19.354              | -42.945      | 4.237         | -1.892               | -8.907       | 5.124         | 0.178   |
| Sensitivity: exclude New York jurisdiction                     | 325 | coverage_m12_all       | -15.2                | -34.526      | 4.125         | -1.153               | -4.111       | 1.805         | 0.167   |
| Sensitivity: complete-availability jurisdictions only          | 256 | coverage_m12_all       | -14.379              | -34.339      | 5.582         | -0.217               | -3.329       | 2.895         | 0.18    |
| Sensitivity: unweighted threshold model                        | 333 | coverage_m12_all       | -19.26               | -35.773      | -2.747        | 0.141                | -3.016       | 3.298         | 0.026   |
| Sensitivity: May all-age coverage                              | 333 | coverage_m5_all        | -2.739               | -3.674       | -1.804        | -0.195               | -2.789       | 2.398         | 0.14    |
| Sensitivity: December age 65+ coverage                         | 333 | coverage_m12_age65plus | -2.337               | -4.092       | -0.581        | -0.675               | -3.094       | 1.743         | 0.429   |
| Sensitivity: virus-adjusted model without season fixed effects | 333 | coverage_m12_all       | -38.237              | -61.346      | -15.128       | -5.099               | -8.175       | -2.023        | 0.005   |

Sensitivity results reinforced model dependence rather than providing confirmatory threshold evidence. Restricting the analysis to the 32 jurisdictions with all eight retained seasons still yielded a below-threshold descriptive slope of -14.4 with hinge p=0.180, indicating that complete-availability restriction did not resolve uncertainty. The unweighted threshold sensitivity yielded hinge p=0.026, showing that threshold behaviour depends materially on the weighting choice rather than converging on a stable signal. The virus-adjusted model without season fixed effects yielded a stronger inverse below-threshold slope of -38.2 with hinge p=0.005, but this specification estimates a different contrast because season effects are no longer absorbed by fixed effects. The May coverage model also produced a materially different pattern, with a below-threshold 95% CI of -3.7 to -1.8 and hinge p=0.140, indicating that threshold behavior depends on exposure timing and model choice rather than converging on a single stable cut point.

## Figure Legends

![Figure 1. State-season trends in excess P&I mortality and December vaccination coverage.](figures/figure1_state_season_trends.png)

![Figure 2. Ecological state-season association between December all-age vaccination coverage and excess P&I mortality.](figures/figure2_threshold_scatter.png)

![Figure 3. Exploratory BIC threshold scan from 20% to 60% December all-age coverage.](figures/figure3_threshold_scan.png)

![Figure 4. National FluView virologic intensity and dominant public-health-laboratory subtype by season.](figures/figure4_fluview_virology.png)

## Discussion

This reproducible surveillance analysis found that official CDC/NCHS and CDC FluView public data can be integrated into a jurisdiction-season panel assessing vaccination coverage and excess P&I mortality. The main quantitative result is the burden-weighted linear association, not the threshold scan. In both weighted and unweighted linear models, the point estimate suggested lower excess P&I mortality at higher December coverage, but the confidence interval crossed the null and the result remained imprecise. This makes the manuscript more useful as a transparent surveillance methods paper than as a definitive inferential study.

The threshold scan is still informative, but only as a secondary diagnostic. The candidate hinge changed across bootstrap and leave-one-season-out re-estimation, the below-threshold confidence interval crossed zero, and split-sample validation did not produce consistent hinge support. The stronger signal in the virus-adjusted model without season fixed effects indicates that threshold evidence is specification-dependent, not convergent. This distinction is important for peer review: a post-selection hinge can be a useful surveillance signal, but it is not an implementation-ready coverage target.

Several findings remain practically important even without a confirmatory threshold. First, programmatic data sources are sufficient for rapid, auditable analyses without manually extracting or fabricating CDC WONDER outputs. Second, December vaccination coverage appears more interpretable than end-of-season May coverage in this dataset, but exposure timing meaningfully alters threshold behavior. Third, missingness is not randomly sprinkled across the panel; it clusters in specific jurisdictions and seasons, which means any generalisation should be made cautiously. Fourth, COVID-era seasons create a major interpretive problem for P&I outcomes because pneumonia deaths can reflect multiple respiratory pathogens and coding changes [4,5]. Any future causal analysis should incorporate age-specific mortality, age-standardised denominators, individual-level vaccination status where available, explicit competing respiratory pathogen indicators, and richer jurisdiction-level confounder data.

## Limitations

This analysis has major limitations. The design is ecological and cannot estimate individual vaccine effectiveness [19]. P&I deaths are not equivalent to laboratory-confirmed influenza deaths. The `average_number_of_deaths` field is an NCHS surveillance benchmark supplied with the dataset rather than a bespoke age-standardised counterfactual model. Vaccination coverage is survey-derived and may vary in measurement error by jurisdiction. Key ecological confounders including age structure, comorbidity burden, socioeconomic context, health-care access, and vaccine strain match were not directly adjusted because comparable jurisdiction-season data were not consistently available. National virologic subtype data cannot be cleanly separated from season fixed effects in the primary specification. The analysis window begins in 2015-16 because the selected programmatic mortality source supports complete-season construction from that point. New York reporting is imperfect because New York City appears as a separate mortality jurisdiction, and this is handled through sensitivity analysis rather than fully resolved.

The public-health interpretation is also bounded by the outcome definition and missingness structure. P&I mortality has long been used in influenza mortality modelling, including historical estimates of influenza-associated mortality and broader respiratory disease burden [13-15]. However, P&I is neither pathogen-specific nor age-standardised in this ecological panel. Several jurisdiction-season cells were unavailable because the NCHS table did not provide usable mortality records for them, and these gaps were concentrated in a limited number of jurisdictions and seasons rather than being uniformly distributed. During and after the emergence of SARS-CoV-2, pneumonia coding and respiratory-virus testing patterns changed enough that COVID-era estimates should be considered surveillance signals rather than influenza-specific mortality estimates [4,5]. For this reason, the pre-COVID sensitivity analysis is part of the core interpretation rather than a peripheral appendix.

Finally, the threshold analysis inherits post-selection uncertainty. The candidate hinge was chosen by BIC from a grid, no formal post-selection correction was attempted, and the split-sample validation results were not consistent with a stable confirmatory threshold signal. The study therefore supports at most the claim that public surveillance data may contain an inverse coverage-mortality signal worthy of further investigation, not that a stable vaccination threshold has been established.

## Conclusions

A reproducible open-data panel can evaluate ecological associations between influenza vaccination coverage and excess P&I mortality, but it cannot establish a causal or implementation-ready vaccination threshold. The most defensible contribution of this work is methodological transparency for public-health surveillance: it shows exactly what can and cannot be inferred from current programmatic CDC/NCHS, FluVaxView, and FluView public surveillance data, and it makes threshold uncertainty explicit rather than overstating a model-dependent hinge result.

## Patient and Public Involvement

Patients and the public were not involved in the design, conduct, reporting, or dissemination planning of this study because the analysis used only publicly released aggregate surveillance tables.

## Data Availability

All source data are public and programmatically accessible from CDC/NCHS and CDC FluView sources [1-5]. The broader workflow code base is mirrored publicly at https://github.com/TerryFYL/ai-research-army. The manuscript-specific frozen release bundle, harmonised analysis dataset, and reproducibility manifest used for this review are available from the corresponding author for peer-review inspection while project-specific public archival deposition is finalized.

## Code Availability

The reproducible analysis workflow is implemented in Python within the public `ai-research-army` code base. Manuscript-specific version provenance, SHA-256 hashes, and the parent repository commit are recorded in the reproducibility manifest available from the corresponding author for this review bundle.

## Ethics Statement

The study used public aggregate surveillance data without individual identifiers. No human-subjects approval was required, and informed consent was not applicable.

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
16. Rolfes MA, Flannery B, Chung JR, O'Halloran A, Garg S, Belongia EA, et al. Effects of influenza vaccination in the United States during the 2017-2018 influenza season. Clin Infect Dis. 2019. https://pubmed.ncbi.nlm.nih.gov/30715278/
17. Muggeo VMR. Estimating regression models with unknown break-points. Stat Med. 2003;22:3055-3071. doi: 10.1002/sim.1545. https://doi.org/10.1002/sim.1545
18. Arellano M. Computing robust standard errors for within-groups estimators. Oxf Bull Econ Stat. 1987;49:431-434. doi: 10.1111/j.1468-0084.1987.mp49004006.x. https://doi.org/10.1111/j.1468-0084.1987.mp49004006.x
19. Morgenstern H. Ecologic studies in epidemiology: concepts, principles, and methods. Annu Rev Public Health. 1995;16:61-81. doi: 10.1146/annurev.pu.16.050195.000425. https://doi.org/10.1146/annurev.pu.16.050195.000425
20. Seabold S, Perktold J. Statsmodels: Econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference. 2010:92-96. doi: 10.25080/MAJORA-92BF1922-011. https://conference.scipy.org.s3-website-us-east-1.amazonaws.com/proceedings/scipy2010/pdfs/seabold.pdf
21. Taylor J, Tibshirani RJ. Statistical learning and selective inference. Proc Natl Acad Sci U S A. 2015;112:7629-7634. doi: 10.1073/pnas.1507583112. https://pubmed.ncbi.nlm.nih.gov/26100887/
