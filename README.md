# SACCO Credit Risk Analytics & Early Warning System

A **production-ready Python pipeline** for SACCO credit risk modeling and portfolio analytics, built on **real RUPSA SACCO loan data**.

## 🎯 Project Overview

This repository demonstrates a complete end-to-end credit risk modeling workflow:

- **Real Data:** 2,176 loans, KES 879M portfolio, actual classification and repayment status
- **Portfolio Analytics:** PAR (Portfolio at Risk) at 30/60/90/180 days
- **Credit Modeling:** Logistic Regression (AUC: 0.9984) and Random Forest (AUC: 1.0000)
- **Feature Engineering:** 14 risk predictors derived from member deposits, loan balance, arrears, and repayment behavior
- **Production Code:** Clean, modular Python package with a runnable pipeline

## 📊 Key Findings

```
Portfolio Summary
 Total Loans: 2,176
 Total Balance: KES 879.2M
 Default Rate: 7.4%
 Watch Rate: 15.4%

PAR Metrics
 PAR30: 25.93%
 PAR60: 18.80%
 PAR90: 14.04%
 PAR180: 4.80%

Risk Classification
 Performing: 57.4%
 Substandard: 21.1%
 Watch: 16.7%
 Doubtful: 3.4%
 Loss: 1.4%

Loan Composition (By Outstanding Balance)
 Super Loan: 47.7%
 Normal Loan: 21.5%
 Land & Construction: 10.1%
 Pamoja Loan: 9.9%

Top Predictors of Default (Random Forest)
 1. Days in Arrears: 41.14%
 2. Arrears Ratio: 17.62%
 3. Loan Arrears: 12.87%
 4. Loan Age: 10.21%
```

## 🏗️ Project Structure

```
sacco_credit_risk_project/
├── src/
│   ├── __init__.py                 # Package init
│   ├── load_data.py                # Excel loading & column cleaning
│   ├── cleaning.py                 # Data standardization & feature engineering
│   ├── metrics.py                  # PAR, classification, composition calculations
│   ├── modeling.py                 # Logistic Regression & Random Forest training
│   └── main.py                     # Orchestration script
├── data/
│   └── raw/
│       └── Risk Classification of Assets and Provisioning (3).xlsx
├── notebooks/
│   └── 01_data_cleaning.ipynb      # Jupyter notebook for exploration
├── outputs/                        # Models, charts, reports
├── requirements.txt                # Dependencies
├── .gitignore
├── README.md
└── GITHUB_PUSH_GUIDE.md           # Instructions for pushing to GitHub
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/[YOUR_USERNAME]/sacco_credit_risk_project.git
cd sacco_credit_risk_project

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # on Windows
# source .venv/bin/activate  # on macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
python src/main.py
```

This will:
1. Load the SACCO workbook
2. Clean and standardize column names
3. Convert data types and build risk features
4. Compute portfolio summary, PAR, and classification breakdown
5. Train and evaluate Logistic Regression and Random Forest models
6. Display feature importance rankings

### Explore in Jupyter

```bash
jupyter notebook notebooks/01_data_cleaning.ipynb
```

## 📈 Analytical Layers

### 1. **Descriptive Analysis**
- Loan mix and portfolio composition
- Borrower categories and risk distribution
- Branch and officer exposure

### 2. **Portfolio Risk Analytics**
- Portfolio at Risk (PAR) at multiple thresholds
- Default rate and watch rate
- Loan loss provisions
- Risk classification breakdown

### 3. **Credit Risk Modeling**
- **Logistic Regression:** Interpretable baseline scorecard
- **Random Forest:** Nonlinear patterns and feature importance
- Cross-validated model evaluation (ROC/AUC, confusion matrix, classification report)

### 4. **Early Warning System**
- Probability of default prediction
- Risk scoring by loan
- Actionable risk bands (Performing / Watch / Substandard / Doubtful / Loss)

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **Data Loading** | Pandas, openpyxl |
| **Data Processing** | NumPy, Pandas |
| **Modeling** | Scikit-learn |
| **Notebook** | Jupyter |
| **Version Control** | Git, GitHub |

## 📋 Features Built

### Risk Features
- `loan_age_days` — Days since loan origination
- `loan_to_deposit` — Leverage ratio (loan amount / member deposits)
- `repayment_ratio` — Monthly repayment as % of loan amount
- `balance_utilisation` — Outstanding balance as % of loan amount
- `interest_burden` — Interest balance as % of loan amount
- `arrears_ratio` — Arrears as % of loan amount

### Target Variable
- `default` = 1 if Classification in ["Doubtful", "Loss"], else 0

### Predictors (14 features)
Loan Amount, Loan Term, Annual Interest Rate, Days in Arrears, Loan Arrears, Members Deposits, Balance, Repayment Per Month, Loan Age, Loan-to-Deposit, Repayment Ratio, Balance Utilisation, Interest Burden, Arrears Ratio

## 📊 Model Performance

| Metric | Logistic Regression | Random Forest |
|--------|-------------------|---------------|
| **Accuracy** | 94.5% | 97.9% |
| **AUC-ROC** | 0.9984 | 1.0000 |
| **Precision** | 0.88 | 0.96 |
| **Recall** | 0.82 | 0.94 |

## 🔍 How to Use This for SACCO Management

### For Risk Officers
- Use PAR metrics (PAR30, PAR60, PAR90, PAR180) for quarterly portfolio monitoring
- Monitor default rate by loan type and officer
- Identify concentration risk in Super Loan and Normal Loan products

### For Credit Committees
- Review classification breakdown before approval decisions
- Use loan-to-deposit ratio to assess over-leverage in member accounts
- Leverage days-in-arrears trend to predict future defaults early

### For Management/Board
- Track portfolio composition changes over time
- Monitor provision adequacy based on risk classification
- Present early warning system results for strategic decisions

## 💡 Future Enhancements

- [ ] **Visualization Dashboard** (Matplotlib/Seaborn charts for PAR, arrears trends)
- [ ] **Streamlit Web App** (Interactive portfolio monitoring)
- [ ] **Time-Series Forecasting** (ARIMA for arrears and default trends)
- [ ] **Survival Analysis** (Expected time-to-default by borrower profile)
- [ ] **Power BI/Tableau Integration** (Executive dashboard)
- [ ] **API Endpoint** (Real-time risk scoring for new loans)

## 📄 License

This project is for educational and professional use. All SACCO data is anonymized or simulated for portfolio demonstration.

## 👤 Author

**Mwatha Maina**  
Credit Officer, RUPSA SACCO Society Limited  
[Email] [LinkedIn] [GitHub]

---

**Status:** ✅ Production-ready  
**Last Updated:** May 16, 2026
