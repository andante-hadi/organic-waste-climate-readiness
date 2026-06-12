# Bio-CNG Screening Assumptions

Date: 2026-06-12

## Purpose

This pathway extends the OFMSW screening model beyond AD-to-electricity by modelling anaerobic digestion followed by biogas upgrading and compression to bio-CNG/biomethane for transport-fuel substitution.

## Current Factor Sources

Biogas production:

- Source for raw biogas yield: ecoinvent 3.12 Cutoff unit-process export from openLCA, `treatment of biowaste by anaerobic digestion`, RoW.
- Biowaste-only biogas yield: `100 m3 biogas/t OFMSW`, based on the dataset statement that 100 litres of biogas per kg biowaste are assumed.
- Methane-equivalent share: `0.6349 m3 CH4-equivalent/m3 biogas`, inferred from the ecoinvent 3.12 biogas net calorific value of 22.73 MJ/m3 divided by CH4 LHV of 35.8 MJ/m3.

Anaerobic digestion process emissions:

- Source: ecoinvent 3.12 Cutoff unit-process export from openLCA.
- Factor: `74.289 kg CO2e/t OFMSW`.
- Derived from direct non-fossil methane and nitrous oxide exchanges, using AR6 GWP100 values.
- Biogenic CO2 is excluded.

Bio-CNG upgrading/compression:

- Methane recovery: `0.97`.
- Electricity demand: `0.45 kWh/m3 raw biogas`.
- These are screening assumptions and should be varied in sensitivity analysis.

Fuel substitution:

- Displaced fuel: generic diesel transport fuel.
- Avoided diesel factor: `0.074 kg CO2e/MJ biomethane`.
- This is currently global and not country-specific.

## Calculation

For each tonne of diverted OFMSW:

1. Raw biogas = `100 m3`.
2. Biomethane = `100 * 0.6349 * 0.97 = 61.6 m3 CH4-equivalent`.
3. Biomethane energy = `61.6 * 35.8 = 2,205 MJ`.
4. Avoided diesel emissions = `2,205 * 0.074 = 163 kg CO2e/t OFMSW`.
5. Upgrading/compression electricity = `100 * 0.45 = 45.0 kWh/t OFMSW`.
6. Electricity burden uses country-specific Ember 2022 grid carbon intensity.

## Interpretation

The bio-CNG pathway is more favorable than AD-to-electricity in countries where:

- transport-fuel substitution value is high;
- grid electricity is not so carbon-intensive that upgrading/compression burdens dominate;
- landfill/dump methane avoidance remains large.

It is less favorable where:

- fossil transport-fuel displacement is weak or uncertain;
- bio-CNG infrastructure, vehicle fleets, standards, or distribution systems are absent;
- upgrading/compression electricity is carbon-intensive or expensive.

## Manuscript Caveat

The current bio-CNG result should be presented as a screening scenario, not a final deployment claim. It needs sensitivity analysis around methane recovery, upgrading electricity, methane slip, displaced fuel, vehicle efficiency equivalence, and country-specific bio-CNG infrastructure readiness.
