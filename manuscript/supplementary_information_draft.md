# Supplementary Information Draft

## Analysis

Climate-ready pathways for municipal organic waste management worldwide

## Supplementary Note 1. Data Sources

The analysis combines country-level waste, development, electricity, life-cycle inventory and boundary datasets. The main public datasets are World Bank What a Waste 3.0, World Development Indicators, Ember yearly electricity data and Natural Earth Admin 0 country boundaries. The life-cycle process parameters are derived from licensed ecoinvent 3.12 Cutoff unit-process exports and documentation; proprietary ecoinvent exchange-level inventory data are not redistributed.

### Supplementary Table 1. Primary datasets

| Dataset | Use in study | File or access route | Availability |
|---|---|---|---|
| What a Waste 3.0 country data | Waste generation, composition, collection and treatment shares | `data/raw/What_a_Waste_3.0_COUNTRY_Dataset_Codebook.xlsx` | Public |
| What a Waste 3.0 city data | Future city-scale extension and validation | `data/raw/What_a_Waste_3.0_CITY_Dataset_Codebook.xlsx` | Public |
| World Development Indicators | Population, income, GDP per capita, urbanization | WDI API/processed CSV | Public |
| Ember yearly electricity data | Country-specific electricity carbon intensity | `data/raw/ember_yearly_electricity_long.csv` | Public |
| Natural Earth Admin 0 | Country boundaries for mapping | `data/raw/natural_earth/` | Public |
| ecoinvent 3.12 cutoff | Process-emission, biogas-yield and nutrient parameters | openLCA export from ecoinvent 3.12 Cutoff Unit with EN15804 and ecoQuery documentation | Licensed |

## Supplementary Note 2. Organic Municipal Waste Definition

Organic municipal solid waste is defined in the central analysis as the sum of food waste and green waste fractions reported in What a Waste 3.0. Wood, paper, sewage sludge and industrial organic residues are excluded from the central definition to avoid mixing materially different waste streams and treatment logics.

The ecoinvent biowaste documentation defines biowaste as biodegradable garden and park waste, food and kitchen waste from households and comparable sources, as well as comparable residues. This definition is close to the food plus green waste scope used in the screening model, but not identical. The manuscript should therefore describe the modelled flow as food and green organic municipal waste rather than all biowaste.

## Supplementary Note 3. First-Pass Methane Screening

The first-pass methane screen estimates annual methane generation potential from current annual food and green organic waste flows sent to disposal-associated pathways. It is not a formal national greenhouse-gas inventory and does not implement a full first-order decay time series.

For each country and disposal pathway:

`CH4 = W x DOC x DOCf x MCF x F x 16/12`

where `W` is food and green OFMSW sent to the pathway, `DOC` is weighted degradable organic carbon, `DOCf` is the decomposable fraction of DOC, `MCF` is the methane correction factor, `F` is methane fraction in landfill gas, and `16/12` converts carbon to methane.

### Supplementary Table 2. Methane screening constants

| Parameter | Value | Notes |
|---|---:|---|
| Food waste DOC | 0.15 | IPCC-style screening value |
| Green waste DOC | 0.20 | IPCC-style screening value |
| DOCf | 0.50 | Screening value |
| Methane fraction, F | 0.50 | Common default |
| Open dump MCF | 0.40 | Screening assumption |
| Controlled landfill MCF | 0.80 | Screening assumption |
| Sanitary landfill MCF | 1.00 | Screening assumption |
| Unspecified landfill MCF | 0.60 | Screening assumption |
| Uncollected MCF | 0.40 | Screening assumption |
| Unaccounted treatment MCF | 0.60 | Screening assumption |
| Methane GWP100 | 27.2 | AR6 biogenic methane value |

## Supplementary Note 4. Pathway Scenario Equations

The deterministic treatment pathways target 50% of currently unmanaged or disposal-associated food and green OFMSW and assume 80% source-separation or capture efficiency. The effective diverted mass is therefore 40% of eligible waste.

For treatment pathways:

`Net benefit = avoided disposal methane + substitution credit - process emissions - energy burden`

For prevention:

`Net benefit = avoided disposal methane + avoided upstream food-system emissions`

The four pathways are:

- Prevention of food waste generation.
- Composting of diverted food and green organic waste.
- Anaerobic digestion with electricity recovery.
- Anaerobic digestion with biomethane/bio-CNG production.

