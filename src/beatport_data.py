import os

import cPickle as pkl
import psycopg2 as pg2

from beatport_api import beatport, sqlport
from time import time, sleep
from pymongo import MongoClient

def build_artist_table(bprt, name):
    '''
    Build artist table
    '''
    artists = bprt.artists_w_genre_id(1)

    slpt = sqlport(name)
    slpt.build_artist_table(artists)
    return

def update_trk_pkl(name, data):
    '''
    Remove old set of trk_ids and update
    '''

    with open(name, 'w') as f:
        pkl.dump(data, f)

    return

def trk_to_eval():
    '''
    Extract audio features for sub-set of tracks
    '''
    with open('track_id_set.pkl', 'r') as fin:
        trk_id_set = pkl.load(fin)

    trk_id_list = list(trk_id_set)

    n_trks = len(trk_id_list)

    return(trk_id_list, n_trks)

def build_audio_db():
    from essentia_api import essentia_api

    trk_id_list, n_trks = trk_to_eval()

    '''
    Initialize MongoDB connection
    '''
    client = MongoClient()
    db = client['beatport']
    audio_feat = db['audio_features']

    for i, trk in enumerate(trk_id_list):

        if bool(audio_feat.find_one({'track_id':str(trk)})):

            print('{} exists, skipped.'.format(i))

        else:

            print('{} tracks left'.format(n_trks - i))

            essentia = essentia_api(audio_feat)

            fname = bprt.save_track_snippet(trk, '../samples/')

            try:
                essentia.execute(fname, audio_feat)

                os.remove(fname)

                del essentia

                with open('audio.log', 'a') as f:

                    f.write('{} track left; trk_id {} done.\n'.format(n_trks - i, trk))

                    trk_id_set.remove(trk)

                    update_trk_pkl('track_id_set.pkl', trk_id_set)

            except Exception:

                os.remove(fname)

                with open('audio_fail.log', 'a') as f:

                    f.write('trk_id {} failed\n'.format(trk))

    client.close()
    return

if __name__ == '__main__':
    now = time()
    '''
    Initialize Beatport API session
    '''
    bprt = beatport('/Users/danius/galvanize/API/mykeys.yaml')
    bprt.initialize()

    '''
    Build SQL table of all artists
    '''
    build_artist_table(bprt, 'danius')
