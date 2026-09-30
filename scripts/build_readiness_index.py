from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

ANALYSIS_FILE = PROCESSED / "country_ofmsw_analysis_dataset.csv"
FOUR_PATHWAY_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_readiness_index.csv"


INCOME_SCORE = {
    "HIC": 1.00,
    "UMIC": 0.75,
    "UMC (2019)": 0.75,
    "LMIC": 0.45,
    "LIC": 0.25,
}


def minmax(series: pd.Series, lower=None, upper=None) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    lo = values.quantile(0.05) if lower is None else lower
    hi = values.quantile(0.95) if upper is None else upper
    scaled = (values - lo) / (hi - lo)
    return scaled.clip(0, 1)


def classify_opportunity(mitigation_score: pd.Series, readiness_score: pd.Series) -> pd.Series:
    out = pd.Series(pd.NA, index=mitigation_score.index, dtype="object")
    high_mitigation = mitigation_score >= 0.67
    high_readiness = readiness_score >= 0.60
    out.loc[high_mitigation & high_readiness] = "Immediate priority"
    out.loc[high_mitigation & ~high_readiness] = "Strategic build-out"
    out.loc[~high_mitigation & high_readiness] = "No-regret / complementary"
    out.loc[~high_mitigation & ~high_readiness] = "Longer-term / local fit"
    out.loc[mitigation_score.isna() | readiness_score.isna()] = pd.NA
    return out


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    analysis = pd.read_csv(ANALYSIS_FILE)
    pathways = pd.read_csv(FOUR_PATHWAY_FILE)
    data = analysis.merge(
        pathways[
            [
                "iso3",
                "ad_screen_net_gwp100_benefit_tco2e",
                "bio_cng_screen_net_gwp100_benefit_tco2e",
                "compost_screen_net_gwp100_benefit_tco2e",
                "prevention_screen_net_gwp100_benefit_tco2e",
                "best_four_pathway_screen",
                "best_four_pathway_benefit_tco2e",
            ]
        ],
        on="iso3",
        how="left",
        validate="1:1",
    )
    data = data[(data["iso3"].notna()) & (data["iso3"] != "iso3c")].copy()

    collection = data["collection_total_population_frac"].combine_first(
        data["collection_total_weight_frac"]
    )
    data["readiness_collection_score"] = collection.clip(0, 1)
    data["readiness_income_score"] = data["income_2022"].map(INCOME_SCORE)
    data["readiness_gdp_score"] = minmax(np.log10(data["gdp_per_capita_current_usd_2022"]))
    data["readiness_urban_score"] = minmax(data["urban_population_pct_2022"], lower=20, upper=95)
    data["readiness_existing_biological_score"] = (
        data["treatment_anaerobic_digestion_frac"].fillna(0)
        + data["treatment_composting_frac"].fillna(0)
    ).clip(0, 0.20) / 0.20
    data["readiness_existing_recovery_score"] = (
        data["treatment_recycling_frac"].fillna(0)
        + data["treatment_mbt_frac"].fillna(0)
        + data["treatment_rdf_frac"].fillna(0)
        + data["treatment_incineration_frac"].fillna(0)
    ).clip(0, 0.60) / 0.60

    required_cols = [
        "collection_total_population_frac",
        "collection_total_weight_frac",
        "landfill_dump_uncollected_frac",
        "food_frac",
        "green_frac",
        "gdp_per_capita_current_usd_2022",
        "urban_population_pct_2022",
        "electricity_carbon_intensity_2022_gco2_kwh",
    ]
    data["readiness_data_completeness_score"] = data[required_cols].notna().mean(axis=1)

    data["readiness_general_score"] = data[
        [
            "readiness_collection_score",
            "readiness_income_score",
            "readiness_gdp_score",
            "readiness_urban_score",
            "readiness_data_completeness_score",
        ]
    ].mean(axis=1, skipna=True)

    data["readiness_prevention_score"] = data[
        [
            "readiness_general_score",
            "readiness_income_score",
            "readiness_data_completeness_score",
        ]
    ].mean(axis=1, skipna=True)
    data["readiness_composting_score"] = data[
        [
            "readiness_collection_score",
            "readiness_existing_biological_score",
            "readiness_urban_score",
            "readiness_data_completeness_score",
        ]
    ].mean(axis=1, skipna=True)
    data["readiness_ad_electricity_score"] = data[
        [
            "readiness_collection_score",
            "readiness_existing_biological_score",
            "readiness_existing_recovery_score",
            "readiness_gdp_score",
            "readiness_data_completeness_score",
        ]
    ].mean(axis=1, skipna=True)
    data["readiness_bio_cng_score"] = data[
        [
            "readiness_collection_score",
            "readiness_gdp_score",
            "readiness_urban_score",
            "readiness_existing_recovery_score",
            "readiness_data_completeness_score",
        ]
    ].mean(axis=1, skipna=True)

    pathway_to_readiness = {
        "Prevention": "readiness_prevention_score",
        "Composting": "readiness_composting_score",
        "AD-electricity": "readiness_ad_electricity_score",
        "AD-bio-CNG": "readiness_bio_cng_score",
    }
    data["best_pathway_readiness_score"] = np.nan
    for pathway, col in pathway_to_readiness.items():
        mask = data["best_four_pathway_screen"] == pathway
        data.loc[mask, "best_pathway_readiness_score"] = data.loc[mask, col]

    available = data["best_four_pathway_benefit_tco2e"].notna()
    data["mitigation_potential_score"] = np.nan
    data.loc[available, "mitigation_potential_score"] = minmax(
        np.log10(data.loc[available, "best_four_pathway_benefit_tco2e"].clip(lower=1))
    )
    data["opportunity_readiness_class"] = classify_opportunity(
        data["mitigation_potential_score"],
        data["best_pathway_readiness_score"],
    )

    output_cols = [
        "iso3",
        "country",
        "region",
        "income_2022",
        "best_four_pathway_screen",
        "best_four_pathway_benefit_tco2e",
        "mitigation_potential_score",
        "best_pathway_readiness_score",
        "opportunity_readiness_class",
        "readiness_general_score",
        "readiness_prevention_score",
        "readiness_composting_score",
        "readiness_ad_electricity_score",
        "readiness_bio_cng_score",
        "readiness_collection_score",
        "readiness_income_score",
        "readiness_gdp_score",
        "readiness_urban_score",
        "readiness_existing_biological_score",
        "readiness_existing_recovery_score",
        "readiness_data_completeness_score",
    ]
    data[output_cols].to_csv(OUTPUT_FILE, index=False)

    data[output_cols].sort_values(
        ["mitigation_potential_score", "best_pathway_readiness_score"],
        ascending=False,
    ).head(40).to_csv(OUTPUTS / "top40_readiness_adjusted_opportunities.csv", index=False)

    counts = (
        data["opportunity_readiness_class"]
        .fillna("Missing/insufficient data")
        .value_counts()
        .rename_axis("opportunity_readiness_class")
        .reset_index(name="countries")
    )
    counts.to_csv(OUTPUTS / "summary_readiness_opportunity_classes.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()
