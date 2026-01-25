from app.services.audio_service import AudioAnalysisService
from app.services.ml_predictor import predict_popularity_score
from app.extensions import db

# Récupération du service d'analyse d'audio
_audio = AudioAnalysisService()

# Calcul du score de popularité d'un fichier audio
def score_audio_file(file_path: str, title: str | None = None, save_to_db: bool = False) -> dict:
    """
    Analyse d'un fichier audio et prédiction de sa popularité.

    - file_path : chemin vers le fichier audio à analyser
    - title : nom de la chanson à utiliser
    - save_to_db : Indique si la chanson et son score doivent être sauvegardés dans la base de données
    - retourne:
        - dictionnaire contenant :
            - "title" : le nom de la chanson
            - "predicted_popularity" : popularité prédite entre 0 et 100
            - "error" : présent si l'analyse audio a échoué
    """
    # Analyse de la chanson
    song = _audio.analyze_file(file_path, song_title=title)
    # Si la chanson n'est pas présente, renvoyer une erreur
    if song is None:
        return {"error": "analysis_failed"}

    # Récupération des caractéristiques de la chanson
    features = song.to_features_dict()
    # Prédiction du score de popularité via les caractéristiques
    score = predict_popularity_score(features)

    # S'il faut sauvegarder dans la base de données
    if save_to_db:
        # Récupération du score de popularité
        song.song_popularity = int(round(score))
        # Ajout de la chanson
        db.session.add(song)
        # Enregistrement des modifications
        db.session.commit()

    # Retour du titre et de la popularité
    return {
        "title": song.song_name,
        "predicted_popularity": round(score, 1),
    }
