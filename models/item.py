from safrs import SAFRSBase
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from db import db, session, Base
from .base_model import BaseModel


class ItemModel(SAFRSBase, Base):
    db_commit = False
    __tablename__ = 'items'
    query = db.session.query_property()
    id = Column(Integer, primary_key=True)
    name = Column(String(length=80))
    price = Column(Float(precision=2))

    store_id = Column(Integer,  ForeignKey('stores.id'), nullable=False,)
    #  store = relationship('StoreModel')
    store = relationship("StoreModel", back_populates="items")

    def __init__(self, name=None, price=None, store_id=None):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter(ItemModel.name == name).first()

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
