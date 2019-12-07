from sqlalchemy import *
from database import (Base)

__all__ = ['NutrientDerivation']


class NutrientDerivation(Base):
    __tablename__ = 'nutrient_derivation'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    seq_num = Column(Integer)
    amount = Column(Integer)
    measure_unit_id = Column(Integer)
    portion_description = Column(String(200))
    modifier = Column(String(50))
    gram_weight = Column(Integer)
    data_points = Column(Integer)
    footnote = Column(String(50))
    min_year_acquired = Column(String(10))
