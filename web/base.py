"""
A file for the configuration of the flask app

This file is needed so that the app and the database could be accessible in other files
"""
import pathlib
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DATABASE_LOCATION = pathlib.Path(__file__).parent.parent / "sneek.db"

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = secrets.token_hex()
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_LOCATION}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