## Supplementary Note 5. ecoinvent-Derived Parameters

The study uses derived factors from ecoinvent documentation and licensed data, not redistributed exchange-level inventory tables. The main article should cite ecoinvent and report the selected version, system model, process names, reference products and geographies.

### Supplementary Table 3. Central ecoinvent-derived and screening parameters

| Pathway | Factor | Value | Unit | Source |
|---|---|---:|---|---|
| Composting | Process emissions | 34.025 | kg CO2e/t OFMSW | ecoinvent 3.12 cutoff unit-process export |
| Anaerobic digestion | Process emissions | 74.289 | kg CO2e/t OFMSW | ecoinvent 3.12 cutoff unit-process export |
| Anaerobic digestion | Biogas yield | 100 | m3 raw biogas/t OFMSW | ecoinvent 3.12 cutoff unit-process export |
| Anaerobic digestion | Biogas net calorific value | 22.73 | MJ/m3 raw biogas | ecoinvent 3.12 biogas product documentation |
| Anaerobic digestion | Methane-equivalent share | 0.6349 | m3 CH4-equivalent/m3 biogas | derived from ecoinvent 3.12 biogas net calorific value |
| AD-electricity | Electricity yield | 189.9 | kWh/t OFMSW | derived from biogas yield, CH4 LHV and 30% efficiency |
| AD-bio-CNG | Methane recovery | 0.97 | m3 CH4 recovered/m3 CH4 input | screening assumption |
| AD-bio-CNG | Upgrading/compression electricity | 0.45 | kWh/m3 raw biogas | screening assumption |
| AD-bio-CNG | Diesel substitution | 0.074 | kg CO2e/MJ biomethane | screening assumption |
| Composting | Nitrogen content | 3.59 | kg N/t OFMSW | ecoinvent 3.12 documentation |
| Composting | Phosphate content | 1.67 | kg phosphate/t OFMSW | ecoinvent 3.12 documentation |
| Composting | Potassium content | 3.16 | kg K/t OFMSW | ecoinvent 3.12 documentation |
| Digestate | Nitrogen content | 11.4 | kg N/t OFMSW | ecoinvent 3.12 documentation |
| Digestate | Phosphate content | 2.3 | kg phosphate/t OFMSW | ecoinvent 3.12 documentation |
| Digestate | Potassium content | 7.9 | kg K/t OFMSW | ecoinvent 3.12 documentation |

## Supplementary Note 6. Avoiding Double Counting

Landfill and dump methane are estimated with the first-pass methane screen. ecoinvent treatment factors are used for managed composting and anaerobic digestion process emissions, not for re-estimating the same baseline disposal methane. This avoids double counting methane emissions when calculating avoided disposal benefits.

Biogenic CO2 is excluded from composting and anaerobic digestion process-emissions factors. Biogenic CH4 and N2O are included using AR6 GWP100 values. The composting factor is based on direct unit-process exchanges of 0.001 kg non-fossil CH4 and 0.000025 kg N2O per kg biowaste. The anaerobic-digestion factor is based on direct unit-process exchanges of 0.0024 kg non-fossil CH4 and 0.000033 kg N2O per kg biowaste.

## Supplementary Note 7. Readiness Index

The readiness screen classifies countries by combining mitigation potential and implementation-readiness indicators. General readiness indicators include collection coverage, income group, GDP per capita, urbanization and data completeness. Pathway-specific readiness indicators include existing biological treatment, recovery infrastructure proxies and conditions relevant to bio-CNG deployment.

Collection readiness is the reported collection coverage by population, supplemented by collection coverage by weight where population coverage is missing. Income readiness scores are 1.00 for high-income countries, 0.75 for upper-middle-income countries, 0.45 for lower-middle-income countries and 0.25 for low-income countries. GDP readiness is based on log10 GDP per capita and min-max scaled between the 5th and 95th percentiles. Urbanization readiness is min-max scaled between 20% and 95% urban population. Existing biological treatment is the reported anaerobic digestion plus composting share, capped at 20%. Existing recovery infrastructure is the reported recycling, mechanical-biological treatment, refuse-derived fuel and incineration share, capped at 60%. Data completeness is the share of required variables available for collection, disposal intensity, food and green composition, GDP per capita, urbanization and electricity carbon intensity.

