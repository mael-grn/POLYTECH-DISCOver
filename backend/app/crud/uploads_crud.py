# app/crud/uploads_crud.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.uploaded_by import UploadedBy
from app.models.song import Song
from app.core.errors import NotFoundError, ForbiddenError

# Création d'un upload pour un utilisateur
def create_upload_for_user(session: Session, *, user_id: int, song_id: int, private: bool) -> tuple[UploadedBy, bool]:
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

    # Envoyer les modification
    try:
        session.flush()
    # Si une erreur d'intégrité apparaît
    except IntegrityError:
        # Annule toutes les modifications non-enregistrées
        session.rollback()
        # Lève l'erreur de conflit
        raise ConflictError(message="Upload already exists")
    
    # Renvoie l'upload et le booléen de création
    return upload, created

# Récupère un upload en fonction d'une chanson
def get_upload_by_song_id(session: Session, *, song_id: int) -> Optional[UploadedBy]:
    return (
        session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )

# Récupère un upload en fonction d'une chanson et de sa privacité
def get_upload_by_song_id_with_private_guard(
    session: Session,
    *,
    song_id: int,
    maybe_user_id: Optional[int],
) -> UploadedBy:
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

# Change la privacité de l'upload pour le propriétaire
def set_upload_private_for_owner(
    session: Session,
    *,
    user_id: int,
    song_id: int,
    private: bool,
) -> UploadedBy:
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

# Liste nos uploads avec nos chansons
def list_my_uploads_with_song(
    session: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
) -> List[Dict[str, Any]]:
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

# Création d'un lien d'upload
def create_upload_link(session: Session, *, user_id: int, song_id: int, private: bool) -> UploadedBy:
    # Créé un lien d'upload
    link = UploadedBy(user_id=user_id, song_id=song_id, private=private)
    # Ajoute ce lien
    session.add(link)
    # Envoie les modifications
    session.flush()
    # Retourne le lien
    return link
