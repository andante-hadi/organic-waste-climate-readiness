from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

CITY_FILE = RAW / "What_a_Waste_3.0_CITY_Dataset_Codebook.xlsx"
OUTPUT_FILE = PROCESSED / "city_ofmsw_screen.csv"


def pct_to_frac(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    # What a Waste city fields are labelled percent, but many are stored as
    # fractions from 0 to 1. Convert only fields that look like 0-100 percents.
    if values.dropna().gt(1).any():
        return values / 100
    return values


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    raw = pd.read_excel(CITY_FILE, sheet_name="City dataset")
    data = pd.DataFrame()
    data["iso3"] = raw["iso3c"]
    data["country"] = raw["country_name"]
    data["region"] = raw["region_id"]
    data["income_2022"] = raw["income_id_2022"]
    data["city"] = raw["city_name"]
    data["city_code"] = raw["city_code"]
    data["population"] = pd.to_numeric(raw["population_number_of_people"], errors="coerce")
    data["population_un"] = pd.to_numeric(raw["population_number_of_people_UN"], errors="coerce")
    data["msw_year"] = pd.to_numeric(raw["msw_total_msw_generation_year"], errors="coerce")
    data["msw_tpy"] = pd.to_numeric(
        raw["msw_total_msw_generated_tons_per_year"], errors="coerce"
    )
    data["msw_kg_cap_day"] = pd.to_numeric(
        raw["msw_total_msw_generated_kg_per_cap_per_day"], errors="coerce"
    )
    data["food_frac"] = pct_to_frac(raw["composition_msw_food_organic_waste_percent"])
    data["green_frac"] = pct_to_frac(raw["composition_msw_yard_garden_green_waste_percent"])
    data["wood_frac"] = pct_to_frac(raw["composition_msw_wood_percent"])
    data["collection_population_frac"] = pct_to_frac(
        raw["waste_collection_coverage_total_percent_of_population"]
    )
    data["collection_waste_frac"] = pct_to_frac(
        raw["waste_collection_coverage_total_percent_of_waste"]
    )

    treatment_map = {
        "open_dump": "waste_treatment_open_dumpsite_percent",
        "controlled_landfill": "waste_treatment_controlled_landfill_percent",
        "sanitary_landfill_gas_system": "waste_treatment_sanitary_landfill_landfill_gas_system_percent",
        "unspecified_landfill": "waste_treatment_landfill_unspecified_percent",
        "anaerobic_digestion": "waste_treatment_anaerobic_digestion_percent",
        "compost": "waste_treatment_compost_percent",
        "recycling": "waste_treatment_recycling_percent",
        "incineration": "waste_treatment_incineration_percent",
        "mbt": "waste_treatment_mbt_percent",
        "rdf": "waste_treatment_rdf_percent",
        "other": "waste_treatment_other_percent",
        "uncollected": "waste_uncollected_percent",
        "unaccounted": "waste_treatment_unaccounted_for_percent",
    }
    for short, col in treatment_map.items():
        data[f"treatment_{short}_frac"] = pct_to_frac(raw[col])

    data["ofmsw_food_green_frac"] = data["food_frac"].fillna(0) + data["green_frac"].fillna(0)
    data.loc[data[["food_frac", "green_frac"]].isna().all(axis=1), "ofmsw_food_green_frac"] = pd.NA
    data["ofmsw_food_green_tpy"] = data["msw_tpy"] * data["ofmsw_food_green_frac"]
    data["landfill_dump_uncollected_frac"] = data[
        [
            "treatment_open_dump_frac",
            "treatment_controlled_landfill_frac",
            "treatment_sanitary_landfill_gas_system_frac",
            "treatment_unspecified_landfill_frac",
            "treatment_uncollected_frac",
            "treatment_unaccounted_frac",
        ]
    ].sum(axis=1, min_count=1)
    data["ofmsw_food_green_to_landfill_dump_uncollected_tpy"] = (
        data["ofmsw_food_green_tpy"] * data["landfill_dump_uncollected_frac"]
    )
    data["existing_biological_treatment_frac"] = data[
        ["treatment_anaerobic_digestion_frac", "treatment_compost_frac"]
    ].sum(axis=1, min_count=1)

    data["ad_asset_capacity_tpy"] = pd.to_numeric(
        raw["anaerobicdigestion__operational_assets_capacity_tpy"], errors="coerce"
    )
    data["compost_asset_capacity_tpy"] = pd.to_numeric(
        raw["compost__operational_assets_capacity_tpy"], errors="coerce"
    )
    data["ad_throughput_tpy"] = pd.to_numeric(
        raw["anaerobicdigestion__throughput_tpy"], errors="coerce"
    )
    data["compost_throughput_tpy"] = pd.to_numeric(
        raw["compost__throughput_tpy"], errors="coerce"
    )
    data["has_ad_asset_data"] = data[["ad_asset_capacity_tpy", "ad_throughput_tpy"]].notna().any(axis=1)
    data["has_compost_asset_data"] = data[
        ["compost_asset_capacity_tpy", "compost_throughput_tpy"]
    ].notna().any(axis=1)

    data.to_csv(OUTPUT_FILE, index=False)

    summary = pd.DataFrame(
        [
            {"metric": "cities_total", "value": len(data)},
            {"metric": "cities_with_msw_tpy", "value": data["msw_tpy"].notna().sum()},
            {"metric": "cities_with_food_or_green_fraction", "value": data["ofmsw_food_green_frac"].notna().sum()},
            {"metric": "cities_with_treatment_shares", "value": data["landfill_dump_uncollected_frac"].notna().sum()},
            {"metric": "ofmsw_food_green_mt", "value": data["ofmsw_food_green_tpy"].sum(skipna=True) / 1e6},
            {
                "metric": "ofmsw_food_green_to_landfill_dump_uncollected_mt",
                "value": data["ofmsw_food_green_to_landfill_dump_uncollected_tpy"].sum(skipna=True) / 1e6,
            },
            {"metric": "cities_with_ad_asset_data", "value": int(data["has_ad_asset_data"].sum())},
            {"metric": "cities_with_compost_asset_data", "value": int(data["has_compost_asset_data"].sum())},
        ]
    )
    summary.to_csv(OUTPUTS / "summary_city_ofmsw_screen.csv", index=False)

    top = data.sort_values("ofmsw_food_green_to_landfill_dump_uncollected_tpy", ascending=False)
    top.head(40).to_csv(OUTPUTS / "top40_city_unmanaged_ofmsw.csv", index=False)

    country_summary = (
        data.groupby(["iso3", "country", "region"], dropna=False)
        .agg(
            cities=("city", "count"),
            city_ofmsw_food_green_tpy=("ofmsw_food_green_tpy", "sum"),
            city_unmanaged_ofmsw_food_green_tpy=(
                "ofmsw_food_green_to_landfill_dump_uncollected_tpy",
                "sum",
            ),
            cities_with_ad_asset_data=("has_ad_asset_data", "sum"),
            cities_with_compost_asset_data=("has_compost_asset_data", "sum"),
        )
        .reset_index()
    )
    country_summary.to_csv(OUTPUTS / "city_ofmsw_by_country_summary.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
