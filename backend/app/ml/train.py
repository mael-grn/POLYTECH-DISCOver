import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import numpy as np


DATASET_PATH = Path(__file__).resolve().parents[2] / "dataset.csv"

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = ARTIFACTS_DIR / "popularity_model.joblib"
FEATURES_JSON_PATH = Path(__file__).resolve().parent / "feature_columns.json"


def clamp_0_100(x: float) -> float:
    return max(0.0, min(100.0, float(x)))


def main():
    df = pd.read_csv(DATASET_PATH)

    if "song_popularity" not in df.columns:
        raise ValueError("dataset.csv doit contenir la colonne 'song_popularity'.")

    # Target régression
    y = df["song_popularity"].astype(float)

    # Features : on enlève la cible et le nom si présent
    drop_cols = [c for c in ["song_popularity", "song_name"] if c in df.columns]
    X = df.drop(columns=drop_cols)

    # On garde uniquement les colonnes numériques
    X = X.select_dtypes(include=["number"])
    feature_cols = X.columns.tolist()

    if len(feature_cols) == 0:
        raise ValueError("Aucune colonne numérique trouvée pour entraîner le modèle.")

    # Split 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    preprocess = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]), feature_cols)
        ],
        remainder="drop"
    )

    # Modèle régression robuste
    model = RandomForestRegressor(
        n_estimators=600,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=2
    )

    pipe = Pipeline([
        ("prep", preprocess),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)

    pred = pipe.predict(X_test)
    pred_clamped = [clamp_0_100(p) for p in pred]

    print("=== Evaluation (Regression) ===")
    print("MAE:", mean_absolute_error(y_test, pred_clamped))
    rmse = np.sqrt(mean_squared_error(y_test, pred_clamped))
    print("RMSE:", rmse)
    print("R2:", r2_score(y_test, pred_clamped))

    # Sauvegarde
    joblib.dump(pipe, MODEL_PATH)
    with open(FEATURES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"Saved model -> {MODEL_PATH}")
    print(f"Saved feature columns -> {FEATURES_JSON_PATH}")


if __name__ == "__main__":
    main()
