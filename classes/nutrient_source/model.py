from sqlalchemy import *
from database import (Base)

__all__ = ['NutrientSource']


class NutrientSource(Base):
    __tablename__ = 'nutrient_source'
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    description = Column(String(200))
    source_id = Column(Integer)
