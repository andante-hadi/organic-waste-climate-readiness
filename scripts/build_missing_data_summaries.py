from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

ANALYSIS_FILE = PROCESSED / "country_ofmsw_analysis_dataset.csv"
READINESS_FILE = PROCESSED / "country_ofmsw_readiness_index.csv"


VARIABLE_GROUPS = {
    "MSW generation": ["msw_2022_tpy"],
    "Food/green composition": ["food_frac", "green_frac"],
    "Disposal/treatment shares": [
        "treatment_open_dump_frac",
        "treatment_controlled_landfill_frac",
        "treatment_sanitary_landfill_frac",
        "treatment_unspecified_landfill_frac",
        "treatment_uncollected_frac",
        "treatment_unaccounted_frac",
    ],
    "Collection coverage": [
        "collection_total_population_frac",
        "collection_total_weight_frac",
    ],
    "WDI development covariates": [
        "gdp_per_capita_current_usd_2022",
        "urban_population_pct_2022",
    ],
    "Electricity carbon intensity": [
        "electricity_carbon_intensity_2022_gco2_kwh",
    ],
}


def has_group_data(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    available_columns = [col for col in columns if col in df.columns]
    if not available_columns:
        return pd.Series(False, index=df.index)
    return df[available_columns].notna().any(axis=1)


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    analysis = pd.read_csv(ANALYSIS_FILE)
    readiness = pd.read_csv(READINESS_FILE)

    data = analysis.merge(
        readiness[
            [
                "iso3",
                "best_four_pathway_screen",
                "opportunity_readiness_class",
            ]
        ],
        on="iso3",
        how="left",
        validate="1:1",
    )
    data = data[(data["iso3"].notna()) & (data["iso3"] != "iso3c")].copy()
    data["has_pathway_assignment"] = data["best_four_pathway_screen"].notna()
    data["is_missing_or_insufficient"] = ~data["has_pathway_assignment"]

    variable_rows = []
    for group, cols in VARIABLE_GROUPS.items():
        has_data = has_group_data(data, cols)
        variable_rows.append(
            {
                "variable_group": group,
                "countries_with_any_data": int(has_data.sum()),
                "countries_missing_all_group_fields": int((~has_data).sum()),
                "coverage_pct": round(float(has_data.mean() * 100), 1),
            }
        )
    pd.DataFrame(variable_rows).to_csv(
        OUTPUTS / "summary_missingness_by_variable_group.csv",
        index=False,
    )

    missing_by_region = (
        data.groupby("region", dropna=False)
        .agg(
            countries=("iso3", "count"),
            pathway_assigned=("has_pathway_assignment", "sum"),
            missing_or_insufficient=("is_missing_or_insufficient", "sum"),
        )
        .reset_index()
    )
    missing_by_region["missing_or_insufficient_pct"] = (
        missing_by_region["missing_or_insufficient"]
        / missing_by_region["countries"]
        * 100
    ).round(1)
    missing_by_region.to_csv(OUTPUTS / "summary_missingness_by_region.csv", index=False)

    missing_by_income = (
        data.groupby("income_2022", dropna=False)
        .agg(
            countries=("iso3", "count"),
            pathway_assigned=("has_pathway_assignment", "sum"),
            missing_or_insufficient=("is_missing_or_insufficient", "sum"),
        )
        .reset_index()
    )
    missing_by_income["missing_or_insufficient_pct"] = (
        missing_by_income["missing_or_insufficient"]
        / missing_by_income["countries"]
        * 100
    ).round(1)
    missing_by_income.to_csv(OUTPUTS / "summary_missingness_by_income.csv", index=False)

    missing_countries = data.loc[
        data["is_missing_or_insufficient"],
        [
            "iso3",
            "country",
            "region",
            "income_2022",
            "msw_2022_tpy",
            "food_frac",
            "green_frac",
            "landfill_dump_uncollected_frac",
            "electricity_carbon_intensity_2022_gco2_kwh",
        ],
    ].copy()
    for group, cols in VARIABLE_GROUPS.items():
        missing_countries[f"has_{group.lower().replace('/', '_').replace(' ', '_')}"] = has_group_data(
            data.loc[data["is_missing_or_insufficient"]],
            cols,
        ).to_numpy()
    missing_countries.to_csv(OUTPUTS / "missing_insufficient_country_diagnostics.csv", index=False)

    print("Wrote missing-data summaries")
    print(missing_by_region.to_string(index=False))


if __name__ == "__main__":
    main()
