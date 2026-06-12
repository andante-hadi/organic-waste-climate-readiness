from pathlib import Path

import pandas as pd

from ecoinvent_factors import load_factor_value


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

BASE_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison.csv"
AD_FILE = PROCESSED / "country_ofmsw_ad_screening.csv"
BIO_CNG_FILE = PROCESSED / "country_ofmsw_bio_cng_screening.csv"
COMPOST_FILE = PROCESSED / "country_ofmsw_compost_screening.csv"
OUTPUT_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison_nutrient_sensitivity.csv"

# Conservative generic fertilizer displacement factors for screening only.
DEFAULT_N_SUBSTITUTION_KGCO2E_PER_KG_N = 5.0
DEFAULT_P_SUBSTITUTION_KGCO2E_PER_KG_PHOSPHATE = 1.0
DEFAULT_K_SUBSTITUTION_KGCO2E_PER_KG_K = 0.5

# Conservative agronomic availability/substitution fractions.
COMPOST_N_AVAILABILITY = 0.20
COMPOST_P_AVAILABILITY = 0.50
COMPOST_K_AVAILABILITY = 0.80
DIGESTATE_N_AVAILABILITY = 0.50
DIGESTATE_P_AVAILABILITY = 0.60
DIGESTATE_K_AVAILABILITY = 0.80


def nutrient_credit_tco2e(
    diverted_tpy: pd.Series,
    n_kg_per_tonne: float,
    p_kg_per_tonne: float,
    k_kg_per_tonne: float,
    n_availability: float,
    p_availability: float,
    k_availability: float,
    n_factor: float,
    p_factor: float,
    k_factor: float,
) -> pd.Series:
    n_credit = diverted_tpy * n_kg_per_tonne * n_availability * n_factor / 1000
    p_credit = diverted_tpy * p_kg_per_tonne * p_availability * p_factor / 1000
    k_credit = diverted_tpy * k_kg_per_tonne * k_availability * k_factor / 1000
    return n_credit + p_credit + k_credit


