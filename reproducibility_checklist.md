# Reproducibility Checklist

## Public Archive Boundary

- [ ] Remove raw ecoinvent files before public archiving.
- [ ] Remove `.spold`, `.zolca`, `.7z` and database-export files.
- [ ] Remove `scripts/__pycache__/`.
- [ ] Remove `.DS_Store`.
- [ ] Check that no ecoQuery screenshots or copied licensed tables are archived.
- [ ] Keep only licence-compliant derived ecoinvent factors.

## Public Inputs

- [ ] Document What a Waste 3.0 country dataset source and access date.
- [ ] Document What a Waste 3.0 city dataset source and access date.
- [ ] Document World Development Indicators variables and access date.
- [ ] Document Ember electricity dataset source and access date.
- [ ] Document Natural Earth boundary version and access date.

## Derived Data

- [ ] Include `data/processed/country_ofmsw_analysis_dataset.csv`.
- [ ] Include `data/processed/country_ofmsw_first_pass_methane.csv`.
- [ ] Include `data/processed/country_ofmsw_four_pathway_comparison.csv`.
- [ ] Include `data/processed/country_ofmsw_four_pathway_sensitivity.csv`.
- [ ] Include `data/processed/country_ofmsw_readiness_index.csv`.
- [ ] Include sensitivity and city-layer processed outputs.
- [ ] Include `data/processed/ecoinvent_screening_factors.csv` only if it contains derived factors, not raw exchanges.

## Code

- [ ] Include all scripts in `scripts/`.
- [ ] Confirm scripts run from repository root.
- [ ] Add `requirements.txt`.
- [ ] Add exact command order in `README.md`.
- [ ] Note that three-pathway scripts are retained for provenance but not central.

## Manuscript Support

- [ ] Include final article draft.
- [ ] Include Supplementary Information.
- [ ] Include references.
- [ ] Include figure plan and final figures.
- [ ] Include assumption notes.
- [ ] Include public archive plan.

## Final Verification

- [ ] Re-run full workflow in a clean folder.
- [ ] Compare regenerated summary outputs against manuscript values.
- [ ] Check that proprietary ecoinvent files are absent.
- [ ] Generate DOI/archive link before final submission or revision.
