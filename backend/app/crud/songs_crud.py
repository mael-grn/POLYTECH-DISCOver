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

    song = Song(**data)
    session.add(song)
    return song



def get_song_with_private_guard(
    session: Session,
    *,
    song_id: int,
    maybe_user_id: Optional[int],
    should_touch_history: bool = True,
) -> Song:
    song = session.get(Song, song_id)
    if song is None:
        raise NotFoundError(message=f"Song {song_id} not found")

    upload = (
        session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )

    if upload is not None and upload.private:
        if maybe_user_id is None or upload.user_id != maybe_user_id:
            raise ForbiddenError(message="Private song")

    if should_touch_history and maybe_user_id is not None:
        touch_history(maybe_user_id, song_id)

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

    skip = max(0, int(skip))
    limit = max(1, min(int(limit), 100))

    q = (
        session.query(Song, UploadedBy)
        .outerjoin(UploadedBy, UploadedBy.song_id == Song.song_id)
    )

    if search:
        if search.isdigit():
            q = q.filter(Song.song_id == int(search))
        else:
            # ton code avait apply_rich_song_search + doublon d'appel.
            # Ici on fait propre via le service existant.
            q = apply_rich_search(q, search, columns=[Song.song_name], mode=mode)

    if maybe_user_id is None:
        q = q.filter(
            or_(
                UploadedBy.song_id.is_(None),      # dataset
                UploadedBy.private.is_(False),     # upload public
            )
        )
    else:
        q = q.filter(
            or_(
                UploadedBy.song_id.is_(None),      # dataset
                UploadedBy.private.is_(False),     # upload public
                UploadedBy.user_id == maybe_user_id,  # uploads du user
            )
        )

    rows = (
        q.order_by(Song.song_id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    items: List[Dict[str, Any]] = []
    for song, upload in rows:
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

    skip = max(0, int(skip))
    limit = max(1, min(int(limit), 100))

    q = (
        session.query(Song, UploadedBy)
        .join(UploadedBy, UploadedBy.song_id == Song.song_id)
        .filter(UploadedBy.user_id == user_id)
    )

    if search:
        q = apply_rich_search(q, search, columns=[Song.song_name], mode=mode)

    rows = (
        q.order_by(UploadedBy.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    items: List[Dict[str, Any]] = []
    for song, upload in rows:
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

    return items



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
    upload = (
        session.query(UploadedBy)
        .filter(UploadedBy.song_id == song_id)
        .first()
    )
    if upload is None:
        raise ForbiddenError(message="This song is part of the dataset and cannot be deleted")

    if upload.user_id != user_id:
        raise ForbiddenError(message="Only the uploader can delete this song")

    song = session.get(Song, song_id)
    if song is None:
        raise NotFoundError(message=f"Song {song_id} not found")

    session.query(History) \
        .filter(History.song_id == song_id) \
        .delete(synchronize_session=False)

    session.delete(upload)
    session.delete(song)
