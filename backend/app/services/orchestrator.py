from app.services.audio_service import AudioAnalysisService
from app.services.ml_predictor import predict_popularity_score
from app.extensions import db

_audio = AudioAnalysisService()

def score_audio_file(file_path: str, title: str | None = None, save_to_db: bool = False) -> dict:
    song = _audio.analyze_file(file_path, song_title=title)
    if song is None:
        return {"error": "analysis_failed"}

    features = song.to_features_dict()
    score = predict_popularity_score(features)

    if save_to_db:
        song.song_popularity = int(round(score))
        db.session.add(song)
        db.session.commit()

    return {
        "title": song.song_name,
        "predicted_popularity": round(score, 1),
    }
