from marshmallow import Schema, fields, validate
from app.config.models_validation.user import name_max_length
from app.config.currencies import SUPPORTED_CURRENCIES


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=name_max_length))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8, max=255))
    default_currency = fields.Str(required=True, validate=validate.OneOf(SUPPORTED_CURRENCIES))


class UserCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=name_max_length))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8, max=255))
    default_currency = fields.Str(required=True, validate=validate.OneOf(SUPPORTED_CURRENCIES))
