# Nature Sustainability Manuscript Skeleton

## Working Title

Reconciling the waste hierarchy with climate-readiness priorities for global organic municipal waste

## Alternative Titles

1. Climate-readiness priorities for global organic municipal waste transitions
2. The waste hierarchy is necessary but insufficient for prioritizing organic waste climate action
3. Spatial priorities for organic municipal waste mitigation depend on hierarchy, methane and readiness

## One-Sentence Contribution

This study shows that prevention remains the most robust principle for organic municipal waste mitigation, but country-level climate investment priorities shift when waste hierarchy, methane baselines, energy substitution, uncertainty and system readiness are evaluated together.

## Nature Sustainability Fit

Nature Sustainability is the primary target because the paper is not only a waste-treatment comparison. Its intended contribution is an integrated sustainability decision framework connecting climate mitigation, circular economy, food-waste prevention, energy substitution, infrastructure readiness, uneven development, and policy prioritization. The manuscript should therefore avoid sounding like a technology-ranking paper. The main story should be that countries need a way to operationalize the waste hierarchy under real-world constraints, especially where prevention, methane avoidance, biological treatment, bioenergy use, collection systems and institutional readiness do not move at the same speed.

The Nature Sustainability version should foreground three questions:

1. How large is the country-level climate burden of food and green organic municipal waste?
2. Where does the waste hierarchy align or conflict with marginal climate opportunity under current national conditions?
3. Which countries represent immediate priorities, strategic build-out cases, complementary no-regret action, or longer-term/local-fit contexts?

## Abstract Draft

Food and green organic municipal waste is a major source of avoidable methane, yet national mitigation planning often relies on generic waste-hierarchy principles or technology-specific case studies. Here we combine World Bank What a Waste 3.0, World Development Indicators, Ember electricity carbon intensity, ecoinvent-derived process parameters and Natural Earth boundaries to screen climate-readiness priorities for organic municipal waste across 217 countries and economies. We compare prevention, composting, anaerobic digestion with electricity recovery, and anaerobic digestion with biomethane/bio-CNG production, and evaluate pathway rankings under uncertainty and system-readiness constraints. We estimate 1.064 billion tonnes per year of food and green organic municipal waste in 2022, of which 516 million tonnes were landfilled, dumped, uncollected or unaccounted in countries with treatment data, corresponding to 514 Mt CO2e per year of first-pass methane burden. In the deterministic screen, AD-bio-CNG provides the largest global GWP100 benefit, followed by prevention, AD-electricity and composting. However, Monte Carlo analysis shows prevention is the most robust country-level winner, while AD-bio-CNG is high-potential but more sensitive to assumptions about biogas yield, methane recovery, upgrading electricity and displaced transport fuel. A readiness layer separates countries into immediate priorities, strategic build-out cases, complementary no-regret opportunities and longer-term local-fit contexts. These results do not overturn the waste hierarchy; they show that hierarchy alone is insufficient for country-level climate investment. Spatial prioritization must jointly consider prevention, methane avoidance, energy substitution and implementation readiness.

## Main Claims To Defend

1. Global food and green OFMSW is large enough to matter for near-term methane mitigation.
2. The waste hierarchy remains directionally correct, but pathway ranking changes when country-level baselines and substitutions are considered.
3. Prevention is the most robust pathway across uncertainty, but not the deterministic winner everywhere.
4. AD-bio-CNG can dominate deterministic climate benefits where methane avoidance and transport-fuel substitution are strong.
5. Readiness changes interpretation: high-potential countries split into immediate priorities and strategic build-out cases.
6. Composting remains climate-positive but is undervalued by a GWP100-only screen because nutrient, soil, cost, deployability and non-climate benefits are not fully represented.

## Editorial Guardrails

- Do not frame the paper as "AD versus prevention". That sounds like a false hierarchy fight.
- Do frame the paper as "how to operationalize the hierarchy when climate opportunity and readiness differ by country".
- Keep ecoinvent details in Methods/Supplementary except where they affect uncertainty.
- Keep bio-CNG in the main text because it changes the policy interpretation, but do not overclaim deployment feasibility.
- Acknowledge that prevention has the strongest normative status and broadest robust signal.
- Treat composting respectfully as a low-complexity, often-ready pathway whose full value is not captured by climate-only accounting.
- Use "screening framework" consistently; avoid implying a final national GHG inventory.

## Figure Plan

