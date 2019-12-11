from sqlalchemy import *
from database import (Base)

__all__ = ['Attribute']


class Attribute(Base):
    __tablename__ = 'food_attribute'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    seq_num = Column(Integer)
    food_attribute_type_id = Column(Integer)
    name = Column(String)
    value = Column(String)
