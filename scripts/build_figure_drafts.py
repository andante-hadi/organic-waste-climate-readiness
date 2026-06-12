from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
FIGURES = ROOT / "manuscript" / "figures"

PATHWAY_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison.csv"
METHANE_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
READINESS_FILE = PROCESSED / "country_ofmsw_readiness_index.csv"
REGION_FILE = OUTPUTS / "summary_four_pathway_by_region.csv"
COUNTS_FILE = OUTPUTS / "summary_four_pathway_best_counts.csv"
GLOBAL_FILE = OUTPUTS / "summary_four_pathway_global_metrics.csv"
SENSITIVITY_GLOBAL_FILE = OUTPUTS / "sensitivity_global_pathway_summary.csv"
SENSITIVITY_COUNTS_FILE = OUTPUTS / "sensitivity_robust_winner_counts.csv"
SENSITIVITY_COUNTRY_FILE = PROCESSED / "country_ofmsw_four_pathway_sensitivity.csv"
CITY_READINESS_FILE = OUTPUTS / "summary_city_by_country_readiness_class.csv"

COLORS = {
    "Prevention": "#2C7FB8",
    "Composting": "#41AB5D",
    "AD-electricity": "#D99000",
    "AD-bio-CNG": "#8E44AD",
    "No robust winner": "#969696",
    "Missing/insufficient data": "#BDBDBD",
}

READINESS_COLORS = {
    "Immediate priority": "#1A9850",
    "Strategic build-out": "#FEE08B",
    "No-regret / complementary": "#91BFDB",
    "Longer-term / local fit": "#D73027",
    "Missing/insufficient data": "#BDBDBD",
}


def save_table(df: pd.DataFrame, name: str) -> None:
    path = OUTPUTS / name
    df.to_csv(path, index=False)
    print(f"Wrote {path}")


def format_axis(ax, grid_axis="x") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis=grid_axis, color="#E6E6E6", linewidth=0.8)
    ax.set_axisbelow(True)


def figure_global_pathways(global_metrics: pd.DataFrame) -> None:
    row = global_metrics.iloc[0]
    totals = pd.DataFrame(
        {
            "pathway": ["AD-bio-CNG", "Prevention", "AD-electricity", "Composting"],
            "net_benefit_mtco2e": [
                row["ad_bio_cng_net_benefit_mtco2e"],
                row["prevention_net_benefit_mtco2e"],
                row["ad_electricity_net_benefit_mtco2e"],
                row["compost_net_benefit_mtco2e"],
            ],
        }
    )
    save_table(totals, "figure_global_pathway_totals.csv")

    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.barh(
        totals["pathway"],
        totals["net_benefit_mtco2e"],
        color=[COLORS[p] for p in totals["pathway"]],
    )
    ax.set_xlabel("Net GWP100 benefit (Mt CO2e yr$^{-1}$)")
    ax.set_ylabel("")
    ax.invert_yaxis()
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_global_pathway_totals.png", dpi=350)
    plt.close(fig)


def figure_region_pathways(region: pd.DataFrame) -> None:
    keep = [
        "region",
        "ad_electricity_net_benefit_mtco2e",
        "ad_bio_cng_net_benefit_mtco2e",
        "compost_net_benefit_mtco2e",
        "prevention_net_benefit_mtco2e",
    ]
    plot_data = region[keep].copy()
    plot_data = plot_data.sort_values("prevention_net_benefit_mtco2e")
    save_table(plot_data, "figure_region_pathway_totals.csv")

    fig, ax = plt.subplots(figsize=(9.0, 5.3))
    y = range(len(plot_data))
    height = 0.18
    series = [
        ("AD-electricity", "ad_electricity_net_benefit_mtco2e", -1.5 * height),
        ("AD-bio-CNG", "ad_bio_cng_net_benefit_mtco2e", -0.5 * height),
        ("Composting", "compost_net_benefit_mtco2e", 0.5 * height),
        ("Prevention", "prevention_net_benefit_mtco2e", 1.5 * height),
    ]
    for label, column, offset in series:
        ax.barh(
            [i + offset for i in y],
            plot_data[column],
            height=height,
            label=label,
            color=COLORS[label],
        )
    ax.set_yticks(list(y))
    ax.set_yticklabels(plot_data["region"])
    ax.set_xlabel("Net GWP100 benefit (Mt CO2e yr$^{-1}$)")
    ax.set_ylabel("")
    ax.legend(frameon=False, ncols=2, loc="lower right")
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_region_pathway_totals.png", dpi=350)
    plt.close(fig)


