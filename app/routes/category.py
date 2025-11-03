from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models.category import Category
from app.schemas.category_schema import CategorySchema, CategoryCreateSchema, DeleteCategorySchema
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

category_bp = Blueprint('category', __name__)

@jwt_required()
@category_bp.route('/category', methods=['POST'])
def create_category():
    try:
        schema = CategoryCreateSchema()
        data = schema.load(request.form)

        category = Category.create(data['name'], get_jwt_identity())

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

@jwt_required()
@category_bp.route('/category', methods=['GET'])
def get_categories():
    user_id = get_jwt_identity()
    categories = Category.get_by_user_id(user_id)
    category_schema = CategorySchema(many=True)
    return jsonify(category_schema.dump(categories)), 200

@jwt_required()
@category_bp.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id):
    schema = DeleteCategorySchema()

    try:
        data = schema.load(request.form)
    except ValidationError as err:
        return jsonify({
            'error': 'Validation error',
            'messages': err.messages
        }), 400
    Category.delete(data['id'])
    return jsonify({'message': 'Category deleted successfully'}), 200