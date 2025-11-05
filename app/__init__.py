from flask import Flask, jsonify
import os
from flask_jwt_extended import JWTManager

from app.load_env import load_env
load_env()

from app.extensions import db, migrate
from app.config.database import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from app.add_env_to_config import add_env_to_config


def create_app():
    app = Flask(__name__)

    add_env_to_config(app, [
        'JWT_SECRET_KEY',
        'JWT_TOKEN_LOCATION',
        ['JWT_COOKIE_SECURE', 'bool'],
        ['JWT_COOKIE_HTTPONLY', 'bool'],
        ['JWT_COOKIE_CSRF_PROTECT', 'bool'],
        ['DEBUG', 'bool'],
        ['PROPAGATE_EXCEPTIONS', 'another_var', 'DEBUG']
    ])

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', SQLALCHEMY_TRACK_MODIFICATIONS)

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    from app.models.user import User
    from app.models.category import Category
    from app.models.record import Record

    from app.routes.general import general_bp
    from app.routes.user import user_bp
    from app.routes.category import category_bp
    from app.routes.record import record_bp
    
    app.register_blueprint(general_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(record_bp)
    
    return app

app = create_app()


