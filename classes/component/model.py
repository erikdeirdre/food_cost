from sqlalchemy import *
from database import (Base)

__all__ = ['Component']


class Component(Base):
    __tablename__ = 'component'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    name = Column(String)
    pct_weight = Column(Float)
    is_refuse = Column(Boolean)
    gram_weight = Column(String)
    data_points = Column(Integer)
    min_year_acquired = Column(Integer)
