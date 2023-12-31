"""
A file for handling messages in channels
"""
import time

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import inspect

from encyption import AESCipher
from web import database, app, User, Channel


class Message(database.Model):
    """
    A class that represents a message

    Supported message types: "text"
    """
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    sent_at = database.Column(database.Integer, nullable=False)
    expired_at = database.Column(database.Integer, nullable=False)
    message_type = database.Column(database.Text, nullable=False)
    content = database.Column(database.LargeBinary, nullable=False)
    channel = database.Column(database.Text, database.ForeignKey('channel.name'), nullable=False)
    sent_by = database.Column(database.Text, database.ForeignKey('user.name'), nullable=False)

    def serialize(self):
        result = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del result["channel"]
        result["content"] = get_cypher().decrypt(result["content"]).decode("utf-8")
        return result


def get_cypher():
    """
    Returns the cipher with the correct key
    """
    return AESCipher(app.config["SECRET"])


@app.route("/api/messages")
@jwt_required()
def get_messages():
    now = time.time()
    username = get_jwt_identity()
    user = User.query.filter_by(name=username).first()
    if not user:
        return f"User {username} was not found", 404
    if user.connected_to is None:
        return "User is not connected to a channel", 400
    messages = Message.query.filter_by(channel=user.connected_to).filter(Message.expired_at > now).order_by(
        Message.sent_at.desc()).all()
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
    now = time.time()
    expired = now + channel.message_duration
    encrypted_content = get_cypher().encrypt(content.encode("utf-8"))
    message = Message(sent_at=now, expired_at=expired, message_type="text", content=encrypted_content,
                      channel=channel.name,
                      sent_by=username)
    database.session.add(message)
    database.session.commit()
    return "", 200
