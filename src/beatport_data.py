import os

import cPickle as pkl
import psycopg2 as pg2

from beatport_api import beatport, sqlport
from essentia_api import essentia_api
from time import time, sleep

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
    bprt = beatport('/Users/danius/galvanize/API/mykeys.yaml')
    bprt.initialize()

    '''
    Build SQL table of all artists
    '''
    # build_artist_table(bprt, 'danius')

    '''
    Extract audio features for sub-set of tracks
    '''
    with open('../data/track_id_set.pkl', 'r') as fin:
        trk_id_set = pkl.load(fin)

    trk_id_set = list(trk_id_set)

    for i, trk in enumerate(trk_id_set):

        essentia = essentia_api()

        fname = bprt.save_track_snippet(trk_id_set[i], '../samples/')

        essentia.execute(fname)

        os.remove(fname)

        del essentia

        sleep(random.sample([0.5, 1, 1.5], 1)[0])

    t = (time() - now) * (1/60.)

    print('Collection tagging took {} minutes'.format(t))
