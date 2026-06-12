from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

AD_FILE = PROCESSED / "country_ofmsw_ad_screening.csv"
COMPOST_FILE = PROCESSED / "country_ofmsw_compost_screening.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_screening_pathway_comparison.csv"


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    ad = pd.read_csv(AD_FILE)
    compost = pd.read_csv(COMPOST_FILE)

    keep_ad = [
        "iso3",
        "country",
        "region",
        "income_2022",
        "ofmsw_food_green_2022_tpy",
        "ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy",
        "electricity_carbon_intensity_2022_gco2_kwh",
        "ad_screen_net_gwp100_benefit_tco2e",
        "ad_screen_avoided_grid_tco2e",
        "ad_screen_grid_credit_share",
    ]
    keep_compost = [
        "iso3",
        "compost_screen_net_gwp100_benefit_tco2e",
    ]

    out = ad[keep_ad].merge(compost[keep_compost], on="iso3", how="left", validate="1:1")
    out["ad_minus_compost_tco2e"] = (
        out["ad_screen_net_gwp100_benefit_tco2e"]
        - out["compost_screen_net_gwp100_benefit_tco2e"]
    )
    out["best_screening_pathway"] = "AD"
    out.loc[
        out["compost_screen_net_gwp100_benefit_tco2e"] > out["ad_screen_net_gwp100_benefit_tco2e"],
        "best_screening_pathway",
    ] = "Composting"
    out.loc[
        out[["ad_screen_net_gwp100_benefit_tco2e", "compost_screen_net_gwp100_benefit_tco2e"]]
        .isna()
        .all(axis=1),
        "best_screening_pathway",
    ] = pd.NA

    out.to_csv(OUTPUT_FILE, index=False)

    ranking_cols = [
        "country",
        "region",
        "income_2022",
        "electricity_carbon_intensity_2022_gco2_kwh",
        "ad_screen_net_gwp100_benefit_tco2e",
        "compost_screen_net_gwp100_benefit_tco2e",
        "ad_minus_compost_tco2e",
        "best_screening_pathway",
    ]
    out.sort_values("ad_minus_compost_tco2e", ascending=False)[ranking_cols].head(30).to_csv(
        OUTPUTS / "top30_ad_advantage_over_compost.csv", index=False
    )

    print(f"Wrote {OUTPUT_FILE}")
    print(
        "Global AD net benefit: "
        f"{out['ad_screen_net_gwp100_benefit_tco2e'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )
    print(
        "Global compost net benefit: "
        f"{out['compost_screen_net_gwp100_benefit_tco2e'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )
    print(
        "Global AD advantage over compost: "
        f"{out['ad_minus_compost_tco2e'].sum(skipna=True) / 1e6:,.1f} Mt CO2e/y"
    )
    print(out["best_screening_pathway"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
