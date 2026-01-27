from sqlalchemy.orm import Session
from app.models.analyze import Analyze
from app.models.song import Song
from app.models.uploaded_by import UploadedBy
def upsert_analyze_for_song(session: Session, *, song_id: int, score_0_100: float) -> Analyze:
    """
    Création ou mise à jour de l'analyse d'une chanson avec un score de popularité.

    - session : instance SQLAlchemy Session
    - song_id : identifiant de la chanson à analyser
    - score_0_100 : score de popularité
    - retourne :
        - l'objet Analyze correspondant à la chanson, créé ou mis à jour
    - exceptions :
        - AttributeError si l'objet Analyze ne contient ni "predicted_popularity" ni "popularity_probability"
    """
    # Recherche si l'analyse d'une certaine chanson existe
    analyze = session.query(Analyze).filter_by(id_song=song_id).first()
    # Si l'analyse n'existe pas
    if analyze is None:
        # Créé une analyse sur cette chanson
        analyze = Analyze(id_song=song_id)
        # Ajoute cette analyse à la session
        session.add(analyze)

    # Si l'analyse contient "predicted_popularity", lui mettre un score de popularité (entre 0 et 100)
    if hasattr(analyze, "predicted_popularity"):
        analyze.predicted_popularity = int(round(score_0_100))
    # Si l'analyse contient "popularity_probability", lui mettre une probabilité de popularité (entre 0 et 1)
    elif hasattr(analyze, "popularity_probability"):
        analyze.popularity_probability = float(score_0_100 / 100.0)
    # Sinon, renvoie une erreur
    else:
        raise AttributeError("Analyze missing predicted_popularity or popularity_probability")

    # Envoi des modifications
    session.flush()
    # Retourne l'analyse
    return analyze




def get_analyze_by_song_id(session: Session, *, song_id: int) -> Analyze | None:
    """
    Récupération de l'analyse d'une chanson donnée par son identifiant.

    - session : instance SQLAlchemy Session
    - song_id : identifiant de la chanson à rechercher
    - retourne :
        - l'objet Analyze correspondant à la chanson si trouvé
        - None si aucune analyse n'existe pour cette chanson
    """
    return session.query(Analyze).filter_by(id_song=song_id).first()


def list_my_analyzes_with_song(session: Session, *, user_id: int, skip: int, limit: int):
    """
    Récupération des uploads d'un utilisateur avec leurs chansons et analyses associées.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur dont on liste les uploads
    - skip : nombre d'éléments à ignorer pour la pagination
    - limit : nombre maximal d'éléments à retourner
    - retourne:
        - liste de dictionnaires contenant pour chaque upload :
            - song_id : identifiant de la chanson
            - song_name : nom de la chanson
            - private : bool indiquant si l'upload est privé
            - analyze : dictionnaire avec les informations d'analyse ou None si aucune analyse
                - predicted_popularity : score de popularité entre 0 et 100 si existant
                - popularity_probability : probabilité de popularité entre 0 et 1 si existante
    """
    # Requête récupérant les uploads, les analyses et les chansons d'un utilisateur quelconque
    rows = (
        session.query(UploadedBy, Song, Analyze)
        .join(Song, Song.song_id == UploadedBy.song_id)
        .outerjoin(Analyze, Analyze.id_song == Song.song_id)
        .filter(UploadedBy.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Création d'un tableau de dictionnaire (pour JSON)
    items = []
    # Boucle sur les éléments de la requête
    for upload, song, analyze in rows:
        # Ajout des éléments de la requête dans le tableau
        items.append({
            "song_id": song.song_id,
            "song_name": song.song_name,
            "private": upload.private,
            "analyze": None if analyze is None else {
                # adapte selon les champs
                "predicted_popularity": getattr(analyze, "predicted_popularity", None),
                "popularity_probability": getattr(analyze, "popularity_probability", None),
            }
        })
    return items

