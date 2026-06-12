# City-Level OFMSW Screen Results

Date: 2026-05-23

## Purpose

This screen uses the What a Waste 3.0 city dataset as a supplementary validation/extension layer. It does not replace the country-level model. Its purpose is to show whether the country-level climate-readiness framing has an urban infrastructure basis and to preserve a possible Nature Cities pivot.

## Output Files

- `data/processed/city_ofmsw_screen.csv`
- `outputs/summary_city_ofmsw_screen.csv`
- `outputs/top40_city_unmanaged_ofmsw.csv`
- `outputs/city_ofmsw_by_country_summary.csv`

## Data Coverage

| Metric | Value |
|---|---:|
| Cities total | 262 |
| Cities with MSW generation | 244 |
| Cities with food or green fraction | 201 |
| Cities with treatment shares | 195 |
| Food plus green OFMSW | 93.9 Mt/y |
| Food plus green OFMSW to landfill/dump/uncollected/unaccounted | 58.3 Mt/y |
| Cities with AD asset data | 8 |
| Cities with compost asset data | 62 |

## Leading City Hotspots

The largest city-level unmanaged/disposal OFMSW hotspots in the first screen include Istanbul, Karachi, Bangkok, Riyadh, Sao Paulo, Dhaka, Kinshasa, Cairo, Moscow, Bogota, Lahore, Rio de Janeiro, Lagos, Ho Chi Minh City, Mexico City, Manila, Dubai, Tehran and Kano.

## Important Data Handling Note

The city workbook labels many composition and treatment fields as percent, but values are stored as fractions from 0 to 1. The script `scripts/build_city_ofmsw_screen.py` uses adaptive conversion: fields are divided by 100 only if observed values exceed 1.

## Interpretation

The city dataset confirms that the country-level model hides substantial urban heterogeneity. The sampled cities alone represent 93.9 Mt/y of food plus green OFMSW and 58.3 Mt/y routed to landfill, dump, uncollected or unaccounted flows. However, city-level treatment and infrastructure fields are sparse: only 8 cities have AD asset data, while 62 have compost asset data. This supports the manuscript's readiness framing and suggests that city-level infrastructure data can help distinguish near-term deployment opportunities from strategic build-out contexts.

## Manuscript Use

Use as supplementary evidence:

- The country-level framework is relevant to urban infrastructure planning.
- City data support the need for readiness indicators, not only national waste quantities.
- Composting appears more widely represented in city asset data than AD, which may matter for deployability.

## Caveats

- City sample is not globally exhaustive.
- City data years vary.
- Many city fields are missing.
- Treatment shares and asset fields require careful validation before pathway modelling.
- The current city screen estimates OFMSW quantities and existing infrastructure signals only; it does not run full pathway benefits.
