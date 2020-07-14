import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/users"
    SQLALCHEMY_TRACK_MODIFICATIONS = False