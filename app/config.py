import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')
    STATIC_TOKEN = os.environ.get('STATIC_TOKEN', 'dev-static-token')
    PROPAGATE_EXCEPTIONS = True
