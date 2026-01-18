from marshmallow import Schema, fields, validate


class SongCreateSchema(Schema):
    """
    Cette classe defini tout ce qui est necessaire ou non pour creer un song.
    """
    song_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))

    song_popularity = fields.Int(required=False, allow_none=True)
    song_duration_ms = fields.Int(required=False, allow_none=True)

    acousticness = fields.Float(required=False, allow_none=True)
    danceability = fields.Float(required=False, allow_none=True)
    energy = fields.Float(required=False, allow_none=True)
    instrumentalness = fields.Float(required=False, allow_none=True)
    key = fields.Int(required=False, allow_none=True)
    liveness = fields.Float(required=False, allow_none=True)
    loudness = fields.Float(required=False, allow_none=True)

    is_in_data_set = fields.Bool(required=False, missing=False)


class SongUpdateSchema(Schema):
    """Cette classe defni ce qui est necessaire pour update un Son soit qaucun mais necessaire au cas ou on veut update un son"""
    song_name = fields.Str(required=False, validate=validate.Length(min=1, max=255))

    song_popularity = fields.Int(required=False, allow_none=True)
    song_duration_ms = fields.Int(required=False, allow_none=True)

    acousticness = fields.Float(required=False, allow_none=True)
    danceability = fields.Float(required=False, allow_none=True)
    energy = fields.Float(required=False, allow_none=True)
    instrumentalness = fields.Float(required=False, allow_none=True)
    key = fields.Int(required=False, allow_none=True)
    liveness = fields.Float(required=False, allow_none=True)
    loudness = fields.Float(required=False, allow_none=True)

    is_in_data_set = fields.Bool(required=False)


class SongReadSchema(Schema):
    """Cette classe defini ce que renvoie l'API au sujet d'un song."""
    song_id = fields.Int(dump_only=True)
    song_name = fields.Str(dump_only=True)

    song_popularity = fields.Int(dump_only=True, allow_none=True)
    song_duration_ms = fields.Int(dump_only=True, allow_none=True)

    acousticness = fields.Float(dump_only=True, allow_none=True)
    danceability = fields.Float(dump_only=True, allow_none=True)
    energy = fields.Float(dump_only=True, allow_none=True)
    instrumentalness = fields.Float(dump_only=True, allow_none=True)
    key = fields.Int(dump_only=True, allow_none=True)
    liveness = fields.Float(dump_only=True, allow_none=True)
    loudness = fields.Float(dump_only=True, allow_none=True)

    is_in_data_set = fields.Bool(dump_only=True)
