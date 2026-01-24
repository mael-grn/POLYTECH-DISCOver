import json
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "popularity_model.joblib"
FEATURES_JSON_PATH = BASE_DIR / "ml" / "feature_columns.json"

_PIPE = joblib.load(MODEL_PATH)
FEATURES_ORDER = json.loads(FEATURES_JSON_PATH.read_text(encoding="utf-8"))

def predict_popularity_score(features: dict) -> float:
    row = {col: features.get(col, None) for col in FEATURES_ORDER}
    X = pd.DataFrame([row])
    y_pred = float(_PIPE.predict(X)[0])
    return max(0.0, min(100.0, y_pred))
