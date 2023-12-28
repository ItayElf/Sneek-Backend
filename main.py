"""
The main file
"""
import pathlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

home_directory = pathlib.Path(__file__).parent.absolute()

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{home_directory / 'sneek.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def main():
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run()


if __name__ == '__main__':
    main()
