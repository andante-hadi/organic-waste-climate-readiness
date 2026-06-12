# First-Pass Methane Screening Assumptions

This note documents the screening calculation in `scripts/estimate_first_pass_methane.py`.

## Purpose

The first-pass methane model is a rapid screening layer. It is intended to identify likely hotspot countries and scale of opportunity before building the final IPCC first-order decay model.

It should not yet be described as a final national inventory estimate.

## Formula

For each country and disposal pathway:

`CH4 = W * DOC * DOCf * MCF * F * 16/12`

Where:

- `W`: food + green OFMSW sent to the disposal pathway, tonnes/year.
- `DOC`: weighted degradable organic carbon for food and green waste.
- `DOCf`: fraction of DOC that decomposes.
- `MCF`: methane correction factor for disposal condition.
- `F`: methane fraction in landfill gas.
- `16/12`: molecular weight conversion from carbon to methane.

## Screening Constants

| Parameter | Value | Notes |
|---|---:|---|
| Food waste DOC | 0.15 | IPCC-style default screening value |
| Garden/green waste DOC | 0.20 | IPCC-style default screening value |
| DOCf | 0.50 | Default screening value |
| Methane fraction in landfill gas, F | 0.50 | Common IPCC default |
| Open dump MCF | 0.40 | Screening assumption |
| Controlled landfill MCF | 0.80 | Screening assumption |
| Sanitary landfill MCF | 1.00 | Screening assumption |
| Unspecified landfill MCF | 0.60 | Screening assumption |
| Uncollected MCF | 0.40 | Screening assumption |
| Unaccounted MCF | 0.60 | Screening assumption |
| AR6 biogenic CH4 GWP100 | 27.2 | Used for CO2e conversion |
| AR6 biogenic CH4 GWP20 | 80.8 | Used for near-term CO2e conversion |

## Current Result

Using available What a Waste 3.0 treatment-share data:

- Countries/economies with methane estimates: 152.
- First-pass methane from food + green waste in landfill/dump/uncollected systems: 18.9 Mt CH4/year.
- First-pass GWP100 climate impact: 514.1 Mt CO2e/year.

## Important Caveats

- Missing treatment shares remain missing; they are not treated as zero.
- The calculation estimates annual methane generation potential from current annual waste flows, not time-distributed first-order decay emissions.
- The final model should use IPCC first-order decay with climate-specific decay rates.
- Landfill gas capture and oxidation are not yet included.
- Food and green waste are modeled; wood and paper are excluded from the current OFMSW definition.
- Uncollected waste has heterogeneous fate, so its MCF should be scenario-tested.

## Sources to Use in Manuscript Methods

- IPCC 2006 Guidelines for National Greenhouse Gas Inventories, Volume 5, Waste.
- IPCC 2019 Refinement to the 2006 Guidelines, Volume 5, Chapter 3: Solid Waste Disposal.
- IPCC AR6 methane GWP values for biogenic methane.
