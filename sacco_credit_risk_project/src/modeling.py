import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def train_models(df, features, target="default"):
    X = df[features].copy()
    y = df[target].copy()

    X = X.fillna(X.median())
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y if len(y.unique()) > 1 else None
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    lr.fit(X_train_scaled, y_train)

    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    lr_probs = lr.predict_proba(X_test_scaled)[:, 1]
    rf_probs = rf.predict_proba(X_test)[:, 1]

    results = {
        "lr": {
            "model": lr,
            "score": lr.score(X_test_scaled, y_test),
            "auc": roc_auc_score(y_test, lr_probs),
            "report": classification_report(y_test, lr.predict(X_test_scaled), output_dict=True),
        },
        "rf": {
            "model": rf,
            "score": rf.score(X_test, y_test),
            "auc": roc_auc_score(y_test, rf_probs),
            "report": classification_report(y_test, rf.predict(X_test), output_dict=True),
        },
        "feature_importance": dict(zip(features, rf.feature_importances_)),
    }
    return results


def best_features(results, top_n=10):
    importance = results.get("feature_importance", {})
    return sorted(importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
