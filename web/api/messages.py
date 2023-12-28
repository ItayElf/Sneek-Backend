"""
A file for handling messages in channels
"""
import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, inspect

from web import database, app, User, Channel


class Message(database.Model):
    """
    A class that represents a message

    Supported message types: "text"
    """
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    sent_at = database.Column(database.DateTime(timezone=True), server_default=func.now(), nullable=False)
    expired_at = database.Column(database.DateTime(timezone=True), server_default=func.now(), nullable=False)
    message_type = database.Column(database.Text, nullable=False)
    content = database.Column(database.Text, nullable=False)
    channel = database.Column(database.Text, database.ForeignKey('channel.name'), nullable=True)
    sent_by = database.Column(database.Text, database.ForeignKey('user.name'), nullable=True)

    def serialize(self):
        result = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del result["channel"]
        del result["id"]
        return result


@app.route("/api/messages")
@jwt_required()
def get_messages():
    now = datetime.datetime.now()
    username = get_jwt_identity()
    user = User.query.filter_by(name=username).first()
    if not user:
        return f"User {username} was not found", 404
    if user.connected_to is None:
        return "User is not connected to a channel", 400
    messages = Message.query.filter_by(channel=user.connected_to).filter(Message.expired_at > now).all()
    return jsonify([message.serialize() for message in messages])


@app.route("/api/messages/text", methods=["POST"])
@jwt_required()
def write_text_messages():
    username = get_jwt_identity()
    user = User.query.filter_by(name=username).first()
    content = request.json.get("content", "")
    if not user:
        return f"User {username} was not found", 404
    if user.connected_to is None:
        return "User is not connected to a channel", 400
    if not content:
        return "Cannot send a message without any content", 400
    channel = Channel.query.filter_by(name=user.connected_to).first()
    now = datetime.datetime.now()
    expired = now + datetime.timedelta(seconds=channel.message_duration)
    message = Message(sent_at=now, expired_at=expired, message_type="text", content=content, channel=channel.name,
                      sent_by=username)
    database.session.add(message)
    database.session.commit()
    return "", 200
