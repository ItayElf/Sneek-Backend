"""
The main file
"""
from _socket import gethostname

from web import create_channels
from web.base import app, database, CONFIGURATION


def setup():
    with app.app_context():
        database.drop_all()
        database.create_all()
        create_channels(CONFIGURATION.channels)


if __name__ == '__main__':
    setup()
    # This is so that pythonanywhere won't run this line
    if 'liveconsole' not in gethostname():
        app.run(host="0.0.0.0")
