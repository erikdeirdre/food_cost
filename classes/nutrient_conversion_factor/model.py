from sqlalchemy import *
from database import (Base)

__all__ = ['NutrientConversionFactor']


class NutrientConversionFactor(Base):
    __tablename__ = 'nutrient_conversion_factor'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
