from flask import Blueprint, jsonify, request, g
from app.core.guards import require_auth
from app.extensions import db
from app.core.guards import optional_auth
from app.crud.analyze_crud import get_analyze_by_song_id
from app.crud.uploads_crud import get_upload_by_song_id_with_private_guard
from app.crud.songs_crud import get_song_with_private_guard
from app.services.ml_predictor import predict_popularity_score

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.get("/analyze/<int:song_id>")
@optional_auth
def get_analyze(song_id: int):
    user_id = g.user_id

    analyze = get_analyze_by_song_id(db.session, song_id=song_id)
    if analyze is None:
        return jsonify({"error": "NotFound"}), 404

    return jsonify({
        "song_id": song_id,
        "predicted_popularity": getattr(analyze, "predicted_popularity", None),
        "popularity_probability": getattr(analyze, "popularity_probability", None),
    }), 200


@analyze_bp.get("/analyze/me")
@require_auth
def get_my_analyzes():
    user_id = g.user_id
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 50, type=int)
    limit = max(1, min(limit, 100))


    from app.crud.uploads_crud import list_my_uploads_with_song

    items = list_my_uploads_with_song(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )


    enriched = []
    for it in items:
        song_id = it["song"]["song_id"] if isinstance(it.get("song"), dict) else it.get("song_id")
        analyze = get_analyze_by_song_id(db.session, song_id=song_id)

        enriched.append({
            **it,
            "analyze": None if analyze is None else {
                "predicted_popularity": getattr(analyze, "predicted_popularity", None),
                "popularity_probability": getattr(analyze, "popularity_probability", None),
            }
        })

    return jsonify({"count": len(enriched), "items": enriched}), 200

@analyze_bp.get("/analyze/<int:song_id>/preview")
@optional_auth
def preview_analyze(song_id: int):
    """
    Rejoue le modèle ML sur une musique existante
    SANS mettre à jour l'analyse stockée.
    """
    user_id = g.user_id

    song = get_song_with_private_guard(
        db.session,
        song_id=song_id,
        maybe_user_id=user_id,
        should_touch_history=False,  )


    features = song.to_features_dict()
    score = predict_popularity_score(features)

    return jsonify({
        "song_id": song.song_id,
        "song_name": song.song_name,
        "predicted_popularity_preview": round(float(score), 1),
        "saved": False,
    }), 200
