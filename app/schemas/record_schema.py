from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import datetime
from app.config.models_validation.record import min_sum
from app.config.currencies import SUPPORTED_CURRENCIES
from app.models.user import User
from app.models.category import Category
from flask_jwt_extended import get_jwt_identity


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    category_id = fields.Int(required=True, validate=validate.Range(min=1))
    sum = fields.Int(required=True, validate=validate.Range(min=min_sum))
    currency = fields.Str(required=True, validate=validate.OneOf(SUPPORTED_CURRENCIES))
    date_time = fields.DateTime(dump_only=True)


class RecordCreateSchema(Schema):
    category_id = fields.Int(required=True, validate=validate.Range(min=1))
    sum = fields.Int(required=True, validate=validate.Range(min=min_sum))
    currency = fields.Str(required=False, validate=validate.OneOf(SUPPORTED_CURRENCIES))
    date_time = fields.DateTime(load_default=datetime.utcnow, allow_none=True)
    
    @validates_schema
    def validate_category_exists_and_belongs_to_user(self, data, **kwargs):
        category = Category.query.get(data['category_id'])
        if category is None:
            raise ValidationError('Category with specified ID does not exist', field_name='category_id')

        authenticated_user_id = int(get_jwt_identity())
        if category.user_id != authenticated_user_id:
            raise ValidationError('Category does not belong to the current user', field_name='category_id')
    
