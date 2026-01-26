# app/crud/songs_crud.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.song import Song
from app.models.uploaded_by import UploadedBy
from app.models.history import History
from app.services.history_service import touch_history
from app.services.search_service import apply_rich_search
from app.core.errors import NotFoundError, ForbiddenError






def create_song_row(session: Session, *, data: dict) -> Song:
    """
    Création d'une nouvelle entrée de chanson dans la base de données.

    - session : instance SQLAlchemy Session
    - data : dictionnaire contenant les champs et valeurs pour la création de la chanson
    - retourne : l'objet Song créé
    """
    # Créé une chanson
    song = Song(**data)
    # Ajoute cette chanson
    session.add(song)
    # Retourne cette chanson
    return song



def get_song_with_private_guard(
    session: Session,
    *,
    song_id: int,
    maybe_user_id: Optional[int],
    should_touch_history: bool = True,
) -> Song:
    """
    Récupération d'une chanson en appliquant les restrictions d'accès aux uploads privés.

    - session : instance SQLAlchemy Session
    - song_id : identifiant de la chanson à récupérer
    - maybe_user_id : identifiant de l'utilisateur effectuant la requête, ou None si non connecté
    - should_touch_history : booléen indiquant si l'historique de l'utilisateur doit être mis à jour
    - retourne : l'objet Song correspondant à la chanson demandée
    - exceptions :
        - NotFoundError : si la chanson n'existe pas
        - ForbiddenError : si la chanson est privée et que l'utilisateur n'a pas le droit d'accès
    """
    # Récupère une chanson
    song = session.get(Song, song_id)
    # Si la chanson est introuvable, retourne une erreur
    if song is None:
        raise NotFoundError(message=f"Song {song_id} not found")

    # Créé un upload
    upload = (
        session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )

    # Si l'upload n'est pas vide et que l'upload est private
    if upload is not None and upload.private:
        # Si l'utilisateur est vide ou que l'utilisateur n'est pas celui qui a rendu private, renvoyer une erreur
        if maybe_user_id is None or upload.user_id != maybe_user_id:
            raise ForbiddenError(message="Private song")

    # Si l'utilisateur est présent et que l'upload doit modifier l'historique, alors il le modifie
    if should_touch_history and maybe_user_id is not None:
        touch_history(maybe_user_id, song_id)

    # Retourne la chanson
    return song



