from sqlalchemy import *
from database import (Base)

__all__ = ['Category']


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    description = Column(String)
