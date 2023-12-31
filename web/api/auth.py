"""
A file for authentication

Since Sneek does not have proper authentication, this file handles the auto-generated names by ip
and their session length. This is done by a JWT token and a record in the database
"""
import hashlib
import random
import string
from datetime import datetime
from typing import Dict, Any, Optional

from flask import request, jsonify
from flask_jwt_extended import decode_token, create_access_token
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from web.base import database, app, CONFIGURATION


class User(database.Model):
    """
    A user of the app
    """
    ip = database.Column(database.Text, primary_key=True)
    name = database.Column(database.Text, nullable=False, unique=True)
    token = database.Column(database.Text, nullable=False)
    connected_to = database.Column(database.Text, database.ForeignKey('channel.name'), nullable=True)

    def serialize(self) -> Dict[str, Any]:
        """
        Returns the user as a dict
        """
        result = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del result["ip"]
        return result


def is_token_expired(token: str) -> bool:
    """
    Returns whether the given token is expired
    """
    decoded_token = decode_token(token, allow_expired=True)
    expiration_time = decoded_token["exp"]
    current_time = datetime.now().timestamp()

    return current_time > expiration_time


def create_new_user(ip: str):
    """
    Creates a new user entry based on the ip

    :param ip: the ip of the client
    """
    ip_hash = hashlib.md5((ip + random.choice(string.printable)).encode("utf-8")).hexdigest()
    while True:
        try:
            name = f"{random.choice(CONFIGURATION.name_adjectives)} {random.choice(CONFIGURATION.name_animals)}"
            token = create_access_token(identity=name)
            user = User(ip=ip_hash, name=name, token=token)
            database.session.add(user)
            database.session.commit()
            return
        except IntegrityError:
            pass  # Try to find a username that is not taken


def get_user(ip: str) -> Optional[User]:
    """
    Returns a user with the given ip

    :param ip: the ip of the desired user
    :return: the user or None if it does not exist
    """
    hashes = [hashlib.md5((ip + pepper).encode("utf-8")).hexdigest() for pepper in string.printable]
    return User.query.filter(User.ip.in_(hashes)).first()


@app.route("/api/user_data")
def user_data():
    request_ip = request.remote_addr
    user = get_user(request_ip)
    if not user or is_token_expired(user.token):
        if user:
            database.session.delete(user)
        create_new_user(request_ip)
        user = get_user(request_ip)
    return jsonify(user.serialize())