### Figure 1. Global OFMSW Burden

Panels:

- World map of food and green OFMSW generation.
- World map of first-pass methane burden from unmanaged/disposal OFMSW.
- Regional stacked or grouped bars for OFMSW and first-pass methane burden.

Existing outputs:

- `manuscript/figures/map_ofmsw_generation.png`
- `manuscript/figures/map_first_pass_methane.png`
- `outputs/summary_four_pathway_by_region.csv`

### Figure 2. Deterministic Four-Pathway Screening

Panels:

- Global pathway net benefits.
- Best deterministic pathway map.
- Top 20 country hotspots colored by best pathway.

Existing outputs:

- `outputs/summary_four_pathway_global_metrics.csv`
- `outputs/top40_four_pathway_screening.csv`
- `manuscript/figures/map_best_pathway.png`

### Figure 3. Uncertainty and Robustness

Panels:

- Global uncertainty intervals for four pathways.
- Robust winning pathway map.
- Country-level win-probability categories.

Existing outputs:

- `outputs/sensitivity_global_pathway_summary.csv`
- `outputs/sensitivity_robust_winner_counts.csv`
- `manuscript/figures/map_robust_winning_pathway.png`

### Figure 4. Mitigation-Readiness Typology

Panels:

- Readiness typology map.
- Matrix of mitigation potential vs readiness.
- Top immediate-priority and strategic-build-out countries.

Existing outputs:

- `manuscript/figures/map_readiness_typology.png`
- `outputs/top40_readiness_adjusted_opportunities.csv`
- `outputs/summary_readiness_opportunity_classes.csv`

### Extended Data Figures

- AD minus prevention map.
- Regional pathway comparison.
- Best-pathway counts.
- Sensitivity assumptions and parameter ranges.
- Missing-data map or table.

Existing outputs:

- `manuscript/figures/map_ad_minus_prevention.png`
- `manuscript/figures/fig_region_pathway_totals.png`
- `manuscript/figures/fig_best_pathway_counts.png`
- `outputs/natural_earth_unmatched_iso3.csv`

## Results Outline

### 1. Organic municipal waste is a large methane-relevant flow

Report:

- 217 countries/economies.
- 1.064 billion t/y food + green OFMSW.
- 516 million t/y unmanaged/disposal OFMSW where treatment data exist.
- 18.9 Mt CH4/y and 514 Mt CO2e/y first-pass GWP100 burden.

### 2. Four pathways produce different global and spatial priorities

Report deterministic global values:

- AD-bio-CNG: 248.9 Mt CO2e/y.
- Prevention: 232.8 Mt CO2e/y.
- AD-electricity: 229.6 Mt CO2e/y.
- Composting: 193.5 Mt CO2e/y.

Report deterministic country counts:

- Prevention: 98.
- AD-bio-CNG: 50.
- AD-electricity: 4.
- Missing: 65.

Interpretation:

- Bio-CNG matters because it shifts AD from electricity-only substitution to transport-fuel substitution.
- Prevention remains central but is not the only high-impact climate pathway under existing waste baselines.

### 3. Robustness analysis protects against overclaiming

Report Monte Carlo global summaries:

- Prevention median: 244.4 Mt CO2e/y; 5-95% range: 131.2-392.6.
- AD-bio-CNG median: 242.3 Mt CO2e/y; 5-95% range: 223.9-265.6.
- AD-electricity median: 230.4 Mt CO2e/y; 5-95% range: 218.7-245.6.
- Composting median: 190.7 Mt CO2e/y; 5-95% range: 182.4-197.0.

Report robust country winners:

- Prevention: 107.
- AD-bio-CNG: 31.
- AD-electricity: 5.
- No robust winner: 9.
- Missing: 65.

Interpretation:

- Prevention is more uncertain globally because avoided upstream food emissions and prevention rate vary widely.
- Despite this, prevention is the most robust country-level winner.
- AD-bio-CNG is high potential but parameter-sensitive.

### 4. Readiness separates immediate action from strategic build-out

Report readiness classes:

- Immediate priority: 43.
- Strategic build-out: 27.
- No-regret/complementary: 64.
- Longer-term/local fit: 18.
- Missing/insufficient data: 65.

Interpretation:

- High mitigation potential alone is insufficient.
- Countries such as the United States, China, Mexico, Brazil, Australia, and Spain appear as immediate or near-immediate AD-bio-CNG/AD opportunities depending on readiness indicators.
- Countries such as India and the Philippines remain prevention-led but may require strategic build-out for implementation.

