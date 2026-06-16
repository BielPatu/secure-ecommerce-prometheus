import os

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-super-secret")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False