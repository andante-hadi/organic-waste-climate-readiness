# Landfill Gas Capture And Oxidation Sensitivity Results

Date: 2026-05-23

## Purpose

This sensitivity tests whether the pathway results depend on assuming no landfill gas capture or oxidation in the central first-pass methane screen. It adjusts methane available for avoidance by disposal category and recalculates GWP100 pathway benefits.

## Output Files

- `data/processed/country_ofmsw_landfill_capture_sensitivity.csv`
- `outputs/summary_landfill_capture_sensitivity.csv`
- `outputs/summary_landfill_capture_best_counts.csv`

## Scenarios

| Scenario | Open dump capture | Controlled landfill capture | Sanitary landfill capture | Unspecified landfill capture | Oxidation for landfill categories |
|---|---:|---:|---:|---:|---:|
| Low capture | 0% | 10% | 25% | 5% | 5% |
| Moderate capture | 0% | 25% | 50% | 15% | 10% |
| High capture | 0% | 50% | 75% | 30% | 10% |

Uncollected and unaccounted flows are assigned no capture in all scenarios.

## Global Results

| Scenario | First-pass CH4 | AD-electricity | AD-bio-CNG | Composting | Prevention |
|---|---:|---:|---:|---:|---:|
| Low capture | 15.6 Mt CH4/y | 193.9 | 213.3 | 157.8 | 217.3 |
| Moderate capture | 12.4 Mt CH4/y | 158.5 | 177.9 | 122.4 | 201.9 |
| High capture | 9.4 Mt CH4/y | 125.8 | 145.2 | 89.7 | 187.6 |

Pathway values are Mt CO2e/y.

## Best Pathway Counts

| Scenario | Prevention | AD-bio-CNG | AD-electricity | Missing |
|---|---:|---:|---:|---:|
| Low capture | 116 | 33 | 3 | 66 |
| Moderate capture | 128 | 22 | 2 | 66 |
| High capture | 135 | 15 | 2 | 66 |

## Interpretation

Landfill gas capture and oxidation reduce the avoided-methane benefit of all diversion pathways. Prevention becomes more dominant as capture assumptions become stronger because a larger share of its benefit comes from avoided upstream food-system emissions rather than only avoided disposal methane.

AD-bio-CNG remains the best pathway in 15 countries/economies even under the high-capture scenario, but its country-level dominance declines from 50 countries/economies in the central screen to 33, 22 and 15 under low, moderate and high capture assumptions, respectively. This supports the manuscript's readiness framing: biological treatment and bio-CNG are important where unmanaged methane risk remains high or capture is weak, while prevention remains the more robust hierarchy-first strategy where managed landfill methane is already partly controlled.

## Caveats

- Capture rates are scenario assumptions, not country-reported facility-level values.
- Oxidation is applied only to landfill categories, not open dumping, uncollected or unaccounted flows.
- The sensitivity does not model time-distributed first-order decay.
- Country-specific landfill gas collection, flaring and energy recovery data would improve this analysis.
