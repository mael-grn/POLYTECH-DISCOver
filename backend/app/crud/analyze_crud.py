from sqlalchemy.orm import Session
from app.models.analyze import Analyze
from app.models.song import Song
def upsert_analyze_for_song(session: Session, *, song_id: int, score_0_100: float) -> Analyze:
    analyze = session.query(Analyze).filter_by(id_song=song_id).first()
    if analyze is None:
        analyze = Analyze(id_song=song_id)
        session.add(analyze)

    if hasattr(analyze, "predicted_popularity"):
        analyze.predicted_popularity = int(round(score_0_100))
    elif hasattr(analyze, "popularity_probability"):
        analyze.popularity_probability = float(score_0_100 / 100.0)
    else:
        raise AttributeError("Analyze missing predicted_popularity or popularity_probability")

    session.flush()
    return analyze




def get_analyze_by_song_id(session: Session, *, song_id: int) -> Analyze | None:
    return session.query(Analyze).filter_by(id_song=song_id).first()


def list_my_analyzes_with_song(session: Session, *, user_id: int, skip: int, limit: int):
    from app.models.uploaded_by import UploadedBy
    rows = (
        session.query(UploadedBy, Song, Analyze)
        .join(Song, Song.song_id == UploadedBy.song_id)
        .outerjoin(Analyze, Analyze.id_song == Song.song_id)
        .filter(UploadedBy.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    items = []
    for upload, song, analyze in rows:
        items.append({
            "song_id": song.song_id,
            "song_name": song.song_name,
            "private": upload.private,
            "analyze": None if analyze is None else {
                # adapte selon vos champs
                "predicted_popularity": getattr(analyze, "predicted_popularity", None),
                "popularity_probability": getattr(analyze, "popularity_probability", None),
            }
        })
    return items

