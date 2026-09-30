from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

AD_FILE = PROCESSED / "country_ofmsw_ad_screening.csv"
COMPOST_FILE = PROCESSED / "country_ofmsw_compost_screening.csv"
PREVENTION_FILE = PROCESSED / "country_ofmsw_prevention_screening.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_three_pathway_comparison.csv"


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    ad = pd.read_csv(AD_FILE)
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
            "ad_screen_net_gwp100_benefit_tco2e",
        ]
    ].merge(
        compost[["iso3", "compost_screen_net_gwp100_benefit_tco2e"]],
        on="iso3",
        how="left",
        validate="1:1",
    ).merge(
        prevention[["iso3", "prevention_screen_net_gwp100_benefit_tco2e"]],
        on="iso3",
        how="left",
        validate="1:1",
    )

    pathway_cols = {
        "AD": "ad_screen_net_gwp100_benefit_tco2e",
        "Composting": "compost_screen_net_gwp100_benefit_tco2e",
        "Prevention": "prevention_screen_net_gwp100_benefit_tco2e",
    }
    has_any_pathway = out[list(pathway_cols.values())].notna().any(axis=1)
    out["best_three_pathway_screen"] = pd.NA
    out.loc[has_any_pathway, "best_three_pathway_screen"] = out.loc[
        has_any_pathway, list(pathway_cols.values())
    ].idxmax(axis=1)
    out["best_three_pathway_screen"] = out["best_three_pathway_screen"].map(
        {value: key for key, value in pathway_cols.items()}
    )
    out["best_three_pathway_benefit_tco2e"] = out[list(pathway_cols.values())].max(axis=1)

    out.to_csv(OUTPUT_FILE, index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "ad_screen_net_gwp100_benefit_tco2e",
        "compost_screen_net_gwp100_benefit_tco2e",
        "prevention_screen_net_gwp100_benefit_tco2e",
        "best_three_pathway_screen",
        "best_three_pathway_benefit_tco2e",
    ]
    out.sort_values("best_three_pathway_benefit_tco2e", ascending=False)[ranking_cols].head(40).to_csv(
        OUTPUTS / "top40_three_pathway_screening.csv", index=False
    )

    print(f"Wrote {OUTPUT_FILE}")
    for label, col in pathway_cols.items():
        print(f"Global {label} net benefit: {out[col].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y")
    print("\nBest pathway counts:")
    print(out["best_three_pathway_screen"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
