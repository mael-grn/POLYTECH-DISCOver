import json
import joblib
import numpy as np
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "popularity_model.joblib"
FEATURES_JSON_PATH = BASE_DIR / "ml" / "feature_columns.json"

_MODEL_BUNDLE = None
_FEATURES_ORDER = None


def _load_bundle():
    global _MODEL_BUNDLE, _FEATURES_ORDER

    if _MODEL_BUNDLE is not None:
        return _MODEL_BUNDLE

    if not MODEL_PATH.exists():
        raise RuntimeError("Modèle ML introuvable. Lance train.py.")

    if MODEL_PATH.stat().st_size == 0:
        raise RuntimeError("Modèle ML vide ou corrompu.")

    _MODEL_BUNDLE = joblib.load(MODEL_PATH)
    _FEATURES_ORDER = json.loads(
        FEATURES_JSON_PATH.read_text(encoding="utf-8")
    )
    return _MODEL_BUNDLE


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
    y01 = 1.0 / (1.0 + np.exp(-z))
    return np.clip(y01 * 100.0, 0.0, 100.0)


def predict_popularity_score(features: dict) -> float:
    bundle = _load_bundle()

    row = {col: features.get(col, None) for col in _FEATURES_ORDER}
    X = pd.DataFrame([row])

    pipe = bundle["pipeline"]
    calibrator = bundle.get("calibrator")

    z = pipe.predict(X)
    raw_score = _inv_logit_to_0_100(np.asarray(z))[0]

    if calibrator is not None:
        raw_score = calibrator.predict([raw_score])[0]

    return _clamp_0_100(raw_score)
