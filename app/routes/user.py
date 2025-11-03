from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
    set_access_cookies
)
from functools import wraps
from marshmallow import ValidationError
from app.models.user import User
from app.schemas.user_schema import UserSchema, UserCreateSchema

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    form = request.form or {}
    user_id = form.get('id')
    password = form.get('password')

    user = User.query.get(user_id)

    if user is None or not password or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    response = jsonify({'message': 'logged in', 'user': user.to_dict()})
    set_access_cookies(response, access_token)
    return response, 200

@user_bp.route('/register', methods=['POST'])
def create_user():
    try:
        schema = UserCreateSchema()
        data = schema.load(request.form)

        user = User.create(data)

        access_token = create_access_token(identity=user.id)
        user_schema = UserSchema()
        response = jsonify({
            'message': 'user created successfully',
            'user': user_schema.dump(user)
        })
        set_access_cookies(response, access_token)
        return response, 201
        
    except ValidationError as err:
        return jsonify({
            'error': 'Validation error',
            'messages': err.messages
        }), 400

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.get_all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users)), 200

@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get_by_id(id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200

@jwt_required()
@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    if User.delete(id):
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404