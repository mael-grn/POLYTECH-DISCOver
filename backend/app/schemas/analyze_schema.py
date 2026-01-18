from marshmallow import Schema, fields


class AnalyzeUpsertSchema(Schema):
    """
    Cette classe defini ce qu"on a besoin pour mettre a jour ou cree une analyze
    """
    popularity_probability = fields.Float(required=True)


class AnalyzeReadSchema(Schema):
    """Cette classe defni ce qui est renvoyer par l'API pour une analyze """
    id_song = fields.Int(dump_only=True)
    popularity_probability = fields.Float(dump_only=True)
