import psycopg2 as pg2
import cPickle as pkl
import numpy as np

from pymongo import MongoClient

def db_connect():
    '''
    Connect to mongodb-org-3
    '''
    client = MongoClient()
    db = client['beatport']
    return(client, db['audio_features'])

def rkbx_tracks(fname):
    '''
    Fetch track ids from the Rekordbox collection
    '''
    with open(fname, 'r') as f:
        return(pkl.load(f))

def mongo_docs(collection, name):
    '''
    Extract feature from MongoDB
    '''
    name_dict = {'track_id':1}

    for n in name:
        name_dict['details.' + name] = 1

    return(collection.find({}, name_dict))

def trk_label(track_id, rkbx_set):
    '''
    Label track data with either purchased (1) or not purchased (0)
    '''
    if track_id in rkbx_set:
        return(1)
    else:
        return(0)

def extract_features(rkbx_set, name):
    '''
    Extract audio features from MongoDB

    INPUT
        name - audio feature names, LIST
    OUTPUT
        arr - track_id, features and label, NumPy array
        columns - Column names, LIST
    '''
    client, audio_features = db_connect()

    soln = []
    for doc in mongo_docs(audio_features, name):
        row = []

        row.append(doc['track_id'])

        row.extend([doc['details'][n] for n in name])

        row.append(rk_label(row[0], rkbx_set))

        soln.append(row)

    client.close()

    return(np.array(soln))
