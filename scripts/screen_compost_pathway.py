from pathlib import Path

import pandas as pd

from ecoinvent_factors import load_factor_value


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

INPUT_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_compost_screening.csv"

# Screening assumptions for composting source-separated food + green OFMSW.
# If data/processed/ecoinvent_screening_factors.csv has numeric values, those
# values override these defaults.
COMPOST_DIVERSION_RATE = 0.50
SOURCE_SEPARATION_CAPTURE_RATE = 0.80
DEFAULT_COMPOST_PROCESS_EMISSIONS_KGCO2E_PER_TONNE_OFMSW = 70


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT_FILE)
    process_emissions, process_emissions_source = load_factor_value(
        "composting",
        "process_emissions",
        DEFAULT_COMPOST_PROCESS_EMISSIONS_KGCO2E_PER_TONNE_OFMSW,
    )

    available = data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"]
    diverted = available * COMPOST_DIVERSION_RATE * SOURCE_SEPARATION_CAPTURE_RATE
    data["compost_screen_diverted_ofmsw_tpy"] = diverted

    diversion_fraction_of_unmanaged = diverted / available
    data["compost_screen_avoided_ch4_tpy"] = data["first_pass_ch4_total_tpy"] * diversion_fraction_of_unmanaged
    data["compost_screen_avoided_landfill_gwp100_tco2e"] = data["compost_screen_avoided_ch4_tpy"] * 27.2
    data["compost_screen_process_tco2e"] = (
        diverted * process_emissions / 1000
    )
    data["compost_screen_net_gwp100_benefit_tco2e"] = (
        data["compost_screen_avoided_landfill_gwp100_tco2e"]
        - data["compost_screen_process_tco2e"]
    )
    data["compost_screen_process_emissions_kgco2e_per_tonne"] = process_emissions
    data["compost_screen_process_emissions_source"] = process_emissions_source

    data.to_csv(OUTPUT_FILE, index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "compost_screen_diverted_ofmsw_tpy",
        "compost_screen_avoided_ch4_tpy",
        "compost_screen_avoided_landfill_gwp100_tco2e",
        "compost_screen_process_tco2e",
        "compost_screen_net_gwp100_benefit_tco2e",
    ]
    data.sort_values("compost_screen_net_gwp100_benefit_tco2e", ascending=False)[ranking_cols].head(30).to_csv(
        OUTPUTS / "top30_compost_screening_net_benefit.csv", index=False
    )

    print(f"Wrote {OUTPUT_FILE}")
    print(
        "Global compost-screening diverted OFMSW: "
        f"{data['compost_screen_diverted_ofmsw_tpy'].sum(skipna=True):,.0f} t/y"
    )
    print(
        "Global compost-screening avoided methane: "
        f"{data['compost_screen_avoided_ch4_tpy'].sum(skipna=True):,.0f} t CH4/y"
    )
    print(
        "Global compost-screening net benefit: "
        f"{data['compost_screen_net_gwp100_benefit_tco2e'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )
    print(f"Compost process emissions factor: {process_emissions:g} kg CO2e/t ({process_emissions_source})")


if __name__ == "__main__":
    main()
