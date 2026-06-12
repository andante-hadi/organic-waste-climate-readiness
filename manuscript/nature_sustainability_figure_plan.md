# Nature Sustainability Figure Architecture

This file defines the target publication figure set. The current standalone figures are analysis outputs; the final submission should combine them into polished multi-panel figures with consistent typography, colors, panel labels and map disclaimers.

## Main Figure Set

### Figure 1. Global organic municipal waste burden

Main claim: food and green organic municipal waste is large enough to matter for near-term climate mitigation, and its unmanaged/disposal burden is spatially uneven.

Final panels:

- **a.** Food and green organic municipal waste generation in 2022.
- **b.** First-pass methane burden from landfill, dumping, uncollected and unaccounted flows.
- **c.** Regional totals for food and green OFMSW, unmanaged/disposal OFMSW and first-pass methane burden.

Layout:

- Two world maps across the top row, side by side.
- One full-width regional bar chart below.
- Main visual message: global burden is large, but spatially concentrated and uneven.

Existing inputs:

- `manuscript/figures/map_ofmsw_generation.png`
- `manuscript/figures/map_first_pass_methane.png`
- `outputs/summary_four_pathway_by_region.csv`

Final caption direction:

**Fig. 1 | Country-level burden of food and green organic municipal waste.** Food and green organic municipal waste generation and first-pass methane burden were estimated for 217 countries and economies using What a Waste 3.0 and IPCC-style screening factors. The screen estimates 1.064 billion tonnes per year of food and green organic municipal waste in 2022, of which 516 million tonnes were landfilled, dumped, uncollected or unaccounted in countries with treatment data, corresponding to 18.9 Mt CH4 yr-1 or 514 Mt CO2e yr-1. Values are intended for prioritization, not as final national inventories.

### Figure 2. Four-pathway climate screening

Main claim: no single pathway is universally dominant; deterministic climate benefits differ between global totals and country-level pathway winners.

Final panels:

- **a.** Global net GWP100 benefit by pathway.
- **b.** Country-level deterministic best pathway map.
- **c.** Deterministic best-pathway country counts.
- **d.** Top 20 country hotspots by best-pathway benefit.

Layout:

- Panel a: compact horizontal bars, four pathways.
- Panel b: world map, largest panel.
- Panel c: small count chart placed beside panel a or below map.
- Panel d: ranked country bars, full-width bottom or right column.
- Main visual message: global totals and country winners tell different stories.

Existing inputs:

- `manuscript/figures/fig_global_pathway_totals.png`
- `manuscript/figures/map_best_pathway.png`
- `manuscript/figures/fig_best_pathway_counts.png`
- `manuscript/figures/fig_top20_country_hotspots.png`
- `outputs/summary_four_pathway_global_metrics.csv`
- `outputs/summary_four_pathway_best_counts.csv`
- `outputs/top40_four_pathway_screening.csv`

Final caption direction:

**Fig. 2 | Deterministic climate benefits of prevention, composting, AD-electricity and AD-bio-CNG.** The central parameterization estimates net GWP100 benefits of 232.8 Mt CO2e yr-1 for prevention, 219.5 Mt CO2e yr-1 for AD-bio-CNG, 209.1 Mt CO2e yr-1 for AD-electricity and 198.6 Mt CO2e yr-1 for composting. At the country level, prevention is the leading deterministic pathway in 121 countries/economies, AD-bio-CNG in 28 and AD-electricity in 3; 65 countries/economies have missing or insufficient pathway data. The global ranking should not be interpreted as a universal technology ranking because pathway benefits depend on methane baselines, energy substitution and implementation context.

### Figure 3. Uncertainty and robust pathway winners

Main claim: uncertainty strengthens the hierarchy-readiness interpretation: prevention is the most robust country-level winner, while AD-bio-CNG remains the largest recovery pathway.

Final panels:

- **a.** Global Monte Carlo intervals by pathway.
- **b.** Robust winning pathway map.
- **c.** Robust winner country counts.
- **d.** Max win-probability distribution or uncertainty-margin inset.

Layout:

- Panel a: interval plot with median and 5-95% range.
- Panel b: world map of robust winners, largest panel.
- Panel c: compact count chart.
- Panel d: uncertainty-confidence histogram or small chart of no-robust-winner cases.
- Main visual message: prevention is robust; bio-CNG is high-potential but more assumption-sensitive.

Existing inputs:

- `manuscript/figures/fig_uncertainty_intervals.png`
- `manuscript/figures/map_robust_winning_pathway.png`
- `manuscript/figures/fig_robust_winner_counts.png`
- `outputs/sensitivity_global_pathway_summary.csv`
- `outputs/sensitivity_robust_winner_counts.csv`
- `data/processed/country_ofmsw_four_pathway_sensitivity.csv`

Needed update:

- Build panel d from `data/processed/country_ofmsw_four_pathway_sensitivity.csv`, or omit if space is tight.

Final caption direction:

