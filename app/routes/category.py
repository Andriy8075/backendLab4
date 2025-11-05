from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models.category import Category
from app.schemas.category_schema import CategorySchema, CategoryCreateSchema
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

category_bp = Blueprint('category', __name__)

@category_bp.route('/category', methods=['POST'])
@jwt_required()
def create_category():
    try:
        schema = CategoryCreateSchema()
        data = schema.load(request.form)

        category = Category.create(data['name'], int(get_jwt_identity()))

        category_schema = CategorySchema()
        return jsonify({
            'message': 'category created successfully',
            'category': category_schema.dump(category)
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'error': 'Validation error',
            'messages': err.messages
        }), 400

@category_bp.route('/category', methods=['GET'])
@jwt_required()
def get_categories():
    user_id = int(get_jwt_identity())
    categories = Category.get_by_user_id(user_id)
    category_schema = CategorySchema(many=True)
    return jsonify(category_schema.dump(categories)), 200

@category_bp.route('/category/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    try:
        category = Category.query.get(id)
        if category is None:
            raise ValidationError('Category with specified ID does not exist', field_name='id')
        if category.user_id != int(get_jwt_identity()):
            raise ValidationError('Category does not belong to the current user', field_name='id')
    except ValidationError as err:
        return jsonify({
            'error': 'Validation error',
            'messages': err.messages
        }), 400
    Category.delete(id)
    return jsonify({'message': 'Category deleted successfully'}), 200