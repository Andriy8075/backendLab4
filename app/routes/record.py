from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models.record import Record
from app.schemas.record_schema import RecordSchema, RecordCreateSchema
from flask_jwt_extended import (
    jwt_required,
)

record_bp = Blueprint('record', __name__)

@record_bp.route('/record', methods=['POST'])
@jwt_required()
def create_record():
    try:
        schema = RecordCreateSchema()
        data = schema.load(request.form)

        record = Record.create(data['category_id'], data['sum'], data.get('currency'))

        record_schema = RecordSchema()
        return jsonify({
            'message': 'record created successfully',
            'record': record_schema.dump(record)
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'error': 'Validation error',
            'messages': err.messages
        }), 400

@record_bp.route('/record/<int:id>', methods=['GET'])
@jwt_required()
def get_record(id):
    record = Record.get_by_id(id)
    if record is None:
        return jsonify({'error': 'Record not found'}), 404

    record_schema = RecordSchema()
    return jsonify(record_schema.dump(record)), 200

@record_bp.route('/record/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_record(id):
    if Record.delete(id):
        return jsonify({'message': 'Record deleted successfully'}), 200
    else:
        return jsonify({'error': 'Record not found'}), 404
