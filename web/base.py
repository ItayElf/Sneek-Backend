"""
A file for the configuration of the flask app

This file is needed so that the app and the database could be accessible in other files
"""
import os
import pathlib
import secrets
from datetime import timedelta

from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from web.configuration import Configuration

_DATABASE_LOCATION = pathlib.Path(__file__).parent.parent / "sneek.db"
_STATIC_FOLDER = pathlib.Path(__file__).parent.parent / "static"
CONFIGURATION = Configuration.load()

app = Flask(__name__, static_folder=str(_STATIC_FOLDER), static_url_path="/")

app.config["JWT_SECRET_KEY"] = secrets.token_hex()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=CONFIGURATION.session_duration_in_hours)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{_DATABASE_LOCATION}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database = SQLAlchemy(app)
jwt = JWTManager(app)


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def serve(path):
    print(repr(path), app.static_url_path, app.static_folder)
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@jwt.expired_token_loader
def my_expired_token_callback(*_):
    return "Session is expired. Try to refresh the page.", 401