def figure_best_counts(counts: pd.DataFrame) -> None:
    counts = counts.copy()
    counts["best_pathway"] = counts["best_pathway"].fillna("Missing/insufficient data")
    order = ["Prevention", "AD-bio-CNG", "AD-electricity", "Composting", "Missing/insufficient data"]
    counts["order"] = counts["best_pathway"].apply(lambda x: order.index(x) if x in order else 99)
    counts = counts.sort_values("order")
    save_table(counts.drop(columns=["order"]), "figure_best_pathway_counts.csv")

    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    ax.barh(
        counts["best_pathway"],
        counts["countries"],
        color=[COLORS.get(p, "#BDBDBD") for p in counts["best_pathway"]],
    )
    ax.set_xlabel("Countries/economies")
    ax.set_ylabel("")
    ax.invert_yaxis()
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_best_pathway_counts.png", dpi=350)
    plt.close(fig)


def figure_robust_counts(counts: pd.DataFrame) -> None:
    counts = counts.copy()
    order = [
        "Prevention",
        "AD-bio-CNG",
        "AD-electricity",
        "Composting",
        "No robust winner",
        "Missing/insufficient data",
    ]
    counts["order"] = counts["robust_winning_pathway"].apply(
        lambda x: order.index(x) if x in order else 99
    )
    counts = counts.sort_values("order")
    save_table(counts.drop(columns=["order"]), "figure_robust_winner_counts.csv")

    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.barh(
        counts["robust_winning_pathway"],
        counts["countries"],
        color=[COLORS.get(p, "#BDBDBD") for p in counts["robust_winning_pathway"]],
    )
    ax.set_xlabel("Countries/economies")
    ax.set_ylabel("")
    ax.invert_yaxis()
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_robust_winner_counts.png", dpi=350)
    plt.close(fig)


