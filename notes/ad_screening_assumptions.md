# Anaerobic Digestion Screening Scenario

This note documents the initial AD scenario in `scripts/screen_ad_pathway.py`.

## Purpose

The scenario estimates the climate benefit of diverting a share of currently unmanaged food + green OFMSW to anaerobic digestion with electricity recovery.

It is a screening scenario. Final values should be replaced or bounded using ecoinvent 3.12 cutoff processes and literature ranges.

## Scenario

The current screening case assumes:

- 50% of currently landfill/dump/uncollected food + green OFMSW is targeted for AD.
- 80% source-separation/capture efficiency.
- Net diverted OFMSW = 40% of currently unmanaged food + green OFMSW.
- Biogas electricity yield = 250 kWh per tonne OFMSW.
- AD process emissions = 50 kg CO2e per tonne OFMSW.
- Avoided landfill methane is proportional to diverted OFMSW.
- Avoided electricity uses country-specific 2022 Ember grid carbon intensity.

## Current Result

- Diverted OFMSW: 206.3 Mt/year.
- Avoided methane: 7.56 Mt CH4/year.
- Net GWP100 benefit: 220.0 Mt CO2e/year.

## Early Interpretation

Most climate benefit comes from avoided landfill/dump methane. Grid electricity credits are still meaningful, especially in countries with carbon-intensive electricity systems.

Among the largest net-benefit countries, grid-credit shares are higher in countries such as India, Indonesia, Iran, Iraq, Egypt, the Philippines, Bangladesh, and Algeria than in countries with cleaner grids such as Brazil, France, Canada, Colombia, or Spain.

## Next Upgrades

- Replace generic AD process emissions with ecoinvent 3.12 cutoff factors.
- Split food waste and green waste because methane yield differs.
- Add digestate nitrogen, phosphorus, and potassium substitution.
- Include leakage, flaring, and methane slip.
- Add capital and operating costs.
- Add feasibility constraints by income group and current collection coverage.
