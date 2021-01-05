from safrs import SAFRSBase
from db import db
from models.base_model import BaseModel

#  class Book(SAFRSBase, db.Model):


class Book(SAFRSBase, db.Model):
    """
        description: Book description
    """
    db_commit = False
    __tablename__ = "Books"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, default="")
    user_id = db.Column(db.String, db.ForeignKey("Users.id"))
    user = db.relationship("User", back_populates="books")