import os
import urllib3
import json
import logging
from sqlalchemy import create_engine
import pandas as pd
from zipfile37 import ZipFile
import glob
from database import (Category, Attribute, Component, FoodPortion,
                      MeasureUnit, Nutrient, NutrientConversionFactor,
                      NutrientSource, NutrientDerivation,
                      ProteinConversionFactor, WWIEAFoodCategory)
from config import Config


def cleanup(dir):
    logging.info('Cleaning up, directory: {}'.format(dir))
    try:
        map(os.unlink, glob.glob(os.path.join(dir, "*")))
    except FileNotFoundError as F:
        logging.info('Directory, {}, not found ... creating'.format(dir))
        os.mkdir(dir)


def download_file(url, dir):
    cleanup(dir)

    file_name = url.split('/')[-1]
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False, )

    f = open(os.path.join(dir, file_name), 'wb')
    meta = r.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    logging.info("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    chunk_size = 8192

    with open(os.path.join(dir, file_name), 'wb') as out:
        while True:
            data = r.read(chunk_size)
            file_size_dl += chunk_size
            logging.info("Downloaded: {} of {} Bytes".format(
                file_size_dl, file_size))
            if not data:
                break
            out.write(data)

    f.close()

    logging.info('Unzipping ... {}'.format(file_name))
    with ZipFile(os.path.join(dir, file_name), 'r') as zip:
        zip.extractall(dir)

    r.release_conn()


def convert_boolean(val):
    if val.upper() == 'Y' or val.upper() == "YES":
        return True

    return False


def load_data(file_name, table_name):
    logging.info('Processing file: {}, table: {}'.format(
        file_name, table_name))

    logging.debug('Reading csv file: {}'.format(file_name))

    data = pd.read_csv(file_name, skip_blank_lines=True)

    logging.debug('Posting data into table: {}'.format(table_name))
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

    logging.debug('Finished posting data to table: {}'.format(table_name))


def main():
    logging.info('Starting ...')

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    URL = os.environ.get('GOVT_DATA_URL') or \
        'https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2019-12-17.zip'

    DATA_DIR = os.environ.get('DATA_DIR') or 'data'
    DATA_DIR = os.path.join(BASE_DIR, DATA_DIR)

    CONFIG_FILE = os.environ.get('CONFIG_FILE') or 'convert.json'
    CONFIG_FILE = os.path.join(BASE_DIR, CONFIG_FILE)

    download_file(URL, DATA_DIR)

    with open(CONFIG_FILE) as json_file:
        logging.debug('Loading config file: {}'.format(CONFIG_FILE))
        mappings = json.load(json_file)
        logging.debug('Finished loading config file: {}'.format(CONFIG_FILE))

        for file_name in glob.glob(os.path.join(DATA_DIR, '*.csv')):
            if file_name in mappings:
                load_data(file_name, mappings[file_name]['model'])

    logging.info('Finished')


if __name__ == '__main__':
    main()
