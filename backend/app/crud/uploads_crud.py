# app/crud/uploads_crud.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.uploaded_by import UploadedBy
from app.models.song import Song
from app.core.errors import NotFoundError, ForbiddenError






def create_upload_for_user(session: Session, *, user_id: int, song_id: int, private: bool) -> tuple[UploadedBy, bool]:
    """
    Création ou mise à jour d'un upload pour un utilisateur et une chanson donnée.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur créant ou mettant à jour l'upload
    - song_id : identifiant de la chanson associée à l'upload
    - private : booléen indiquant si l'upload doit être privé
    - retourne :
        - tuple(upload, created)
            - upload : instance UploadedBy correspondante
            - created : booléen indiquant si l'upload a été créé ou existait déjà
    - exceptions :
        - ConflictError : si un upload identique existe déjà et provoque une erreur d'intégrité
    """
    # Récupération de l'upload
    upload = (
        session.query(UploadedBy)
        .filter_by(song_id=song_id, user_id=user_id)
        .first()
    )
    # Initialisation d'un booléen vérifiant si l'upload a été créé (initialisé à False)
    created = False
    # Si l'upload est vide
    if upload is None:
        # Création d'un upload
        upload = UploadedBy(song_id=song_id, user_id=user_id, private=private)
        # Ajoute l'upload
        session.add(upload)
        # Affectation de created à True
        created = True
    # Sinon, changer ou non la privacité de l'upload
    else:
        upload.private = private

    # Envoyer les modifications
    try:
        session.flush()
    # Si une erreur d'intégrité apparaît
    except IntegrityError:
        # Annule toutes les modifications non-enregistrées
        session.rollback()
        # Lève l'erreur de conflit
        raise ConflictError(message="Upload already exists")

    return upload, created


def get_upload_by_song_id(session: Session, *, song_id: int) -> Optional[UploadedBy]:
    """
    Récupération du premier upload correspondant à une chanson donnée.

    - session : instance SQLAlchemy Session
    - song_id : identifiant de la chanson dont on cherche l'upload
    - retourne: 
        - une instance UploadedBy si un upload existe pour cette chanson
        - None si aucun upload n'est trouvé
    """
    return (
        session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )


def get_upload_by_song_id_with_private_guard(
    session: Session,
    *,
    song_id: int,
    maybe_user_id: Optional[int],
) -> UploadedBy:
    """
    Récupération d'un upload pour une chanson donnée et vérification des droits d'accès.

    - session : instance SQLAlchemy Session
    - song_id : identifiant de la chanson dont on cherche l'upload
    - maybe_user_id : identifiant de l'utilisateur effectuant la requête, ou None si non connecté
    - retourne :
        - l'objet UploadedBy correspondant à l'upload si l'accès est autorisé.
    """
    # Récupère l'upload
    upload = get_upload_by_song_id(session, song_id=song_id)
    # Si l'upload est vide, renvoyer une erreur
    if upload is None:
        raise NotFoundError(message=f"No upload found for song_id={song_id}")

    # Si l'upload est privé
    if upload.private:
        # Si l'utilisateur est vide ou que l'utilisateur de l'upload n'est pas l'utilisateur courant, lever une erreur
        if maybe_user_id is None or upload.user_id != maybe_user_id:
            raise ForbiddenError(message="Private upload")

    # Retourne l'upload
    return upload


def set_upload_private_for_owner(
    session: Session,
    *,
    user_id: int,
    song_id: int,
    private: bool,
) -> UploadedBy:
    """
    Mise à jour de la privacité d'un upload pour son propriétaire.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur tentant de modifier l'upload
    - song_id : identifiant de la chanson associée à l'upload
    - private : booléen indiquant si l'upload doit être privé ou public
    - retourne:
        - l'objet UploadedBy mis à jour.
    """
    # Récupère l'upload
    upload = get_upload_by_song_id(session, song_id=song_id)
    # Si l'upload est vide, lève une erreur
    if upload is None:
        raise NotFoundError(message=f"No upload found for song_id={song_id}")

    # Si l'utilisateur de l'upload n'est pas l'utilisateur courant, lève une erreur
    if upload.user_id != user_id:
        raise ForbiddenError(message="Only the uploader can update this upload")

    # Change la privacité de l'upload
    upload.private = private
    # Retourne l'upload
    return upload


def list_my_uploads_with_song(
    session: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """
    Liste des uploads d'un utilisateur avec les informations des chansons associées.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur dont on souhaite lister les uploads.
    - skip : nombre d'éléments à ignorer pour la pagination
    - limit : nombre maximal d'éléments à retourner
    - retourne :
        - Une liste de dictionnaires contenant pour chaque upload :
            - "song_id" : identifiant de la chanson
            - "song_name" : nom de la chanson
            - "song_duration_ms" : durée de la chanson en millisecondes
            - "private" : booléen indiquant si l'upload est privé
            - "uploaded_at" : date de l'upload
    """
    # Récupère skip s'il est positif (0 sinon)
    skip = max(0, int(skip))
    # Récupère limit s'il est entre 1 et 100 (1 ou 100 sinon)
    limit = max(1, min(int(limit), 100))

    # Récupération de l'upload et de la chanson en fonction de la chanson et de l'utilisateur
    rows = (
        session.query(UploadedBy, Song)
        .join(Song, Song.song_id == UploadedBy.song_id)
        .filter(UploadedBy.user_id == user_id)
        .order_by(UploadedBy.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Retourne les caractéristiques de la chanson et de l'upload
    return [
        {
            "song_id": song.song_id,
            "song_name": song.song_name,
            "song_duration_ms": song.song_duration_ms,
            "private": upload.private,
            "uploaded_at": upload.date,
        }
        for upload, song in rows
    ]


def create_upload_link(session: Session, *, user_id: int, song_id: int, private: bool) -> UploadedBy:
    """
    Création d'un lien d'upload entre un utilisateur et une chanson.

    - session : instance SQLAlchemy Session
    - user_id : identifiant de l'utilisateur qui upload la chanson
    - song_id : identifiant de la chanson à lier à l'utilisateur
    - private : booléen indiquant si l'upload doit être privé ou public
    - retourne :
        - l'objet `UploadedBy` créé, représentant le lien d'upload
    """
    # Créé un lien d'upload
    link = UploadedBy(user_id=user_id, song_id=song_id, private=private)
    # Ajoute ce lien
    session.add(link)
    # Envoie les modifications
    session.flush()
    # Retourne le lien
    return link
