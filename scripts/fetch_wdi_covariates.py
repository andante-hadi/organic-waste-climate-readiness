from pathlib import Path
import json
from urllib.request import urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

OUTPUT_RAW = RAW / "wdi_2022_covariates.csv"
OUTPUT_PROCESSED = PROCESSED / "wdi_2022_covariates.csv"

INDICATORS = {
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd_2022",
    "NY.GDP.MKTP.CD": "gdp_current_usd_2022",
    "SP.POP.TOTL": "population_wdi_2022",
    "SP.URB.TOTL.IN.ZS": "urban_population_pct_2022",
}


def fetch_indicator(indicator: str) -> pd.DataFrame:
    url = (
        "https://api.worldbank.org/v2/country/all/indicator/"
        f"{indicator}?format=json&per_page=20000&date=2022"
    )
    with urlopen(url, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if len(payload) < 2:
        raise RuntimeError(f"No data returned for {indicator}")
    rows = []
    for item in payload[1]:
        country = item.get("country", {})
        rows.append(
            {
                "iso3": item.get("countryiso3code"),
                "country_wdi": country.get("value"),
                "indicator": indicator,
                "value": item.get("value"),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    frames = [fetch_indicator(indicator) for indicator in INDICATORS]
    long = pd.concat(frames, ignore_index=True)
    long.to_csv(OUTPUT_RAW, index=False)

    wide = (
        long.pivot_table(index=["iso3", "country_wdi"], columns="indicator", values="value", aggfunc="first")
        .reset_index()
        .rename(columns=INDICATORS)
    )
    wide = wide[wide["iso3"].astype(str).str.len() == 3].copy()
    wide.to_csv(OUTPUT_PROCESSED, index=False)

    print(f"Wrote {OUTPUT_PROCESSED}")
    print(f"Countries/economies with WDI rows: {len(wide)}")


if __name__ == "__main__":
    main()
