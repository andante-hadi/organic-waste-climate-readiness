# ecoinvent 3.12 Integration Protocol

## Purpose

Use ecoinvent 3.12 cutoff to replace generic screening assumptions for anaerobic digestion, composting, landfill/incineration background treatment, transport, electricity, and fertilizer substitution.

The study should report derived emission factors and methods, but should not redistribute proprietary ecoinvent unit-process inventory data.

## Confirmed Access

Access confirmed in Chrome through ecoQuery:

- URL: `ecoquery.ecoinvent.org/3.12/cutoff`
- System model: cutoff
- Version: 3.12

## Process Mapping File

Use:

`data/processed/ecoinvent_process_mapping_template.csv`

Fill in:

- `selected_process_name`
- `selected_reference_product`
- `unit`
- `target_geography`
- `notes`

## Priority Processes

### Anaerobic Digestion

Search ecoQuery for:

- `anaerobic digestion biowaste`
- `anaerobic digestion food waste`
- `treatment of biowaste by anaerobic digestion`
- `biogas electricity`

Needed factors:

- kg CO2e per tonne OFMSW treated.
- kWh electricity per tonne OFMSW, if energy recovery is modeled separately.
- methane leakage or direct CH4 emissions, if available.
- digestate output per tonne OFMSW, if available.

### Composting

Search ecoQuery for:

- `composting biowaste`
- `composting food waste`
- `green waste composting`
- `treatment of biowaste by composting`

Needed factors:

- kg CO2e per tonne OFMSW treated.
- direct CH4 and N2O emissions if available.
- compost output per tonne OFMSW, if available.

### Fertilizer Substitution

Search ecoQuery for:

- `market for nitrogen fertiliser`
- `urea`
- `ammonium nitrate`
- `market for phosphate fertiliser`
- `triple superphosphate`
- `market for potassium fertiliser`
- `potassium chloride`

Needed factors:

- kg CO2e per kg N.
- kg CO2e per kg P2O5 or P.
- kg CO2e per kg K2O or K.

### Baseline Treatment

Search ecoQuery for:

- `municipal solid waste landfill`
- `biowaste landfill`
- `sanitary landfill`
- `waste incineration`
- `municipal solid waste incineration`

Needed factors:

- kg CO2e per tonne treated, excluding or carefully separating methane if IPCC model is used separately.

### Transport

Search ecoQuery for:

- `transport freight lorry`
- `lorry 16-32 metric ton`
- `municipal waste collection`

Needed factors:

- kg CO2e per tonne-km.

## Recommended Extraction Table

Create:

`data/processed/ecoinvent_screening_factors.csv`

Suggested columns:

- `pathway`
- `factor_name`
- `ecoinvent_version`
- `system_model`
- `process_name`
- `reference_product`
- `geography`
- `unit`
- `value`
- `value_unit`
- `impact_method`
- `notes`

## Important Method Choice

For landfill methane, avoid double counting:

- Use IPCC first-order decay for landfill/dump methane.
- Use ecoinvent only for non-methane background burdens, or clearly document if ecoinvent landfill emissions are used instead.

## Reporting

In the manuscript:

- Cite ecoinvent 3.12 and the system model.
- Report selected process names and geographies in supplementary information.
- Report derived factors, not raw exchange-level inventory data.
- Run sensitivity tests across plausible process choices and geographies.
