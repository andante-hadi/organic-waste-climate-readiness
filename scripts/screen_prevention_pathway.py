from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

INPUT_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_prevention_screening.csv"

# Screening assumptions for food-waste prevention.
# Upstream avoided food production is represented by a conservative generic factor
# until replaced by food-system-specific datasets or ecoinvent/EXIOBASE factors.
FOOD_WASTE_PREVENTION_RATE = 0.20
AVOIDED_UPSTREAM_FOOD_KGCO2E_PER_TONNE = 1_500


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT_FILE)

    food_unmanaged_tpy = (
        data["msw_2022_tpy"]
        * data["food_frac"]
        * data["landfill_dump_uncollected_frac"]
    )
    prevented = food_unmanaged_tpy * FOOD_WASTE_PREVENTION_RATE
    data["prevention_screen_prevented_food_waste_tpy"] = prevented

    diversion_fraction_of_unmanaged_food_green = prevented / data[
        "ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"
    ]
    data["prevention_screen_avoided_ch4_tpy"] = (
        data["first_pass_ch4_total_tpy"] * diversion_fraction_of_unmanaged_food_green
    )
    data["prevention_screen_avoided_landfill_gwp100_tco2e"] = (
        data["prevention_screen_avoided_ch4_tpy"] * 27.2
    )
    data["prevention_screen_avoided_upstream_tco2e"] = (
        prevented * AVOIDED_UPSTREAM_FOOD_KGCO2E_PER_TONNE / 1000
    )
    data["prevention_screen_net_gwp100_benefit_tco2e"] = (
        data["prevention_screen_avoided_landfill_gwp100_tco2e"]
        + data["prevention_screen_avoided_upstream_tco2e"]
    )
    data["prevention_screen_upstream_share"] = (
        data["prevention_screen_avoided_upstream_tco2e"]
        / data["prevention_screen_net_gwp100_benefit_tco2e"]
    )

    data.to_csv(OUTPUT_FILE, index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "prevention_screen_prevented_food_waste_tpy",
        "prevention_screen_avoided_ch4_tpy",
        "prevention_screen_avoided_landfill_gwp100_tco2e",
        "prevention_screen_avoided_upstream_tco2e",
        "prevention_screen_net_gwp100_benefit_tco2e",
        "prevention_screen_upstream_share",
    ]
    data.sort_values("prevention_screen_net_gwp100_benefit_tco2e", ascending=False)[ranking_cols].head(30).to_csv(
        OUTPUTS / "top30_prevention_screening_net_benefit.csv", index=False
    )

    print(f"Wrote {OUTPUT_FILE}")
    print(
        "Global prevention-screening food waste prevented: "
        f"{data['prevention_screen_prevented_food_waste_tpy'].sum(skipna=True):,.0f} t/y"
    )
    print(
        "Global prevention-screening avoided methane: "
        f"{data['prevention_screen_avoided_ch4_tpy'].sum(skipna=True):,.0f} t CH4/y"
    )
    print(
        "Global prevention-screening net benefit: "
        f"{data['prevention_screen_net_gwp100_benefit_tco2e'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )


if __name__ == "__main__":
    main()
