# app/crud/uploads_crud.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from sqlalchemy.orm import Session

from app.models.uploaded_by import UploadedBy
from app.models.song import Song
from app.core.errors import NotFoundError, ForbiddenError






def create_upload_for_user(
    session: Session,
    *,
    user_id: int,
    song_id: int,
    private: bool,
) -> UploadedBy:

    row = UploadedBy(song_id=song_id, user_id=user_id, private=private)
    session.add(row)
    return row


def get_upload_by_song_id(session: Session, *, song_id: int) -> Optional[UploadedBy]:
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

    upload = get_upload_by_song_id(session, song_id=song_id)
    if upload is None:
        raise NotFoundError(message=f"No upload found for song_id={song_id}")

    if upload.private:
        if maybe_user_id is None or upload.user_id != maybe_user_id:
            raise ForbiddenError(message="Private upload")

    return upload


def set_upload_private_for_owner(
    session: Session,
    *,
    user_id: int,
    song_id: int,
    private: bool,
) -> UploadedBy:

    upload = get_upload_by_song_id(session, song_id=song_id)
    if upload is None:
        raise NotFoundError(message=f"No upload found for song_id={song_id}")

    if upload.user_id != user_id:
        raise ForbiddenError(message="Only the uploader can update this upload")

    upload.private = private
    return upload


def list_my_uploads_with_song(
    session: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    skip = max(0, int(skip))
    limit = max(1, min(int(limit), 100))

    rows = (
        session.query(UploadedBy, Song)
        .join(Song, Song.song_id == UploadedBy.song_id)
        .filter(UploadedBy.user_id == user_id)
        .order_by(UploadedBy.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

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
