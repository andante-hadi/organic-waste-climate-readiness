from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

AD_FILE = PROCESSED / "country_ofmsw_ad_screening.csv"
BIO_CNG_FILE = PROCESSED / "country_ofmsw_bio_cng_screening.csv"
COMPOST_FILE = PROCESSED / "country_ofmsw_compost_screening.csv"
PREVENTION_FILE = PROCESSED / "country_ofmsw_prevention_screening.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison_gwp20.csv"

GWP20_BIOGENIC_CH4 = 80.8


def methane_gwp20(avoided_ch4_tpy: pd.Series) -> pd.Series:
    return avoided_ch4_tpy * GWP20_BIOGENIC_CH4


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    ad = pd.read_csv(AD_FILE)
    bio_cng = pd.read_csv(BIO_CNG_FILE)
    compost = pd.read_csv(COMPOST_FILE)
    prevention = pd.read_csv(PREVENTION_FILE)

    out = ad[
        [
            "iso3",
            "country",
            "region",
            "income_2022",
            "ofmsw_food_green_2022_tpy",
            "ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy",
            "electricity_carbon_intensity_2022_gco2_kwh",
            "ad_screen_avoided_ch4_tpy",
            "ad_screen_avoided_grid_tco2e",
            "ad_screen_process_tco2e",
        ]
    ].merge(
        bio_cng[
            [
                "iso3",
                "bio_cng_screen_avoided_ch4_tpy",
                "bio_cng_screen_avoided_diesel_tco2e",
                "bio_cng_screen_upgrading_electricity_tco2e",
                "bio_cng_screen_process_tco2e",
            ]
        ],
        on="iso3",
        how="left",
        validate="1:1",
    ).merge(
        compost[
            [
                "iso3",
                "compost_screen_avoided_ch4_tpy",
                "compost_screen_process_tco2e",
            ]
        ],
        on="iso3",
        how="left",
        validate="1:1",
    ).merge(
        prevention[
            [
                "iso3",
                "prevention_screen_avoided_ch4_tpy",
                "prevention_screen_avoided_upstream_tco2e",
            ]
        ],
        on="iso3",
        how="left",
        validate="1:1",
    )

    out["ad_screen_avoided_landfill_gwp20_tco2e"] = methane_gwp20(
        out["ad_screen_avoided_ch4_tpy"]
    )
    out["bio_cng_screen_avoided_landfill_gwp20_tco2e"] = methane_gwp20(
        out["bio_cng_screen_avoided_ch4_tpy"]
    )
    out["compost_screen_avoided_landfill_gwp20_tco2e"] = methane_gwp20(
        out["compost_screen_avoided_ch4_tpy"]
    )
    out["prevention_screen_avoided_landfill_gwp20_tco2e"] = methane_gwp20(
        out["prevention_screen_avoided_ch4_tpy"]
    )

    out["ad_screen_net_gwp20_benefit_tco2e"] = (
        out["ad_screen_avoided_landfill_gwp20_tco2e"]
        + out["ad_screen_avoided_grid_tco2e"]
        - out["ad_screen_process_tco2e"]
    )
    out["bio_cng_screen_net_gwp20_benefit_tco2e"] = (
        out["bio_cng_screen_avoided_landfill_gwp20_tco2e"]
        + out["bio_cng_screen_avoided_diesel_tco2e"]
        - out["bio_cng_screen_upgrading_electricity_tco2e"]
        - out["bio_cng_screen_process_tco2e"]
    )
    out["compost_screen_net_gwp20_benefit_tco2e"] = (
        out["compost_screen_avoided_landfill_gwp20_tco2e"]
        - out["compost_screen_process_tco2e"]
    )
    out["prevention_screen_net_gwp20_benefit_tco2e"] = (
        out["prevention_screen_avoided_landfill_gwp20_tco2e"]
        + out["prevention_screen_avoided_upstream_tco2e"]
    )

    pathway_cols = {
        "AD-electricity": "ad_screen_net_gwp20_benefit_tco2e",
        "AD-bio-CNG": "bio_cng_screen_net_gwp20_benefit_tco2e",
        "Composting": "compost_screen_net_gwp20_benefit_tco2e",
        "Prevention": "prevention_screen_net_gwp20_benefit_tco2e",
    }
    cols = list(pathway_cols.values())
    has_any_pathway = out[cols].notna().any(axis=1)
    out["best_four_pathway_screen_gwp20"] = pd.NA
    out.loc[has_any_pathway, "best_four_pathway_screen_gwp20"] = out.loc[
        has_any_pathway, cols
    ].idxmax(axis=1)
    out["best_four_pathway_screen_gwp20"] = out["best_four_pathway_screen_gwp20"].map(
        {value: key for key, value in pathway_cols.items()}
    )
    out["best_four_pathway_benefit_gwp20_tco2e"] = out[cols].max(axis=1)

    out.to_csv(OUTPUT_FILE, index=False)

    summary = pd.DataFrame(
        [
            {
                "pathway": label,
                "net_benefit_mtco2e": out[col].sum(skipna=True) / 1e6,
            }
            for label, col in pathway_cols.items()
        ]
    )
    summary.to_csv(OUTPUTS / "summary_four_pathway_global_metrics_gwp20.csv", index=False)

    counts = (
        out["best_four_pathway_screen_gwp20"]
        .fillna("Missing/insufficient data")
        .value_counts()
        .rename_axis("best_pathway_gwp20")
        .reset_index(name="countries")
    )
    counts.to_csv(OUTPUTS / "summary_four_pathway_best_counts_gwp20.csv", index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "ad_screen_net_gwp20_benefit_tco2e",
        "bio_cng_screen_net_gwp20_benefit_tco2e",
        "compost_screen_net_gwp20_benefit_tco2e",
        "prevention_screen_net_gwp20_benefit_tco2e",
        "best_four_pathway_screen_gwp20",
        "best_four_pathway_benefit_gwp20_tco2e",
    ]
    out.sort_values("best_four_pathway_benefit_gwp20_tco2e", ascending=False)[
        ranking_cols
    ].head(40).to_csv(OUTPUTS / "top40_four_pathway_screening_gwp20.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    for label, col in pathway_cols.items():
        print(f"Global {label} GWP20 net benefit: {out[col].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y")
    print("\nGWP20 best pathway counts:")
    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()