General readiness is the mean of collection, income, GDP, urbanization and data-completeness scores. Pathway readiness scores are:

- Prevention: general readiness, income and data completeness.
- Composting: collection, existing biological treatment, urbanization and data completeness.
- AD-electricity: collection, existing biological treatment, existing recovery infrastructure, GDP and data completeness.
- AD-bio-CNG: collection, GDP, urbanization, existing recovery infrastructure and data completeness.

The best-pathway readiness score is the pathway-specific readiness score corresponding to the deterministic best pathway. Mitigation potential is calculated from the log10 deterministic best-pathway benefit and min-max scaled between the 5th and 95th percentiles among countries with valid pathway results.

Countries/economies are assigned to:

- Immediate priority: mitigation score >=0.67 and readiness score >=0.60.
- Strategic build-out: mitigation score >=0.67 and readiness score <0.60.
- No-regret/complementary: mitigation score <0.67 and readiness score >=0.60.
- Longer-term/local fit: mitigation score <0.67 and readiness score <0.60.
- Missing/insufficient data: insufficient pathway or readiness data.

### Supplementary Table 4. Readiness class counts

| Class | Countries/economies |
|---|---:|
| Immediate priority | 46 |
| Strategic build-out | 24 |
| No-regret/complementary | 68 |
| Longer-term/local fit | 14 |
| Missing/insufficient data | 65 |

## Supplementary Note 8. Sensitivity Analysis

Monte Carlo sensitivity analysis propagates uncertainty in prevention rate, avoided upstream food emissions, AD process emissions, composting process emissions, biogas yield, methane share, electricity conversion efficiency, methane recovery, upgrading/compression electricity and diesel substitution. For each country and iteration, the pathway with the largest net GWP100 benefit is identified. Countries are assigned a robust winning pathway where one pathway dominates the uncertainty ensemble; otherwise, they are classified as having no robust winner.

The central Monte Carlo analysis uses 1,000 iterations and random seed 20260523. Robust winners are assigned where one pathway has the highest country-level net benefit in at least 50% of iterations. Countries with valid results but no pathway reaching this threshold are classified as no robust winner.

### Supplementary Table 5. Monte Carlo parameter distributions

| Parameter | Distribution | Low | Mode/central | High | Unit |
|---|---|---:|---:|---:|---|
| AD process emissions | triangular | 40 | 74.289 | 130 | kg CO2e/t OFMSW |
| Compost process emissions | triangular | 20 | 34.025 | 90 | kg CO2e/t OFMSW |
| Biogas yield | triangular | 70 | 100 | 150 | m3 raw biogas/t OFMSW |
| Methane-equivalent share | uniform | 0.55 | NA | 0.70 | m3 CH4-equivalent/m3 biogas |
| Electricity conversion efficiency | uniform | 0.25 | NA | 0.40 | fraction |
| Methane recovery for bio-CNG | uniform | 0.90 | NA | 0.99 | fraction |
| Upgrading/compression electricity | triangular | 0.25 | 0.45 | 0.80 | kWh/m3 raw biogas |
| Diesel substitution factor | uniform | 0.055 | NA | 0.090 | kg CO2e/MJ biomethane |
| Prevention rate | uniform | 0.10 | NA | 0.30 | fraction of unmanaged food waste |
| Avoided upstream food emissions | triangular | 800 | 1500 | 2800 | kg CO2e/t prevented food waste |

### Supplementary Table 6. Global sensitivity summary

| Pathway | Mean | p05 | Median | p95 | Unit |
|---|---:|---:|---:|---:|---|
| AD-electricity | 210.1 | 201.0 | 210.0 | 219.7 | Mt CO2e/yr |
| AD-bio-CNG | 217.3 | 204.8 | 216.8 | 231.6 | Mt CO2e/yr |
| Composting | 195.6 | 189.7 | 195.9 | 200.1 | Mt CO2e/yr |
| Prevention | 249.5 | 131.2 | 244.4 | 392.6 | Mt CO2e/yr |

### Supplementary Table 7. Robust winner counts

| Robust winner | Countries/economies |
|---|---:|
| Prevention | 125 |
| AD-bio-CNG | 20 |
| AD-electricity | 5 |
| No robust winner | 2 |
| Missing/insufficient data | 65 |

## Supplementary Note 9. GWP20 Near-Term Methane Sensitivity

