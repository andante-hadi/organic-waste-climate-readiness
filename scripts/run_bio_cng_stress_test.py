from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

BIO_CNG_FILE = PROCESSED / "country_ofmsw_bio_cng_screening.csv"
BASE_COMPARISON_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_bio_cng_stress_test.csv"

METHANE_GWP100 = 27.2
KG_PER_TONNE = 1000

SCENARIOS = [
    {
        "scenario": "central",
        "diesel_substitution_multiplier": 1.00,
        "upgrading_electricity_multiplier": 1.00,
        "process_emissions_multiplier": 1.00,
        "methane_slip_pct_of_biomethane": 0.00,
    },
    {
        "scenario": "moderate_stress",
        "diesel_substitution_multiplier": 0.80,
        "upgrading_electricity_multiplier": 1.25,
        "process_emissions_multiplier": 1.10,
        "methane_slip_pct_of_biomethane": 0.01,
    },
    {
        "scenario": "high_stress",
        "diesel_substitution_multiplier": 0.60,
        "upgrading_electricity_multiplier": 1.50,
        "process_emissions_multiplier": 1.25,
        "methane_slip_pct_of_biomethane": 0.03,
    },
]


def main() -> None:
    bio = pd.read_csv(BIO_CNG_FILE)
    base = pd.read_csv(
        BASE_COMPARISON_FILE,
        usecols=[
            "iso3",
            "country",
            "region",
            "income_2022",
            "ad_screen_net_gwp100_benefit_tco2e",
            "compost_screen_net_gwp100_benefit_tco2e",
            "prevention_screen_net_gwp100_benefit_tco2e",
            "best_four_pathway_screen",
        ],
    )

    data = bio.merge(base, on=["iso3", "country", "region", "income_2022"], how="left", validate="1:1")

    scenario_frames = []
    for scenario in SCENARIOS:
        frame = data[
            [
                "iso3",
                "country",
                "region",
                "income_2022",
                "bio_cng_screen_biomethane_m3",
                "bio_cng_screen_avoided_landfill_gwp100_tco2e",
                "bio_cng_screen_avoided_diesel_tco2e",
                "bio_cng_screen_upgrading_electricity_tco2e",
                "bio_cng_screen_process_tco2e",
                "bio_cng_screen_net_gwp100_benefit_tco2e",
                "ad_screen_net_gwp100_benefit_tco2e",
                "compost_screen_net_gwp100_benefit_tco2e",
                "prevention_screen_net_gwp100_benefit_tco2e",
                "best_four_pathway_screen",
            ]
        ].copy()
        frame["scenario"] = scenario["scenario"]
        frame["diesel_substitution_multiplier"] = scenario["diesel_substitution_multiplier"]
        frame["upgrading_electricity_multiplier"] = scenario["upgrading_electricity_multiplier"]
        frame["process_emissions_multiplier"] = scenario["process_emissions_multiplier"]
        frame["methane_slip_pct_of_biomethane"] = scenario["methane_slip_pct_of_biomethane"]

        frame["bio_cng_stress_avoided_diesel_tco2e"] = (
            frame["bio_cng_screen_avoided_diesel_tco2e"]
            * scenario["diesel_substitution_multiplier"]
        )
        frame["bio_cng_stress_upgrading_electricity_tco2e"] = (
            frame["bio_cng_screen_upgrading_electricity_tco2e"]
            * scenario["upgrading_electricity_multiplier"]
        )
        frame["bio_cng_stress_process_tco2e"] = (
            frame["bio_cng_screen_process_tco2e"]
            * scenario["process_emissions_multiplier"]
        )
        frame["bio_cng_stress_methane_slip_tco2e"] = (
            frame["bio_cng_screen_biomethane_m3"]
            * scenario["methane_slip_pct_of_biomethane"]
            * 0.7168
            / KG_PER_TONNE
            * METHANE_GWP100
        )
        frame["bio_cng_stress_net_gwp100_benefit_tco2e"] = (
            frame["bio_cng_screen_avoided_landfill_gwp100_tco2e"]
            + frame["bio_cng_stress_avoided_diesel_tco2e"]
            - frame["bio_cng_stress_upgrading_electricity_tco2e"]
            - frame["bio_cng_stress_process_tco2e"]
            - frame["bio_cng_stress_methane_slip_tco2e"]
        )

        comparator_cols = [
            "bio_cng_stress_net_gwp100_benefit_tco2e",
            "ad_screen_net_gwp100_benefit_tco2e",
            "compost_screen_net_gwp100_benefit_tco2e",
            "prevention_screen_net_gwp100_benefit_tco2e",
        ]
        labels = {
            "bio_cng_stress_net_gwp100_benefit_tco2e": "AD-bio-CNG",
            "ad_screen_net_gwp100_benefit_tco2e": "AD-electricity",
            "compost_screen_net_gwp100_benefit_tco2e": "Composting",
            "prevention_screen_net_gwp100_benefit_tco2e": "Prevention",
        }
        has_any = frame[comparator_cols].notna().any(axis=1)
        frame["best_pathway_under_bio_cng_stress"] = pd.NA
        frame.loc[has_any, "best_pathway_under_bio_cng_stress"] = frame.loc[
            has_any, comparator_cols
        ].idxmax(axis=1)
        frame["best_pathway_under_bio_cng_stress"] = frame[
            "best_pathway_under_bio_cng_stress"
        ].map(labels)
        frame["bio_cng_remains_best"] = (
            frame["best_pathway_under_bio_cng_stress"] == "AD-bio-CNG"
        )

        scenario_frames.append(frame)

    out = pd.concat(scenario_frames, ignore_index=True)
    out.to_csv(OUTPUT_FILE, index=False)

    summary = (
        out.groupby("scenario", dropna=False)
        .agg(
            bio_cng_net_benefit_mtco2e=("bio_cng_stress_net_gwp100_benefit_tco2e", lambda s: s.sum(skipna=True) / 1e6),
            bio_cng_best_countries=("bio_cng_remains_best", "sum"),
        )
        .reset_index()
    )
    summary.to_csv(OUTPUTS / "summary_bio_cng_stress_test.csv", index=False)

    counts = (
        out.groupby(["scenario", "best_pathway_under_bio_cng_stress"], dropna=False)
        .size()
        .reset_index(name="countries")
    )
    counts.to_csv(OUTPUTS / "summary_bio_cng_stress_best_counts.csv", index=False)

    top = out[out["scenario"] == "high_stress"].sort_values(
        "bio_cng_stress_net_gwp100_benefit_tco2e", ascending=False
    )
    top.head(40).to_csv(OUTPUTS / "top40_bio_cng_high_stress.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(summary.to_string(index=False))
    print("\nBest pathway counts under bio-CNG stress:")
    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()
