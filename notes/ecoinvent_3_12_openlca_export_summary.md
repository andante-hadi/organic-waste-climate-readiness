# ecoinvent 3.12 openLCA export summary

This note records derived parameters extracted from user-provided openLCA Excel exports of `ecoinvent 3.12 Cutoff Unit with EN15804.zolca`. It does not reproduce raw exchange tables and should not be treated as a redistributable substitute for ecoinvent.

## Source exports

- `treatment of biowaste by anaerobic digestion | biowaste | Cutoff, U`, geography Rest-of-World, reference product `biowaste`, unit kg.
- `treatment of biowaste by anaerobic digestion | biogas | Cutoff, U`, geography Rest-of-World, reference product `biogas`, unit m3.
- `treatment of biowaste, industrial composting | biowaste | Cutoff, U`, geography Rest-of-World, reference product `biowaste`, unit kg.
- `treatment of biowaste, industrial composting | compost | Cutoff, U`, geography Rest-of-World, reference product `compost`, unit kg.

## Derived model factors

### Anaerobic digestion

- Biogas yield: 0.1 m3/kg biowaste = 100 m3/t biowaste.
- Direct non-fossil methane: 0.0024 kg CH4/kg biowaste.
- Direct dinitrogen monoxide: 0.000033 kg N2O/kg biowaste.
- Direct non-fossil CO2: 0.21 kg/kg biowaste, excluded from GWP100 process-emission factor.
- Direct fossil CO2 exchange was not present in the exported output table.
- AR6 GWP100 direct process-emission factor excluding biogenic CO2:
  - 0.0024 x 27.2 x 1000 = 65.28 kg CO2e/t.
  - 0.000033 x 273 x 1000 = 9.009 kg CO2e/t.
  - Total = 74.289 kg CO2e/t.
- Biogas product net calorific value: 22.73 MJ/m3.
- Methane-equivalent share in biogas is inferred as 22.73 MJ/m3 divided by 35.8 MJ/m3 CH4 = 0.6349 m3 CH4-equivalent/m3 biogas.
- AD-electricity yield used in the screening model:
  - 100 m3 biogas/t x 0.6349 m3 CH4-equivalent/m3 biogas x 9.97 kWh/m3 CH4 x 0.30 = 189.903 kWh/t.

### Industrial composting

- Direct non-fossil methane: 0.001 kg CH4/kg biowaste.
- Direct dinitrogen monoxide: 0.000025 kg N2O/kg biowaste.
- Direct non-fossil CO2: 0.22 kg/kg biowaste, excluded from GWP100 process-emission factor.
- Direct fossil CO2 exchange was not present in the exported output table.
- AR6 GWP100 direct process-emission factor excluding biogenic CO2:
  - 0.001 x 27.2 x 1000 = 27.2 kg CO2e/t.
  - 0.000025 x 273 x 1000 = 6.825 kg CO2e/t.
  - Total = 34.025 kg CO2e/t.

## Interpretation

The 3.12 export replaces the former 3.1 biogas-yield proxy. The lower 3.12 biogas yield materially reduces AD-electricity and AD-bio-CNG benefits. In the updated GWP100 deterministic screen, prevention becomes the largest global pathway, while AD-bio-CNG remains the largest recovery pathway.
