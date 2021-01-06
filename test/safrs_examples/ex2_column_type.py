#!/usr/bin/env python
#
# column type example: declare a column type for input validation and serialization
#
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI, ValidationError
from sqlalchemy.types import TypeDecorator
from db import db

db = SQLAlchemy()


class EmailType(TypeDecorator):
    """
        example class to perform email validation
        DB Email Type class: validates email address when bound
    """

    impl = db.String(100)

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value:
            if "@" not in value:
                raise ValidationError("Email Validation Error {}".format(value))

        return value


class User(SAFRSBase, db.Model):
    """
        description: User description
    """

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(EmailType)


def create_api(app, HOST="localhost", PORT=5000, API_PREFIX=""):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(User)
    user = User(name="test", email="email@x.org")
    print("Starting API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))
    admin = Admin(app, url="/admin")
    admin.add_view(sqla.ModelView(User, db.session))


def create_app(config_filename=None, host="localhost"):
    app = Flask("demo_app")
    app.secret_key = "not so secret"
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite://")
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_api(app, host)
    return app


host = "localhost"
app = create_app(host=host)

if __name__ == "__main__":
    app.run(host=host)
