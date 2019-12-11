import urllib3
import json
from zipfile37 import ZipFile
import glob


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


def process_files(mapping_file='convert.json'):
    with open(mapping_file, 'r') as map_file:
        mappings = json.load(map_file)

    for name in glob.glob('*.csv'):
        if name in mappings:
            print(mappings[name])


url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2019-10-11.zip"
#download_file(url)

process_files('convert.json')
