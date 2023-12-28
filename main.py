"""
The main file
"""
from web.base import app, database


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def main():
    with app.app_context():
        database.drop_all()
        database.create_all()
    app.run()


if __name__ == '__main__':
    main()
