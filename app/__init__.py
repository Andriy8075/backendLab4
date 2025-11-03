from flask import Flask, jsonify
import os
from flask_jwt_extended import JWTManager

from app.load_env import load_env
load_env()

from app.extensions import db, migrate
from app.config.database import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', SQLALCHEMY_TRACK_MODIFICATIONS)

    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    app.config['DEBUG'] = debug
    app.config['PROPAGATE_EXCEPTIONS'] = debug

    db.init_app(app)
    migrate.init_app(app, db)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_HTTPONLY"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
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


