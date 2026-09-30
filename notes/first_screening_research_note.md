# First Screening Research Note

## Study Frame

This first screening model combines:

- World Bank What a Waste 3.0 country-level waste generation, composition, collection, treatment, and projections.
- World Bank WDI 2022 GDP, population, and urbanization covariates.
- Ember 2022 electricity carbon intensity.
- IPCC-style screening constants for methane potential.

The current scope is food + green organic municipal solid waste. It excludes paper and wood from the OFMSW definition for now.

## Early Global Results

Estimated global 2022 food + green OFMSW:

- 1.064 billion tonnes/year.

Estimated food + green OFMSW sent to landfill, dump, uncollected, or unaccounted systems where treatment data exist:

- 516 million tonnes/year.

First-pass methane from this unmanaged/disposal fraction:

- 18.9 Mt CH4/year.
- 514.1 Mt CO2e/year using AR6 biogenic methane GWP100.

## Three Pathway Screening

The first comparison uses deliberately simple assumptions:

- AD: divert 40% of currently unmanaged food + green OFMSW to anaerobic digestion.
- Composting: divert 40% of currently unmanaged food + green OFMSW to composting.
- Prevention: prevent 20% of currently unmanaged food waste and include avoided upstream food production emissions.

Global net GWP100 benefits:

| Pathway | Net benefit |
|---|---:|
| Food-waste prevention | 232.8 Mt CO2e/year |
| Anaerobic digestion | 220.0 Mt CO2e/year |
| Composting | 191.2 Mt CO2e/year |

Best pathway counts among countries/economies with enough data:

| Best pathway | Count |
|---|---:|
| Prevention | 118 |
| Anaerobic digestion | 34 |
| Composting | 0 |
| Missing/insufficient data | 66 |

## Leading Hotspots

Largest first-pass methane contributors include:

- China
- United States
- Brazil
- India
- Mexico
- Russian Federation
- Indonesia
- Turkiye
- Saudi Arabia
- Australia

Largest countries where prevention is currently the best screening pathway include:

- India
- Brazil
- Indonesia
- Turkiye
- Iran
- Iraq
- Egypt
- Thailand
- Philippines
- Colombia

Largest countries where AD is currently the best screening pathway include:

- China
- United States
- Mexico
- Russian Federation
- Saudi Arabia
- Australia
- Argentina
- Spain
- Myanmar
- France

## Main Scientific Signal

The first result supports a strong high-impact-journal argument:

There is no single globally optimal OFMSW intervention. Prevention is the largest global opportunity when avoided food production is counted, but AD can outperform prevention in selected countries because of large disposal methane avoidance, high electricity carbon intensity, high unmanaged OFMSW mass, or a combination of these. Composting remains beneficial but does not dominate in this first climate-only screening.

## Important Caveats

- This is not yet a final IPCC first-order decay inventory.
- Treatment-share gaps are preserved as missing, not imputed.
- AD and composting process emissions use generic screening factors.
- Prevention uses a generic upstream avoided food-production factor.
- ecoinvent 3.12 cutoff has not yet been integrated into the calculations.
- Nutrient substitution from compost/digestate is not yet included.
- Costs are not yet included.
- Feasibility and collection/source-separation constraints are still simplified.

## Next Analysis Priorities

1. Replace generic AD and compost process factors with ecoinvent 3.12 cutoff factors.
2. Add digestate/compost nutrient substitution using FAOSTAT fertilizer data.
3. Add cost ranges and build a marginal abatement curve.
4. Add uncertainty ranges and Monte Carlo sensitivity analysis.
5. Impute or scenario-test missing treatment shares for major countries such as Pakistan and Nigeria.
6. Build first manuscript figures: global hotspot map, pathway-best map, and mitigation wedge chart.
