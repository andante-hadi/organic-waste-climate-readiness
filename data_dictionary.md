# Data Dictionary

This document describes the main processed datasets used in the Nature Sustainability manuscript draft. It focuses on publication-facing outputs rather than every intermediate file.

## Common Identifiers

| Column | Meaning |
|---|---|
| `iso3` | ISO3 country/economy code used for joins. |
| `country` | Country/economy name. |
| `region` | World Bank-style regional grouping used in the analysis. |
| `income_2022` | 2022 income group. |

## `data/processed/country_ofmsw_analysis_dataset.csv`

Main harmonized country dataset combining What a Waste 3.0, WDI and Ember.

| Column | Meaning |
|---|---|
| `msw_tpy` | Reported municipal solid waste generation in tonnes per year for the source reporting year. |
| `msw_kg_cap_day` | Reported municipal solid waste generation in kg per capita per day. |
| `msw_2022_tpy` | Estimated municipal solid waste generation in 2022, tonnes per year. |
| `population_2022` | 2022 population used for waste projection/normalization. |
| `food_pct` | Food waste share of municipal solid waste, percent. |
| `green_pct` | Green/garden waste share of municipal solid waste, percent. |
| `wood_pct` | Wood waste share of municipal solid waste, percent. |
| `food_frac` | Food waste share as a fraction. |
| `green_frac` | Green/garden waste share as a fraction. |
| `wood_frac` | Wood waste share as a fraction. |
| `collection_total_population_pct` | Reported collection coverage as percent of population. |
| `collection_total_weight_pct` | Reported collection coverage as percent of generated waste mass. |
| `treatment_*_pct` | Reported treatment share in percent for the named pathway. |
| `treatment_*_frac` | Reported treatment share as a fraction for the named pathway. |
| `ofmsw_food_green_frac` | Food plus green waste fraction of MSW. |
| `ofmsw_food_green_2022_tpy` | Food plus green OFMSW in 2022, tonnes per year. |
| `ofmsw_food_green_wood_2022_tpy` | Food plus green plus wood organic waste in 2022, tonnes per year. |
| `landfill_dump_uncollected_frac` | Combined fraction assigned to landfill, dumping, uncollected and unaccounted pathways in the screen. |
| `known_diversion_or_treatment_frac` | Combined fraction assigned to known treatment/diversion pathways. |
| `ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy` | Food plus green OFMSW associated with landfill, dumping, uncollected and unaccounted flows, tonnes per year. |
| `gdp_current_usd_2022` | GDP in current US dollars, 2022. |
| `gdp_per_capita_current_usd_2022` | GDP per capita in current US dollars, 2022. |
| `urban_population_pct_2022` | Urban population share in 2022, percent. |
| `electricity_carbon_intensity_2022_gco2_kwh` | Electricity carbon intensity in 2022, gCO2/kWh. |
| `ofmsw_food_green_2022_kg_per_cap_day` | Food plus green OFMSW generation in kg per capita per day. |
| `unmanaged_ofmsw_food_green_2022_kg_per_cap_day` | Landfill/dump/uncollected/unaccounted food plus green OFMSW in kg per capita per day. |

## `data/processed/country_ofmsw_first_pass_methane.csv`

First-pass methane screening output.

| Column | Meaning |
|---|---|
| `ofmsw_food_green_2022_tpy` | Food plus green OFMSW in 2022, tonnes per year. |
| `ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy` | Eligible disposal-associated OFMSW flow, tonnes per year. |
| `doc_food_green_weighted` | Weighted degradable organic carbon value for food plus green OFMSW. |
| `first_pass_ch4_*_tpy` | First-pass methane estimate by disposal pathway, tonnes CH4 per year. |
| `first_pass_ch4_total_tpy` | Total first-pass methane generation estimate, tonnes CH4 per year. |
| `first_pass_co2e_gwp100_tpy` | First-pass methane burden using GWP100, tonnes CO2e per year. |
| `first_pass_co2e_gwp20_tpy` | First-pass methane burden using GWP20, tonnes CO2e per year, if present. |
| `first_pass_ch4_kg_per_cap_year` | First-pass methane burden per capita, kg CH4 per person per year. |

## `data/processed/country_ofmsw_four_pathway_comparison.csv`

Deterministic four-pathway screening results.