### 5. Reinterpreting the waste hierarchy

Main point:

- The hierarchy is not wrong.
- But policy cannot allocate climate finance from hierarchy alone.
- Prevention should remain the first principle, while biological treatment and bio-CNG are needed for unavoidable or already-generated OFMSW, especially where methane baselines are high.

## Methods Outline

### Data

- What a Waste 3.0: waste generation, composition, treatment shares, projections.
- WDI: GDP, GDP per capita, population, urbanization.
- Ember: electricity carbon intensity.
- ecoinvent 3.12 cutoff documentation: AD/compost process emissions and nutrient contents.
- ecoinvent 3.1 cutoff proxy: biogas yield where 3.12 exchange-level access was unavailable.
- Natural Earth Admin 0, 1:50m: country boundaries.

### OFMSW Definition

Primary definition:

- Food + green waste.

Sensitivity candidate:

- Food + green + wood.

### Baseline Methane

- IPCC-style first-pass methane model.
- Food DOC: 0.15.
- Green DOC: 0.20.
- DOCf: 0.5.
- F methane: 0.5.
- AR6 methane GWP100: 27.2.
- Treatment MCF values for open dump, controlled landfill, sanitary landfill, unspecified landfill, uncollected, and unaccounted flows.

### Pathway Scenarios

Prevention:

- Prevent 20% of unmanaged food waste in deterministic screen.
- Avoid upstream food production emissions.

Composting:

- Divert 40% of currently unmanaged food + green OFMSW.
- Apply ecoinvent-derived process emissions.
- Nutrient/soil-carbon credits currently reserved for sensitivity/extension.

AD-electricity:

- Divert 40% of currently unmanaged food + green OFMSW.
- Use ecoinvent-derived AD process emissions.
- Use ecoinvent 3.1 proxy biogas yield converted to electricity.
- Apply country-specific grid carbon intensity.

AD-bio-CNG:

- Divert 40% of currently unmanaged food + green OFMSW.
- Use ecoinvent 3.1 proxy biogas yield and methane share.
- Apply methane recovery, upgrading/compression electricity, and diesel substitution assumptions.
- Apply country-specific grid carbon intensity for upgrading/compression burden.

### Readiness Index

General indicators:

- Collection coverage.
- Income class.
- GDP per capita.
- Urbanization.
- Data completeness.

Pathway-specific indicators:

- Existing biological treatment for composting and AD.
- Existing recovery/infrastructure proxy for AD and bio-CNG.
- Urbanization and GDP per capita for bio-CNG readiness.

Decision classes:

- Immediate priority.
- Strategic build-out.
- No-regret/complementary.
- Longer-term/local fit.

### Sensitivity Analysis

Monte Carlo parameters:

- AD process emissions.
- Composting process emissions.
- Biogas yield.
- Methane share.
- Electricity conversion efficiency.
- Methane recovery.
- Upgrading/compression electricity.
- Diesel substitution factor.
- Prevention rate.
- Avoided upstream food emission factor.

Outputs:

- Global pathway uncertainty intervals.
- Country-level robust winning pathway.
- No-robust-winner countries.

## Key Limitations To State Clearly

- The model is a screening framework, not a final national GHG inventory.
- What a Waste treatment shares have missingness and reporting heterogeneity.
- ecoinvent 3.12 exchange-level access was unavailable; biogas yield uses ecoinvent 3.1 as a transparent proxy.
- Bio-CNG results depend on assumed displaced fuel, upgrading energy, methane recovery, and infrastructure readiness.
- Nutrient, soil-carbon, public-health, cost, and behavioral dimensions are not fully represented.
- Prevention potential is difficult to observe directly and has wide uncertainty.

## Target Journal Logic

Primary target:

- Nature Sustainability: integrated sustainability decision framework for waste, climate, circular economy, infrastructure readiness and policy prioritization.

Backup target:

- Resources, Conservation & Recycling: technical systems paper on resource recovery, LCA-informed pathway comparison and circular-economy transition.

Conditional alternatives:

- Nature Food: viable if the manuscript is reframed around food-waste prevention and food-system circularity.
- Nature Cities: viable if a city-scale layer is added from the What a Waste city dataset.
- Renewable and Sustainable Energy Reviews: viable only after pivoting toward bioenergy and adding a substantial review component.
