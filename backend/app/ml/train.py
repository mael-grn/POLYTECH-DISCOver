import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.isotonic import IsotonicRegression


DATASET_PATH = Path(__file__).resolve().parents[2] / "dataset.csv"

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = ARTIFACTS_DIR / "popularity_model.joblib"
FEATURES_JSON_PATH = Path(__file__).resolve().parent / "feature_columns.json"



MP3_COMPAT_FEATURES = [
    "song_duration_ms",
    "tempo",
    "loudness",
    "key",
    "audio_mode",
    "time_signature",
]


def clamp_0_100(x: float) -> float:
    return max(0.0, min(100.0, float(x)))


def logit_scaled_popularity(y: np.ndarray) -> np.ndarray:
    y01 = np.clip(y / 100.0, 1e-4, 1.0 - 1e-4)
    return np.log(y01 / (1.0 - y01))


def inv_logit_to_0_100(z: np.ndarray) -> np.ndarray:
    y01 = 1.0 / (1.0 + np.exp(-z))
    return np.clip(y01 * 100.0, 0.0, 100.0)


def main():
    df = pd.read_csv(DATASET_PATH)

    if "song_popularity" not in df.columns:
        raise ValueError("dataset.csv doit contenir la colonne 'song_popularity'.")

    feature_cols = [c for c in MP3_COMPAT_FEATURES if c in df.columns]
    if len(feature_cols) < 3:
        raise ValueError(
            f"Pas assez de colonnes MP3-compat dans dataset.csv. "
            f"Trouvées: {feature_cols}"
        )


    X = df[feature_cols].copy()


    y_raw = df["song_popularity"].astype(float).to_numpy()

    X_train, X_temp, y_train_raw, y_temp_raw = train_test_split(
        X, y_raw, test_size=0.20, random_state=42
    )
    X_val, X_test, y_val_raw, y_test_raw = train_test_split(
        X_temp, y_temp_raw, test_size=0.50, random_state=42
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

    base_model = RandomForestRegressor(
        n_estimators=800,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=6,
        max_depth=18,
    )

    pipe = Pipeline([
        ("prep", preprocess),
        ("model", base_model),
    ])


    y_train = logit_scaled_popularity(y_train_raw)

    pipe.fit(X_train, y_train)


    val_pred_z = pipe.predict(X_val)
    val_pred_0_100 = inv_logit_to_0_100(val_pred_z)


    iso = IsotonicRegression(out_of_bounds="clip")
    iso.fit(val_pred_0_100, y_val_raw)


    test_pred_z = pipe.predict(X_test)
    test_pred_0_100 = inv_logit_to_0_100(test_pred_z)
    test_pred_cal = iso.predict(test_pred_0_100)
    test_pred_cal = np.array([clamp_0_100(p) for p in test_pred_cal])

    print("=== Evaluation (MP3-compatible regression + calibration) ===")
    print("Features used:", feature_cols)
    print("MAE:", mean_absolute_error(y_test_raw, test_pred_cal))
    print("RMSE:", np.sqrt(mean_squared_error(y_test_raw, test_pred_cal)))
    print("R2:", r2_score(y_test_raw, test_pred_cal))


    bundle = {
        "pipeline": pipe,
        "calibrator": iso,
        "feature_cols": feature_cols,
        "target_transform": "logit_scaled_popularity_v1",
    }
    joblib.dump(bundle, MODEL_PATH)

    with open(FEATURES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"Saved model bundle -> {MODEL_PATH}")
    print(f"Saved feature columns -> {FEATURES_JSON_PATH}")


if __name__ == "__main__":
    main()
