import numpy as np
import pandas as pd


def standardize_sacco_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.rename(columns={
        "Classification": "Classification",
        "Classification ": "Classification",
        "Date _Loan Given": "Date_Loan_Given",
    })
    df = df.loc[df["Member_No"].notna()]
    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        "Loan_Amount",
        "Repayment_Per_Month",
        "Loan_Term",
        "Balance",
        "Loan_Balance_Expected",
        "Actual_Balance",
        "Expected_Interest_Paid",
        "Interest_balance",
        "Latest_Amount_Paid",
        "Loan_Arrears",
        "Days_in_Arrears",
        "Annual_pct_Rate",
        "Loan_Loss_Provision_Amount",
        "Members_Deposits",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Date_Loan_Given" in df.columns:
        df["Date_Loan_Given"] = pd.to_datetime(df["Date_Loan_Given"], errors="coerce")

    return df


def build_risk_features(df: pd.DataFrame, reference_date=None) -> pd.DataFrame:
    df = df.copy()
    if reference_date is None:
        reference_date = pd.Timestamp.today()

    df["Classification"] = df["Classification"].astype(str).str.strip()
    df["default"] = np.where(df["Classification"].isin(["Doubtful", "Loss"]), 1, 0)
    df["watch"] = np.where(df["Classification"] == "Watch", 1, 0)
    df["loan_type"] = df["Loan_Name"].fillna("Unknown")
    df["loan_age_days"] = (reference_date - df["Date_Loan_Given"]).dt.days.clip(lower=0)

    df["loan_to_deposit"] = np.where(
        df["Members_Deposits"] > 0,
        df["Loan_Amount"] / df["Members_Deposits"],
        np.nan,
    )
    df["repayment_ratio"] = df["Repayment_Per_Month"] / df["Loan_Amount"].replace(0, np.nan)
    df["balance_utilisation"] = df["Balance"] / df["Loan_Amount"].replace(0, np.nan)
    df["interest_burden"] = df["Interest_balance"].fillna(0) / df["Loan_Amount"].replace(0, np.nan)
    df["arrears_ratio"] = df["Loan_Arrears"].fillna(0) / df["Loan_Amount"].replace(0, np.nan)

    df["loan_term_bucket"] = pd.cut(
        df["Loan_Term"].fillna(0),
        bins=[-1, 1, 12, 36, 63, 999],
        labels=["flash", "short", "medium", "long", "very_long"],
    )

    return df


def prepare_model_data(df: pd.DataFrame):
    df = df.copy()
    features = [
        "Loan_Amount",
        "Loan_Term",
        "Annual_pct_Rate",
        "Days_in_Arrears",
        "Loan_Arrears",
        "Members_Deposits",
        "Balance",
        "Repayment_Per_Month",
        "loan_age_days",
        "loan_to_deposit",
        "repayment_ratio",
        "balance_utilisation",
        "interest_burden",
        "arrears_ratio",
    ]
    if "loan_type" in df.columns:
        df["loan_type_enc"] = pd.factorize(df["loan_type"])[0]
        features.append("loan_type_enc")
    return df, features
