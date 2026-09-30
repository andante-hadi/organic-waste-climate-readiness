from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

METHANE_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
BASE_COMPARISON_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison.csv"
AD_FILE = PROCESSED / "country_ofmsw_ad_screening.csv"
BIO_CNG_FILE = PROCESSED / "country_ofmsw_bio_cng_screening.csv"
COMPOST_FILE = PROCESSED / "country_ofmsw_compost_screening.csv"
PREVENTION_FILE = PROCESSED / "country_ofmsw_prevention_screening.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_landfill_capture_sensitivity.csv"

GWP100 = 27.2

SCENARIOS = {
    "low_capture": {
        "open_dump": 0.00,
        "controlled_landfill": 0.10,
        "sanitary_landfill": 0.25,
        "unspecified_landfill": 0.05,
        "uncollected": 0.00,
        "unaccounted": 0.00,
        "oxidation": 0.05,
    },
    "moderate_capture": {
        "open_dump": 0.00,
        "controlled_landfill": 0.25,
        "sanitary_landfill": 0.50,
        "unspecified_landfill": 0.15,
        "uncollected": 0.00,
        "unaccounted": 0.00,
        "oxidation": 0.10,
    },
    "high_capture": {
        "open_dump": 0.00,
        "controlled_landfill": 0.50,
        "sanitary_landfill": 0.75,
        "unspecified_landfill": 0.30,
        "uncollected": 0.00,
        "unaccounted": 0.00,
        "oxidation": 0.10,
    },
}


def adjusted_ch4(data: pd.DataFrame, scenario: dict[str, float]) -> pd.Series:
    parts = []
    for pathway in [
        "open_dump",
        "controlled_landfill",
        "sanitary_landfill",
        "unspecified_landfill",
        "uncollected",
        "unaccounted",
    ]:
        col = f"first_pass_ch4_{pathway}_tpy"
        capture = scenario[pathway]
        oxidation = scenario["oxidation"] if "landfill" in pathway else 0.0
        parts.append(data[col] * (1 - capture) * (1 - oxidation))
    return pd.concat(parts, axis=1).sum(axis=1, min_count=1)


