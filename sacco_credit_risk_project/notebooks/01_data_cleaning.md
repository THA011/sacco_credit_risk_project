# 01 Data Cleaning & Review

This notebook describes the first project step for SACCO credit risk analytics.

## Goals

- Load the real SACCO workbook
- Standardize and clean column names
- Convert dates and numeric fields
- Create risk features for PAR and modeling

## Example workflow

```python
from src.load_data import load_sacco_excel
from src.cleaning import standardize_sacco_data, convert_types, build_risk_features

raw = load_sacco_excel()
df = standardize_sacco_data(raw)
df = convert_types(df)
df = build_risk_features(df)

print(df.columns)
print(df.head())
```

## Notes

- The workbook should be placed in `data/raw/`
- The sheet name is `Risk Classification of Assets a`
- The header row begins at row 15 in the Excel workbook