The central manuscript reports GWP100 results. A deterministic GWP20 sensitivity was also calculated by replacing the methane GWP100 value with a GWP20 value of 80.8 while leaving the central pathway assumptions unchanged. This sensitivity tests whether near-term methane weighting changes pathway priorities.

### Supplementary Table 8. Deterministic GWP20 pathway totals

| Pathway | Net benefit | Unit |
|---|---:|---|
| AD-bio-CNG | 624.7 | Mt CO2e/yr |
| AD-electricity | 614.3 | Mt CO2e/yr |
| Composting | 603.9 | Mt CO2e/yr |
| Prevention | 413.5 | Mt CO2e/yr |

### Supplementary Table 9. Deterministic GWP20 best-pathway counts

| Best pathway under GWP20 | Countries/economies |
|---|---:|
| AD-bio-CNG | 129 |
| AD-electricity | 15 |
| Composting | 8 |
| Missing/insufficient data | 66 |

Under GWP20, treatment pathways that avoid methane from already-generated or disposal-associated organic waste become more prominent. This supports the main claim that prevention remains the upstream hierarchy priority, but climate-investment sequencing depends on methane timing and country-specific baseline conditions.

## Supplementary Note 10. Nutrient-Credit Sensitivity

The central GWP100 screen does not fully credit compost and digestate nutrient substitution. A conservative nutrient-credit sensitivity was therefore calculated using documented compost and digestate N, phosphate and K contents and generic fertilizer displacement factors. The purpose is to test whether nutrient credits materially change pathway ranking, not to provide a definitive agronomic LCA.

The screening factors are 5.0 kg CO2e/kg N, 1.0 kg CO2e/kg phosphate and 0.5 kg CO2e/kg K. Availability/substitution fractions are 20% N, 50% phosphate and 80% K for compost, and 50% N, 60% phosphate and 80% K for digestate.

### Supplementary Table 10. Conservative nutrient-credit sensitivity

| Pathway | Central | Nutrient credit | With nutrients | Unit |
|---|---:|---:|---:|---|
| AD-electricity | 209.1 | 6.8 | 215.9 | Mt CO2e/yr |
| AD-bio-CNG | 219.5 | 6.8 | 226.3 | Mt CO2e/yr |
| Composting | 198.6 | 1.2 | 199.8 | Mt CO2e/yr |
| Prevention | 232.8 | 0.0 | 232.8 | Mt CO2e/yr |

### Supplementary Table 11. Best-pathway counts with nutrient credits

| Best pathway with nutrient credits | Countries/economies |
|---|---:|
| Prevention | 114 |
| AD-bio-CNG | 34 |
| AD-electricity | 3 |
| Composting | 1 |
| Missing/insufficient data | 66 |

Under conservative assumptions, nutrient credits modestly increase AD and composting benefits but do not overturn the central GWP100 interpretation. Final fertilizer substitution should harmonize phosphate/P/P2O5 units and account for agronomic availability, nutrient losses, soil-carbon effects, compost quality and market displacement limits.

## Supplementary Note 11. Soil Carbon And Humus Effects

The central GWP100 screen does not credit soil organic carbon accrual or humus formation from compost or digestate. This is a conservative choice. Soil-carbon benefits are context-specific and depend on compost or digestate quality, application rate, crop and soil type, baseline soil organic carbon, climate, land management, time horizon, permanence and whether carbon storage is additional.

The ecoinvent documentation copied for composting and anaerobic digestion includes humus-related information and indicates that compost and digestate have different capacities to build humus. These data support the qualitative conclusion that composting and digestate may provide soil benefits not captured by the central climate-only screen. However, applying a single global soil-carbon credit would risk overstating benefits in some countries and understating them in others.

The main manuscript therefore interprets composting results as conservative climate-only estimates, not as full assessments of composting's agronomic, soil-health or circular-economy value.

## Supplementary Note 12. Bio-CNG Stress Test

Because AD-bio-CNG is the largest deterministic recovery pathway in the central screen, a stress test was used to examine sensitivity to less favorable assumptions about fuel displacement, upgrading/compression electricity, process emissions and methane slip.

### Supplementary Table 12. Bio-CNG stress-test assumptions

| Scenario | Diesel substitution | Upgrading electricity | Process emissions | Methane slip |
|---|---:|---:|---:|---:|
| Central | 100% | 100% | 100% | 0% of biomethane |
| Moderate stress | 80% | 125% | 110% | 1% of biomethane |
| High stress | 60% | 150% | 125% | 3% of biomethane |

