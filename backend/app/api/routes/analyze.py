from flask import Blueprint, jsonify, request, g
from app.core.guards import require_auth
from app.extensions import db

from app.crud.analyze_crud import get_analyze_by_song_id
from app.crud.uploads_crud import get_upload_by_song_id_with_private_guard

# Création d'un module pour les routes dérivant de analyze
analyze_bp = Blueprint("analyze", __name__)

# Gestion de la route "/analyze/<int:song_id>"
@analyze_bp.get("/analyze/<int:song_id>")
@require_auth
def get_analyze(song_id: int):
    """
    Récupération de l'analyse d'une chanson spécifique.

    - méthode: GET
    - song_id : identifiant de la chanson à analyser
    - retourne : JSON + code HTTP
        - 200 si succès
        - 404 si analyse introuvable
    """
    # Récupération de l'identifiant utilisateur
    user_id = g.user_id

    # Vérification de l'autorisation d'accès à la chanson
    get_upload_by_song_id_with_private_guard(
        db.session,
        song_id=song_id,
        maybe_user_id=user_id,
    )

    # Récupère l'analyse reliée à la chanson
    analyze = get_analyze_by_song_id(db.session, song_id=song_id)
    # S'il n'y a pas d'analyse, renvoyer une erreur
    if analyze is None:
        return jsonify({"error": "NotFound"}), 404

    # Retourne la chanson et le score de probabilité
    return jsonify({
        "song_id": song_id,
        "predicted_popularity": getattr(analyze, "predicted_popularity", None),
        "popularity_probability": getattr(analyze, "popularity_probability", None),
    }), 200

# Gestion de la route "/analyze/me"
@analyze_bp.get("/analyze/me")
@require_auth
def get_my_analyzes():
    """
    Récupération des analyses des chansons uploadées par l'utilisateur connecté.

    - méthode: GET
    - retourne : JSON avec :
        - count : nombre d'éléments renvoyés
        - items : liste des uploads
    - code HTTP : 200 si succès
    """
    # Récupération de l'identifiant d'utilisateur
    user_id = g.user_id
    # Lecture du paramètre d'URL "skip"
    skip = request.args.get("skip", 0, type=int)
    # Lecture du paramètre d'URL "limit"
    limit = request.args.get("limit", 50, type=int)
    # Bornement de limit entre 1 et 100
    limit = max(1, min(limit, 100))


    from app.crud.uploads_crud import list_my_uploads_with_song
    
    # Récupération des uploads de l'utilisateur
    items = list_my_uploads_with_song(
        db.session,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )

    # Création d'un tableau pour les scores de popularité
    enriched = []
    # Boucle sur chaque upload
    for it in items:
        # Récupération de l'identifiant de la chanson
        song_id = it["song"]["song_id"] if isinstance(it.get("song"), dict) else it.get("song_id")
        # Récupération de l'analyse de la chanson
        analyze = get_analyze_by_song_id(db.session, song_id=song_id)
        # Ajout de l'upload et de l'analyse dans le tableau
        enriched.append({
            **it,
            "analyze": None if analyze is None else {
                "predicted_popularity": getattr(analyze, "predicted_popularity", None),
                "popularity_probability": getattr(analyze, "popularity_probability", None),
            }
        })

    # Retourne le nombre d'éléments renvoyés et la liste des uploads
    return jsonify({"count": len(enriched), "items": enriched}), 200
