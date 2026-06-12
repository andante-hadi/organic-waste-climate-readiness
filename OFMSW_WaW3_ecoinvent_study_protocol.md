# Study Protocol: Global OFMSW Methane and Circularity Pathways

## Working Title

Global climate and circularity benefits of diverting organic municipal solid waste under country-specific pathways to 2050

## Core Hypothesis

The climate and circular-economy value of OFMSW diversion is highly country-specific. The best pathway differs depending on organic waste generation, current collection and disposal systems, climate, electricity mix, fertilizer demand, and institutional capacity. A single global recommendation such as "compost food waste" or "build anaerobic digestion" is therefore suboptimal.

## Target Journals

- Nature Sustainability
- Nature Climate Change
- Nature Cities
- Nature Food
- One Earth
- Global Environmental Change

## Primary Research Question

Which OFMSW intervention pathway provides the largest net climate, energy, nutrient, and cost-effectiveness benefit by country and region from 2022 to 2050?

## Intervention Pathways

1. Baseline / business-as-usual waste management.
2. Improved collection with current treatment mix.
3. Landfill gas capture for existing disposal systems.
4. Composting of source-separated OFMSW.
5. Anaerobic digestion with electricity and/or heat recovery.
6. Anaerobic digestion with digestate nutrient recovery.
7. Food waste prevention before disposal.
8. Hybrid pathway optimized by country context.

## Core Datasets

| No. | Dataset | Role in Study | Access |
|---:|---|---|---|
| 1 | World Bank What a Waste 3.0 country-level database | Country MSW generation, composition, collection, treatment/disposal, projections, financing/institutional variables | Open, CC-BY 4.0 |
| 2 | World Bank What a Waste 3.0 city-level database | City validation, urban heterogeneity, sensitivity checks | Open, CC-BY 4.0 |
| 3 | UNEP Food Waste Index 2024 | Food waste by sector; cross-check for food fraction of OFMSW | Open |
| 4 | IPCC 2006 Guidelines + 2019 Refinement | Methane model, degradable organic carbon, methane correction factors, oxidation, recovery | Open |
| 5 | World Bank World Development Indicators | GDP, income group, population, urbanization, governance and development covariates | Open API |
| 6 | UN DESA World Population Prospects / World Urbanization Prospects | Population and urbanization projections to 2050 | Open CSV/Excel |
| 7 | Ember electricity data | Country electricity carbon intensity for avoided electricity from biogas | Open CSV/API |
| 8 | FAOSTAT | Fertilizer use, crop nutrient demand, agricultural context | Open API/downloads |
| 9 | WorldClim or ERA5 | Temperature/rainfall/climate-zone effects on methane and treatment suitability | Open |
| 10 | ecoinvent 3.12 cutoff | LCI/LCA background factors for composting, AD, landfill, incineration, transport, electricity, fertilizer substitution | Licensed access available |

## Key Variables

### From What a Waste 3.0

- Total MSW generation by country and city.
- Per-capita MSW generation.
- Waste composition: food/green/organic fractions where available.
- Collection coverage.
- Treatment and disposal shares: open dump, controlled landfill, sanitary landfill, recycling, composting, incineration, other.
- Cost, financing, legal, institutional, and private-sector variables where available.
- 2050 projections and scenario variables.

### Derived OFMSW Variables

- OFMSW generation: MSW generation multiplied by organic fraction.
- Collected OFMSW and uncollected OFMSW.
- OFMSW sent to landfill/dump/open burning/composting/AD/incineration.
- Methane-generating OFMSW mass.
- Recoverable food-waste fraction.
- Recoverable green-waste fraction.

### Climate and Circularity Outcomes

- Methane emissions under baseline and scenarios.
- CO2e using GWP20 and GWP100.
- Avoided methane from diversion.
- Avoided grid electricity emissions from biogas energy.
- Avoided synthetic fertilizer emissions from compost/digestate nutrient substitution.
- Net GHG balance by pathway.
- Cost per tCO2e avoided.
- Nutrient recovery: nitrogen, phosphorus, potassium.
- Energy recovery: kWh electricity and/or MJ heat.
- Equity indicators: benefits per capita, benefits relative to GDP, benefits in low- and middle-income countries.

## Modeling Framework

### Step 1: Waste Flow Model

For each country:

