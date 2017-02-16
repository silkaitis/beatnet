import os

import cPickle as pkl
import psycopg2 as pg2

from beatport_api import beatport, sqlport
from essentia_api import essentia_api
from time import time, sleep
from pymongo import MongoClient
from __future__ import print_function

def build_artist_table(bprt, name):
    '''
    Build artist table
    '''
    artists = bprt.find_all_artists_by_genre_id(1)

    slpt = sqlport(name)
    slpt.build_artist_table(artists)
    return

if __name__ == '__main__':
    now = time()
    '''
    Initialize Beatport API session
    '''
    bprt = beatport('/home/ubuntu/new_release_prediction/mykeys.yaml')
    bprt.initialize()

    '''
    Build SQL table of all artists
    '''
    # build_artist_table(bprt, 'danius')

    '''
    Extract audio features for sub-set of tracks
    '''
    with open('track_id_set.pkl', 'r') as fin:
        trk_id_set = pkl.load(fin)

    trk_id_set = list(trk_id_set)

    n_trks = len(trk_id_set)

    '''
    Initialize MongoDB connection
    '''
    client = MongoClient()
    db = client['beatport']
    audio_feat = db['audio_features']

    for i, trk in enumerate(trk_id_set):

        if bool(audio_feat.find_one({'track_id':str(trk)})):

            print('{} exists, skipped.'.format(i))

        else:

            print('{} of {} complete'.format(i, n_trks))

            essentia = essentia_api(audio_feat)

            fname = bprt.save_track_snippet(trk, '../samples/')

            essentia.execute(fname, audio_feat)

            os.remove(fname)

            del essentia

            with open('audio.log', 'a') as f:
                f.write('{} of {} done; trk_id:{}'.format(i, n_trks, trk))

    client.close()
