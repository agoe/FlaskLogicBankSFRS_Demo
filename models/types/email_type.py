from safrs import ValidationError
from sqlalchemy import TypeDecorator
from db import db


class EmailType(TypeDecorator):
    """
        example class to perform email validation
        DB Email Type class: validates email address when bound
    """

    def process_literal_param(self, value, dialect):
        pass

    impl = db.String(767)

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value:
            if "@" not in value:
                raise ValidationError("Email Validation Error {}".format(value))
        return value
