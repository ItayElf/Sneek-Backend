"""
A file for authentication

Since Sneek does not have proper authentication, this file handles the auto-generated names by ip
and their session length. This is done by a JWT token and a record in the database
"""
from web.base import database


class User(database.Model):
    """
    A user of the app
    """
    ip = database.Column(database.String(50), primary_key=True)
    name = database.Column(database.String(100), nullable=False, unique=True)
    token = database.Column(database.String(100), nullable=False)
