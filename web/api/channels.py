"""
A file for sending messages in channels
"""
from typing import Any, Dict, List

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from web import database, User, app


class Channel(database.Model):
    """
    A class that represents a channel in the app
    """
    name = database.Column(database.String(100), primary_key=True)
    max_participants = database.Column(database.Integer)

    def get_connected_participants(self) -> int:
        """
        Returns how many users are currently connected to this channel
        """
        return len(User.query.filter_by(connected_to=self.name).all())

    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the channel and returns its data as a dict
        """
        return {
            "name": self.name,
            "max_participants": self.max_participants,
            "connected_participants": self.get_connected_participants()
        }

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        """
        Returns a channel from a json

        :param data: the json that represents the channel
        """
        return cls(**data)


def create_channels(channels: List[Dict[str, Any]]):
    """
    Insets a given list of channels to the database

    :param channels: the channels to insert
    """
    for channel in channels:
        database.session.add(Channel.from_json(channel))
    database.session.commit()


@app.route("/api/channels")
def get_channels():
    channels = Channel.query.all()
    return jsonify([channel.serialize() for channel in channels])


@app.route("/api/channels/join", methods=["POST"])
@jwt_required()
def join_channel():
    username = get_jwt_identity()
    user = User.query.filter_by(name=username).first()
    if not user:
        return f"User {username} was not found", 404
    channel_name = request.json.get("channel", "")
    channel = Channel.query.filter_by(name=channel_name).first()
    if not channel:
        return f"Channel {channel_name} does not exists", 404
    if channel.max_participants is not None and channel.get_connected_participants() >= channel.max_participants:
        return "Channel is full", 400
    if user.connected_to == channel.name:
        return "Already connected to channel", 400
    user.connected_to = channel_name
    database.session.commit()
    return "", 200
