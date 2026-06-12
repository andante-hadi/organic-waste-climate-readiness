from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

COUNTRY_FILE = RAW / "What_a_Waste_3.0_COUNTRY_Dataset_Codebook.xlsx"
OUTPUT_FILE = PROCESSED / "country_ofmsw_master.csv"


COLS = {
    "iso3": "Country code",
    "region": "Region",
    "country": "Country name ",
    "income_generation_year": "Income group (waste generation year)",
    "income_2022": "Income group (2022)",
    "gdp": "GDP",
    "population_generation_year": "Population in waste generation year",
    "msw_year_reported": "MSW generation - year reported",
    "msw_tpy": "MSW generation (t/y)",
    "msw_kg_cap_day": "MSW generation (kg/capita/day)",
    "msw_2022_tpy": "MSW generation - projected 2022 (t/year)",
    "population_2022": "Population in 2022",
    "msw_2030_tpy": "MSW generation - projected 2030 (t/y)",
    "population_2030": "Population in 2030",
    "msw_2040_tpy": "MSW generation - projected 2040 (t/y)",
    "population_2040": "Population in 2040",
    "msw_2050_tpy": "MSW generation - projected 2050 (t/y)",
    "population_2050": "Population in 2050",
    "food_pct": "Composition - food  (% weight MSW)",
    "green_pct": "Composition - garden/green/horticultural (% weight MSW)",
    "wood_pct": "Composition - wood (% weight MSW)",
    "collection_total_population_pct": "Collection coverage - total (% population)",
    "collection_total_weight_pct": "Collection coverage - total (% weight MSW)",
    "treatment_open_dump_pct": "Treatment - open dump (% weight MSW generated)",
    "treatment_controlled_landfill_pct": "Treatment - controlled landfill (% weight MSW generated)",
    "treatment_sanitary_landfill_pct": "Treatment - sanitary landfill (% weight MSW generated)",
    "treatment_unspecified_landfill_pct": "Treatment - unspecified landfill (% weight MSW generated)",
    "treatment_anaerobic_digestion_pct": "Treatment - anaerobic digestion (% weight MSW generated)",
    "treatment_composting_pct": "Treatment - composting (% weight MSW generated)",
    "treatment_recycling_pct": "Treatment - recycling (% weight MSW generated)",
    "treatment_incineration_pct": "Treatment - incineration (% weight MSW generated)",
    "treatment_mbt_pct": "Treatment - MBT (% weight MSW generated)",
    "treatment_rdf_pct": "Treatment - RDF (% weight MSW generated)",
    "treatment_other_pct": "Treatment - other (% weight MSW generated)",
    "treatment_uncollected_pct": "Treatment - uncollected (% weight MSW generated)",
    "treatment_unaccounted_pct": "Treatment - unaccounted for (% weight MSW generated)",
}


PERCENT_COLUMNS = [
    "food_pct",
    "green_pct",
    "wood_pct",
    "collection_total_population_pct",
    "collection_total_weight_pct",
    "treatment_open_dump_pct",
    "treatment_controlled_landfill_pct",
    "treatment_sanitary_landfill_pct",
    "treatment_unspecified_landfill_pct",
    "treatment_anaerobic_digestion_pct",
    "treatment_composting_pct",
    "treatment_recycling_pct",
    "treatment_incineration_pct",
    "treatment_mbt_pct",
    "treatment_rdf_pct",
    "treatment_other_pct",
    "treatment_uncollected_pct",
    "treatment_unaccounted_pct",
]


def pct_to_fraction(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.dropna().quantile(0.95) <= 1:
        return numeric
    return numeric / 100.0


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)

    raw = pd.read_excel(COUNTRY_FILE, sheet_name="Country dataset")
    data = raw[list(COLS.values())].rename(columns={v: k for k, v in COLS.items()})

    for column in data.columns:
        if column not in {"iso3", "region", "country", "income_generation_year", "income_2022"}:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    for column in PERCENT_COLUMNS:
        data[column.replace("_pct", "_frac")] = pct_to_fraction(data[column])

    data["ofmsw_food_green_frac"] = data["food_frac"].fillna(0) + data["green_frac"].fillna(0)
    data["ofmsw_food_green_wood_frac"] = data["ofmsw_food_green_frac"] + data["wood_frac"].fillna(0)

    for year_col in ["msw_tpy", "msw_2022_tpy", "msw_2030_tpy", "msw_2040_tpy", "msw_2050_tpy"]:
        prefix = year_col.replace("msw_", "").replace("_tpy", "")
        data[f"ofmsw_food_green_{prefix}_tpy"] = data[year_col] * data["ofmsw_food_green_frac"]
        data[f"ofmsw_food_green_wood_{prefix}_tpy"] = data[year_col] * data["ofmsw_food_green_wood_frac"]

    landfill_like = [
        "treatment_open_dump_frac",
        "treatment_controlled_landfill_frac",
        "treatment_sanitary_landfill_frac",
        "treatment_unspecified_landfill_frac",
        "treatment_uncollected_frac",
        "treatment_unaccounted_frac",
    ]
    diversion = [
        "treatment_anaerobic_digestion_frac",
        "treatment_composting_frac",
        "treatment_recycling_frac",
        "treatment_incineration_frac",
        "treatment_mbt_frac",
        "treatment_rdf_frac",
        "treatment_other_frac",
    ]

    data["landfill_dump_uncollected_frac"] = data[landfill_like].sum(axis=1, min_count=1)
    data["known_diversion_or_treatment_frac"] = data[diversion].sum(axis=1, min_count=1)
    data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"] = (
        data["ofmsw_food_green_2022_tpy"] * data["landfill_dump_uncollected_frac"]
    )

    data = data.sort_values(["region", "country"], na_position="last")
    data.to_csv(OUTPUT_FILE, index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(f"Countries/economies: {len(data)}")
    print(
        "Total projected 2022 OFMSW food+green: "
        f"{data['ofmsw_food_green_2022_tpy'].sum(skipna=True):,.0f} t/y"
    )
    print(
        "Total projected 2022 OFMSW food+green to landfill/dump/uncollected: "
        f"{data['ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy'].sum(skipna=True):,.0f} t/y"
    )


if __name__ == "__main__":
    main()
