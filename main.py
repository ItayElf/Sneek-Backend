"""
The main file
"""
from web import create_channels
from web.base import app, database, CONFIGURATION


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def main():
    with app.app_context():
        database.drop_all()
        database.create_all()
        create_channels(CONFIGURATION.channels)
    app.run()


if __name__ == '__main__':
    main()
