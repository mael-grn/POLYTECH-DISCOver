from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.extensions import db
from app.models.song import Song
from app.schemas.song_schema import SongCreateSchema, SongReadSchema
from sqlalchemy.exc import SQLAlchemyError

songs_bp = Blueprint("songs", __name__)

song_create_schema = SongCreateSchema()
song_read_schema = SongReadSchema()
songs_read_schema = SongReadSchema(many=True)

@songs_bp.post("/songs")
def create_song():
    schema_song = request.get_json(silent=True)
    if schema_song is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    try:
        data = song_create_schema.load(schema_song)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "messages": err.messages}), 422

    song = Song(**data)

    db.session.add(song)
    db.session.commit()

    return jsonify(song_read_schema.dump(song)), 201

@songs_bp.get("/songs/<int:song_id>")
def get_song(song_id: int):
    """
    Récupère une chanson par son ID.
    """
    song = db.session.get(Song, song_id)  # SQLAlchemy 1.4+/2.x

    if song is None:
        return jsonify({"error": "NotFound", "message": f"Song {song_id} not found"}), 404

    return jsonify(song_read_schema.dump(song)), 200

@songs_bp.get("/songs")
def list_songs():
    """
    Liste des songs avec une limit de 50 par defaut et un max de 100 et on en skip 0.
    """
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 50))
    except ValueError:
        return jsonify({"error": "ValidationError", "message": "skip/limit must be integers"}), 422

    if skip < 0:
        skip = 0
    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100

    songs = (
        db.session.query(Song)
        .order_by(Song.song_id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return jsonify({
        "skip": skip,
        "limit": limit,
        "count": len(songs),
        "items": songs_read_schema.dump(songs),
    }), 200
