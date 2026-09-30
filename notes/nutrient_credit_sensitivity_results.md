# Nutrient-Credit Sensitivity Results

Date: 2026-06-12

## Purpose

This sensitivity tests whether excluding compost and digestate nutrient substitution materially undervalues composting or anaerobic digestion in the central GWP100 screen.

## Output Files

- `data/processed/country_ofmsw_four_pathway_comparison_nutrient_sensitivity.csv`
- `outputs/summary_nutrient_credit_sensitivity.csv`
- `outputs/summary_best_counts_nutrient_sensitivity.csv`

## Conservative Screening Assumptions

Fertilizer displacement factors:

- Nitrogen: 5.0 kg CO2e/kg N.
- Phosphate: 1.0 kg CO2e/kg phosphate.
- Potassium: 0.5 kg CO2e/kg K.

Agronomic availability/substitution fractions:

- Compost N: 20%.
- Compost phosphate: 50%.
- Compost K: 80%.
- Digestate N: 50%.
- Digestate phosphate: 60%.
- Digestate K: 80%.

Nutrient contents:

- Compost: 3.59 kg N/t OFMSW, 1.67 kg phosphate/t OFMSW, 3.16 kg K/t OFMSW.
- Digestate: 11.4 kg N/t OFMSW, 2.3 kg phosphate/t OFMSW, 7.9 kg K/t OFMSW.

## Global Results

| Pathway | Central | Nutrient credit | With nutrients |
|---|---:|---:|---:|
| AD-electricity | 209.1 | 6.8 | 215.9 |
| AD-bio-CNG | 219.5 | 6.8 | 226.3 |
| Composting | 198.6 | 1.2 | 199.8 |
| Prevention | 232.8 | 0.0 | 232.8 |

Unit: Mt CO2e/y.

## Best Pathway Counts With Nutrient Credits

| Best pathway | Countries/economies |
|---|---:|
| Prevention | 114 |
| AD-bio-CNG | 34 |
| AD-electricity | 3 |
| Composting | 1 |
| Missing/insufficient data | 66 |

## Interpretation

Under conservative assumptions, nutrient credits modestly increase the climate benefit of AD and composting. The additional credit is larger for AD because the documented digestate nutrient content is higher than the compost nutrient content in the current ecoinvent-derived factors. The sensitivity does not overturn the central GWP100 interpretation: prevention remains the largest deterministic global pathway and the most robust country-level winner, while AD-bio-CNG remains the largest recovery pathway.

## Caveats

- Phosphate is treated in the unit reported by the ecoinvent documentation-derived factor; final fertilizer substitution should harmonize phosphate/P/P2O5 units.
- The sensitivity does not include soil carbon, humus formation, agronomic timing, nutrient losses, local fertilizer type, compost quality, or market displacement limits.
- Results should be presented as supplementary directional evidence, not a definitive nutrient-substitution LCA.
