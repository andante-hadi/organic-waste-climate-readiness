from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch


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
READINESS_WEIGHTING_FILE = OUTPUTS / "summary_readiness_weighting_robustness.csv"

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


def figure_conceptual_framework() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    left = [
        "Hierarchy\npreference",
        "Methane\nopportunity",
        "Robustness",
        "Readiness",
    ]
    y_positions = [0.78, 0.58, 0.38, 0.18]
    colors = ["#2C7FB8", "#D95F02", "#666666", "#1A9850"]

    ax.text(
        0.04,
        0.94,
        "Mitigation-readiness screen",
        fontsize=13,
        weight="bold",
        color="#222222",
        ha="left",
        va="center",
    )
    ax.text(
        0.04,
        0.89,
        "Four decision layers convert hierarchy principles into deployment priorities",
        fontsize=8.8,
        color="#555555",
        ha="left",
        va="center",
    )

    for title, y, color in zip(left, y_positions, colors):
        box = FancyBboxPatch(
            (0.04, y - 0.07),
            0.34,
            0.12,
            boxstyle="round,pad=0.012,rounding_size=0.012",
            facecolor=color,
            alpha=0.13,
            edgecolor=color,
            linewidth=1.1,
        )
        ax.add_patch(box)
        ax.text(
            0.21,
            y,
            title,
            fontsize=12,
            weight="bold",
            color="#222222",
            va="center",
            ha="center",
        )
        ax.annotate(
            "",
            xy=(0.55, y),
            xytext=(0.39, y),
            arrowprops=dict(arrowstyle="->", lw=1.2, color="#555555", shrinkA=0, shrinkB=0),
        )

    output = FancyBboxPatch(
        (0.56, 0.11),
        0.38,
        0.74,
        boxstyle="round,pad=0.016,rounding_size=0.015",
        facecolor="#F7F7F7",
        edgecolor="#333333",
        linewidth=1.1,
    )
    ax.add_patch(output)
    ax.text(
        0.75,
        0.77,
        "Deployment priority",
        fontsize=13,
        weight="bold",
        ha="center",
        color="#222222",
    )
    priorities = [
        ("Immediate priority", "#1A9850"),
        ("Strategic build-out", "#FEE08B"),
        ("No-regret / complementary", "#91BFDB"),
        ("Longer-term / local fit", "#D73027"),
    ]
    for i, (label, color) in enumerate(priorities):
        y = 0.64 - i * 0.13
        priority_box = FancyBboxPatch(
            (0.62, y - 0.045),
            0.26,
            0.075,
            boxstyle="round,pad=0.008,rounding_size=0.01",
            facecolor=color,
            alpha=0.9,
            edgecolor="white",
            linewidth=0.8,
        )
        ax.add_patch(priority_box)
        ax.text(0.75, y - 0.008, label, ha="center", va="center", fontsize=9, color="#222222")
    ax.text(
        0.75,
        0.17,
        "Policy sequencing,\nnot universal ranking",
        ha="center",
        va="center",
        fontsize=9,
        color="#333333",
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_conceptual_framework.png", dpi=350)
    plt.close(fig)


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


def figure_win_probability_by_winner(sensitivity_country: pd.DataFrame) -> None:
    data = sensitivity_country.copy()
    data = data[
        data["robust_winning_pathway"].notna()
        & (data["robust_winning_pathway"] != "Missing/insufficient data")
    ].copy()
    order = ["Prevention", "AD-bio-CNG", "AD-electricity", "No robust winner"]
    data = data[data["robust_winning_pathway"].isin(order)]
    positions = {label: i for i, label in enumerate(order)}

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    for label in order:
        subset = data[data["robust_winning_pathway"] == label]
        if subset.empty:
            continue
        x = [positions[label]] * len(subset)
        ax.scatter(
            x,
            subset["max_win_probability"],
            s=24,
            alpha=0.55,
            color=COLORS.get(label, "#777777"),
            edgecolor="white",
            linewidth=0.25,
        )
        median = subset["max_win_probability"].median()
        ax.plot(
            [positions[label] - 0.28, positions[label] + 0.28],
            [median, median],
            color="#222222",
            linewidth=1.5,
        )
    ax.axhline(0.50, color="#333333", linestyle="--", linewidth=0.9)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=20, ha="right")
    ax.set_ylim(0.45, 1.02)
    ax.set_ylabel("Maximum pathway win probability")
    ax.set_xlabel("")
    format_axis(ax, grid_axis="y")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_win_probability_by_winner.png", dpi=350)
    plt.close(fig)


