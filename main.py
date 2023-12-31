"""
The main file
"""

from web import create_channels
from web.base import app, database, CONFIGURATION


def main():
    with app.app_context():
        database.drop_all()
        database.create_all()
        create_channels(CONFIGURATION.channels)
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
