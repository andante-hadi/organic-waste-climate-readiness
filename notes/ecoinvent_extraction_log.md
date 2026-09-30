# ecoinvent Extraction Log

Date: 2026-05-22

## Access

ecoQuery access was confirmed in the user's Chrome session for:

- ecoinvent version: 3.12
- system model: cutoff
- URL family: `ecoquery.ecoinvent.org/3.12/cutoff`

No credentials were copied or stored.

## Confirmed Process Matches

### Anaerobic Digestion

Search term used in ecoQuery:

- `anaerobic digestion biowaste`

Confirmed activity:

- `treatment of biowaste by anaerobic digestion`

Confirmed datasets visible in ecoQuery:

- Reference product `biowaste`, unit `kg`, geography `RoW`, dataset ID 15839.
- Reference product `biowaste`, unit `kg`, geography `CH`, dataset ID 14988.
- Reference product `biogas`, unit `m3`, geography `RoW`, dataset ID 14935.
- Reference product `biogas`, unit `m3`, geography `CH`, dataset ID 15343.

Current mapping choice:

- Use the RoW `biowaste` treatment dataset as the global default for AD treatment.
- Use the CH dataset as a sensitivity case.
- Treat the `biogas` reference-product datasets carefully to avoid double counting with allocated treatment burdens.

The mapping table has been updated in `data/processed/ecoinvent_process_mapping_template.csv`.

## Pending Process Searches

The following process families still need confirmation in ecoQuery before LCA factors are entered:

- Composting of biowaste or food/green waste.
- Mineral fertilizer markets for N, P, and K substitution.
- Baseline landfill and incineration treatment processes.
- Waste transport or freight lorry process for tonne-km sensitivity.
- Optional ecoinvent electricity market processes as a sensitivity to Ember grid intensity.

## Browser Note

After the AD search, the direct ecoQuery search URL for `treatment of biowaste by composting` loaded as a blank pink page in Chrome. The browser session still appeared logged in, but the page body did not render process results. Because ecoinvent is licensed data, no process names or factors should be guessed. Composting and the remaining process rows should be extracted from a functioning ecoQuery page or directly from the licensed ecoinvent database tools available to the user.

## Data Handling Rule

For publication and repository sharing:

- OK to report selected process names, reference products, geographies, system model, and derived impact factors.
- Do not redistribute proprietary exchange-level inventory tables from ecoinvent.
