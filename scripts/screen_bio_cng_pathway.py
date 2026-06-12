from pathlib import Path

import pandas as pd

from ecoinvent_factors import load_factor_value


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

INPUT_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_bio_cng_screening.csv"

BIO_CNG_DIVERSION_RATE = 0.50
SOURCE_SEPARATION_CAPTURE_RATE = 0.80

DEFAULT_BIOGAS_YIELD_M3_PER_TONNE_OFMSW = 100
DEFAULT_METHANE_SHARE_M3_PER_M3_BIOGAS = 0.634916
DEFAULT_METHANE_RECOVERY = 0.97
DEFAULT_UPGRADING_COMPRESSION_KWH_PER_M3_BIOGAS = 0.45
DEFAULT_DIESEL_SUBSTITUTION_KGCO2E_PER_MJ = 0.074
DEFAULT_AD_PROCESS_EMISSIONS_KGCO2E_PER_TONNE_OFMSW = 74.289
METHANE_LHV_MJ_PER_M3 = 35.8


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT_FILE)

    biogas_yield, biogas_yield_source = load_factor_value(
        "bio_cng",
        "biogas_yield",
        DEFAULT_BIOGAS_YIELD_M3_PER_TONNE_OFMSW,
    )
    methane_share, methane_share_source = load_factor_value(
        "bio_cng",
        "methane_share",
        DEFAULT_METHANE_SHARE_M3_PER_M3_BIOGAS,
    )
    methane_recovery, methane_recovery_source = load_factor_value(
        "bio_cng",
        "methane_recovery",
        DEFAULT_METHANE_RECOVERY,
    )
    upgrading_electricity, upgrading_electricity_source = load_factor_value(
        "bio_cng",
        "upgrading_compression_electricity",
        DEFAULT_UPGRADING_COMPRESSION_KWH_PER_M3_BIOGAS,
    )
    diesel_substitution, diesel_substitution_source = load_factor_value(
        "bio_cng",
        "diesel_substitution",
        DEFAULT_DIESEL_SUBSTITUTION_KGCO2E_PER_MJ,
    )
    process_emissions, process_emissions_source = load_factor_value(
        "anaerobic_digestion",
        "process_emissions",
        DEFAULT_AD_PROCESS_EMISSIONS_KGCO2E_PER_TONNE_OFMSW,
    )

    available = data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"]
    diverted = available * BIO_CNG_DIVERSION_RATE * SOURCE_SEPARATION_CAPTURE_RATE
    data["bio_cng_screen_diverted_ofmsw_tpy"] = diverted

    diversion_fraction_of_unmanaged = diverted / available
    data["bio_cng_screen_avoided_ch4_tpy"] = (
        data["first_pass_ch4_total_tpy"] * diversion_fraction_of_unmanaged
    )
    data["bio_cng_screen_avoided_landfill_gwp100_tco2e"] = (
        data["bio_cng_screen_avoided_ch4_tpy"] * 27.2
    )

    data["bio_cng_screen_raw_biogas_m3"] = diverted * biogas_yield
    data["bio_cng_screen_biomethane_m3"] = (
        data["bio_cng_screen_raw_biogas_m3"] * methane_share * methane_recovery
    )
    data["bio_cng_screen_biomethane_energy_mj"] = (
        data["bio_cng_screen_biomethane_m3"] * METHANE_LHV_MJ_PER_M3
    )
    data["bio_cng_screen_avoided_diesel_tco2e"] = (
        data["bio_cng_screen_biomethane_energy_mj"] * diesel_substitution / 1000
    )
    data["bio_cng_screen_upgrading_electricity_mwh"] = (
        data["bio_cng_screen_raw_biogas_m3"] * upgrading_electricity / 1000
    )
    data["bio_cng_screen_upgrading_electricity_tco2e"] = (
        data["bio_cng_screen_upgrading_electricity_mwh"]
        * data["electricity_carbon_intensity_2022_gco2_kwh"]
        / 1000
    )
    data["bio_cng_screen_process_tco2e"] = diverted * process_emissions / 1000
    data["bio_cng_screen_net_gwp100_benefit_tco2e"] = (
        data["bio_cng_screen_avoided_landfill_gwp100_tco2e"]
        + data["bio_cng_screen_avoided_diesel_tco2e"]
        - data["bio_cng_screen_upgrading_electricity_tco2e"]
        - data["bio_cng_screen_process_tco2e"]
    )
    data["bio_cng_screen_fuel_credit_share"] = (
        data["bio_cng_screen_avoided_diesel_tco2e"]
        / data["bio_cng_screen_net_gwp100_benefit_tco2e"]
    )

    data["bio_cng_screen_biogas_yield_m3_per_tonne"] = biogas_yield
    data["bio_cng_screen_methane_share"] = methane_share
    data["bio_cng_screen_methane_recovery"] = methane_recovery
    data["bio_cng_screen_upgrading_kwh_per_m3_biogas"] = upgrading_electricity
    data["bio_cng_screen_diesel_substitution_kgco2e_per_mj"] = diesel_substitution
    data["bio_cng_screen_process_emissions_kgco2e_per_tonne"] = process_emissions
    data["bio_cng_screen_biogas_yield_source"] = biogas_yield_source
    data["bio_cng_screen_methane_share_source"] = methane_share_source
    data["bio_cng_screen_methane_recovery_source"] = methane_recovery_source
    data["bio_cng_screen_upgrading_electricity_source"] = upgrading_electricity_source
    data["bio_cng_screen_diesel_substitution_source"] = diesel_substitution_source
    data["bio_cng_screen_process_emissions_source"] = process_emissions_source

    data.to_csv(OUTPUT_FILE, index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "bio_cng_screen_diverted_ofmsw_tpy",
        "bio_cng_screen_biomethane_m3",
        "bio_cng_screen_avoided_landfill_gwp100_tco2e",
        "bio_cng_screen_avoided_diesel_tco2e",
        "bio_cng_screen_upgrading_electricity_tco2e",
        "bio_cng_screen_net_gwp100_benefit_tco2e",
        "bio_cng_screen_fuel_credit_share",
    ]
    data.sort_values("bio_cng_screen_net_gwp100_benefit_tco2e", ascending=False)[
        ranking_cols
    ].head(30).to_csv(OUTPUTS / "top30_bio_cng_screening_net_benefit.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(
        "Global bio-CNG-screening biomethane: "
        f"{data['bio_cng_screen_biomethane_m3'].sum(skipna=True) / 1e9:,.1f} billion m3/y"
    )
    print(
        "Global bio-CNG-screening net benefit: "
        f"{data['bio_cng_screen_net_gwp100_benefit_tco2e'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )


if __name__ == "__main__":
    main()
