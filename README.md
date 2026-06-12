# Organic Waste Climate Readiness

This repository contains the analysis code, processed public datasets, figure source data and non-proprietary results supporting the manuscript:

**Climate-ready pathways for municipal organic waste management worldwide**

The study develops a global country-level screening framework for comparing prevention, composting, anaerobic digestion with electricity recovery, and anaerobic digestion with biomethane/bio-CNG production for food and green organic municipal waste. It combines public waste, development, electricity and spatial datasets with documented ecoinvent-derived screening parameters to estimate methane mitigation opportunities, pathway rankings, uncertainty and implementation readiness across countries and economies.

## Core Research Question

How should countries operationalize the waste hierarchy for organic municipal waste when prevention, methane avoidance, energy substitution and implementation readiness differ by national context?

## Current Main Result

The analysis estimates 1.064 billion tonnes per year of food and green OFMSW in 2022 across 217 countries and economies. Of this, 516 million tonnes are associated with landfill, dumping, uncollected waste or unaccounted treatment flows in countries with treatment data, corresponding to a first-pass methane burden of 514 Mt CO2e per year.

Four pathways are screened:

- Prevention
- Composting
- Anaerobic digestion with electricity recovery
- Anaerobic digestion with biomethane/bio-CNG production

The deterministic global GWP100 screen gives the largest total benefit to prevention, followed by AD-bio-CNG, AD-electricity and composting. Monte Carlo sensitivity also identifies prevention as the most robust country-level winner. The readiness layer separates immediate priorities from strategic build-out, no-regret/complementary and longer-term/local-fit contexts.

## Directory Structure

```text
data/raw/          Public input files included for reproducibility
data/processed/    Harmonized analysis tables
outputs/           Summary tables and derived outputs
scripts/           Reproducible data processing and modelling scripts
manuscript/        Article draft, supplement, figures and submission materials
notes/             Assumption notes, extraction logs and decision records
```

## Environment

The workflow is written in Python. Required packages are listed in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

The figure and mapping scripts require `matplotlib`, `geopandas`, `shapely` and `pyogrio`. If these are not installed, the tabular analysis scripts can still be inspected and many processed outputs can still be reused, but figures will not regenerate.

## Main Manuscript Files

- `manuscript/nature_sustainability_article_draft.md`
- `manuscript/supplementary_information_draft.md`
- `manuscript/nature_sustainability_figure_plan.md`
- `manuscript/nature_sustainability_cover_letter_draft.md`
- `manuscript/nature_sustainability_submission_checklist.md`
- `manuscript/references_draft.md`

## Main Analysis Outputs

- `data/processed/country_ofmsw_analysis_dataset.csv`
- `data/processed/country_ofmsw_first_pass_methane.csv`
- `data/processed/country_ofmsw_four_pathway_comparison.csv`
- `data/processed/country_ofmsw_four_pathway_sensitivity.csv`
- `data/processed/country_ofmsw_readiness_index.csv`
- `outputs/summary_four_pathway_global_metrics.csv`
- `outputs/sensitivity_global_pathway_summary.csv`
- `outputs/sensitivity_robust_winner_counts.csv`
- `outputs/summary_readiness_opportunity_classes.csv`

## Reproducible Workflow

Run scripts from the repository root.

```bash
python scripts/build_country_ofmsw_master.py
python scripts/fetch_wdi_covariates.py
python scripts/extract_ember_carbon_intensity.py
python scripts/build_analysis_dataset.py
python scripts/estimate_first_pass_methane.py
python scripts/screen_ad_pathway.py
python scripts/screen_compost_pathway.py
python scripts/screen_prevention_pathway.py
python scripts/screen_bio_cng_pathway.py
python scripts/compare_four_screening_pathways.py
python scripts/build_readiness_index.py
python scripts/run_four_pathway_sensitivity.py
python scripts/build_four_pathway_summary_tables.py
python scripts/build_figure_drafts.py
python scripts/build_shapefile_maps.py
```

Some earlier three-pathway scripts are retained for provenance but are no longer the main manuscript workflow.

## Licensed Data Boundary

This public archive does not redistribute raw ecoinvent source files, `.zolca` databases, ecoSpold files or exchange-level inventory tables. The manuscript uses derived screening parameters from licensed ecoinvent 3.12 Cutoff unit-process exports and documentation. These derived parameters are reported in the Methods and Supplementary Information so that the screening analysis can be inspected without redistributing proprietary inventory data.

For publication and archiving:

- OK to share public datasets where their licences permit redistribution.
- OK to share processed model outputs and derived ecoinvent factors where licence-compliant.
- OK to report selected ecoinvent process names, versions, system models, reference products, geographies and derived factors.
- Do not share raw ecoinvent ecoSpold2 files, `.zolca` databases or exchange-level inventory tables.

## Public Reproducibility Boundary

The project is intended to be archived with two reproduction levels:

1. **Open reproduction:** public datasets, processed outputs, scripts and licence-compliant derived factors reproduce the reported screening results.
2. **Licensed reproduction:** users with ecoinvent access can verify or update the underlying ecoinvent-derived factors.

See `manuscript/public_archive_plan.md` and `reproducibility_checklist.md` before preparing a public repository.

## Current Limitations

- The methane model is a first-pass screening model, not a full first-order decay inventory.
- Landfill gas capture and oxidation are not included in the central methane screen.
- ecoinvent 3.12 Cutoff unit-process exports are used for direct process emissions, biogas yield and biogas net calorific value; methane-equivalent share is inferred from the reported biogas net calorific value.
- Bio-CNG results depend on methane recovery, upgrading electricity, displaced fuel and readiness assumptions.
- Compost/digestate nutrient and soil-carbon benefits are documented but not fully credited in the central GWP100 screen.
- The repository is intended as a reproducibility archive for screening results, not as a substitute for local facility-level life-cycle assessment.

## Target Journal

Primary target: **Nature Sustainability**

Backup target: **Resources, Conservation & Recycling**
