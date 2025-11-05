import os
from app.env_manager import to_bool

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
USE_SSL = to_bool(os.getenv('USE_SSL'))

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}' + ('?sslmode=require' if USE_SSL else '')

SQLALCHEMY_TRACK_MODIFICATIONS = False