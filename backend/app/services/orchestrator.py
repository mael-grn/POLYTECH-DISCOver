from app.services.audio_service import AudioAnalysisService
from app.services.ml_predictor import predict_popularity_score
from app.extensions import db

_audio = AudioAnalysisService() #création d'une instance du service d'analyse audio

def score_audio_file(file_path: str, title: str | None = None, save_to_db: bool = False) -> dict:
    song = _audio.analyze_file(file_path, song_title=title) #analyse du fichier audio pour extraire les caractéristiques
    if song is None:
        return {"error": "analysis_failed"}

    features = song.to_features_dict()          #conversion des caractéristiques extraites en dictionnaire
    score = predict_popularity_score(features)  #prédiction du score de popularité à partir des caractéristiques

    if save_to_db:                               #si demandé, sauvegarde du morceau et de son score dans la base de données
        song.song_popularity = int(round(score)) #mise à jour de la popularité du morceau
        db.session.add(song)                     #ajout du morceau à la session de la base de données
        db.session.commit()                      #validation des changements dans la base de données

    return {                                     #retourne le titre du morceau et son score prédit
        "title": song.song_name,
        "predicted_popularity": round(score, 1),
    }
