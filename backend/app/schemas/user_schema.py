from marshmallow import fields, validate, Schema

class UserCreateSchema(Schema):
    """Cette class defini tout ce qui est attendu pour Creer un user"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, load_only=True)

class UserLoginSchema(Schema):
    """Cette class defini tout ce qui est attendu pour se connecter (login)."""
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=128))

class UserReadSchema(Schema):
    """Cette class defini tout ce que renvoie l'API au sujet de l"utilisateur"""
    user_id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
