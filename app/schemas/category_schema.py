from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from app.config.models_validation.category import name_max_length
from app.models.user import User
from app.models.category import Category


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=name_max_length))
    user_id = fields.Int(required=True, validate=validate.Range(min=1))


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=name_max_length))
    user_id = fields.Int(required=True, validate=validate.Range(min=1))
    
    @validates_schema
    def validate_user_exists(self, data, **kwargs):
        if 'user_id' in data:
            user = User.query.get(data['user_id'])
            if user is None:
                raise ValidationError('User with specified ID does not exist', field_name='user_id')

    @validates_schema
    def validate_unique_category_name(self, data, **kwargs):
        if 'name' in data:
            category = Category.query.filter_by(name=data['name'], user_id=data['user_id']).first()
            if category is not None:
                raise ValidationError('Category with this name already exists for this user', field_name='name')

class DeleteCategorySchema(Schema):
    id = fields.Int(required=True, validate=validate.Range(min=1))

    @validates_schema
    def validate_category_exists_and_belongs_to_user(self, data, **kwargs):
        category = Category.query.get(data['id'])
        if category is None:
            raise ValidationError('Category with specified ID does not exist', field_name='id')
        if category.user_id != get_jwt_identity():
            raise ValidationError('Category does not belong to the current user', field_name='id')