| Column | Meaning |
|---|---|
| `ofmsw_food_green_2022_tpy` | Food plus green OFMSW in 2022, tonnes per year. |
| `ofmsw_food_green_2022_to_landfill_dump_uncollected_tpy` | Eligible disposal-associated OFMSW flow, tonnes per year. |
| `electricity_carbon_intensity_2022_gco2_kwh` | Electricity carbon intensity used for AD-electricity and bio-CNG electricity burdens. |
| `ad_screen_net_gwp100_benefit_tco2e` | Net GWP100 benefit of AD-electricity pathway, tonnes CO2e per year. |
| `bio_cng_screen_net_gwp100_benefit_tco2e` | Net GWP100 benefit of AD-bio-CNG pathway, tonnes CO2e per year. |
| `compost_screen_net_gwp100_benefit_tco2e` | Net GWP100 benefit of composting pathway, tonnes CO2e per year. |
| `prevention_screen_net_gwp100_benefit_tco2e` | Net GWP100 benefit of prevention pathway, tonnes CO2e per year. |
| `best_four_pathway_screen` | Deterministic pathway with the largest net benefit. |
| `best_four_pathway_benefit_tco2e` | Net benefit of the deterministic best pathway, tonnes CO2e per year. |

## `data/processed/country_ofmsw_readiness_index.csv`

Readiness and opportunity classification.

| Column | Meaning |
|---|---|
| `best_four_pathway_screen` | Deterministic best pathway from the four-pathway screen. |
| `best_four_pathway_benefit_tco2e` | Net benefit of deterministic best pathway, tonnes CO2e per year. |
| `mitigation_potential_score` | Normalized mitigation potential score. |
| `best_pathway_readiness_score` | Readiness score associated with the deterministic best pathway. |
| `opportunity_readiness_class` | Final class: immediate priority, strategic build-out, no-regret/complementary, longer-term/local fit, or missing/insufficient data. |
| `readiness_general_score` | General implementation-readiness score. |
| `readiness_prevention_score` | Readiness score for prevention. |
| `readiness_composting_score` | Readiness score for composting. |
| `readiness_ad_electricity_score` | Readiness score for AD-electricity. |
| `readiness_bio_cng_score` | Readiness score for AD-bio-CNG. |
| `readiness_collection_score` | Collection-coverage component of readiness. |
| `readiness_income_score` | Income-group component of readiness. |
| `readiness_gdp_score` | GDP-per-capita component of readiness. |
| `readiness_urban_score` | Urbanization component of readiness. |
| `readiness_existing_biological_score` | Existing biological treatment proxy. |
| `readiness_existing_recovery_score` | Existing recovery/infrastructure proxy. |
| `readiness_data_completeness_score` | Data-completeness component of readiness. |

## `data/processed/country_ofmsw_four_pathway_sensitivity.csv`

Country-level Monte Carlo pathway-winner output.

| Column | Meaning |
|---|---|
| `win_probability_AD-electricity` | Share of Monte Carlo iterations in which AD-electricity has the highest net benefit. |
| `win_probability_AD-bio-CNG` | Share of Monte Carlo iterations in which AD-bio-CNG has the highest net benefit. |
| `win_probability_Composting` | Share of Monte Carlo iterations in which composting has the highest net benefit. |
| `win_probability_Prevention` | Share of Monte Carlo iterations in which prevention has the highest net benefit. |
| `robust_winning_pathway` | Pathway classified as robust winner, or no robust winner/missing. |
| `max_win_probability` | Highest pathway win probability across all pathways. |

## `data/processed/ecoinvent_screening_factors.csv`

Derived ecoinvent and screening parameters used in pathway models. This file reports derived factors only and should not include proprietary exchange-level inventory tables.

| Column | Meaning |
|---|---|
| `pathway` | Pathway or parameter family. |
| `factor_name` | Name of parameter. |
| `ecoinvent_version` | ecoinvent version or `screening` for non-ecoinvent assumptions. |
| `system_model` | ecoinvent system model, where relevant. |
| `process_name` | Selected process name, where relevant. |
| `reference_product` | ecoinvent reference product, where relevant. |
| `geography` | ecoinvent geography or global assumption scope. |
| `unit` | Functional basis for the factor. |
| `value` | Numeric factor value. |
| `value_unit` | Unit of the numeric value. |
| `impact_method` | Impact method or source type. |
| `notes` | Calculation notes and caveats. |

## Key Output Summary Tables

| File | Meaning |
|---|---|
| `outputs/summary_four_pathway_global_metrics.csv` | Global total OFMSW, methane burden and pathway benefits. |
| `outputs/summary_four_pathway_by_region.csv` | Regional totals and pathway benefits. |
| `outputs/summary_four_pathway_by_income.csv` | Income-group totals and pathway benefits. |
| `outputs/summary_four_pathway_best_counts.csv` | Deterministic best-pathway country counts. |
| `outputs/sensitivity_global_pathway_summary.csv` | Monte Carlo global pathway intervals. |
| `outputs/sensitivity_robust_winner_counts.csv` | Robust winner country counts. |
| `outputs/summary_readiness_opportunity_classes.csv` | Readiness class counts. |
| `outputs/top40_four_pathway_screening.csv` | Top country opportunities by deterministic best-pathway benefit. |
| `outputs/top40_readiness_adjusted_opportunities.csv` | Top country opportunities with readiness scores and classes. |
