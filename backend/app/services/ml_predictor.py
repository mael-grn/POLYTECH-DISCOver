import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# Chemin du dossier app
BASE_DIR = Path(__file__).resolve().parents[1]
# Chemin du modèle
MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "popularity_model.joblib"
# Chemin du fichier JSON contenant les colonnes utilisées par le modèle
FEATURES_JSON_PATH = BASE_DIR / "ml" / "feature_columns.json"

_BUNDLE = joblib.load(MODEL_PATH)
FEATURES_ORDER = json.loads(FEATURES_JSON_PATH.read_text(encoding="utf-8"))

def _clamp_0_100(x: float) -> float:
    """
    Force une valeur à rester dans l'intervalle [0 ; 100].

    - x : entrée
    - retourne :
        - 0 si x < 0
        - 100 si x > 100
        - x sinon
    """
    return max(0.0, min(100.0, float(x)))

def _inv_logit_to_0_100(z: np.ndarray) -> np.ndarray:
    """
    Transforme des valeurs via la fonction sigmoïde en pourcentages [0 ; 100].

    - z : tableau NumPy de valeurs
    - retourne : tableau NumPy de nombres contenus entre 0 et 100
    """
    # Fonction sigmoïde permettant de retourner un nombre entre 0 et 1
    y01 = 1.0 / (1.0 + np.exp(-z))
    # Multiplication par 100 pour obtenir un pourcentage
    return np.clip(y01 * 100.0, 0.0, 100.0)

# Prédiction d'un score de popularité
def predict_popularity_score(features: dict) -> float:
    # Récupération des caractéristiques
    row = {col: features.get(col, None) for col in FEATURES_ORDER}
    # Création du DataFrame des caractéristiques
    X = pd.DataFrame([row])

    # Nouveau bundle
    if isinstance(_BUNDLE, dict) and "pipeline" in _BUNDLE:
        # Récupération du pipeline
        pipe = _BUNDLE["pipeline"]
        # Récupération du calibrateur s'il existe (None sinon)
        calibrator = _BUNDLE.get("calibrator", None)

        # Application du pipeline
        z = pipe.predict(X)
        # Transformation du logit entre 0 et 100
        raw_score = _inv_logit_to_0_100(np.asarray(z))[0]
        
        # Vérification que le calibrateur n'est pas None
        if calibrator is not None:
            # Prédiction via le calibrateur
            cal_score = float(calibrator.predict([raw_score])[0])
            # Retour du score calibré
            return _clamp_0_100(cal_score)
        # Si le calibrateur est nul, retour du score brut
        return _clamp_0_100(float(raw_score))

    # Ancien format

    # Prédiction du score entre 0 et 100
    y_pred = float(_BUNDLE.predict(X)[0])
    # Retour du score
    return _clamp_0_100(y_pred)
