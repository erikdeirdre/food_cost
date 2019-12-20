from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from database import (Base, Attribute, Category, Component, FoodPortion,
                      MeasureUnit, Nutrient, NutrientConversionFactor,
                      NutrientDerivation, NutrientSource,
                      ProteinConversionFactor, WWIEAFoodCategory)
from sqlalchemy import (create_engine, MetaData)
from sqlalchemy.orm import (sessionmaker, scoped_session)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                       convert_unicode=True)
metadata = MetaData(engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.query = db_session.query_property()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database with proper tables"""
    Base.metadata.create_all(bind=db.engine)
    db.session.commit()
    print("Initialized the database")


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
