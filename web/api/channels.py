"""
A file for sending messages in channels
"""
from typing import Any, Dict, List

from web import database


class Channel(database.Model):
    """
    A class that represents a channel in the app
    """
    name = database.Column(database.String(100), primary_key=True)
    max_participants = database.Column(database.Integer)

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