### Supplementary Table 13. Bio-CNG stress-test results

| Scenario | Bio-CNG net benefit | AD-bio-CNG best | AD-electricity best | Prevention best | Missing |
|---|---:|---:|---:|---:|---:|
| Central | 219.5 Mt CO2e/yr | 28 | 3 | 121 | 66 |
| Moderate stress | 207.7 Mt CO2e/yr | 15 | 12 | 125 | 66 |
| High stress | 192.6 Mt CO2e/yr | 1 | 20 | 127 | 66 |

Bio-CNG remains globally beneficial under stress assumptions, but its country-level dominance is sensitive. This supports treating AD-bio-CNG as a high-potential pathway where methane avoidance, transport-fuel substitution and infrastructure readiness align, rather than as a universally robust option.

## Supplementary Note 13. Landfill Gas Capture And Oxidation Sensitivity

The central first-pass methane screen does not explicitly include landfill gas capture or oxidation. A scenario sensitivity was therefore used to test whether pathway conclusions depend on this assumption.

### Supplementary Table 14. Landfill gas capture and oxidation scenarios

| Scenario | Controlled landfill capture | Sanitary landfill capture | Unspecified landfill capture | Landfill oxidation |
|---|---:|---:|---:|---:|
| Low capture | 10% | 25% | 5% | 5% |
| Moderate capture | 25% | 50% | 15% | 10% |
| High capture | 50% | 75% | 30% | 10% |

Open dumping, uncollected and unaccounted flows are assigned no capture.

### Supplementary Table 15. Pathway results under landfill capture sensitivity

| Scenario | First-pass CH4 | AD-electricity | AD-bio-CNG | Composting | Prevention |
|---|---:|---:|---:|---:|---:|
| Low capture | 15.6 Mt CH4/yr | 173.4 | 183.8 | 163.0 | 217.3 |
| Moderate capture | 12.4 Mt CH4/yr | 138.0 | 148.4 | 127.5 | 201.9 |
| High capture | 9.4 Mt CH4/yr | 105.3 | 115.7 | 94.8 | 187.6 |

Pathway values are Mt CO2e/yr.

### Supplementary Table 16. Best-pathway counts under landfill capture sensitivity

| Scenario | Prevention | AD-bio-CNG | AD-electricity | Missing |
|---|---:|---:|---:|---:|
| Low capture | 129 | 20 | 3 | 66 |
| Moderate capture | 137 | 14 | 1 | 66 |
| High capture | 142 | 9 | 1 | 66 |

Landfill gas capture and oxidation reduce the avoided-methane benefit of all diversion pathways. Prevention becomes more dominant as capture assumptions increase because its benefit includes avoided upstream food-system emissions. AD-bio-CNG remains relevant in a subset of countries/economies even under high-capture assumptions, supporting a context-specific rather than universal interpretation.

## Supplementary Note 14. City-Level Validation Layer

The What a Waste 3.0 city dataset was screened as a supplementary validation and extension layer. The city screen estimates food plus green OFMSW and landfill/dump/uncollected/unaccounted flows where city-level generation, composition and treatment-share data are available. It also records whether cities report anaerobic digestion or composting asset/throughput data.

### Supplementary Table 17. City-level screen coverage

| Metric | Value |
|---|---:|
| Cities total | 262 |
| Cities with MSW generation | 244 |
| Cities with food or green fraction | 201 |
| Cities with treatment shares | 195 |
| Food plus green OFMSW | 93.9 Mt/yr |
| Food plus green OFMSW to landfill/dump/uncollected/unaccounted | 58.3 Mt/yr |
| Cities with AD asset data | 8 |
| Cities with compost asset data | 62 |

The city layer confirms that national results hide substantial urban heterogeneity and that implementation readiness cannot be inferred from waste quantities alone. Composting asset data are more commonly reported than AD asset data in the city dataset, suggesting that low-complexity biological treatment may be more immediately observable in urban systems, while AD and bio-CNG require more targeted infrastructure validation.

### Supplementary Table 18. City unmanaged/disposal OFMSW by country readiness class

