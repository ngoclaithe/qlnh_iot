import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_FOLDER = os.path.join(BASE_DIR, "instance")
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

DB_PATH = os.path.join(DB_FOLDER, "data_restaurant.db")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secrect_key'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False