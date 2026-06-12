from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

MASTER_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison.csv"
METHANE_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"


def sum_million_tonnes(series: pd.Series) -> float:
    return series.sum(skipna=True) / 1e6


def summarize_group(data: pd.DataFrame, group_col: str) -> pd.DataFrame:
    grouped = data.groupby(group_col, dropna=False)
    return grouped.agg(
        countries=("iso3", "count"),
        ofmsw_food_green_2022_mt=(
            "ofmsw_food_green_2022_tpy",
            sum_million_tonnes,
        ),
        unmanaged_ofmsw_food_green_2022_mt=(
            "ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy",
            sum_million_tonnes,
        ),
        first_pass_ch4_mt=("first_pass_ch4_total_tpy", sum_million_tonnes),
        first_pass_gwp100_mtco2e=("first_pass_co2e_gwp100_tpy", sum_million_tonnes),
        ad_electricity_net_benefit_mtco2e=(
            "ad_screen_net_gwp100_benefit_tco2e",
            sum_million_tonnes,
        ),
        ad_bio_cng_net_benefit_mtco2e=(
            "bio_cng_screen_net_gwp100_benefit_tco2e",
            sum_million_tonnes,
        ),
        compost_net_benefit_mtco2e=(
            "compost_screen_net_gwp100_benefit_tco2e",
            sum_million_tonnes,
        ),
        prevention_net_benefit_mtco2e=(
            "prevention_screen_net_gwp100_benefit_tco2e",
            sum_million_tonnes,
        ),
    ).reset_index()


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    pathways = pd.read_csv(MASTER_FILE)
    methane = pd.read_csv(
        METHANE_FILE,
        usecols=["iso3", "first_pass_ch4_total_tpy", "first_pass_co2e_gwp100_tpy"],
    )
    data = pathways.merge(methane, on="iso3", how="left", validate="1:1")
    data = data[
        (data["region"].notna())
        & (data["region"] != "region_id")
        & (data["country"].notna())
        & (data["country"] != "country_name")
    ].copy()

    global_summary = pd.DataFrame(
        [
            {
                "countries": len(data),
                "countries_with_any_pathway_result": data[
                    "best_four_pathway_screen"
                ].notna().sum(),
                "ofmsw_food_green_2022_mt": sum_million_tonnes(
                    data["ofmsw_food_green_2022_tpy"]
                ),
                "unmanaged_ofmsw_food_green_2022_mt": sum_million_tonnes(
                    data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"]
                ),
                "first_pass_ch4_mt": sum_million_tonnes(data["first_pass_ch4_total_tpy"]),
                "first_pass_gwp100_mtco2e": sum_million_tonnes(
                    data["first_pass_co2e_gwp100_tpy"]
                ),
                "ad_electricity_net_benefit_mtco2e": sum_million_tonnes(
                    data["ad_screen_net_gwp100_benefit_tco2e"]
                ),
                "ad_bio_cng_net_benefit_mtco2e": sum_million_tonnes(
                    data["bio_cng_screen_net_gwp100_benefit_tco2e"]
                ),
                "compost_net_benefit_mtco2e": sum_million_tonnes(
                    data["compost_screen_net_gwp100_benefit_tco2e"]
                ),
                "prevention_net_benefit_mtco2e": sum_million_tonnes(
                    data["prevention_screen_net_gwp100_benefit_tco2e"]
                ),
            }
        ]
    )
    global_summary.to_csv(OUTPUTS / "summary_four_pathway_global_metrics.csv", index=False)

    by_region = summarize_group(data, "region").sort_values(
        "ad_bio_cng_net_benefit_mtco2e", ascending=False
    )
    by_region.to_csv(OUTPUTS / "summary_four_pathway_by_region.csv", index=False)

    by_income = summarize_group(data, "income_2022").sort_values(
        "ad_bio_cng_net_benefit_mtco2e", ascending=False
    )
    by_income.to_csv(OUTPUTS / "summary_four_pathway_by_income.csv", index=False)

    best_counts = (
        data["best_four_pathway_screen"]
        .fillna("Missing/insufficient data")
        .value_counts()
        .rename_axis("best_pathway")
        .reset_index(name="countries")
    )
    best_counts.to_csv(OUTPUTS / "summary_four_pathway_best_counts.csv", index=False)

    print(f"Wrote {OUTPUTS / 'summary_four_pathway_global_metrics.csv'}")
    print(f"Wrote {OUTPUTS / 'summary_four_pathway_by_region.csv'}")
    print(f"Wrote {OUTPUTS / 'summary_four_pathway_by_income.csv'}")
    print(f"Wrote {OUTPUTS / 'summary_four_pathway_best_counts.csv'}")


if __name__ == "__main__":
    main()