def main() -> None:
    base = pd.read_csv(BASE_FILE)
    ad = pd.read_csv(AD_FILE, usecols=["iso3", "ad_screen_diverted_ofmsw_tpy"])
    bio_cng = pd.read_csv(BIO_CNG_FILE, usecols=["iso3", "bio_cng_screen_diverted_ofmsw_tpy"])
    compost = pd.read_csv(COMPOST_FILE, usecols=["iso3", "compost_screen_diverted_ofmsw_tpy"])

    compost_n, compost_n_source = load_factor_value("composting", "compost_n", 3.59)
    compost_p, compost_p_source = load_factor_value("composting", "compost_p", 1.67)
    compost_k, compost_k_source = load_factor_value("composting", "compost_k", 3.16)
    digestate_n, digestate_n_source = load_factor_value("anaerobic_digestion", "digestate_n", 11.4)
    digestate_p, digestate_p_source = load_factor_value("anaerobic_digestion", "digestate_p", 2.3)
    digestate_k, digestate_k_source = load_factor_value("anaerobic_digestion", "digestate_k", 7.9)

    n_factor, n_factor_source = load_factor_value(
        "fertilizer", "nitrogen_substitution", DEFAULT_N_SUBSTITUTION_KGCO2E_PER_KG_N
    )
    p_factor, p_factor_source = load_factor_value(
        "fertilizer", "phosphorus_substitution", DEFAULT_P_SUBSTITUTION_KGCO2E_PER_KG_PHOSPHATE
    )
    k_factor, k_factor_source = load_factor_value(
        "fertilizer", "potassium_substitution", DEFAULT_K_SUBSTITUTION_KGCO2E_PER_KG_K
    )

    out = base.merge(ad, on="iso3", how="left", validate="1:1").merge(
        bio_cng, on="iso3", how="left", validate="1:1"
    ).merge(compost, on="iso3", how="left", validate="1:1")

    out["compost_nutrient_credit_tco2e"] = nutrient_credit_tco2e(
        out["compost_screen_diverted_ofmsw_tpy"],
        compost_n,
        compost_p,
        compost_k,
        COMPOST_N_AVAILABILITY,
        COMPOST_P_AVAILABILITY,
        COMPOST_K_AVAILABILITY,
        n_factor,
        p_factor,
        k_factor,
    )
    out["ad_electricity_nutrient_credit_tco2e"] = nutrient_credit_tco2e(
        out["ad_screen_diverted_ofmsw_tpy"],
        digestate_n,
        digestate_p,
        digestate_k,
        DIGESTATE_N_AVAILABILITY,
        DIGESTATE_P_AVAILABILITY,
        DIGESTATE_K_AVAILABILITY,
        n_factor,
        p_factor,
        k_factor,
    )
    out["bio_cng_nutrient_credit_tco2e"] = nutrient_credit_tco2e(
        out["bio_cng_screen_diverted_ofmsw_tpy"],
        digestate_n,
        digestate_p,
        digestate_k,
        DIGESTATE_N_AVAILABILITY,
        DIGESTATE_P_AVAILABILITY,
        DIGESTATE_K_AVAILABILITY,
        n_factor,
        p_factor,
        k_factor,
    )

    out["ad_screen_net_gwp100_benefit_with_nutrients_tco2e"] = (
        out["ad_screen_net_gwp100_benefit_tco2e"]
        + out["ad_electricity_nutrient_credit_tco2e"]
    )
    out["bio_cng_screen_net_gwp100_benefit_with_nutrients_tco2e"] = (
        out["bio_cng_screen_net_gwp100_benefit_tco2e"]
        + out["bio_cng_nutrient_credit_tco2e"]
    )
    out["compost_screen_net_gwp100_benefit_with_nutrients_tco2e"] = (
        out["compost_screen_net_gwp100_benefit_tco2e"]
        + out["compost_nutrient_credit_tco2e"]
    )
    out["prevention_screen_net_gwp100_benefit_with_nutrients_tco2e"] = out[
        "prevention_screen_net_gwp100_benefit_tco2e"
    ]

    pathway_cols = {
        "AD-electricity": "ad_screen_net_gwp100_benefit_with_nutrients_tco2e",
        "AD-bio-CNG": "bio_cng_screen_net_gwp100_benefit_with_nutrients_tco2e",
        "Composting": "compost_screen_net_gwp100_benefit_with_nutrients_tco2e",
        "Prevention": "prevention_screen_net_gwp100_benefit_with_nutrients_tco2e",
    }
    cols = list(pathway_cols.values())
    has_any_pathway = out[cols].notna().any(axis=1)
    out["best_four_pathway_with_nutrients"] = pd.NA
    out.loc[has_any_pathway, "best_four_pathway_with_nutrients"] = out.loc[
        has_any_pathway, cols
    ].idxmax(axis=1)
    out["best_four_pathway_with_nutrients"] = out[
        "best_four_pathway_with_nutrients"
    ].map({value: key for key, value in pathway_cols.items()})
    out["best_four_pathway_with_nutrients_benefit_tco2e"] = out[cols].max(axis=1)

    out["nutrient_credit_assumption_note"] = (
        "Conservative screening nutrient credit; phosphate treated as reported kg phosphate; "
        "not central manuscript result."
    )
    out["nutrient_credit_factor_sources"] = (
        f"N={n_factor_source}; P={p_factor_source}; K={k_factor_source}; "
        f"compost_N={compost_n_source}; compost_P={compost_p_source}; compost_K={compost_k_source}; "
        f"digestate_N={digestate_n_source}; digestate_P={digestate_p_source}; digestate_K={digestate_k_source}"
    )

    out.to_csv(OUTPUT_FILE, index=False)

    summary = pd.DataFrame(
        [
            {
                "pathway": "AD-electricity",
                "central_mtco2e": out["ad_screen_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
                "nutrient_credit_mtco2e": out["ad_electricity_nutrient_credit_tco2e"].sum(skipna=True) / 1e6,
                "with_nutrients_mtco2e": out["ad_screen_net_gwp100_benefit_with_nutrients_tco2e"].sum(skipna=True) / 1e6,
            },
            {
                "pathway": "AD-bio-CNG",
                "central_mtco2e": out["bio_cng_screen_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
                "nutrient_credit_mtco2e": out["bio_cng_nutrient_credit_tco2e"].sum(skipna=True) / 1e6,
                "with_nutrients_mtco2e": out["bio_cng_screen_net_gwp100_benefit_with_nutrients_tco2e"].sum(skipna=True) / 1e6,
            },
            {
                "pathway": "Composting",
                "central_mtco2e": out["compost_screen_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
                "nutrient_credit_mtco2e": out["compost_nutrient_credit_tco2e"].sum(skipna=True) / 1e6,
                "with_nutrients_mtco2e": out["compost_screen_net_gwp100_benefit_with_nutrients_tco2e"].sum(skipna=True) / 1e6,
            },
            {
                "pathway": "Prevention",
                "central_mtco2e": out["prevention_screen_net_gwp100_benefit_tco2e"].sum(skipna=True) / 1e6,
                "nutrient_credit_mtco2e": 0.0,
                "with_nutrients_mtco2e": out["prevention_screen_net_gwp100_benefit_with_nutrients_tco2e"].sum(skipna=True) / 1e6,
            },
        ]
    )
    summary.to_csv(OUTPUTS / "summary_nutrient_credit_sensitivity.csv", index=False)

    counts = (
        out["best_four_pathway_with_nutrients"]
        .fillna("Missing/insufficient data")
        .value_counts()
        .rename_axis("best_pathway_with_nutrients")
        .reset_index(name="countries")
    )
    counts.to_csv(OUTPUTS / "summary_best_counts_nutrient_sensitivity.csv", index=False)

    print(f"Wrote {OUTPUT_FILE}")
    print(summary.to_string(index=False))
    print("\nBest pathway counts with nutrient credits:")
    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()