def list_songs_with_upload_guard_and_search(
    session: Session,
    *,
    maybe_user_id: Optional[int],
    skip: int,
    limit: int,
    search: str,
    mode: str,  # "any" | "all"
) -> List[Dict[str, Any]]:
    """
    Récupération d'une liste de chansons avec gestion des uploads privés et recherche avancée.

    - session : instance SQLAlchemy Session
    - maybe_user_id : identifiant de l'utilisateur effectuant la requête, ou None si non connecté
    - skip : nombre d'éléments à ignorer pour la pagination
    - limit : nombre maximal d'éléments à retourner
    - search : texte de recherche
    - mode : mode de recherche avancée
    - retourne :
        - liste de dictionnaires contenant les informations des chansons et uploads visibles
            - champs de chanson : song_id, song_name, song_duration_ms, song_popularity, acousticness, danceability, energy
            - champ upload : None ou dictionnaire {user_id, private, date}
    """
    # Récupère skip s'il est positif (0 sinon)
    skip = max(0, int(skip))
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(int(limit), 100))

    # Récupère la chanson et l'upload correspondant
    q = (
        session.query(Song, UploadedBy)
        .outerjoin(UploadedBy, UploadedBy.song_id == Song.song_id)
    )
    # Si la recherche n'est pas vide
    if search:
        # Si la recherche est un nombre, rechercher l'identifiant 
        if search.isdigit():
            q = q.filter(Song.song_id == int(search))
            # Sinon, faire une recherche avancée
        else:

            q = apply_rich_search(q, search, columns=[Song.song_name], mode=mode)

    # Si l'utilisateur est vide
    if maybe_user_id is None:
        # Filtrer la recherche en fonction de la chanson et de la privacité
        q = q.filter(
            or_(
                UploadedBy.song_id.is_(None),      # dataset
                UploadedBy.private.is_(False),     # upload public
            )
        )
    # Sinon
    else:
        # Filtrer la recherche en fonction de la chanson, de la privacité et de l'utilisateur
        q = q.filter(
            or_(
                UploadedBy.song_id.is_(None),      # dataset
                UploadedBy.private.is_(False),     # upload public
                UploadedBy.user_id == maybe_user_id,  # uploads du user
            )
        )
    # Exécution de la requête
    rows = (
        q.order_by(Song.song_id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Création d'un tableau de dictionnaire (pour JSON)
    items: List[Dict[str, Any]] = []
    # Boucle sur les éléments de la requête
    for song, upload in rows:
        # Ajout des éléments de la requête dans le tableau
        items.append({
            "song_id": song.song_id,
            "song_name": song.song_name,
            "song_duration_ms": getattr(song, "song_duration_ms", None),
            "song_popularity": getattr(song, "song_popularity", None),
            "acousticness": getattr(song, "acousticness", None),
            "danceability": getattr(song, "danceability", None),
            "energy": getattr(song, "energy", None),
            "upload": None if upload is None else {
                "user_id": upload.user_id,
                "private": upload.private,
                "date": upload.date,
            }
        })
    # Retour du tableau
    return items



def list_my_songs_with_search(
    session: Session,
    *,
    user_id: int,
    skip: int,
    limit: int,
    search: str,
    mode: str,  # "any" | "all"
) -> List[Dict[str, Any]]:
    """
    Récupération de la liste des chansons uploadées par un utilisateur avec recherche avancée.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur dont on liste les chansons
    - skip : nombre d'éléments à ignorer pour la pagination
    - limit : nombre maximal d'éléments à retourner
    - search : texte de recherche sur le nom de la chanson
    - mode: mode de recherche avancée
    - retourne :
        - liste de dictionnaires contenant les informations des chansons et de leur upload
            - champs de chanson : song_id, song_name, song_duration_ms, song_popularity, acousticness, danceability, energy
            - champ upload : dictionnaire {user_id, private, date}
    """
    # Récupère skip s'il est positif (0 sinon)
    skip = max(0, int(skip))
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(int(limit), 100))

    # Récupère la chanson et l'upload correspondant
    q = (
        session.query(Song, UploadedBy)
        .join(UploadedBy, UploadedBy.song_id == Song.song_id)
        .filter(UploadedBy.user_id == user_id)
    )

    # Si la recherche n'est pas vide, faire une recherche avancée
    if search:
        q = apply_rich_search(q, search, columns=[Song.song_name], mode=mode)

    # Exécution de la requête
    rows = (
        q.order_by(UploadedBy.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Création d'un tableau de dictionnaire (pour JSON)
    items: List[Dict[str, Any]] = []
    # Boucle sur les éléments de la requête
    for song, upload in rows:
        # Ajout des éléments de la requête dans le tableau
        items.append({
            "song_id": song.song_id,
            "song_name": song.song_name,
            "song_duration_ms": getattr(song, "song_duration_ms", None),
            "song_popularity": getattr(song, "song_popularity", None),
            "acousticness": getattr(song, "acousticness", None),
            "danceability": getattr(song, "danceability", None),
            "energy": getattr(song, "energy", None),
            "upload": {
                "user_id": upload.user_id,
                "private": upload.private,
                "date": upload.date,
            }
        })

    # Retour du tableau
    return items



def delete_uploaded_song_for_owner(
    session: Session,
    *,
    user_id: int,
    song_id: int,
) -> None:
    """
    Suppression d'ne chanson uploadée par un utilisateur, ainsi que son upload et son historique.

    - session: instance SQLAlchemy Session pour effectuer les requêtes
    - user_id: identifiant de l'utilisateur tentant de supprimer la chanson
    - song_id: identifiant de la chanson à supprimer
    - exceptions :
        - ForbiddenError : si la chanson fait partie du dataset ou n'appartient pas à l'utilisateur.
        - NotFoundError : si la chanson n'existe pas.
    """
    # Création d'un upload
    upload = (
        session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )
    # Si l'upload est vide, renvoie une erreur
    if upload is None:
        raise ForbiddenError(message="This song is part of the dataset and cannot be deleted")

    # Si l'utilisateur de l'upload est différent de l'utilisateur actuel, renvoie une erreur
    if upload.user_id != user_id:
        raise ForbiddenError(message="Only the uploader can delete this song")

    # Récupère la chanson
    song = session.get(Song, song_id)
    # Si la chanson est introuvable, renvoie une erreur
    if song is None:
        raise NotFoundError(message=f"Song {song_id} not found")

    # Supprime l'historique de la chanson
    session.query(History) \
        .filter(History.song_id == song_id) \
        .delete(synchronize_session=False)

    # Supprime l'upload
    session.delete(upload)
    # Supprime la chanson
    session.delete(song)

def create_song_from_features(
        session: Session,
        *,
        song_name: str,
        features: dict,
        is_in_data_set: bool = False
) -> Song:
    """
    Création d'une instance de Song avec des caractéristiques audio et ajout à la session.

    - session : instance SQLAlchemy Session
    - song_name : nom de la chanson
    - features : dictionnaire contenant les caractéristiques audio
    - is_in_data_set : indique si la chanson fait partie du dataset
    - retourne : instance Song créée et ajoutée à la session
    """
    # Créé une chanson avec des caractéristiques
    song = Song(
        song_name=song_name,
        song_popularity=None,
        song_duration_ms=features.get("song_duration_ms"),
        acousticness=features.get("acousticness"),
        danceability=features.get("danceability"),
        energy=features.get("energy"),
        instrumentalness=features.get("instrumentalness"),
        key=features.get("key"),
        liveness=features.get("liveness"),
        loudness=features.get("loudness"),
        tempo=features.get("tempo"),
        audio_mode=features.get("audio_mode"),
        speechiness=features.get("speechiness"),
        time_signature=features.get("time_signature"),
        audio_valence=features.get("audio_valence"),
        is_in_data_set=is_in_data_set,
    )
    # Ajoute cette chanson
    session.add(song)
    # Envoie les modifications
    session.flush()
    # Retourne la chanson
    return song
