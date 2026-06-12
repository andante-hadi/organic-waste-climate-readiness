from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

INPUT_FILE = RAW / "ember_yearly_electricity_long.csv"
OUTPUT_FILE = PROCESSED / "ember_electricity_carbon_intensity.csv"


def main() -> None:
    usecols = ["Area", "ISO 3 code", "Year", "Area type", "Category", "Subcategory", "Variable", "Unit", "Value"]
    data = pd.read_csv(INPUT_FILE, usecols=usecols)
    ci = data[
        (data["Area type"] == "Country or economy")
        & (data["Category"] == "Power sector emissions")
        & (data["Subcategory"] == "CO2 intensity")
        & (data["Variable"] == "CO2 intensity")
        & (data["Unit"] == "gCO2/kWh")
    ].copy()

    ci = ci.rename(
        columns={
            "Area": "country_ember",
            "ISO 3 code": "iso3",
            "Year": "year",
            "Value": "electricity_carbon_intensity_gco2_kwh",
        }
    )
    ci = ci[["iso3", "country_ember", "year", "electricity_carbon_intensity_gco2_kwh"]]

    latest = ci.sort_values("year").groupby("iso3", as_index=False).tail(1)
    latest = latest.rename(
        columns={
            "year": "electricity_carbon_intensity_latest_year",
            "electricity_carbon_intensity_gco2_kwh": "electricity_carbon_intensity_latest_gco2_kwh",
        }
    )

    y2022 = ci[ci["year"] == 2022].rename(
        columns={"electricity_carbon_intensity_gco2_kwh": "electricity_carbon_intensity_2022_gco2_kwh"}
    )[["iso3", "electricity_carbon_intensity_2022_gco2_kwh"]]

    out = latest.merge(y2022, on="iso3", how="left")
    out.to_csv(OUTPUT_FILE, index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(f"Countries/economies with Ember carbon intensity: {len(out)}")
    print(f"Countries/economies with 2022 carbon intensity: {out['electricity_carbon_intensity_2022_gco2_kwh'].notna().sum()}")


if __name__ == "__main__":
    main()
