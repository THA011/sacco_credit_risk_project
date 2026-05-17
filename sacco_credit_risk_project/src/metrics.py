import pandas as pd


def portfolio_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "total_loans": [len(df)],
        "total_balance": [df["Balance"].sum()],
        "average_loan_amount": [df["Loan_Amount"].mean()],
        "default_rate": [df["default"].mean()],
        "watch_rate": [df["watch"].mean()],
    })


def par_metrics(df: pd.DataFrame) -> dict:
    total_balance = df["Balance"].sum()
    return {
        "PAR30": df.loc[df["Days_in_Arrears"] > 30, "Balance"].sum() / total_balance if total_balance else 0,
        "PAR60": df.loc[df["Days_in_Arrears"] > 60, "Balance"].sum() / total_balance if total_balance else 0,
        "PAR90": df.loc[df["Days_in_Arrears"] > 90, "Balance"].sum() / total_balance if total_balance else 0,
        "PAR180": df.loc[df["Days_in_Arrears"] > 180, "Balance"].sum() / total_balance if total_balance else 0,
    }


def classification_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Classification")
          .agg(
              loans=("Member_No", "count"),
              balance=("Balance", "sum")
          )
          .assign(pct_of_portfolio=lambda x: x["balance"] / x["balance"].sum())
          .sort_values(by="balance", ascending=False)
    )


def loan_composition(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Loan_Name")
          .agg(
              loans=("Member_No", "count"),
              balance=("Balance", "sum")
          )
          .assign(pct_of_portfolio=lambda x: x["balance"] / x["balance"].sum())
          .sort_values(by="balance", ascending=False)
    )
