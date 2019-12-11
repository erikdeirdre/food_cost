from sqlalchemy import *
from database import (Base)

__all__ = ['MeasureUnit']


class MeasureUnit(Base):
    __tablename__ = 'measure_unit'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
