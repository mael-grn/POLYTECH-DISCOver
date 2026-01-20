from marshmallow import Schema, fields

class SongUploadInfoSchema(Schema):
    """Schema pour definir ce qui est necessaire pour savoir si un son est prive ou non et connaitre a qui il est"""
    user_id = fields.Int(allow_none=True)
    private = fields.Bool(allow_none=True)
    date = fields.DateTime(allow_none=True)

class SongListItemSchema(Schema):
    """Defini les information renvoyer pour affichier dans la liste de """
    song_id = fields.Int(required=True)
    song_name = fields.Str(required=True)

    song_duration_ms = fields.Int(allow_none=True)
    song_popularity = fields.Int(allow_none=True)
    acousticness = fields.Float(allow_none=True)
    danceability = fields.Float(allow_none=True)
    energy = fields.Float(allow_none=True)
    upload = fields.Nested(SongUploadInfoSchema, allow_none=True)
