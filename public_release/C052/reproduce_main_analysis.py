#!/usr/bin/env python3
"""Reproduce the main C052 linear analyses from analysis_ready.csv."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups


PRIMARY_FORMULA = "net_excess_pct_of_expected ~ coverage_m12_all + C(jurisdiction) + C(year_season)"
INTERACTION_FORMULA = (
    "net_excess_pct_of_expected ~ coverage_m12_all + covid_era + coverage_x_covid_era + "
    "C(jurisdiction) + C(year_season)"
)


def normal_two_sided_p(z_score: float) -> float:
    return math.erfc(abs(float(z_score)) / math.sqrt(2.0))


def robust_row(fit, term: str, label: str, *, scale: float = 10.0, groups=None) -> dict[str, float | str]:
    names = list(fit.model.exog_names)
    term_idx = names.index(term)
    if label == "HC3":
        robust = fit.get_robustcov_results(cov_type="HC3")
        beta = float(robust.params[term_idx])
        se = float(robust.bse[term_idx])
        p_value = float(robust.pvalues[term_idx])
    elif label == "Two-way clustered (jurisdiction + season)":
        cov_both, _, _ = cov_cluster_2groups(
            fit,
            group=pd.Categorical(fit.model.data.frame["jurisdiction"]).codes,
            group2=pd.Categorical(fit.model.data.frame["year_season"]).codes,
        )
        beta = float(fit.params.iloc[term_idx])
        se = math.sqrt(max(float(cov_both[term_idx, term_idx]), 0.0))
        p_value = normal_two_sided_p(beta / max(se, 1e-12))
    else:
        robust = fit.get_robustcov_results(cov_type="cluster", groups=groups)
        beta = float(robust.params[term_idx])
        se = float(robust.bse[term_idx])
        p_value = float(robust.pvalues[term_idx])
    return {
        "term": term,
        "se_scheme": label,
        "estimate_per_10pp": beta * scale,
        "ci_low": (beta - 1.96 * se) * scale,
        "ci_high": (beta + 1.96 * se) * scale,
        "p_value": p_value,
    }


def fit_weighted(df: pd.DataFrame, formula: str):
    return smf.wls(formula, data=df, weights=df["weight"]).fit()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).resolve().with_name("analysis_ready.csv"),
        help="Path to the C052 analysis_ready.csv file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().with_name("reproduction_outputs"),
        help="Directory for JSON/CSV outputs.",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    df["coverage_x_covid_era"] = df["coverage_m12_all"] * df["covid_era"]
    precovid = df[df["season_start"] <= 2019].copy()
    if precovid.empty:
        raise RuntimeError("Pre-COVID subset is empty")

    primary_fit = fit_weighted(precovid, PRIMARY_FORMULA)
    pooled_fit = fit_weighted(df, PRIMARY_FORMULA)
    interaction_fit = fit_weighted(df, INTERACTION_FORMULA)

    primary_rows = [
        robust_row(primary_fit, "coverage_m12_all", "HC3"),
        robust_row(primary_fit, "coverage_m12_all", "Jurisdiction-clustered", groups=precovid["jurisdiction"]),
        robust_row(primary_fit, "coverage_m12_all", "Season-clustered", groups=precovid["year_season"]),
        robust_row(primary_fit, "coverage_m12_all", "Two-way clustered (jurisdiction + season)"),
    ]
    interaction_rows = [
        robust_row(interaction_fit, "coverage_x_covid_era", "HC3"),
        robust_row(interaction_fit, "coverage_x_covid_era", "Jurisdiction-clustered", groups=df["jurisdiction"]),
        robust_row(interaction_fit, "coverage_x_covid_era", "Season-clustered", groups=df["year_season"]),
        robust_row(interaction_fit, "coverage_x_covid_era", "Two-way clustered (jurisdiction + season)"),
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(primary_rows).to_csv(args.output_dir / "primary_precovid_alternative_inference.csv", index=False)
    pd.DataFrame(interaction_rows).to_csv(args.output_dir / "era_interaction_alternative_inference.csv", index=False)

    pooled_cluster = pooled_fit.get_robustcov_results(
        cov_type="cluster",
        groups=df["jurisdiction"],
    )
    pooled_idx = list(pooled_fit.model.exog_names).index("coverage_m12_all")
    summary = {
        "data_file": str(args.data),
        "n_rows": int(df.shape[0]),
        "n_precovid_rows": int(precovid.shape[0]),
        "primary_formula": PRIMARY_FORMULA,
        "interaction_formula": INTERACTION_FORMULA,
        "primary_precovid_jurisdiction_clustered_slope_per_10pp": primary_rows[1]["estimate_per_10pp"],
        "primary_precovid_jurisdiction_clustered_ci": [
            primary_rows[1]["ci_low"],
            primary_rows[1]["ci_high"],
        ],
        "pooled_jurisdiction_clustered_slope_per_10pp": float(pooled_cluster.params[pooled_idx]) * 10.0,
        "pooled_jurisdiction_clustered_p_value": float(pooled_cluster.pvalues[pooled_idx]),
        "era_interaction_jurisdiction_clustered_delta_per_10pp": interaction_rows[1]["estimate_per_10pp"],
        "era_interaction_jurisdiction_clustered_ci": [
            interaction_rows[1]["ci_low"],
            interaction_rows[1]["ci_high"],
        ],
    }
    (args.output_dir / "reproduction_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
