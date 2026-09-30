from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

INPUT_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
OUTPUT_COUNTRY_FILE = PROCESSED / "country_ofmsw_four_pathway_sensitivity.csv"

N_ITER = 1000
RANDOM_SEED = 20260523

DIVERSION_RATE = 0.50
SOURCE_SEPARATION_CAPTURE_RATE = 0.80
METHANE_LHV_MJ_PER_M3 = 35.8
CH4_LHV_KWH_PER_M3 = 9.97


def uniform(rng: np.random.Generator, low: float, high: float, size: int) -> np.ndarray:
    return rng.uniform(low, high, size=size)


def triangular(
    rng: np.random.Generator,
    low: float,
    mode: float,
    high: float,
    size: int,
) -> np.ndarray:
    return rng.triangular(low, mode, high, size=size)


def summarize(values: np.ndarray, name: str) -> dict:
    return {
        "pathway": name,
        "mean_mtco2e": float(np.nanmean(values)),
        "p05_mtco2e": float(np.nanpercentile(values, 5)),
        "p50_mtco2e": float(np.nanpercentile(values, 50)),
        "p95_mtco2e": float(np.nanpercentile(values, 95)),
    }


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    data = pd.read_csv(INPUT_FILE)
    data = data[(data["iso3"].notna()) & (data["iso3"] != "iso3c")].copy()

    available = data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"].to_numpy()
    food_unmanaged = (
        data["msw_2022_tpy"]
        * data["food_frac"]
        * data["landfill_dump_uncollected_frac"]
    ).to_numpy()
    first_pass_ch4 = data["first_pass_ch4_total_tpy"].to_numpy()
    grid_ci = data["electricity_carbon_intensity_2022_gco2_kwh"].to_numpy()

    diverted = available * DIVERSION_RATE * SOURCE_SEPARATION_CAPTURE_RATE
    diversion_fraction = np.divide(
        diverted,
        available,
        out=np.full_like(diverted, np.nan, dtype=float),
        where=available != 0,
    )
    avoided_landfill = first_pass_ch4 * diversion_fraction * 27.2

    global_results = []
    country_wins = np.zeros((len(data), 4), dtype=float)
    pathway_order = ["AD-electricity", "AD-bio-CNG", "Composting", "Prevention"]

    ad_global = []
    bio_cng_global = []
    compost_global = []
    prevention_global = []

    for _ in range(N_ITER):
        ad_process = triangular(rng, 40, 74.289, 130, 1)[0]
        compost_process = triangular(rng, 20, 34.025, 90, 1)[0]
        biogas_yield = triangular(rng, 70, 100, 150, 1)[0]
        methane_share = uniform(rng, 0.55, 0.70, 1)[0]
        electricity_eff = uniform(rng, 0.25, 0.40, 1)[0]
        methane_recovery = uniform(rng, 0.90, 0.99, 1)[0]
        upgrading_kwh = triangular(rng, 0.25, 0.45, 0.80, 1)[0]
        diesel_substitution = uniform(rng, 0.055, 0.090, 1)[0]
        prevention_rate = uniform(rng, 0.10, 0.30, 1)[0]
        upstream_food = triangular(rng, 800, 1500, 2800, 1)[0]

        ad_electricity_yield = (
            biogas_yield * methane_share * CH4_LHV_KWH_PER_M3 * electricity_eff
        )
        ad_grid_credit = diverted * ad_electricity_yield / 1000 * grid_ci / 1000
        ad_process_burden = diverted * ad_process / 1000
        ad_net = avoided_landfill + ad_grid_credit - ad_process_burden

        biomethane_m3 = diverted * biogas_yield * methane_share * methane_recovery
        biomethane_mj = biomethane_m3 * METHANE_LHV_MJ_PER_M3
        diesel_credit = biomethane_mj * diesel_substitution / 1000
        upgrading_burden = diverted * biogas_yield * upgrading_kwh / 1000 * grid_ci / 1000
        bio_cng_net = avoided_landfill + diesel_credit - upgrading_burden - ad_process_burden

        compost_net = avoided_landfill - diverted * compost_process / 1000

        prevented = food_unmanaged * prevention_rate
        prevention_fraction = np.divide(
            prevented,
            available,
            out=np.full_like(prevented, np.nan, dtype=float),
            where=available != 0,
        )
        prevention_net = (
            first_pass_ch4 * prevention_fraction * 27.2
            + prevented * upstream_food / 1000
        )

        stacked = np.vstack([ad_net, bio_cng_net, compost_net, prevention_net]).T
        valid = ~np.all(np.isnan(stacked), axis=1)
        winners = np.full(len(data), -1)
        winners[valid] = np.nanargmax(stacked[valid], axis=1)
        for idx in range(4):
            country_wins[:, idx] += winners == idx

        ad_global.append(np.nansum(ad_net) / 1e6)
        bio_cng_global.append(np.nansum(bio_cng_net) / 1e6)
        compost_global.append(np.nansum(compost_net) / 1e6)
        prevention_global.append(np.nansum(prevention_net) / 1e6)

    global_summary = pd.DataFrame(
        [
            summarize(np.array(ad_global), "AD-electricity"),
            summarize(np.array(bio_cng_global), "AD-bio-CNG"),
            summarize(np.array(compost_global), "Composting"),
            summarize(np.array(prevention_global), "Prevention"),
        ]
    )
    global_summary.to_csv(OUTPUTS / "sensitivity_global_pathway_summary.csv", index=False)

    win_prob = country_wins / N_ITER
    country = data[["iso3", "country", "region", "income_2022"]].copy()
    for idx, pathway in enumerate(pathway_order):
        country[f"win_probability_{pathway}"] = win_prob[:, idx]
    robust = []
    for row in win_prob:
        if row.max() >= 0.5:
            robust.append(pathway_order[int(np.argmax(row))])
        elif row.max() == 0:
            robust.append("Missing/insufficient data")
        else:
            robust.append("No robust winner")
    country["robust_winning_pathway"] = robust
    country["max_win_probability"] = win_prob.max(axis=1)
    country.to_csv(OUTPUT_COUNTRY_FILE, index=False)

    robust_counts = (
        country["robust_winning_pathway"]
        .value_counts()
        .rename_axis("robust_winning_pathway")
        .reset_index(name="countries")
    )
    robust_counts.to_csv(OUTPUTS / "sensitivity_robust_winner_counts.csv", index=False)

    print(f"Wrote {OUTPUTS / 'sensitivity_global_pathway_summary.csv'}")
    print(f"Wrote {OUTPUT_COUNTRY_FILE}")
    print(robust_counts.to_string(index=False))


if __name__ == "__main__":
    main()
