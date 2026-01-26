import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from app import create_app
from app.extensions import db
from app.models.song import Song
from app.models.analyze import Analyze

#chemins des fichiers nécessaires 
BASE_DIR = Path(__file__).resolve().parent / "app"
MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "popularity_model.joblib"
FEATURES_JSON_PATH = BASE_DIR / "ml" / "feature_columns.json"


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


def inv_logit_to_0_100(z: np.ndarray) -> np.ndarray:
    """
    Transforme des valeurs via la fonction sigmoïde en pourcentages [0 ; 100].

    - z : tableau NumPy de valeurs
    - retourne : tableau NumPy de nombres contenus entre 0 et 100
    """
    y01 = 1.0 / (1.0 + np.exp(-z))
    return np.clip(y01 * 100.0, 0.0, 100.0)


def build_row_from_song(song: Song, feature_cols: list[str]) -> pd.DataFrame:
    """
    Construit une ligne de DataFrame à partir d'une instance Song.

    - song : instance de Song
    - feature_cols : liste des noms de colonnes attendues
    - retourne : DataFrame avec une seule ligne contenant les caractéristiques de la chanson
    """
    # Récupération des caractéristiques d'une chanson
    feats = song.to_features_dict()
    row = {col: feats.get(col, None) for col in feature_cols}
    # Retourne le DataFrame avec toutes les données d'une chanson
    return pd.DataFrame([row])


def set_analyze_fields(analyze: Analyze, score_0_100: float) -> None:
    """
    Met à jour les champs de l'objet Analyze avec un score de popularité.

    - analyze : instance de Analyze à mettre à jour
    - score_0_100 : score de popularité entre 0 et 100
    """
    score_0_100 = clamp_0_100(score_0_100)

    # Si la table Analyze a "predicted_popularity", y insérer le score de popularité arrondie
    if hasattr(analyze, "predicted_popularity"):
        analyze.predicted_popularity = int(round(score_0_100))
    # Si la table Analyze a "popularity_probability", y insérer la popularité dans un intervalle [0 ; 1]
    elif hasattr(analyze, "popularity_probability"):
        analyze.popularity_probability = float(score_0_100 / 100.0)
    # Sinon, mettre une erreur
    else:
        raise AttributeError(
            "Analyze n'a ni 'predicted_popularity' ni 'popularity_probability'."
        )


def predict_score_0_100(model_bundle, X: pd.DataFrame) -> float:
    """
    Supporte:
    - ancien format: Pipeline sklearn -> predict directement (0..100)
    - nouveau format: dict bundle {pipeline, calibrator} avec sortie logit -> inverse logit -> calibrator
    """
    # Nouveau bundle
    if isinstance(model_bundle, dict) and "pipeline" in model_bundle:
        # Récupération du pipeline
        pipe = model_bundle["pipeline"]
        # Récupération du calibrateur s'il existe (None sinon)
        calibrator = model_bundle.get("calibrator", None)

        # Application du pipeline
        z = pipe.predict(X)  # logit
        raw = float(inv_logit_to_0_100(np.asarray(z))[0])

        # Vérification que le calibrateur n'est pas None
        if calibrator is not None:
            # Prédiction via le calibrateur
            cal = float(calibrator.predict([raw])[0])
            # Retour du score calibré
            return clamp_0_100(cal)

        # Si le calibrateur est nul, retour du score brut
        return clamp_0_100(raw)
    
    
    # Ancien format

    # Prédiction du score entre 0 et 100
    pred = float(model_bundle.predict(X)[0])
    # Retour du score
    return clamp_0_100(pred)


def main():
    # Création de l'application
    app = create_app()

    # Chargement du modèle
    model_bundle = joblib.load(MODEL_PATH)
    # Chargement des colonnes
    feature_cols = json.loads(FEATURES_JSON_PATH.read_text(encoding="utf-8"))

    # Limite le nombre de chansons traitées à 500
    PAGE_SIZE = 500

    # Active l'application
    with app.app_context():
        print("Backfill Analyze (create si absent / update sinon)")

        # Initialisation de l'identifiant de la page, du nombre de chansons traités, du nombre d'objets Analyze créés et du nombre d'objets Analyze mis à jour
        last_id = 0
        processed = created = updated = 0

        # Boucle tant qu'il reste des chansons à traiter
        while True:
            # Récupère les chansons suivant la dernière chanson traitée
            songs = (
                Song.query
                .filter(Song.is_in_data_set.is_(True), Song.song_id > last_id)
                .order_by(Song.song_id.asc())
                .limit(PAGE_SIZE)
                .all()
            )

            # S'il n'y a pas de chansons, arrêter la boucle
            if not songs:
                break

            # Boucle sur toutes les chansons récupérées
            for song in songs:
                # Transformation d'une chanson en DataFrame
                X = build_row_from_song(song, feature_cols)
                # Prédiction du score de popularité
                score = predict_score_0_100(model_bundle, X)

                # Récupération de l'analyse
                analyze = song.analyze
                # S'il n'y a aucune analyse
                if analyze is None:
                    # Création d'un nouvel objet Analyze
                    analyze = Analyze(id_song=song.song_id)
                    # Insertion de l'analyse dans la base de données
                    db.session.add(analyze)
                    # Incrémentation du nombre d'objets créés
                    created += 1
                # S'il y a une analyse, incrémente le nombre d'objets mis à jour
                else:
                    updated += 1

                # Mise à jour du score en fonction des colonnes présentes dans Analyze ("predicted_popularity" ou "popularity_probability")
                set_analyze_fields(analyze, score)

                # Incrémentation du nombre de chansons traitées
                processed += 1
                # Mise à jour du dernier identifiant
                last_id = song.song_id

            # Enregistrement de la base de données
            db.session.commit()
            print(
                f"Progress: processed={processed}, created={created}, updated={updated}, last_id={last_id}"
            )

        print(f"Done. processed={processed}, created={created}, updated={updated}")


if __name__ == "__main__":
    main()
