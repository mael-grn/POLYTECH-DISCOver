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

# Création de chanson
def create_song_row(session: Session, *, data: dict) -> Song:
    # Créé une chanson
    song = Song(**data)
    # Ajoute cette chanson
    session.add(song)
    # Retourne cette chanson
    return song

# Récupère une chanson dépendamment de sa privacité
def get_song_with_private_guard(
    session: Session,
    *,
    song_id: int,
    maybe_user_id: Optional[int],
    should_touch_history: bool = True,
) -> Song:
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

# Liste nos chansons via upload et recherche
def list_songs_with_upload_guard_and_search(
    session: Session,
    *,
    maybe_user_id: Optional[int],
    skip: int,
    limit: int,
    search: str,
    mode: str,  # "any" | "all"
) -> List[Dict[str, Any]]:
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

# Liste nos chansons via recherche
def list_my_songs_with_search(
    session: Session,
    *,
    user_id: int,
    skip: int,
    limit: int,
    search: str,
    mode: str,  # "any" | "all"
) -> List[Dict[str, Any]]:
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

# Suppression d'une chanson privée uploadée
def delete_uploaded_song_for_owner(
    session: Session,
    *,
    user_id: int,
    song_id: int,
) -> None:
    """
    :param session:
    :param user_id:
    :param song_id:
    :return:
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

# Création d'une chanson via ses caractéristiques
def create_song_from_features(
        session: Session,
        *,
        song_name: str,
        features: dict,
        is_in_data_set: bool = False
) -> Song:
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