def main() -> None:
    methane = pd.read_csv(METHANE_FILE)
    base = pd.read_csv(BASE_COMPARISON_FILE)
    ad = pd.read_csv(
        AD_FILE,
        usecols=[
            "iso3",
            "ad_screen_avoided_ch4_tpy",
            "ad_screen_avoided_grid_tco2e",
            "ad_screen_process_tco2e",
        ],
    )
    bio = pd.read_csv(
        BIO_CNG_FILE,
        usecols=[
            "iso3",
            "bio_cng_screen_avoided_ch4_tpy",
            "bio_cng_screen_avoided_diesel_tco2e",
            "bio_cng_screen_upgrading_electricity_tco2e",
            "bio_cng_screen_process_tco2e",
        ],
    )
    compost = pd.read_csv(
        COMPOST_FILE,
        usecols=[
            "iso3",
            "compost_screen_avoided_ch4_tpy",
            "compost_screen_process_tco2e",
        ],
    )
    prevention = pd.read_csv(
        PREVENTION_FILE,
        usecols=[
            "iso3",
            "prevention_screen_avoided_ch4_tpy",
            "prevention_screen_avoided_upstream_tco2e",
        ],
    )

    components = base[
        [
            "iso3",
            "country",
            "region",
            "income_2022",
            "best_four_pathway_screen",
        ]
    ].merge(ad, on="iso3", how="left", validate="1:1").merge(
        bio, on="iso3", how="left", validate="1:1"
    ).merge(
        compost, on="iso3", how="left", validate="1:1"
    ).merge(
        prevention, on="iso3", how="left", validate="1:1"
    )

    frames = []
    central_total_ch4 = methane["first_pass_ch4_total_tpy"]
    central_total_ch4 = central_total_ch4.replace(0, pd.NA)
    methane_keys = methane[["iso3", "first_pass_ch4_total_tpy"]].copy()

    for name, scenario in SCENARIOS.items():
        scenario_methane = methane[["iso3"]].copy()
        scenario_methane["scenario"] = name
        scenario_methane["adjusted_first_pass_ch4_total_tpy"] = adjusted_ch4(
            methane, scenario
        )
        scenario_methane["methane_adjustment_ratio"] = (
            scenario_methane["adjusted_first_pass_ch4_total_tpy"]
            / central_total_ch4
        )
        scenario_methane = scenario_methane.merge(methane_keys, on="iso3", how="left")

        frame = components.merge(scenario_methane, on="iso3", how="left", validate="1:1")
        ratio = frame["methane_adjustment_ratio"]

        frame["ad_capture_sens_net_gwp100_benefit_tco2e"] = (
            frame["ad_screen_avoided_ch4_tpy"] * ratio * GWP100
            + frame["ad_screen_avoided_grid_tco2e"]
            - frame["ad_screen_process_tco2e"]
        )
        frame["bio_cng_capture_sens_net_gwp100_benefit_tco2e"] = (
            frame["bio_cng_screen_avoided_ch4_tpy"] * ratio * GWP100
            + frame["bio_cng_screen_avoided_diesel_tco2e"]
            - frame["bio_cng_screen_upgrading_electricity_tco2e"]
            - frame["bio_cng_screen_process_tco2e"]
        )
        frame["compost_capture_sens_net_gwp100_benefit_tco2e"] = (
            frame["compost_screen_avoided_ch4_tpy"] * ratio * GWP100
            - frame["compost_screen_process_tco2e"]
        )
        frame["prevention_capture_sens_net_gwp100_benefit_tco2e"] = (
            frame["prevention_screen_avoided_ch4_tpy"] * ratio * GWP100
            + frame["prevention_screen_avoided_upstream_tco2e"]
        )

        pathway_cols = {
            "AD-electricity": "ad_capture_sens_net_gwp100_benefit_tco2e",
            "AD-bio-CNG": "bio_cng_capture_sens_net_gwp100_benefit_tco2e",
            "Composting": "compost_capture_sens_net_gwp100_benefit_tco2e",
            "Prevention": "prevention_capture_sens_net_gwp100_benefit_tco2e",
        }
        cols = list(pathway_cols.values())
        has_any = frame[cols].notna().any(axis=1)
        frame["best_pathway_landfill_capture_sensitivity"] = pd.NA
        frame.loc[has_any, "best_pathway_landfill_capture_sensitivity"] = frame.loc[
            has_any, cols
        ].idxmax(axis=1)
        frame["best_pathway_landfill_capture_sensitivity"] = frame[
            "best_pathway_landfill_capture_sensitivity"
        ].map({value: key for key, value in pathway_cols.items()})
        frames.append(frame)

    out = pd.concat(frames, ignore_index=True)
    out.to_csv(OUTPUT_FILE, index=False)

    summary_rows = []
    for scenario, group in out.groupby("scenario"):
        summary_rows.append(
            {
                "scenario": scenario,
                "first_pass_ch4_mt": group["adjusted_first_pass_ch4_total_tpy"].sum(skipna=True) / 1e6,
                "ad_electricity_mtco2e": group["ad_capture_sens_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
                "ad_bio_cng_mtco2e": group["bio_cng_capture_sens_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
                "composting_mtco2e": group["compost_capture_sens_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
                "prevention_mtco2e": group["prevention_capture_sens_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
            }
        )
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(OUTPUTS / "summary_landfill_capture_sensitivity.csv", index=False)

    counts = (
        out.groupby(["scenario", "best_pathway_landfill_capture_sensitivity"], dropna=False)
        .size()
        .reset_index(name="countries")
    )
    counts.to_csv(OUTPUTS / "summary_landfill_capture_best_counts.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(summary.to_string(index=False))
    print("\nBest pathway counts under landfill capture sensitivity:")
    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()