**Fig. 3 | Pathway uncertainty and robust country-level winners.** Monte Carlo analysis propagates uncertainty in prevention rates, avoided upstream food emissions, process emissions, biogas yield, methane share, electricity conversion, methane recovery, upgrading electricity and displaced transport fuel. Median global net benefits are 244.4 Mt CO2e yr-1 for prevention, 216.8 Mt CO2e yr-1 for AD-bio-CNG, 210.0 Mt CO2e yr-1 for AD-electricity and 195.9 Mt CO2e yr-1 for composting. Prevention is the robust winner in 125 countries/economies, AD-bio-CNG in 20 and AD-electricity in 5; two countries/economies have no robust winner and 65 have missing or insufficient data.

### Figure 4. Climate-readiness typology

Main claim: mitigation potential is not the same as deployability; the framework separates immediate action from strategic build-out.

Final panels:

- **a.** Readiness typology map.
- **b.** Mitigation potential versus readiness matrix.
- **c.** Top immediate-priority and strategic-build-out countries.
- **d.** City-layer alignment inset showing city unmanaged/disposal OFMSW by country readiness class.

Layout:

- Panel a: world map across the top or left.
- Panel b: scatter/matrix with quadrant labels and threshold lines.
- Panel c: ranked country opportunities split by immediate priority and strategic build-out.
- Panel d: compact city-layer validation bar chart.
- Main visual message: high mitigation potential does not automatically mean near-term deployability.

Existing inputs:

- `manuscript/figures/map_readiness_typology.png`
- `manuscript/figures/fig_readiness_scatter.png`
- `outputs/summary_readiness_opportunity_classes.csv`
- `outputs/top40_readiness_adjusted_opportunities.csv`
- `outputs/summary_city_by_country_readiness_class.csv`

Needed update:

- Build panel c from `outputs/top40_readiness_adjusted_opportunities.csv`.
- Build panel d from `outputs/summary_city_by_country_readiness_class.csv`.

Final caption direction:

**Fig. 4 | Climate-readiness typology for organic municipal waste transitions.** Countries/economies are classified by mitigation potential and implementation readiness into immediate priority, strategic build-out, no-regret/complementary, longer-term/local fit, or missing/insufficient data classes. The first readiness screen identifies 46 immediate-priority countries/economies, 24 strategic build-out cases, 68 no-regret/complementary contexts, 14 longer-term/local-fit contexts and 65 missing or insufficiently characterized cases. The typology separates where climate action may be deployable now from where large mitigation potential requires institutional and infrastructure build-out.

## Extended Data Figures

### Extended Data Fig. 1. Biological-treatment advantage over prevention

Existing input:

- `manuscript/figures/map_ad_minus_prevention.png`

Purpose:

- Show where biological treatment can exceed prevention in the deterministic climate-only screen.

### Extended Data Fig. 2. Regional pathway totals and income-group results

Existing inputs:

- `manuscript/figures/fig_region_pathway_totals.png`
- `outputs/summary_four_pathway_by_income.csv`

Purpose:

- Support regional and development-status heterogeneity without overloading the main figures.

### Extended Data Fig. 3. Sensitivity stress tests

Existing inputs:

- `outputs/summary_bio_cng_stress_test.csv`
- `outputs/summary_bio_cng_stress_best_counts.csv`
- `outputs/summary_landfill_capture_sensitivity.csv`
- `outputs/summary_landfill_capture_best_counts.csv`
- `outputs/summary_nutrient_credit_sensitivity.csv`

Purpose:

- Show that the manuscript's interpretation does not depend on a single bio-CNG, landfill capture or nutrient-credit assumption.

### Extended Data Fig. 4. Missing data and spatial join diagnostics

Existing inputs:

- `outputs/natural_earth_join_report.csv`
- `outputs/natural_earth_unmatched_iso3.csv`

Purpose:

- Transparently document mapping coverage and countries/economies that could not be mapped.

### Extended Data Fig. 5. Ecoinvent-derived parameter table

Existing inputs:

- `data/processed/ecoinvent_screening_factors.csv`
- `notes/ecoinvent_extraction_log.md`
- `notes/ecoinvent_3_12_openlca_export_summary.md`

Purpose:

- Keep proprietary-source details out of the main narrative while preserving transparent derived factors and limitations.

## Figure Work Still Needed

1. Generate composite main figures 1-4 from the standalone assets and CSV outputs.
2. Build Fig. 3d uncertainty-confidence panel.
3. Build Fig. 4c top-country readiness panel.
4. Build Fig. 4d city-layer alignment panel.
5. Rebuild all maps/plots with consistent Nature-style colors, typography and labels.
6. Export final figures as high-resolution PNG/PDF and keep editable plotting scripts.
7. Add map disclaimer language for journal submission if needed.

## Visual Standards

- Use one stable pathway palette throughout:
  - Prevention: blue.
  - Composting: green.
  - AD-electricity: amber.
  - AD-bio-CNG: purple or magenta.
  - Missing/insufficient data: light grey.
- Use the same category names in all figures and text.
- Avoid map color scales that imply false precision; use binned legends for burden maps.
- Include units directly in axis labels.
- Put panel labels `a`, `b`, `c`, `d` outside plotting areas where possible.
- Add this map note to figure captions or Methods if required: "Map boundaries delineate study areas and do not necessarily depict accepted national boundaries."
