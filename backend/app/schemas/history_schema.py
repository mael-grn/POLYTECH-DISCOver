from marshmallow import Schema, fields


class HistoryCreateSchema(Schema):
    """
    Cette classe defini ce qui est necessaire pour creer un history.
    """
    song_id = fields.Int(required=True)
    user_id = fields.Int(required=True)


class HistoryReadSchema(Schema):
    """Cette classe defini ce qui est renvoyer par l'API au sujet de l'history"""
    song_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)

    last_research = fields.DateTime(dump_only=True)
    date = fields.DateTime(dump_only=True)
