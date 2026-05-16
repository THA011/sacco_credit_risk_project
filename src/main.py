from pathlib import Path
from src.load_data import load_sacco_excel
from src.cleaning import convert_types, standardize_sacco_data, build_risk_features, prepare_model_data
from src.metrics import portfolio_summary, par_metrics, classification_breakdown, loan_composition
from src.modeling import train_models, best_features


def main():
    base = Path(__file__).resolve().parents[1]
    raw_file = base / "data" / "raw" / "Risk Classification of Assets and Provisioning (3).xlsx"

    if not raw_file.exists():
        raise FileNotFoundError(
            f"Raw Excel file not found. Copy the workbook to: {raw_file}"
        )

    df = load_sacco_excel(raw_file)
    df = standardize_sacco_data(df)
    df = convert_types(df)
    df = build_risk_features(df)

    df = df.loc[df["Member_No"].notna() & df["Loan_Name"].notna()]

    summary = portfolio_summary(df)
    pars = par_metrics(df)
    classification = classification_breakdown(df)
    composition = loan_composition(df)

    df, features = prepare_model_data(df)
    model_results = train_models(df, features, target="default")

    print("\n=== Portfolio Summary ===")
    print(summary.to_string(index=False))

    print("\n=== PAR Metrics ===")
    for key, value in pars.items():
        print(f"{key}: {value:.2%}")

    print("\n=== Classification Breakdown ===")
    print(classification.to_string())

    print("\n=== Loan Composition ===")
    print(composition.to_string())

    print("\n=== Model Results ===")
    print(f"Logistic Regression AUC: {model_results['lr']['auc']:.4f}")
    print(f"Random Forest AUC:       {model_results['rf']['auc']:.4f}")

    print("\n=== Top Features (RF) ===")
    for feature, score in best_features(model_results, top_n=10):
        print(f"{feature}: {score:.4f}")


if __name__ == "__main__":
    main()