| Country readiness class | Cities | City OFMSW | City unmanaged/disposal OFMSW | Cities with AD asset data | Cities with compost asset data |
|---|---:|---:|---:|---:|---:|
| Immediate priority | 83 | 46.9 Mt/yr | 27.5 Mt/yr | 2 | 26 |
| Strategic build-out | 41 | 25.0 Mt/yr | 15.3 Mt/yr | 3 | 12 |
| Missing/insufficient country data | 49 | 14.1 Mt/yr | 12.7 Mt/yr | 1 | 5 |
| No-regret/complementary | 76 | 6.6 Mt/yr | 1.6 Mt/yr | 1 | 18 |
| Longer-term/local fit | 13 | 1.2 Mt/yr | 1.2 Mt/yr | 1 | 1 |

Most sampled city unmanaged/disposal OFMSW lies in countries classified as immediate priorities or strategic build-out cases, reinforcing the urban-infrastructure relevance of the country-level readiness typology.

## Supplementary Note 15. Mapping And Boundary Data

Country maps use Natural Earth Admin 0 boundaries at 1:50m resolution. Model ISO3 codes were joined to Natural Earth `ADM0_A3`. The current join matches 212 of 217 model ISO3 entries. Unmatched codes are `CHI`, `GIB`, `PSE`, `SSD` and `XKX`. Final submission maps should include standard boundary-disclaimer language required by the journal.

## Supplementary Note 16. Missing-Data Diagnostics

The pathway and readiness screens classify 65 countries/economies as missing or insufficiently characterized. This class is not driven by missing MSW generation data, which are available for all 217 countries/economies in the harmonized country dataset. Instead, missingness is concentrated in food/green composition, disposal/treatment shares and collection coverage.

### Supplementary Table 19. Coverage by variable group

| Variable group | Countries/economies with data | Countries/economies missing group | Coverage |
|---|---:|---:|---:|
| MSW generation | 217 | 0 | 100.0% |
| Food/green composition | 179 | 38 | 82.5% |
| Disposal/treatment shares | 174 | 43 | 80.2% |
| Collection coverage | 138 | 79 | 63.6% |
| WDI development covariates | 216 | 1 | 99.5% |
| Electricity carbon intensity | 202 | 15 | 93.1% |

### Supplementary Table 20. Missing or insufficient pathway assignment by region

| Region | Countries/economies | Pathway assigned | Missing/insufficient | Missing/insufficient |
|---|---:|---:|---:|---:|
| East Asia and Pacific | 37 | 32 | 5 | 13.5% |
| Europe and Central Asia | 58 | 43 | 15 | 25.9% |
| Latin America and the Caribbean | 42 | 30 | 12 | 28.6% |
| Middle East and North Africa | 21 | 20 | 1 | 4.8% |
| North America | 3 | 3 | 0 | 0.0% |
| South Asia | 8 | 7 | 1 | 12.5% |
| Sub-Saharan Africa | 48 | 17 | 31 | 64.6% |

### Supplementary Table 21. Missing or insufficient pathway assignment by income group

| Income group | Countries/economies | Pathway assigned | Missing/insufficient | Missing/insufficient |
|---|---:|---:|---:|---:|
| High income | 83 | 59 | 24 | 28.9% |
| Low income | 25 | 8 | 17 | 68.0% |
| Lower-middle income | 54 | 38 | 16 | 29.6% |
| Upper-middle income | 54 | 46 | 8 | 14.8% |
| Upper-middle income (2019 classification) | 1 | 1 | 0 | 0.0% |

Missingness is therefore unevenly distributed and highest in low-income countries and Sub-Saharan Africa. This pattern supports the readiness interpretation: data capacity, collection systems and treatment reporting are themselves part of implementation readiness. The results should not be interpreted as evidence that missing countries have low mitigation potential; rather, they identify where improved waste characterization and treatment reporting would be especially valuable.

## Supplementary Note 17. Limitations

## Supplementary Note 17. Readiness Threshold Robustness

The central readiness typology uses mitigation-potential and readiness thresholds of 0.67 and 0.60, respectively. Because these thresholds are screening choices rather than empirically estimated breakpoints, we tested whether the class structure is sensitive to threshold changes of plus or minus 15% in a 3 x 3 grid. Lower thresholds move more countries into the immediate-priority class, whereas higher thresholds move more countries into longer-term/local-fit contexts. The central interpretation is unchanged: the typology should be used to distinguish likely near-term deployment contexts from strategic build-out and lower-complexity no-regret contexts, not as a fixed national ranking.

