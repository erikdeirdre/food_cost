import urllib3
import json
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zipfile37 import ZipFile
import glob
from classes import (Category, Attribute, Component,
                    MeasureUnit)
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


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


def process_attribute_file(csv_file, mappings):
    attribute = Attribute()
    session = Session()

    line_count = 0
    buffer = []

    with open(csv_file) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            if line_count:
                buffer.append(
                    Attribute(
                        id=row[0],
                        fdc_id=row[1],
                        seq_num=row[2],
                        food_attribute_type_id=row[3],
                        name=row[4],
                        value=row[5]
                    )
                )
                if len(buffer) % 10000 == 0:
                    session.bulk_save_objects(buffer)
                    buffer = []
            line_count += 1

        session.bulk_save_objects(buffer)

    print(f'Processed {line_count} lines.')


def process_files(mapping_file='convert.json'):
    with open(mapping_file, 'r') as map_file:
        mappings = json.load(map_file)

    for file_name in glob.glob('*.csv'):
        if file_name in mappings:
            if mappings[file_name]['model'] == 'attribute':
                process_attribute_file(file_name, mappings[file_name])


url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2019-10-11.zip"
#download_file(url)

process_files('convert.json')
