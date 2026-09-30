from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
FIGURES = ROOT / "manuscript" / "figures"
NATURAL_EARTH = (
    ROOT
    / "data"
    / "raw"
    / "natural_earth"
    / "ne_50m_admin_0_countries"
    / "ne_50m_admin_0_countries.shp"
)

PATHWAY_FILE = PROCESSED / "country_ofmsw_four_pathway_comparison.csv"
METHANE_FILE = PROCESSED / "country_ofmsw_first_pass_methane.csv"
READINESS_FILE = PROCESSED / "country_ofmsw_readiness_index.csv"
SENSITIVITY_FILE = PROCESSED / "country_ofmsw_four_pathway_sensitivity.csv"

ROBINSON = "+proj=robin +lon_0=0 +datum=WGS84 +units=m +no_defs"

PATHWAY_COLORS = {
    "AD-electricity": "#2C7FB8",
    "AD-bio-CNG": "#08519C",
    "Composting": "#41AB5D",
    "Prevention": "#D95F02",
    "Missing/insufficient data": "#D9D9D9",
}

READINESS_COLORS = {
    "Immediate priority": "#1A9850",
    "Strategic build-out": "#FEE08B",
    "No-regret / complementary": "#91BFDB",
    "Longer-term / local fit": "#D73027",
    "Missing/insufficient data": "#D9D9D9",
}


def clean_axes(ax) -> None:
    ax.set_axis_off()
    ax.set_facecolor("white")


def add_source_note(fig) -> None:
    fig.text(
        0.02,
        0.02,
        "Boundary: Natural Earth Admin 0 (1:50m). Values: What a Waste 3.0, WDI, Ember, ecoinvent-derived screening model.",
        fontsize=7,
        color="#555555",
    )


def plot_choropleth(gdf, column, title, outfile, cmap, legend_label, scheme="quantiles") -> None:
    fig, ax = plt.subplots(figsize=(12, 6.5))
    clean_axes(ax)
    gdf.plot(ax=ax, color="#F1F1F1", edgecolor="#FFFFFF", linewidth=0.25)
    if scheme == "quantiles":
        gdf.dropna(subset=[column]).plot(
            ax=ax,
            column=column,
            cmap=cmap,
            scheme="Quantiles",
            k=5,
            legend=True,
            edgecolor="#FFFFFF",
            linewidth=0.25,
            legend_kwds={"loc": "lower left", "title": legend_label, "frameon": False},
        )
    else:
        gdf.dropna(subset=[column]).plot(
            ax=ax,
            column=column,
            cmap=cmap,
            legend=True,
            edgecolor="#FFFFFF",
            linewidth=0.25,
            legend_kwds={"loc": "lower left", "label": legend_label, "shrink": 0.6},
        )
    ax.set_title(title, fontsize=16, loc="left", pad=10)
    add_source_note(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 0.98))
    fig.savefig(FIGURES / outfile, dpi=350)
    plt.close(fig)


def plot_pathway_map(gdf) -> None:
    plot_data = gdf.copy()
    plot_data["pathway_plot"] = plot_data["best_four_pathway_screen"].fillna(
        "Missing/insufficient data"
    )
    fig, ax = plt.subplots(figsize=(12, 6.5))
    clean_axes(ax)
    for pathway, color in PATHWAY_COLORS.items():
        subset = plot_data[plot_data["pathway_plot"] == pathway]
        if not subset.empty:
            subset.plot(ax=ax, color=color, edgecolor="#FFFFFF", linewidth=0.25)
    ax.set_title("Best screened OFMSW climate pathway by country", fontsize=16, loc="left", pad=10)
    handles = [
        Patch(facecolor=color, edgecolor="none", label=label)
        for label, color in PATHWAY_COLORS.items()
    ]
    ax.legend(handles=handles, loc="lower left", frameon=False, ncols=2)
    add_source_note(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 0.98))
    fig.savefig(FIGURES / "map_best_pathway.png", dpi=350)
    plt.close(fig)


def plot_categorical_map(gdf, column, title, outfile, colors) -> None:
    plot_data = gdf.copy()
    plot_data[column] = plot_data[column].fillna("Missing/insufficient data")
    fig, ax = plt.subplots(figsize=(12, 6.5))
    clean_axes(ax)
    for category, color in colors.items():
        subset = plot_data[plot_data[column] == category]
        if not subset.empty:
            subset.plot(ax=ax, color=color, edgecolor="#FFFFFF", linewidth=0.25)
    ax.set_title(title, fontsize=16, loc="left", pad=10)
    handles = [
        Patch(facecolor=color, edgecolor="none", label=label)
        for label, color in colors.items()
    ]
    ax.legend(handles=handles, loc="lower left", frameon=False, ncols=2)
    add_source_note(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 0.98))
    fig.savefig(FIGURES / outfile, dpi=350)
    plt.close(fig)


