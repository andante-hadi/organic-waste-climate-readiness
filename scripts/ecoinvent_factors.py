from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FACTORS_FILE = ROOT / "data" / "processed" / "ecoinvent_screening_factors.csv"


def load_factor_value(pathway: str, factor_name: str, default: float) -> tuple[float, str]:
    """Return an ecoinvent factor when the factor table has a numeric value."""
    if not FACTORS_FILE.exists():
        return default, "generic_screening_default"

    factors = pd.read_csv(FACTORS_FILE)
    matches = factors[
        (factors["pathway"] == pathway)
        & (factors["factor_name"] == factor_name)
    ]
    if matches.empty:
        return default, "generic_screening_default"

    value = pd.to_numeric(matches.iloc[0]["value"], errors="coerce")
    if pd.isna(value):
        return default, "generic_screening_default"

    row = matches.iloc[0]
    version = str(row.get("ecoinvent_version", "")).strip()
    system_model = str(row.get("system_model", "")).strip()
    impact_method = str(row.get("impact_method", "")).strip()
    source_parts = ["ecoinvent"]
    if version:
        source_parts.append(version)
    if system_model:
        source_parts.append(system_model)
    if impact_method:
        source_parts.append(impact_method)
    return float(value), "_".join(source_parts).replace(" ", "_")
