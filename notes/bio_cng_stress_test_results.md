# Bio-CNG Stress-Test Results

Date: 2026-05-23

## Purpose

This stress test checks how sensitive the AD-bio-CNG pathway is to less favorable assumptions about displaced diesel, upgrading/compression electricity, process emissions and methane slip. This is important because AD-bio-CNG is the largest deterministic GWP100 pathway in the central screen.

## Output Files

- `data/processed/country_ofmsw_bio_cng_stress_test.csv`
- `outputs/summary_bio_cng_stress_test.csv`
- `outputs/summary_bio_cng_stress_best_counts.csv`
- `outputs/top40_bio_cng_high_stress.csv`

## Scenarios

| Scenario | Diesel substitution | Upgrading electricity | Process emissions | Methane slip |
|---|---:|---:|---:|---:|
| Central | 100% | 100% | 100% | 0% of biomethane |
| Moderate stress | 80% | 125% | 110% | 1% of biomethane |
| High stress | 60% | 150% | 125% | 3% of biomethane |

Methane slip is converted to GWP100 using methane density of 0.7168 kg/m3 and GWP100 = 27.2.

## Global Bio-CNG Results

| Scenario | Bio-CNG net benefit |
|---|---:|
| Central | 248.9 Mt CO2e/y |
| Moderate stress | 227.7 Mt CO2e/y |
| High stress | 201.1 Mt CO2e/y |

## Best Pathway Counts

| Scenario | AD-bio-CNG | AD-electricity | Prevention | Missing |
|---|---:|---:|---:|---:|
| Central | 50 | 4 | 98 | 66 |
| Moderate stress | 23 | 19 | 110 | 66 |
| High stress | 6 | 31 | 115 | 66 |

## Interpretation

Bio-CNG remains globally beneficial under stress assumptions, but its country-level dominance is sensitive. Under moderate stress, AD-bio-CNG remains the best deterministic pathway in 23 countries/economies, down from 50 in the central screen. Under high stress, it remains best in only 6 countries/economies, while prevention becomes the leading pathway in 115 countries/economies and AD-electricity in 31.

This supports careful wording in the manuscript: AD-bio-CNG is a high-potential pathway where methane avoidance, fuel substitution and infrastructure readiness align, but it should not be presented as broadly robust without local validation of methane recovery, upgrading energy, vehicle/fuel offtake and methane slip.

## Manuscript Use

Use in Supplementary Information and Discussion as evidence that:

- bio-CNG can be important but is assumption-sensitive;
- prevention remains the more robust first-principle pathway;
- readiness and local infrastructure constraints are central to responsible pathway sequencing.
