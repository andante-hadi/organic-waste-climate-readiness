from pathlib import Path

import pandas as pd

from ecoinvent_factors import load_factor_value


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

INPUT_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_ad_screening.csv"

# Screening assumptions for AD of source-separated food + green OFMSW.
# If data/processed/ecoinvent_screening_factors.csv has numeric values, those
# values override these defaults.
AD_DIVERSION_RATE = 0.50
SOURCE_SEPARATION_CAPTURE_RATE = 0.80
DEFAULT_BIOGAS_ELECTRICITY_KWH_PER_TONNE_OFMSW = 250
DEFAULT_AD_PROCESS_EMISSIONS_KGCO2E_PER_TONNE_OFMSW = 50


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT_FILE)
    electricity_yield, electricity_yield_source = load_factor_value(
        "anaerobic_digestion",
        "electricity_yield",
        DEFAULT_BIOGAS_ELECTRICITY_KWH_PER_TONNE_OFMSW,
    )
    process_emissions, process_emissions_source = load_factor_value(
        "anaerobic_digestion",
        "process_emissions",
        DEFAULT_AD_PROCESS_EMISSIONS_KGCO2E_PER_TONNE_OFMSW,
    )

    available = data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"]
    diverted = available * AD_DIVERSION_RATE * SOURCE_SEPARATION_CAPTURE_RATE
    data["ad_screen_diverted_ofmsw_tpy"] = diverted

    diversion_fraction_of_unmanaged = diverted / available
    data["ad_screen_avoided_ch4_tpy"] = data["first_pass_ch4_total_tpy"] * diversion_fraction_of_unmanaged
    data["ad_screen_avoided_landfill_gwp100_tco2e"] = data["ad_screen_avoided_ch4_tpy"] * 27.2

    data["ad_screen_electricity_generated_mwh"] = diverted * electricity_yield / 1000
    data["ad_screen_avoided_grid_tco2e"] = (
        data["ad_screen_electricity_generated_mwh"]
        * data["electricity_carbon_intensity_2022_gco2_kwh"]
        / 1000
    )
    data["ad_screen_process_tco2e"] = diverted * process_emissions / 1000
    data["ad_screen_net_gwp100_benefit_tco2e"] = (
        data["ad_screen_avoided_landfill_gwp100_tco2e"]
        + data["ad_screen_avoided_grid_tco2e"]
        - data["ad_screen_process_tco2e"]
    )
    data["ad_screen_grid_credit_share"] = (
        data["ad_screen_avoided_grid_tco2e"]
        / data["ad_screen_net_gwp100_benefit_tco2e"]
    )
    data["ad_screen_electricity_yield_kwh_per_tonne"] = electricity_yield
    data["ad_screen_process_emissions_kgco2e_per_tonne"] = process_emissions
    data["ad_screen_electricity_yield_source"] = electricity_yield_source
    data["ad_screen_process_emissions_source"] = process_emissions_source

    data.to_csv(OUTPUT_FILE, index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "ad_screen_diverted_ofmsw_tpy",
        "ad_screen_avoided_ch4_tpy",
        "ad_screen_avoided_landfill_gwp100_tco2e",
        "ad_screen_avoided_grid_tco2e",
        "ad_screen_net_gwp100_benefit_tco2e",
        "ad_screen_grid_credit_share",
        "electricity_carbon_intensity_2022_gco2_kwh",
    ]
    data.sort_values("ad_screen_net_gwp100_benefit_tco2e", ascending=False)[ranking_cols].head(30).to_csv(
        OUTPUTS / "top30_ad_screening_net_benefit.csv", index=False
    )

    print(f"Wrote {OUTPUT_FILE}")
    print(
        "Global AD-screening diverted OFMSW: "
        f"{data['ad_screen_diverted_ofmsw_tpy'].sum(skipna=True):,.0f} t/y"
    )
    print(
        "Global AD-screening avoided methane: "
        f"{data['ad_screen_avoided_ch4_tpy'].sum(skipna=True):,.0f} t CH4/y"
    )
    print(
        "Global AD-screening net benefit: "
        f"{data['ad_screen_net_gwp100_benefit_tco2e'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )
    print(f"AD electricity yield factor: {electricity_yield:g} kWh/t ({electricity_yield_source})")
    print(f"AD process emissions factor: {process_emissions:g} kg CO2e/t ({process_emissions_source})")


if __name__ == "__main__":
    main()