def plot_advantage_map(gdf) -> None:
    plot_data = gdf.copy()
    values = plot_data["ad_minus_prevention_mtco2e"]
    vmax = values.abs().quantile(0.95)
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    fig, ax = plt.subplots(figsize=(12, 6.5))
    clean_axes(ax)
    gdf.plot(ax=ax, color="#F1F1F1", edgecolor="#FFFFFF", linewidth=0.25)
    plot_data.dropna(subset=["ad_minus_prevention_mtco2e"]).plot(
        ax=ax,
        column="ad_minus_prevention_mtco2e",
        cmap="RdBu",
        norm=norm,
        legend=True,
        edgecolor="#FFFFFF",
        linewidth=0.25,
        legend_kwds={
            "label": "AD minus prevention benefit (Mt CO2e/y)",
            "shrink": 0.6,
        },
    )
    ax.set_title("Where anaerobic digestion outperforms prevention", fontsize=16, loc="left", pad=10)
    add_source_note(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 0.98))
    fig.savefig(FIGURES / "map_ad_minus_prevention.png", dpi=350)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    world = gpd.read_file(NATURAL_EARTH)
    pathways = pd.read_csv(PATHWAY_FILE)
    readiness = pd.read_csv(
        READINESS_FILE,
        usecols=["iso3", "opportunity_readiness_class", "best_pathway_readiness_score"],
    )
    sensitivity = pd.read_csv(
        SENSITIVITY_FILE,
        usecols=["iso3", "robust_winning_pathway", "max_win_probability"],
    )
    methane = pd.read_csv(
        METHANE_FILE,
        usecols=[
            "iso3",
            "ofmsw_food_green_2022_tpy",
            "ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy",
            "first_pass_co2e_gwp100_tpy",
        ],
    )
    data = pathways.merge(
        methane, on="iso3", how="left", validate="1:1", suffixes=("", "_methane")
    ).merge(
        readiness, on="iso3", how="left", validate="1:1"
    ).merge(
        sensitivity, on="iso3", how="left", validate="1:1"
    )
    data = data[(data["iso3"].notna()) & (data["iso3"] != "iso3c")].copy()
    data["ofmsw_food_green_2022_mt"] = data["ofmsw_food_green_2022_tpy_methane"].fillna(
        data["ofmsw_food_green_2022_tpy"]
    ) / 1e6
    data["unmanaged_ofmsw_food_green_2022_mt"] = (
        data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy_methane"].fillna(
            data["ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy"]
        )
        / 1e6
    )
    data["first_pass_methane_mtco2e"] = data["first_pass_co2e_gwp100_tpy"] / 1e6
    data["ad_minus_prevention_mtco2e"] = (
        data[["ad_screen_net_gwp100_benefit_tco2e", "bio_cng_screen_net_gwp100_benefit_tco2e"]].max(axis=1)
        - data["prevention_screen_net_gwp100_benefit_tco2e"]
    ) / 1e6

    join = world.merge(data, left_on="ADM0_A3", right_on="iso3", how="left", validate="m:1")
    join = join.to_crs(ROBINSON)
    join.to_file(OUTPUTS / "country_ofmsw_natural_earth_join.geojson", driver="GeoJSON")

    match_report = pd.DataFrame(
        {
            "metric": [
                "model_iso3_count",
                "matched_model_iso3_count",
                "unmatched_model_iso3_count",
            ],
            "value": [
                data["iso3"].nunique(),
                data["iso3"].isin(set(world["ADM0_A3"])).sum(),
                len(set(data["iso3"]) - set(world["ADM0_A3"])),
            ],
        }
    )
    match_report.to_csv(OUTPUTS / "natural_earth_join_report.csv", index=False)
    unmatched = sorted(set(data["iso3"]) - set(world["ADM0_A3"]))
    pd.DataFrame({"unmatched_iso3": unmatched}).to_csv(
        OUTPUTS / "natural_earth_unmatched_iso3.csv", index=False
    )

    plot_choropleth(
        join,
        "ofmsw_food_green_2022_mt",
        "Food and green OFMSW generation, 2022",
        "map_ofmsw_generation.png",
        "YlGnBu",
        "Mt/y",
    )
    plot_choropleth(
        join,
        "first_pass_methane_mtco2e",
        "First-pass methane burden from unmanaged/disposal OFMSW",
        "map_first_pass_methane.png",
        "OrRd",
        "Mt CO2e/y",
    )
    plot_pathway_map(join)
    plot_advantage_map(join)
    plot_categorical_map(
        join,
        "opportunity_readiness_class",
        "Mitigation-readiness typology for best screened pathway",
        "map_readiness_typology.png",
        READINESS_COLORS,
    )
    plot_categorical_map(
        join,
        "robust_winning_pathway",
        "Robust winning pathway across sensitivity analysis",
        "map_robust_winning_pathway.png",
        {
            **PATHWAY_COLORS,
            "No robust winner": "#969696",
        },
    )

    print(f"Wrote {OUTPUTS / 'country_ofmsw_natural_earth_join.geojson'}")
    print(f"Wrote {OUTPUTS / 'natural_earth_join_report.csv'}")
    print(f"Unmatched ISO3: {', '.join(unmatched)}")


if __name__ == "__main__":
    main()
