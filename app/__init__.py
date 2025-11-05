from flask import Flask
from flask_jwt_extended import JWTManager

from app.env_manager import load_env, add_env_to_config
load_env()

from app.extensions import db, migrate
from app.config.database import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from app.config.env_to_config import env_to_config_values_array
from app.blueprints_manager import register_blueprints_in_routes

app = Flask(__name__)

add_env_to_config(app, env_to_config_values_array)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', SQLALCHEMY_TRACK_MODIFICATIONS)

db.init_app(app)
migrate.init_app(app, db)
JWTManager(app)

register_blueprints_in_routes(app, ['general', 'user', 'category', 'record'])



