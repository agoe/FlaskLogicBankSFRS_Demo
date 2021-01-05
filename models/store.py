from typing import List

from safrs import SAFRSBase
from models.types.choice_ext import ChoiceType
from sqlalchemy_utils.types.email import EmailType

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import db, Base, session
from models.item import ItemModel
from safrs.util import classproperty



class StoreModel(SAFRSBase, Base):
    __tablename__ = 'stores'
    STORE_TYPES = [
        (u'online', u'Online'),
        (u'pos', u'POS')
    ]

    query = db.session.query_property()
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=80))
    email: str = Column(EmailType(length=40))
    store_type: str = Column('type', ChoiceType(STORE_TYPES))
    item_count: int = Column(Integer)
    #  items: List[ItemModel] = relationship('ItemModel', lazy='dynamic')
    items: List['ItemModel'] = relationship("ItemModel", back_populates="store")

    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def json(self):
        item: ItemModel
#       return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items]}
        return {'id': self.id, 'name': self.name, 'email': self.email, 'type': self.store_type,
                'item_count': self.item_count}

    @classproperty
    def _s_collection_name(cls):
        return "StoreModels"

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
