from pymongo import MongoClient
import pandas as pd
import json
from os import listdir
from os.path import isfile, join

password = 'filmfinder'
user = 'filmfinder'
dbname = 'SimMatrix'
client = MongoClient(f"mongodb+srv://filmfinder:{password}@simmatrix.wmevb.mongodb.net/{dbname}?retryWrites=true&w=majority")

def keys_to_int(x):
    return {int(k): v for k, v in x if not isinstance(k, str)}

def write_data_to_mongo(csvfile, client, collectionName):
    chunksize, index = 100, 0
    for chunk in pd.read_csv(csvfile, chunksize=chunksize):
        records = json.loads(chunk.T.to_json()).values()
        # records = keys_to_int(records.)
        if records:
            client[dbname][collectionName].insert_many(records)
            index += 1
            print(f'inserted {index*chunksize} records of {csvfile}')


mypath = 'reco_data'


def get_files():

    allFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    csvFiles = [f for f in allFiles if f.endswith('.csv')]
    return csvFiles


def read_file_to_push():
    csvFiles = get_files()
    for csvFile in csvFiles:

        # Splitting as the name is same in mongo client
        collectionName = csvFile.split('.')[0]
        csvFile = join(mypath, csvFile)
        write_data_to_mongo(csvFile, client, collectionName)

# read_file_to_push()
mat = 'movie_movie'
f = join(mypath, mat)
f = f + '.csv'


write_data_to_mongo(f, client, mat)
