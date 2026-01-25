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

# Récupère le chemin du fichier CSV
DATASET_PATH = Path(__file__).resolve().parents[2] / "dataset.csv"

# Créé un dossier artifacts dans le dossier courant
ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

# Chemin du modèle
MODEL_PATH = ARTIFACTS_DIR / "popularity_model.joblib"
# Chemin des caractéristiques du modèle
FEATURES_JSON_PATH = Path(__file__).resolve().parent / "feature_columns.json"

# Caractéristiques d'un fichier MP3
MP3_COMPAT_FEATURES = [
    "song_duration_ms",
    "tempo",
    "loudness",
    "key",
    "audio_mode",
    "time_signature",
]

def clamp_0_100(x: float) -> float:
    """
    Force une valeur à rester dans l'intervalle [0 ; 100].

    - x : entrée
    - retourne :
        - 0 si x < 0
        - 100 si x > 100
        - x sinon
    """
    return max(0.0, min(100.0, float(x)))

def logit_scaled_popularity(y: np.ndarray) -> np.ndarray:
    """
    Applique une transformation logit à des pourcentage.

    - y : tableau NumPy de valeurs dans l'intervalle [0 ; 100]
    - retourne : tableau NumPy de nombres réels
    """
    # Division par 100 pour obtenir une probabilité entre 0 et 1
    y01 = np.clip(y / 100.0, 1e-4, 1.0 - 1e-4)
    # Fonction logit permettant d'avoir n'importe quel nombre réel
    return np.log(y01 / (1.0 - y01))

def inv_logit_to_0_100(z: np.ndarray) -> np.ndarray:
    """
    Transforme des valeurs via la fonction sigmoïde en pourcentages [0 ; 100].

    - z : tableau NumPy de valeurs
    - retourne : tableau NumPy de nombres contenus entre 0 et 100
    """
    # Fonction sigmoïde permettant de retourner un nombre entre 0 et 1
    y01 = 1.0 / (1.0 + np.exp(-z))
    # Multiplication par 100 pour obtenir un pourcentage
    return np.clip(y01 * 100.0, 0.0, 100.0)


def main():
    # Lecture du fichier CSV
    df = pd.read_csv(DATASET_PATH)

    # Si la colonne "song_popularity" n'existe pas, lever une erreur
    if "song_popularity" not in df.columns:
        raise ValueError("dataset.csv doit contenir la colonne 'song_popularity'.")

    # Création d'un tableau contenant les caractéristiques d'un MP3 étant dans les colonnes du CSV
    feature_cols = [c for c in MP3_COMPAT_FEATURES if c in df.columns]
    # S'il y a moins de 3 éléments dans le tableau, lever une erreur
    if len(feature_cols) < 3:
        raise ValueError(
            f"Pas assez de colonnes MP3-compat dans dataset.csv. "
            f"Trouvées: {feature_cols}"
        )

    # Initialisation d'un DataFrame avec les caractéristiques
    X = df[feature_cols].copy()

    # Initialisation d'un DataFrame pour les popularités des chansons
    y_raw = df["song_popularity"].astype(float).to_numpy()

    # Entraînement sur 80% des données
    X_train, X_temp, y_train_raw, y_temp_raw = train_test_split(
        X, y_raw, test_size=0.20, random_state=42
    )
    # Tests et validation sur les 20% restantes 
    X_val, X_test, y_val_raw, y_test_raw = train_test_split(
        X_temp, y_temp_raw, test_size=0.50, random_state=42
    )

    # Prétraitement des caractéristiques
    preprocess = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]), feature_cols)
        ],
        remainder="drop"
    )

    # Création du modèle de base
    base_model = RandomForestRegressor(
        n_estimators=800,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=6,
        max_depth=18,
    )

    # Création du pipeline
    pipe = Pipeline([
        ("prep", preprocess),
        ("model", base_model),
    ])

    # Transforme les popularités en logit
    y_train = logit_scaled_popularity(y_train_raw)

    # Entraînement du pipeline
    pipe.fit(X_train, y_train)

    # Prédiction de validation (en logit)
    val_pred_z = pipe.predict(X_val)
    # Prédiction de validation (en probabilité entre 0 et 100)
    val_pred_0_100 = inv_logit_to_0_100(val_pred_z)

    # Création d'un isotone
    iso = IsotonicRegression(out_of_bounds="clip")
    # Ajustement des prédictions
    iso.fit(val_pred_0_100, y_val_raw)

    # Prédictions sur le test (en logit)
    test_pred_z = pipe.predict(X_test)
    # Prédictions sur le test (en probabilité entre 0 et 100)
    test_pred_0_100 = inv_logit_to_0_100(test_pred_z)
    # Calibration isotone
    test_pred_cal = iso.predict(test_pred_0_100)
    # Bornement des valeurs entre 0 et 100
    test_pred_cal = np.array([clamp_0_100(p) for p in test_pred_cal])

    print("=== Evaluation (MP3-compatible regression + calibration) ===")
    print("Features used:", feature_cols)
    print("MAE:", mean_absolute_error(y_test_raw, test_pred_cal))
    print("RMSE:", np.sqrt(mean_squared_error(y_test_raw, test_pred_cal)))
    print("R2:", r2_score(y_test_raw, test_pred_cal))

    # Création du modèle final
    bundle = {
        "pipeline": pipe,
        "calibrator": iso,
        "feature_cols": feature_cols,
        "target_transform": "logit_scaled_popularity_v1",
    }
    # Sauvegarde du modèle
    joblib.dump(bundle, MODEL_PATH)

    # Sauvegarde des caractéristiques
    with open(FEATURES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"Saved model bundle -> {MODEL_PATH}")
    print(f"Saved feature columns -> {FEATURES_JSON_PATH}")

# Lancement du main
if __name__ == "__main__":
    main()
