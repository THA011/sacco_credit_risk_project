from pathlib import Path
import pandas as pd


import re

def clean_column_names(columns):
    def clean(c):
        if c is None:
            return c
        name = str(c).strip()
        name = name.replace("\n", " ")
        name = re.sub(r"\s+", " ", name)
        name = name.strip()
        name = name.replace(" ", "_")
        name = name.replace("%", "pct")
        name = re.sub(r"_+", "_", name)
        return name

    return [clean(c) for c in columns]


def load_sacco_excel(path: Path = None):
    """Load the SACCO loan workbook from a raw Excel file."""
    if path is None:
        path = Path(__file__).resolve().parents[1] / "data" / "raw" / "Risk Classification of Assets and Provisioning (3).xlsx"

    if not path.exists():
        raise FileNotFoundError(f"Expected raw data file at: {path}")

    sheet_name = "Risk Classification of Assets a"
    df = pd.read_excel(path, sheet_name=sheet_name, header=14, engine="openpyxl")
    df.columns = clean_column_names(df.columns)
    return df


def load_and_preview(path: Path = None, rows: int = 10):
    """Return a preview of the loaded SACCO workbook."""
    df = load_sacco_excel(path)
    return df.head(rows)
