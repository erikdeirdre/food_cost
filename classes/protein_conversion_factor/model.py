from sqlalchemy import *
from database import (Base)

__all__ = ['ProteinConversionFactor']


class ProteinConversionFactor(Base):
    __tablename__ = 'protein_conversion_factor'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