def figure_robust_recovery_opportunities(
    sensitivity_country: pd.DataFrame, pathways: pd.DataFrame
) -> None:
    data = sensitivity_country.drop(columns=["country"], errors="ignore").merge(
        pathways[
            [
                "iso3",
                "country",
                "best_four_pathway_screen",
                "best_four_pathway_benefit_tco2e",
            ]
        ],
        on="iso3",
        how="left",
        validate="1:1",
    )
    data = data[
        data["robust_winning_pathway"].isin(["AD-bio-CNG", "AD-electricity"])
    ].dropna(subset=["best_four_pathway_benefit_tco2e"])
    data["best_benefit_mtco2e"] = data["best_four_pathway_benefit_tco2e"] / 1e6
    data = data.sort_values("best_benefit_mtco2e", ascending=False).head(12)
    save_table(
        data[
            [
                "country",
                "robust_winning_pathway",
                "max_win_probability",
                "best_benefit_mtco2e",
            ]
        ],
        "figure_robust_recovery_opportunities.csv",
    )

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    draw = data.sort_values("best_benefit_mtco2e")
    bars = ax.barh(
        draw["country"],
        draw["best_benefit_mtco2e"],
        color=[COLORS.get(p, "#777777") for p in draw["robust_winning_pathway"]],
    )
    for bar, prob in zip(bars, draw["max_win_probability"]):
        ax.text(
            bar.get_width() + 0.15,
            bar.get_y() + bar.get_height() / 2,
            f"{prob:.2f}",
            va="center",
            ha="left",
            fontsize=8,
            color="#333333",
        )
    ax.set_xlabel("Best screened pathway benefit (Mt CO2e yr$^{-1}$)")
    ax.set_ylabel("")
    ax.set_title("Robust AD recovery opportunities", loc="left", fontsize=11)
    ax.text(
        0.99,
        0.02,
        "Labels show win probability",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#555555",
    )
    format_axis(ax)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_robust_recovery_opportunities.png", dpi=350)
    plt.close(fig)


def figure_readiness_weighting_robustness(weighting: pd.DataFrame) -> None:
    data = weighting.copy()
    data["Scenario"] = data["Scenario"].replace(
        {
            "Central equal weights": "Central",
            "Economic-capacity-heavy": "Economic\ncapacity",
            "Data-completeness-heavy": "Data\ncompleteness",
            "Infrastructure-heavy": "Infrastructure",
            "Collection-heavy": "Collection",
        }
    )
    order = ["Central", "Collection", "Economic\ncapacity", "Infrastructure", "Data\ncompleteness"]
    data["order"] = data["Scenario"].apply(lambda x: order.index(x) if x in order else 99)
    data = data.sort_values("order")

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    bars = ax.bar(
        data["Scenario"],
        data["Immediate priority"],
        color="#1A9850",
        alpha=0.85,
    )
    ax.axhline(46, color="#333333", linestyle="--", linewidth=0.9)
    for bar, pct in zip(bars, data["Central immediate priorities retained (%)"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.0,
            f"{pct:.0f}% retained",
            ha="center",
            va="bottom",
            fontsize=8,
            color="#333333",
        )
    ax.set_ylim(0, max(data["Immediate priority"]) + 10)
    ax.set_ylabel("Immediate-priority countries/economies")
    ax.set_xlabel("")
    ax.set_title("Readiness classes under alternative weights", loc="left", fontsize=11)
    format_axis(ax, grid_axis="y")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_readiness_weighting_robustness.png", dpi=350)
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
    weighting = pd.read_csv(READINESS_WEIGHTING_FILE)

    figure_global_pathways(global_metrics)
    figure_conceptual_framework()
    figure_region_pathways(region)
    figure_best_counts(counts)
    figure_robust_counts(sensitivity_counts)
    figure_uncertainty_intervals(sensitivity_global)
    figure_hotspots(pathways, methane)
    figure_readiness_scatter(readiness)
    figure_uncertainty_confidence(sensitivity_country)
    figure_win_probability_by_winner(sensitivity_country)
    figure_robust_recovery_opportunities(sensitivity_country, pathways)
    figure_top_readiness_countries(readiness)
    figure_city_readiness_alignment(city_readiness)
    figure_readiness_weighting_robustness(weighting)


if __name__ == "__main__":
    main()