### Supplementary Table 22. Readiness class counts under threshold variation

| Mitigation threshold | Readiness threshold | Mitigation change | Readiness change | Immediate priority | Strategic build-out | No-regret / complementary | Longer-term / local fit | Missing/insufficient |
|---:|---:|---|---|---:|---:|---:|---:|---:|
| 0.57 | 0.51 | -15% | -15% | 79 | 13 | 54 | 6 | 65 |
| 0.57 | 0.60 | -15% | central | 64 | 28 | 50 | 10 | 65 |
| 0.57 | 0.69 | -15% | +15% | 49 | 43 | 39 | 21 | 65 |
| 0.67 | 0.51 | central | -15% | 60 | 10 | 73 | 9 | 65 |
| 0.67 | 0.60 | central | central | 46 | 24 | 68 | 14 | 65 |
| 0.67 | 0.69 | central | +15% | 34 | 36 | 54 | 28 | 65 |
| 0.77 | 0.51 | +15% | -15% | 39 | 8 | 94 | 11 | 65 |
| 0.77 | 0.60 | +15% | central | 31 | 16 | 83 | 22 | 65 |
| 0.77 | 0.69 | +15% | +15% | 24 | 23 | 64 | 41 | 65 |

We also tested whether the readiness typology is sensitive to the equal-weight assumption used in the central pathway-specific readiness scores. Alternative weighting schemes doubled the weight of collection coverage, economic capacity, existing infrastructure or data completeness while keeping the central mitigation and readiness thresholds fixed. The immediate-priority class remains stable under these alternatives: 41-54 countries/economies are classified as immediate priorities, and 89.1-100.0% of the central immediate-priority countries/economies remain in that class.

### Supplementary Table 23. Readiness class counts under alternative weighting schemes

| Scenario | Immediate priority | Strategic build-out | No-regret / complementary | Longer-term / local fit | Missing/insufficient | Countries changing class from central | Central immediate priorities retained |
|---|---:|---:|---:|---:|---:|---:|---:|
| Central equal weights | 46 | 24 | 68 | 14 | 65 | 0 | 46 (100.0%) |
| Collection-heavy | 46 | 24 | 69 | 13 | 65 | 1 | 46 (100.0%) |
| Economic-capacity-heavy | 41 | 29 | 64 | 18 | 65 | 9 | 41 (89.1%) |
| Infrastructure-heavy | 45 | 25 | 68 | 14 | 65 | 1 | 45 (97.8%) |
| Data-completeness-heavy | 54 | 16 | 71 | 11 | 65 | 11 | 46 (100.0%) |

## Supplementary Note 18. Limitations

The analysis is a screening framework rather than a final inventory or site-specific LCA. Main limitations include:

- Missing and heterogeneous treatment-share reporting in What a Waste 3.0.
- Use of a first-pass methane model rather than a full first-order decay model.
- No explicit landfill gas capture or oxidation in the central methane screen.
- Methane-equivalent share is inferred from ecoinvent 3.12 net calorific value rather than measured as a reported volumetric gas-composition parameter.
- Global rather than country-specific diesel substitution factor for bio-CNG.
- Limited representation of soil carbon, fertilizer substitution, agronomic performance, cost, public health and behavioural feasibility.
- Prevention rates and avoided upstream food-system emissions are uncertain and context-specific.

## Supplementary Data Files To Archive

- `data/processed/country_ofmsw_analysis_dataset.csv`
- `data/processed/country_ofmsw_first_pass_methane.csv`
- `data/processed/country_ofmsw_four_pathway_comparison.csv`
- `data/processed/country_ofmsw_four_pathway_sensitivity.csv`
- `data/processed/country_ofmsw_readiness_index.csv`
- `data/processed/country_ofmsw_readiness_weighting_robustness.csv`
- `outputs/summary_four_pathway_global_metrics.csv`
- `outputs/sensitivity_global_pathway_summary.csv`
- `outputs/sensitivity_robust_winner_counts.csv`
- `outputs/summary_readiness_opportunity_classes.csv`
- `outputs/summary_readiness_threshold_robustness.csv`
- `outputs/summary_readiness_threshold_robustness_grid.csv`
- `outputs/summary_readiness_weighting_robustness.csv`

Licensed ecoinvent source files and raw exchange-level inventory tables should not be archived publicly.
