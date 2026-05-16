# SACCO Credit Risk Analytics & Early Warning System

This project is a GitHub-ready SACCO credit risk analytics system built from your real RUPSA SACCO loan monitoring workbook.

## What is included

- Data loading and cleaning for the actual SACCO Excel file
- Feature engineering for credit risk and portfolio analytics
- PAR calculation and portfolio composition analysis
- Logistic Regression and Random Forest modeling
- Decision-ready metrics for Portfolio at Risk, risk classification, and loan concentration

## Project structure

```
sacco_credit_risk_project/
├── data/
│   ├── raw/
│   │   └── Risk Classification of Assets and Provisioning (3).xlsx
├── notebooks/
│   └── 01_data_cleaning.md
├── outputs/
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    ├── load_data.py
    ├── cleaning.py
    ├── metrics.py
    ├── modeling.py
    └── main.py
```

## How to use

1. Place the workbook `Risk Classification of Assets and Provisioning (3).xlsx` into `data/raw/`.
2. Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the analysis:

```bash
python src/main.py
```

## Why this approach is better

This project is grounded in your actual SACCO dataset and the real workbook structure. It is not a simulated example. The code is designed to:

- use the actual sheet name and header row from your workbook
- standardize the real SACCO column labels
- compute PAR and risk classification from actual balance and arrears fields
- build models using real operational features such as loan amount, arrears, balance, deposit exposure, and interest burden

That makes this repository ready for GitHub and directly usable in your credit officer workflow.
