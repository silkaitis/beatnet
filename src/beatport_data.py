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

def _setup_progress_bar(num_pages):
    curses.initscr()
    curses.curs_set(0)

    sentence = 'Page {} of {} complete.'.format(' '*len(str(num_pages)), str(num_pages))

    sys.stdout.write(sentence)
    sys.stdout.flush()

    sys.stdout.write('\b' * (len(sentence) - 5))

    return

def _update_progress_bar(curr_page):
    pg = str(curr_page)

    sys.stdout.write(pg)
    sys.stdout.flush()
    sys.stdout.write('\b' * len(pg))

    return

def _escape_progress_bar():
    sys.stdout.write('\n')
    curses.curs_set(1)
    curses.reset_shell_mode()
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

    essentia = essentia_api()

    trk_id_set = list(trk_id_set)

    _setup_progress_bar(len(trk_id_set))

    for i, trk in enumerate(trk_id_set):

        _update_progress_bar(i)

        fname = bprt.save_track_snippet(trk_id_set[i], '../samples/')

        essentia.execute(fname)

        os.remove(fname)

        sleep(random.sample([0.5,1,1.5,2], 1)[0])

    _escape_progress_bar()

    t = (time() - now) * (1/60.)

    print('Collection tagging took {} minutes'.format(t))
