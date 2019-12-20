from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Attribute(Base):
    __tablename__ = 'attribute'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    seq_num = Column(Integer)
    food_attribute_type_id = Column(Integer)
    name = Column(String)
    value = Column(String)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    description = Column(String)


class Component(Base):
    __tablename__ = 'component'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    name = Column(String)
    pct_weight = Column(Float)
    is_refuse = Column(Boolean)
    gram_weight = Column(Float)
    data_points = Column(Integer)
    min_year_acquired = Column(Integer)


class FoodPortion(Base):
    __tablename__ = 'portion'
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


class MeasureUnit(Base):
    __tablename__ = 'measure_unit'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))


class Nutrient(Base):
    __tablename__ = 'nutrient'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    nutrient_nbr = Column(Integer)
    rank = Column(Integer)


class NutrientConversionFactor(Base):
    __tablename__ = 'nutrient_conversion_factor'
    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)


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


class NutrientSource(Base):
    __tablename__ = 'nutrient_source'
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    description = Column(String(200))
    source_id = Column(Integer)


class ProteinConversionFactor(Base):
    __tablename__ = 'protein_conversion_factor'
    id = Column(Integer, primary_key=True)
    value = Column(Float)


class WWIEAFoodCategory(Base):
    __tablename__ = 'wweia_food_category'
    code = Column(Integer, primary_key=True)
    description = Column(String(200))
