from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

CITY_FILE = PROCESSED / "city_ofmsw_screen.csv"
READINESS_FILE = PROCESSED / "country_ofmsw_readiness_index.csv"
SENSITIVITY_FILE = PROCESSED / "country_ofmsw_four_pathway_sensitivity.csv"
OUTPUT_FILE = PROCESSED / "city_country_alignment.csv"


def main() -> None:
    city = pd.read_csv(CITY_FILE)
    readiness = pd.read_csv(
        READINESS_FILE,
        usecols=[
            "iso3",
            "best_four_pathway_screen",
            "best_four_pathway_benefit_tco2e",
            "opportunity_readiness_class",
            "mitigation_potential_score",
            "best_pathway_readiness_score",
        ],
    )
    sensitivity = pd.read_csv(
        SENSITIVITY_FILE,
        usecols=["iso3", "robust_winning_pathway", "max_win_probability"],
    )

    out = city.merge(readiness, on="iso3", how="left", validate="m:1").merge(
        sensitivity, on="iso3", how="left", validate="m:1"
    )
    out["city_unmanaged_ofmsw_mt"] = (
        out["ofmsw_food_green_to_landfill_dump_uncollected_tpy"] / 1e6
    )
    out["city_ofmsw_mt"] = out["ofmsw_food_green_tpy"] / 1e6
    out.to_csv(OUTPUT_FILE, index=False)

    top = out.sort_values("ofmsw_food_green_to_landfill_dump_uncollected_tpy", ascending=False)
    top.head(50).to_csv(OUTPUTS / "top50_city_country_alignment.csv", index=False)

    class_summary = (
        out.groupby("opportunity_readiness_class", dropna=False)
        .agg(
            cities=("city", "count"),
            city_ofmsw_mt=("city_ofmsw_mt", "sum"),
            city_unmanaged_ofmsw_mt=("city_unmanaged_ofmsw_mt", "sum"),
            cities_with_ad_asset_data=("has_ad_asset_data", "sum"),
            cities_with_compost_asset_data=("has_compost_asset_data", "sum"),
        )
        .reset_index()
        .sort_values("city_unmanaged_ofmsw_mt", ascending=False)
    )
    class_summary.to_csv(OUTPUTS / "summary_city_by_country_readiness_class.csv", index=False)

    pathway_summary = (
        out.groupby("best_four_pathway_screen", dropna=False)
        .agg(
            cities=("city", "count"),
            city_ofmsw_mt=("city_ofmsw_mt", "sum"),
            city_unmanaged_ofmsw_mt=("city_unmanaged_ofmsw_mt", "sum"),
            cities_with_ad_asset_data=("has_ad_asset_data", "sum"),
            cities_with_compost_asset_data=("has_compost_asset_data", "sum"),
        )
        .reset_index()
        .sort_values("city_unmanaged_ofmsw_mt", ascending=False)
    )
    pathway_summary.to_csv(OUTPUTS / "summary_city_by_country_best_pathway.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print("\nCity OFMSW by country readiness class:")
    print(class_summary.to_string(index=False))
    print("\nCity OFMSW by country best pathway:")
    print(pathway_summary.to_string(index=False))


if __name__ == "__main__":
    main()
