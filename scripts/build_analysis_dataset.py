from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

OFMSW_FILE = PROCESSED / "country_ofmsw_master.csv"
WDI_FILE = PROCESSED / "wdi_2022_covariates.csv"
EMBER_FILE = PROCESSED / "ember_electricity_carbon_intensity.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_analysis_dataset.csv"


def main() -> None:
    ofmsw = pd.read_csv(OFMSW_FILE)
    wdi = pd.read_csv(WDI_FILE)
    ember = pd.read_csv(EMBER_FILE)

    merged = ofmsw.merge(wdi, on="iso3", how="left", validate="m:1")
    merged = merged.merge(ember, on="iso3", how="left", validate="m:1")
    merged["ofmsw_food_green_2022_kg_per_cap_day"] = (
        merged["ofmsw_food_green_2022_tpy"] * 1000 / merged["population_wdi_2022"] / 365
    )
    merged["unmanaged_ofmsw_food_green_2022_kg_per_cap_day"] = (
        merged["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"]
        * 1000
        / merged["population_wdi_2022"]
        / 365
    )

    merged.to_csv(OUTPUT_FILE, index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(f"Rows: {len(merged)}")
    print(f"Rows with WDI GDP per capita: {merged['gdp_per_capita_current_usd_2022'].notna().sum()}")
    print(f"Rows with urbanization: {merged['urban_population_pct_2022'].notna().sum()}")
    print(
        "Rows with Ember 2022 electricity carbon intensity: "
        f"{merged['electricity_carbon_intensity_2022_gco2_kwh'].notna().sum()}"
    )


if __name__ == "__main__":
    main()
