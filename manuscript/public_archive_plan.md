# Public Archive Plan

## Purpose

This note separates files that can be deposited publicly from files that should remain private because of licence constraints, especially ecoinvent.

## Archive-Ready Public Package

Recommended public archive contents:

- `README.md`
- `data_manifest.md`
- `scripts/`
- `manuscript/nature_sustainability_article_draft.md`
- `manuscript/supplementary_information_draft.md`
- `manuscript/references_draft.md`
- `manuscript/figures/`
- `outputs/`
- Public processed tables in `data/processed/`

## Public Data Inputs

These can generally be cited and, subject to their terms, archived or linked:

- What a Waste 3.0 country dataset
- What a Waste 3.0 city dataset
- World Development Indicators
- Ember electricity data
- Natural Earth country boundaries

For large public raw files, it may be cleaner to provide download instructions and checksums rather than re-archive the files.

## Files To Exclude From Public Archive

Exclude:

- `data/raw/ecoinvent_3_1_cutoff_ecospold02/`
- ecoinvent `.spold` files
- raw exchange-level ecoinvent inventory tables
- any exported ecoinvent database files
- screenshots or copied tables if they reproduce licensed ecoinvent content beyond derived factors

## ecoinvent-Derived Data That Can Be Reported

The manuscript and supplement may report:

- ecoinvent version
- system model
- selected process names
- reference products
- geographies
- units
- derived process-emission factors
- derived biogas-yield proxy
- derived nutrient-content values
- notes on how factors were calculated

The reporting should be limited to the factor values required for reproducibility and should avoid redistributing full proprietary inventory contents.

## Suggested Repository Layout For Submission

```text
README.md
data_manifest.md
data_dictionary.md
requirements.txt
data/
  processed/
  raw_public/
outputs/
scripts/
manuscript/
notes/
```

Where `data/raw_public/` contains only public datasets or pointers/checksums to public datasets. Licensed ecoinvent raw files should be replaced by a note explaining how licensed users can reproduce the derived factors.

## Files To Remove Before Public Archiving

Remove transient or private files before creating a public repository:

- `.DS_Store`
- `scripts/__pycache__/`
- `data/raw/ecoinvent_3_1_cutoff_ecospold02/`
- any `.spold`, `.zolca`, `.7z`, `.zip` or database-export files containing ecoinvent data
- local screenshots of ecoQuery tables where they reproduce licensed content
- browser downloads or personal-account metadata

## Public Package Manifest

Recommended minimum public package:

```text
README.md
data_manifest.md
data_dictionary.md
requirements.txt
scripts/
data/processed/
outputs/
manuscript/nature_sustainability_article_draft.md
manuscript/supplementary_information_draft.md
manuscript/references_draft.md
manuscript/nature_sustainability_figure_plan.md
manuscript/figures/
notes/first_pass_methane_assumptions.md
notes/ad_screening_assumptions.md
notes/bio_cng_screening_assumptions.md
notes/soil_carbon_humus_treatment.md
notes/ecoinvent_3_1_biogas_proxy.md
notes/ecoinvent_extraction_log.md
```

Raw public data can be included only where terms permit redistribution. Otherwise, provide download links and scripts or instructions to rebuild the processed tables.

## Reproduction Levels

Because ecoinvent is licensed, the archive should describe two reproduction levels:

1. **Open reproduction:** uses public datasets, processed derived-factor tables and scripts to reproduce all reported screening results.
2. **Licensed reproduction:** allows ecoinvent users to verify or update derived process factors from their licensed database access.

This distinction should be stated clearly in the README and data availability statement.

## Data Availability Text

Public input datasets, processed country-level outputs and analysis scripts will be deposited in a public repository upon submission or publication. The study also uses licensed ecoinvent-derived parameters. Raw ecoinvent source files and exchange-level inventory data cannot be redistributed; the manuscript and Supplementary Information report the selected processes, system model, geographies and derived factors needed to understand and reproduce the screening model by licensed users.

## Code Availability Text

All scripts used for data harmonization, methane screening, pathway comparison, uncertainty analysis, readiness classification and figure generation will be deposited in a public repository. The code is designed to run from the repository root and uses processed public inputs plus licence-compliant derived ecoinvent factors. Proprietary ecoinvent source files are excluded from the public code archive.

## Licence Note For Repository

Use an open-source licence for code, such as MIT or BSD-3-Clause, and a separate data-use note explaining that third-party data remain subject to their original terms. Do not apply an open data licence to ecoinvent-derived source material or any file that could be interpreted as redistributing proprietary inventory data.
