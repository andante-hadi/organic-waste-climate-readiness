# Data Manifest

This file tracks datasets for the OFMSW + What a Waste 3.0 + ecoinvent study.

## Primary Data

| Dataset | Expected File/Access | Status | Notes |
|---|---|---|---|
| What a Waste 3.0 country-level data and codebook | `data/raw/What_a_Waste_3.0_COUNTRY_Dataset_Codebook.xlsx` | Downloaded | Public World Bank dataset, CC-BY 4.0 |
| What a Waste 3.0 city-level data and codebook | `data/raw/What_a_Waste_3.0_CITY_Dataset_Codebook.xlsx` | Downloaded | Public World Bank dataset, CC-BY 4.0 |
| UNEP Food Waste Index 2024 | PDF/appendix/table extraction | To download | Used to validate food-waste fraction and sector split |
| IPCC 2006 Guidelines and 2019 Refinement | PDF/equation extraction | To download | Used for methane calculation framework |
| World Development Indicators | API/CSV | To acquire | GDP, population, urbanization, income group |
| UN DESA WPP/WUP | CSV/Excel | To acquire | Population and urbanization projections |
| Ember electricity data | CSV/API | To acquire | Electricity carbon intensity by country |
| FAOSTAT fertilizer/crop data | API/CSV | To acquire | Fertilizer substitution and nutrient demand |
| WorldClim or ERA5 | Raster/API/CSV | To acquire | Climate zones or temperature/rainfall modifiers |
| ecoinvent 3.12 cutoff | ecoQuery/export/openLCA | Access confirmed | Use for LCI factors; respect license terms |

## Project Folders

- `data/raw`: original downloaded files, unchanged.
- `data/processed`: cleaned and harmonized tables.
- `scripts`: reproducible data cleaning and modeling scripts.
- `outputs`: figures, tables, and model outputs.
- `manuscript`: article outline, methods, and drafted text.
- `notes`: meeting notes, search logs, and decision records.

## First Build Target

Created `data/processed/country_ofmsw_master.csv` with first-pass World Bank variables:

- ISO3 country code.
- Country name.
- MSW generation.
- Organic fraction.
- OFMSW generation.
- Collection rate.
- Disposal shares.
- GDP per capita.
- Income group.
- Population.
- Urban population share.
- Electricity carbon intensity.
- Fertilizer use.
- Climate zone or mean annual temperature.

The current version includes World Bank What a Waste 3.0 variables only. External covariates will be merged in later scripts.
