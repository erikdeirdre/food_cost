from sqlalchemy import *
from database import (Base)

__all__ = ['Nutrient']


class Nutrient(Base):
    __tablename__ = 'nutrient'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    nutrient_nbr = Column(Integer)
    rank = Column(Integer)