MSW generation -> OFMSW fraction -> collected/uncollected split -> treatment/disposal allocation -> baseline emissions.

### Step 2: Methane Model

Use IPCC first-order decay or simplified Tier 1/Tier 2 equations depending on data availability.

Core parameters:

- Degradable organic carbon.
- Methane correction factor by disposal type.
- Fraction of DOC dissimilated.
- Methane fraction in landfill gas.
- Methane recovery.
- Oxidation factor.
- Climate-dependent decay rate where feasible.

### Step 3: LCA Pathway Model

Use ecoinvent 3.12 cutoff to estimate process-level environmental burdens for:

- Composting of organic waste.
- Anaerobic digestion of biowaste/food waste.
- Landfill treatment of biowaste/MSW.
- Municipal waste incineration where relevant.
- Transport of waste.
- Electricity and heat substitution.
- Synthetic fertilizer substitution.

### Step 4: Scenario Analysis to 2050

Scenarios:

- Business as usual.
- Low ambition: improved collection, reduced open dumping, modest composting/AD.
- High ambition: food waste prevention, high source separation, AD/composting where suitable, landfill gas recovery.
- Country-optimized pathway: choose best mix based on net climate benefit and feasibility constraints.

### Step 5: Uncertainty and Sensitivity

Run Monte Carlo or Latin Hypercube uncertainty over:

- Organic fraction.
- Collection coverage.
- Methane correction factors.
- DOC and decay rates.
- AD methane yield.
- Compost emissions.
- Electricity carbon intensity.
- Fertilizer substitution rate.
- Capital and operating cost ranges.

## Main Figures

1. Global map of OFMSW generation and mismanaged OFMSW.
2. Baseline methane emissions from OFMSW by country/region.
3. Country-level best pathway map: prevention, composting, AD, landfill gas capture, or hybrid.
4. Marginal abatement curve: cost per tCO2e avoided by intervention and region.
5. 2050 scenario wedge chart showing methane reductions by pathway.
6. Equity plot: mitigation potential vs current waste-management capacity/income group.
7. Nutrient recovery potential compared with fertilizer demand.

## Candidate Novel Contributions

- First global country-level OFMSW pathway optimization using What a Waste 3.0 and ecoinvent 3.12.
- Direct comparison of prevention, composting, AD, landfill gas capture, and hybrid pathways under one harmonized framework.
- Integration of climate mitigation, nutrient recovery, energy substitution, costs, and equity.
- Identification of countries where basic collection expansion is more climate-effective than advanced treatment.
- Identification of countries where AD or composting is likely over-promoted relative to prevention or landfill gas capture.

## First Analysis Milestone

Build a reproducible country-level dataset with:

- Country name and ISO code.
- Total MSW generation.
- Organic fraction.
- Estimated OFMSW generation.
- Collection rate.
- Disposal/treatment shares.
- Baseline OFMSW to landfill/dump/open disposal.
- GDP per capita and income group.
- Population and urban population.
- Electricity carbon intensity.
- Fertilizer use.
- Climate zone or mean annual temperature.

The first publishable result should be a global map and ranking of OFMSW methane mitigation potential under three simple interventions:

1. Food waste prevention.
2. Diversion to composting.
3. Diversion to anaerobic digestion with energy recovery.

## Immediate Next Tasks

1. Download What a Waste 3.0 country and city Excel files.
2. Inspect the codebooks and identify exact variable names.
3. Build the country-level master table.
4. Identify ecoinvent 3.12 processes for landfill, composting, anaerobic digestion, transport, electricity, and fertilizer.
5. Create initial IPCC methane calculation notebook/script.
6. Produce the first baseline OFMSW generation and methane-potential plots.

## Source Links

- What a Waste 3.0: https://www.worldbank.org/what-a-waste
- What a Waste Data Catalog: https://datacatalog.worldbank.org/infrastructure-data/search/dataset/0039597/what-a-waste-global-database
- UNEP Food Waste Index 2024: https://www.unep.org/resources/publication/food-waste-index-report-2024
- World Development Indicators: https://datatopics.worldbank.org/world-development-indicators
- UN World Urbanization Prospects: https://population.un.org/wup/index.html
- Ember API: https://ember-energy.org/data/api/
- FAOSTAT: https://www.fao.org/faostat/
- Copernicus Climate Data Store: https://climate.copernicus.eu/climate-data-store
