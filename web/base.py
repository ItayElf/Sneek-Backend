"""
A file for the configuration of the flask app

This file is needed so that the app and the database could be accessible in other files
"""
import pathlib
import secrets
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from web.configuration import Configuration

_DATABASE_LOCATION = pathlib.Path(__file__).parent.parent / "sneek.db"
CONFIGURATION = Configuration.load()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = secrets.token_hex()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=CONFIGURATION.session_duration_in_hours)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{_DATABASE_LOCATION}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database = SQLAlchemy(app)
jwt = JWTManager(app)
