from typing import List
from safrs import SAFRSBase
from db import db
from models.base_model import BaseModel


class User(SAFRSBase, db.Model):
    """
        description: User description
    """
    #  db_commit = False;
    __tablename__ = "Users"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, default="")
    email = db.Column(db.String, default="")
    books: List = db.relationship("Book", back_populates="user", lazy="dynamic")