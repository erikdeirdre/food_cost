import os
import urllib3
import json
import csv
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import pandas as pd
from zipfile37 import ZipFile
import glob
from database import (Category, Attribute, Component, FoodPortion,
                      MeasureUnit, Nutrient, NutrientConversionFactor,
                      NutrientSource, NutrientDerivation,
                      ProteinConversionFactor, WWIEAFoodCategory)

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

engine = sa.create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
connection = engine.connect()


def download_file(url):
    file_name = url.split('/')[-1]
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)

    f = open(file_name, 'wb')
    meta = r.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    chunk_size = 8192

    with open(file_name, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)

    f.close()

    with ZipFile(file_name, 'r') as zip:
        zip.extractall()

    r.release_conn()


def convert_boolean(val):
    if val.upper() == 'Y' or val.upper() == "YES":
        return True

    return False


def load_data(file_name, table_name):
    data = pd.read_csv(file_name, skip_blank_lines=True)

    if 'food_component.csv' not in file_name:
        data.to_sql(table_name, con=engine, if_exists='replace')

    if 'food_component.csv' in file_name:
        data['pct_weight'] = pd.to_numeric(
            data['pct_weight'], errors='coerce'
        ).fillna(0).astype('float')
        data['is_refuse'] = data['is_refuse'].apply(convert_boolean)
        data['min_year_acquired'] = pd.to_numeric(
            data['min_year_acquired'], errors='coerce'
        ).fillna(0).astype('int64')
        data.to_sql(table_name, con=engine, if_exists='replace')


url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2019-10-11.zip"
download_file(url)

with open("convert.json") as json_file:
    mappings = json.load(json_file)
    for file_name in glob.glob('*.csv'):
        if file_name in mappings:
            load_data(file_name, mappings[file_name]['model'])
