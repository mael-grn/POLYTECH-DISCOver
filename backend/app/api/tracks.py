# backend/app/api/tracks.py

from flask import Blueprint, jsonify, request
import json

from ..core.db import db
from ..models.track import Track
from ..models.history import SearchHistory

tracks_bp = Blueprint("tracks", __name__)

#######################################################
#   GET : liste des tracks (dataset Kaggle)
#######################################################

@tracks_bp.route("/", methods=["GET"])
def list_tracks():
    limit = int(request.args.get("limit", 100))
    tracks = Track.query.limit(limit).all()
    return jsonify([t.to_dict() for t in tracks])


#######################################################
#   GET : un track précis
#######################################################

@tracks_bp.route("/<int:track_id>", methods=["GET"])
def get_track(track_id):
    track = Track.query.get_or_404(track_id)
    return jsonify(track.to_dict())


#######################################################
#   POST : analyse d’un morceau venant du dataset
#######################################################

@tracks_bp.route("/<int:track_id>/analyze", methods=["POST"])
def analyze_track(track_id):
    # Dans le futur : on récupérera l'user via JWT
    data = request.get_json()
    user_id = data.get("user_id")  # temporaire

    if not user_id:
        return jsonify({"error": "user_id manquant"}), 400

    track = Track.query.get_or_404(track_id)

    # ---- ICI TU METTRAS TA PRÉDICTION RÉELLE ----
    prediction_result = {
        "success_score": 0.81,
        "will_succeed": True,
        "reason": "High energy + danceability",
        "tempo": track.tempo,
        "energy": track.energy
    }
    # ---------------------------------------------

    history_entry = SearchHistory(
        user_id=user_id,
        track_id=track.id,
        search_type="dataset",
        display_name=track.track_name,
        result_json=json.dumps(prediction_result)
    )

    db.session.add(history_entry)
    db.session.commit()

    return jsonify({
        "track": track.to_dict(),
        "analysis": prediction_result
    })


#######################################################
#   GET : historique d’un utilisateur
#######################################################

@tracks_bp.route("/history/<int:user_id>", methods=["GET"])
def get_user_history(user_id):
    entries = SearchHistory.query.filter_by(user_id=user_id).all()

    result = []
    for h in entries:
        result.append({
            "id": h.id,
            "search_type": h.search_type,
            "display_name": h.display_name,
            "result": json.loads(h.result_json) if h.result_json else None,
            "created_at": h.created_at.isoformat(),
        })

    return jsonify(result)
