import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "popularity_model.joblib"
FEATURES_JSON_PATH = BASE_DIR / "ml" / "feature_columns.json"

_BUNDLE = joblib.load(MODEL_PATH)
FEATURES_ORDER = json.loads(FEATURES_JSON_PATH.read_text(encoding="utf-8"))


def _clamp_0_100(x: float) -> float:
    return max(0.0, min(100.0, float(x)))


def _inv_logit_to_0_100(z: np.ndarray) -> np.ndarray:
    y01 = 1.0 / (1.0 + np.exp(-z))
    return np.clip(y01 * 100.0, 0.0, 100.0)


def predict_popularity_score(features: dict) -> float:

    row = {col: features.get(col, None) for col in FEATURES_ORDER}
    X = pd.DataFrame([row])

    if isinstance(_BUNDLE, dict) and "pipeline" in _BUNDLE:
        pipe = _BUNDLE["pipeline"]
        calibrator = _BUNDLE.get("calibrator", None)


        z = pipe.predict(X)
        raw_score = _inv_logit_to_0_100(np.asarray(z))[0]

        if calibrator is not None:

            cal_score = float(calibrator.predict([raw_score])[0])
            return _clamp_0_100(cal_score)

        return _clamp_0_100(float(raw_score))


    y_pred = float(_BUNDLE.predict(X)[0])
    return _clamp_0_100(y_pred)
