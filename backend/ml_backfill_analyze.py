import json
from pathlib import Path

import joblib
import pandas as pd

from app import create_app
from app.extensions import db
from app.models.song import Song
from app.models.analyze import Analyze

BASE_DIR = Path(__file__).resolve().parent / "app"
MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "popularity_model.joblib"
FEATURES_JSON_PATH = BASE_DIR / "ml" / "feature_columns.json"


def clamp_0_100(x: float) -> float:
    return max(0.0, min(100.0, float(x)))


def build_row_from_song(song: Song, feature_cols: list[str]) -> pd.DataFrame:
    feats = song.to_features_dict()
    row = {col: feats.get(col, None) for col in feature_cols}
    return pd.DataFrame([row])


def set_analyze_fields(analyze: Analyze, score_0_100: float) -> None:
    score_0_100 = clamp_0_100(score_0_100)

    if hasattr(analyze, "predicted_popularity"):
        analyze.predicted_popularity = int(round(score_0_100))
    elif hasattr(analyze, "popularity_probability"):
        analyze.popularity_probability = float(score_0_100 / 100.0)
    else:
        raise AttributeError(
            "Analyze n'a ni 'predicted_popularity' ni 'popularity_probability'."
        )


def main():
    app = create_app()
    pipe = joblib.load(MODEL_PATH)
    feature_cols = json.loads(FEATURES_JSON_PATH.read_text(encoding="utf-8"))

    PAGE_SIZE = 500

    with app.app_context():
        print("Backfill Analyze (pagination par song_id)")

        last_id = 0
        processed = created = updated = 0

        while True:
            # récupère une page stable d’IDs
            songs = (
                Song.query
                .filter(Song.is_in_data_set.is_(True), Song.song_id > last_id)
                .order_by(Song.song_id.asc())
                .limit(PAGE_SIZE)
                .all()
            )

            if not songs:
                break

            for song in songs:
                X = build_row_from_song(song, feature_cols)
                score = float(pipe.predict(X)[0])
                score = clamp_0_100(score)

                analyze = song.analyze
                if analyze is None:
                    analyze = Analyze(id_song=song.song_id)
                    db.session.add(analyze)
                    created += 1
                else:
                    updated += 1

                set_analyze_fields(analyze, score)

                processed += 1
                last_id = song.song_id

            db.session.commit()
            print(f"Progress: processed={processed}, created={created}, updated={updated}, last_id={last_id}")

        print(f"Done. processed={processed}, created={created}, updated={updated}")


if __name__ == "__main__":
    main()
