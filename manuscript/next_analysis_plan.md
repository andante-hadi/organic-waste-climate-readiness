# Next Analysis Plan

This plan lists the analyses most likely to improve the paper before a Nature Sustainability submission.

## Priority 1. Near-Term Methane Sensitivity

Purpose:

- Show whether the main pathway and readiness conclusions hold under a 20-year methane framing.
- Strengthen the climate relevance for near-term methane action.

Current status:

- `country_ofmsw_first_pass_methane.csv` already includes `first_pass_co2e_gwp20_tpy`.
- Main four-pathway screen reports GWP100.
- Deterministic GWP20 pathway sensitivity has been implemented.

Completed work:

- Added `scripts/compare_four_screening_pathways_gwp20.py`.
- Produced `data/processed/country_ofmsw_four_pathway_comparison_gwp20.csv`.
- Produced `outputs/summary_four_pathway_global_metrics_gwp20.csv`.
- Produced `outputs/summary_four_pathway_best_counts_gwp20.csv`.
- Documented results in `notes/gwp20_sensitivity_results.md`.
- Added GWP20 tables to the Supplementary Information draft.

Remaining work:

- Optional: create a GWP100 versus GWP20 supplementary figure.
- Optional: extend Monte Carlo sensitivity to GWP20 robust winners.

Expected manuscript use:

- Main text can remain GWP100.
- Supplementary sensitivity can show near-term methane framing strengthens the importance of unmanaged organic waste.

## Priority 2. Landfill Gas Capture And Oxidation Sensitivity

Purpose:

- Address reviewer concern that landfill methane may be overestimated where gas capture or oxidation is significant.

Current status:

- Central methane screen does not explicitly include landfill gas capture or oxidation.
- Landfill gas capture and oxidation sensitivity has been implemented.

Completed work:

- Added `scripts/apply_landfill_capture_sensitivity.py`.
- Produced `data/processed/country_ofmsw_landfill_capture_sensitivity.csv`.
- Produced `outputs/summary_landfill_capture_sensitivity.csv`.
- Produced `outputs/summary_landfill_capture_best_counts.csv`.
- Documented results in `notes/landfill_capture_sensitivity_results.md`.
- Added landfill capture sensitivity tables to the Supplementary Information draft.

Remaining work:

- Replace scenario assumptions with country-specific landfill gas collection data if available.
- Optional: implement full first-order decay timing.

Expected manuscript use:

- Supplementary sensitivity and limitation.
- Useful response to reviewers who focus on national inventory consistency.

## Priority 3. Compost And Digestate Nutrient-Credit Sensitivity

Purpose:

- Avoid undervaluing composting and digestate in a climate-only screen.
- Show whether nutrient substitution changes pathway rankings.

Current status:

- ecoinvent documentation-derived nutrient contents are available:
  - Compost: 3.59 kg N/t, 1.67 kg phosphate/t, 3.16 kg K/t.
  - Digestate: 11.4 kg N/t, 2.3 kg phosphate/t, 7.9 kg K/t.
- Conservative nutrient-credit sensitivity has been implemented.

Completed work:

- Added `scripts/apply_nutrient_credit_sensitivity.py`.
- Produced `data/processed/country_ofmsw_four_pathway_comparison_nutrient_sensitivity.csv`.
- Produced `outputs/summary_nutrient_credit_sensitivity.csv`.
- Produced `outputs/summary_best_counts_nutrient_sensitivity.csv`.
- Documented results in `notes/nutrient_credit_sensitivity_results.md`.
- Added nutrient-credit tables to the Supplementary Information draft.

Remaining work:

- Harmonize phosphate/P/P2O5 units before final submission.
- Add soil-carbon/humus sensitivity or justify exclusion.
- Replace generic fertilizer displacement factors with more defensible literature or ecoinvent-derived values if available.

Expected manuscript use:

- Supplementary sensitivity.
- Discussion support for the claim that composting is undervalued by GWP100-only screening.

## Priority 4. Bio-CNG Methane Slip And Fuel-Substitution Sensitivity

Purpose:

- Make the bio-CNG result credible and not overconfident.

Current status:

- Central pathway assumes 97% methane recovery, 0.45 kWh/m3 raw biogas for upgrading/compression, and 0.074 kg CO2e/MJ biomethane diesel substitution.
- Bio-CNG stress test has been implemented.

Completed work:

- Added `scripts/run_bio_cng_stress_test.py`.
- Produced `data/processed/country_ofmsw_bio_cng_stress_test.csv`.
- Produced `outputs/summary_bio_cng_stress_test.csv`.
- Produced `outputs/summary_bio_cng_stress_best_counts.csv`.
- Documented results in `notes/bio_cng_stress_test_results.md`.
- Added bio-CNG stress-test tables to the Supplementary Information draft.

Remaining work:

- Replace stress-test ranges with literature-supported ranges before final submission.
- Consider country-specific transport-fuel displacement factors.

Expected manuscript use:

- Supplementary sensitivity.
- Main text caveat that AD-bio-CNG is high-potential but infrastructure- and assumption-sensitive.

## Priority 5. City-Level Validation Or Extension

Purpose:

- Strengthen urban relevance and increase credibility for Nature Sustainability and possible Nature Cities backup.

Current status:

- What a Waste 3.0 city dataset is downloaded but not yet integrated.
- First city-level OFMSW screen has been implemented.

Completed work:

- Added `scripts/build_city_ofmsw_screen.py`.
- Produced `data/processed/city_ofmsw_screen.csv`.
- Produced `outputs/summary_city_ofmsw_screen.csv`.
- Produced `outputs/top40_city_unmanaged_ofmsw.csv`.
- Produced `outputs/city_ofmsw_by_country_summary.csv`.
- Documented results in `notes/city_ofmsw_screen_results.md`.
- Added city-level validation table to the Supplementary Information draft.

Remaining work:

- Compare city hotspots with country-level pathway/readiness classes. Completed as first alignment screen.
- Add optional city figure or table if space allows.
- Validate treatment-share units and missingness city by city before detailed pathway modelling.

Expected manuscript use:

- Either a Supplementary validation layer or a short main-text paragraph.
- Could support an urban infrastructure transition framing.

## Priority 6. Final Figure Redesign

Purpose:

- Convert draft plots into Nature-style multi-panel figures.

Current status:

- All main figure components exist as standalone PNGs.

Needed work:

- Combine panels into four figure plates.
- Harmonize colors, labels and typography.
- Add map disclaimers and color-accessibility checks.
- Export high-resolution figures and editable source files.

Expected manuscript use:

- Main submission figures.

## Suggested Order

1. Optional city-country alignment figure.
2. Optional first-order decay timing sensitivity.
3. Final figure redesign.

GWP20, conservative nutrient-credit, bio-CNG stress-test, landfill capture, city-level screening and soil-carbon/humus justification have been completed. The remaining order gives the fastest improvement in scientific robustness before investing time in final artwork.
