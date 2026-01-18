from marshmallow import Schema, fields


class UploadCreateSchema(Schema):
    """
    Cette classe defini ce qui est necessaire pour creer un uploaded_by."""
    song_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    private = fields.Bool(required=False, missing=False)


class UploadUpdateSchema(Schema):
    """Cette classe defini ce qui est necessaire ou non pour modifier un uploaded_by en soi pour savoir si il reste prive ou non ?"""
    private = fields.Bool(required=False)


class UploadReadSchema(Schema):
    """Cette classe defini ce qui est renvoyer par l'API au sujet de uploaded_by"""
    song_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    date = fields.DateTime(dump_only=True)
    private = fields.Bool(dump_only=True)
