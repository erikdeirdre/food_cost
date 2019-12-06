from sqlalchemy import *
from database import (Base)

__all__ = ['WWIEAFoodCategory']


class WWIEAFoodCategory(Base):
    __tablename__ = 'wweia_food_category'
    code = Column(Integer, primary_key=True)
    description = Column(String(200))