def figure_uncertainty_intervals(sensitivity: pd.DataFrame) -> None:
    order = ["Prevention", "AD-bio-CNG", "AD-electricity", "Composting"]
    plot_data = sensitivity.set_index("pathway").loc[order].reset_index()

    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    y = range(len(plot_data))
    lower = plot_data["p50_mtco2e"] - plot_data["p05_mtco2e"]
    upper = plot_data["p95_mtco2e"] - plot_data["p50_mtco2e"]
    ax.errorbar(
        plot_data["p50_mtco2e"],
        y,
        xerr=[lower, upper],
        fmt="o",
        color="#222222",
        ecolor="#555555",
        elinewidth=1.4,
        capsize=4,
    )
    for i, pathway in enumerate(plot_data["pathway"]):
        ax.scatter(plot_data.loc[i, "p50_mtco2e"], i, s=80, color=COLORS[pathway], zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels(plot_data["pathway"])
    ax.set_xlabel("Net GWP100 benefit (Mt CO2e yr$^{-1}$)")
    ax.set_ylabel("")
    ax.invert_yaxis()
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_uncertainty_intervals.png", dpi=350)
    plt.close(fig)


def figure_hotspots(pathways: pd.DataFrame, methane: pd.DataFrame) -> None:
    data = pathways.merge(
        methane[["iso3", "first_pass_co2e_gwp100_tpy"]],
        on="iso3",
        how="left",
        validate="1:1",
    )
    hotspots = data[
        [
            "country",
            "region",
            "best_four_pathway_screen",
            "best_four_pathway_benefit_tco2e",
            "first_pass_co2e_gwp100_tpy",
        ]
    ].dropna(subset=["best_four_pathway_benefit_tco2e"])
    hotspots = hotspots.sort_values("best_four_pathway_benefit_tco2e", ascending=False).head(20)
    hotspots["best_pathway_benefit_mtco2e"] = hotspots["best_four_pathway_benefit_tco2e"] / 1e6
    hotspots["first_pass_methane_mtco2e"] = hotspots["first_pass_co2e_gwp100_tpy"] / 1e6
    save_table(hotspots, "figure_top20_country_hotspots.csv")

    fig, ax = plt.subplots(figsize=(8.0, 6.2))
    plot_data = hotspots.sort_values("best_pathway_benefit_mtco2e")
    ax.barh(
        plot_data["country"],
        plot_data["best_pathway_benefit_mtco2e"],
        color=[COLORS.get(p, "#808080") for p in plot_data["best_four_pathway_screen"]],
    )
    ax.set_xlabel("Best screened pathway benefit (Mt CO2e yr$^{-1}$)")
    ax.set_ylabel("")
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_top20_country_hotspots.png", dpi=350)
    plt.close(fig)


def figure_readiness_scatter(readiness: pd.DataFrame) -> None:
    plot_data = readiness.dropna(
        subset=[
            "mitigation_potential_score",
            "best_pathway_readiness_score",
            "opportunity_readiness_class",
        ]
    ).copy()

    fig, ax = plt.subplots(figsize=(6.2, 5.3))
    for label, color in READINESS_COLORS.items():
        subset = plot_data[plot_data["opportunity_readiness_class"] == label]
        if subset.empty:
            continue
        ax.scatter(
            subset["best_pathway_readiness_score"],
            subset["mitigation_potential_score"],
            s=35,
            alpha=0.78,
            label=label,
            color=color,
            edgecolor="white",
            linewidth=0.35,
        )
    ax.axhline(0.67, color="#555555", linewidth=0.8, linestyle="--")
    ax.axvline(0.60, color="#555555", linewidth=0.8, linestyle="--")
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("Best-pathway readiness score")
    ax.set_ylabel("Mitigation potential score")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    format_axis(ax, grid_axis="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_readiness_scatter.png", dpi=350)
    plt.close(fig)


def figure_uncertainty_confidence(sensitivity_country: pd.DataFrame) -> None:
    data = sensitivity_country.copy()
    data = data[
        data["robust_winning_pathway"].notna()
        & (data["robust_winning_pathway"] != "Missing/insufficient data")
    ]

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    bins = [0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    ax.hist(
        data["max_win_probability"],
        bins=bins,
        color="#666666",
        edgecolor="white",
        linewidth=0.8,
    )
    ax.axvline(0.50, color="#222222", linestyle="--", linewidth=1)
    ax.set_xlabel("Maximum pathway win probability")
    ax.set_ylabel("Countries/economies")
    format_axis(ax, grid_axis="y")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_uncertainty_confidence.png", dpi=350)
    plt.close(fig)


def figure_top_readiness_countries(readiness: pd.DataFrame) -> None:
    keep_classes = ["Immediate priority", "Strategic build-out"]
    plot_data = readiness[
        readiness["opportunity_readiness_class"].isin(keep_classes)
    ].copy()
    plot_data = plot_data.sort_values("best_four_pathway_benefit_tco2e", ascending=False).head(16)
    plot_data["best_benefit_mtco2e"] = plot_data["best_four_pathway_benefit_tco2e"] / 1e6
    save_table(
        plot_data[
            [
                "country",
                "region",
                "best_four_pathway_screen",
                "best_benefit_mtco2e",
                "mitigation_potential_score",
                "best_pathway_readiness_score",
                "opportunity_readiness_class",
            ]
        ],
        "figure_top_readiness_countries.csv",
    )

    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    draw = plot_data.sort_values("best_benefit_mtco2e")
    ax.barh(
        draw["country"],
        draw["best_benefit_mtco2e"],
        color=[READINESS_COLORS.get(c, "#999999") for c in draw["opportunity_readiness_class"]],
    )
    ax.set_xlabel("Best screened pathway benefit (Mt CO2e yr$^{-1}$)")
    ax.set_ylabel("")
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_top_readiness_countries.png", dpi=350)
    plt.close(fig)


def figure_city_readiness_alignment(city_readiness: pd.DataFrame) -> None:
    data = city_readiness.copy()
    data["opportunity_readiness_class"] = data["opportunity_readiness_class"].fillna(
        "Missing / insufficient data"
    )
    data = data.sort_values("city_unmanaged_ofmsw_mt", ascending=True)

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.barh(
        data["opportunity_readiness_class"],
        data["city_unmanaged_ofmsw_mt"],
        color=[READINESS_COLORS.get(c, "#BDBDBD") for c in data["opportunity_readiness_class"]],
    )
    ax.set_xlabel("City unmanaged/disposal OFMSW (Mt yr$^{-1}$)")
    ax.set_ylabel("")
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_city_readiness_alignment.png", dpi=350)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    pathways = pd.read_csv(PATHWAY_FILE)
    methane = pd.read_csv(METHANE_FILE)
    readiness = pd.read_csv(READINESS_FILE)
    region = pd.read_csv(REGION_FILE)
    counts = pd.read_csv(COUNTS_FILE)
    global_metrics = pd.read_csv(GLOBAL_FILE)
    sensitivity_global = pd.read_csv(SENSITIVITY_GLOBAL_FILE)
    sensitivity_counts = pd.read_csv(SENSITIVITY_COUNTS_FILE)
    sensitivity_country = pd.read_csv(SENSITIVITY_COUNTRY_FILE)
    city_readiness = pd.read_csv(CITY_READINESS_FILE)

    figure_global_pathways(global_metrics)
    figure_region_pathways(region)
    figure_best_counts(counts)
    figure_robust_counts(sensitivity_counts)
    figure_uncertainty_intervals(sensitivity_global)
    figure_hotspots(pathways, methane)
    figure_readiness_scatter(readiness)
    figure_uncertainty_confidence(sensitivity_country)
    figure_top_readiness_countries(readiness)
    figure_city_readiness_alignment(city_readiness)


if __name__ == "__main__":
    main()
