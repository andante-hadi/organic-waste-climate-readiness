from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

INPUT_FILE = PROCESSED / "country_ofmsw_analysis_dataset.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"

# First-pass IPCC-style constants for screening, not final inventory reporting.
# Final manuscript model should use IPCC first-order decay with climate-specific k values.
DOC_FOOD = 0.15
DOC_GREEN = 0.20
DOCF = 0.50
F_CH4 = 0.50
CH4_C_RATIO = 16 / 12
GWP100_BIOGENIC_CH4_AR6 = 27.2
GWP20_BIOGENIC_CH4_AR6 = 80.8

MCF = {
    "open_dump": 0.4,
    "controlled_landfill": 0.8,
    "sanitary_landfill": 1.0,
    "unspecified_landfill": 0.6,
    "uncollected": 0.4,
    "unaccounted": 0.6,
}


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_FILE)
    food = data["food_frac"].fillna(0)
    green = data["green_frac"].fillna(0)
    organic = food + green

    # Weighted DOC for the part of OFMSW represented by food + green waste.
    data["doc_food_green_weighted"] = ((food * DOC_FOOD) + (green * DOC_GREEN)) / organic.replace(0, pd.NA)

    pathways = {
        "open_dump": "treatment_open_dump_frac",
        "controlled_landfill": "treatment_controlled_landfill_frac",
        "sanitary_landfill": "treatment_sanitary_landfill_frac",
        "unspecified_landfill": "treatment_unspecified_landfill_frac",
        "uncollected": "treatment_uncollected_frac",
        "unaccounted": "treatment_unaccounted_frac",
    }

    ch4_cols = []
    for pathway, column in pathways.items():
        waste_t = data["ofmsw_food_green_2022_tpy"] * data[column]
        ch4_t = waste_t * data["doc_food_green_weighted"] * DOCF * MCF[pathway] * F_CH4 * CH4_C_RATIO
        out_col = f"first_pass_ch4_{pathway}_tpy"
        data[out_col] = ch4_t
        ch4_cols.append(out_col)

    data["first_pass_ch4_total_tpy"] = data[ch4_cols].sum(axis=1, min_count=1)
    data["first_pass_co2e_gwp100_tpy"] = data["first_pass_ch4_total_tpy"] * GWP100_BIOGENIC_CH4_AR6
    data["first_pass_co2e_gwp20_tpy"] = data["first_pass_ch4_total_tpy"] * GWP20_BIOGENIC_CH4_AR6
    data["first_pass_ch4_kg_per_cap_year"] = data["first_pass_ch4_total_tpy"] * 1000 / data["population_wdi_2022"]

    data.to_csv(OUTPUT_FILE, index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "ofmsw_food_green_2022_tpy",
        "ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy",
        "first_pass_ch4_total_tpy",
        "first_pass_co2e_gwp100_tpy",
        "first_pass_co2e_gwp20_tpy",
        "first_pass_ch4_kg_per_cap_year",
    ]
    data.sort_values("first_pass_ch4_total_tpy", ascending=False)[ranking_cols].head(30).to_csv(
        OUTPUTS / "top30_first_pass_methane.csv", index=False
    )

    print(f"Wrote {OUTPUT_FILE}")
    print(
        "Global first-pass CH4 from food+green waste in landfill/dump/uncollected systems: "
        f"{data['first_pass_ch4_total_tpy'].sum(skipna=True):,.0f} t CH4/y"
    )
    print(
        "Global first-pass GWP100: "
        f"{data['first_pass_co2e_gwp100_tpy'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )
    print(
        "Countries/economies with first-pass methane estimates: "
        f"{data['first_pass_ch4_total_tpy'].notna().sum()}"
    )


if __name__ == "__main__":
    main()
