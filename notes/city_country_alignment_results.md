# City-Country Alignment Results

Date: 2026-05-23

## Purpose

This analysis links the What a Waste 3.0 city-level OFMSW screen to the country-level best pathway, robust pathway and readiness classes. It tests whether the city dataset supports the country-level readiness typology.

## Output Files

- `data/processed/city_country_alignment.csv`
- `outputs/top50_city_country_alignment.csv`
- `outputs/summary_city_by_country_readiness_class.csv`
- `outputs/summary_city_by_country_best_pathway.csv`

## City OFMSW By Country Readiness Class

| Country readiness class | Cities | City OFMSW | City unmanaged/disposal OFMSW | Cities with AD asset data | Cities with compost asset data |
|---|---:|---:|---:|---:|---:|
| Immediate priority | 79 | 41.3 Mt/y | 22.7 Mt/y | 2 | 26 |
| Strategic build-out | 45 | 30.7 Mt/y | 20.2 Mt/y | 3 | 12 |
| Missing/insufficient country data | 49 | 14.1 Mt/y | 12.7 Mt/y | 1 | 5 |
| No-regret/complementary | 70 | 6.2 Mt/y | 1.5 Mt/y | 1 | 18 |
| Longer-term/local fit | 19 | 1.6 Mt/y | 1.3 Mt/y | 1 | 1 |

## City OFMSW By Country Best Pathway

| Country best pathway | Cities | City OFMSW | City unmanaged/disposal OFMSW | Cities with AD asset data | Cities with compost asset data |
|---|---:|---:|---:|---:|---:|
| Prevention | 116 | 40.1 Mt/y | 24.7 Mt/y | 6 | 25 |
| AD-bio-CNG | 91 | 36.2 Mt/y | 17.6 Mt/y | 1 | 30 |
| Missing/insufficient country data | 49 | 14.1 Mt/y | 12.7 Mt/y | 1 | 5 |
| AD-electricity | 6 | 3.5 Mt/y | 3.4 Mt/y | 0 | 2 |

## Interpretation

The city alignment supports the country-level readiness typology. Most sampled city unmanaged/disposal OFMSW lies in countries classified as either immediate priorities or strategic build-out cases. This means the national framework is not only abstract: it points to urban systems where large organic waste flows and infrastructure gaps co-exist.

The city layer also supports a nuanced pathway interpretation. Cities in prevention-led countries account for the largest city unmanaged/disposal OFMSW in the city sample, while cities in AD-bio-CNG-led countries also account for a large share. However, city asset data show compost assets are reported more often than AD assets. This reinforces the paper's claim that pathway priority and implementation readiness are separate dimensions.

## Manuscript Use

Use as supplementary evidence or one sentence in the Discussion:

> A supplementary screen of 262 cities showed that 42.8 Mt/y of sampled city unmanaged/disposal OFMSW lies in countries classified as immediate priorities or strategic build-out cases, reinforcing the urban-infrastructure relevance of the country-level readiness typology.

## Caveats

- City sample is not comprehensive.
- City years vary.
- City asset reporting is sparse and may be inconsistent.
- This is an alignment screen, not city-level pathway modelling.
