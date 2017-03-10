import os, sys

from beatport_api import beatport, sqlport
from pymongo import MongoClient
from essentia_api import essentia_api

def mongo_connect():
    '''
    Initialize MongoDB connection
    '''
    client = MongoClient()
    db = client['beatport']
    new_releases = db['new_releases']

    return(client, new_releases)

def analyze_new_releases(db_collection, tracks):
    '''
    Extract audio features from new releases
    '''
    n_trks = len(tracks)
    
    for i, trk in enumerate(list(tracks)):

        if bool(db_collection.find_one({'track_id':str(trk)})):

            print('{} exists, skipped.'.format(i))

        else:

            print('{} tracks left'.format(n_trks - i))

            essentia = essentia_api(db_collection)

            fname = bprt.save_track_snippet(trk, '../samples/')

            try:
                essentia.execute(fname, db_collection)

                os.remove(fname)

                del essentia

                with open('release.log', 'a') as f:

                    f.write('trk_id {} passed\n'.format(n_trks - i, trk))

            except Exception:

                os.remove(fname)

                with open('release.log', 'a') as f:

                    f.write('trk_id {} failed\n'.format(trk))

    return

if __name__ == '__main__':
    '''
    Initialize Beatport API session
    '''
    bprt = beatport('/home/ubuntu/new_release_prediction/mykeys.yaml')
    bprt.initialize()

    '''
    Fetch Track IDs in Date Range
    '''
    new_release_ids = bprt.tracks_w_dates(sys.argv[1], sys.argv[2])

    '''
    Analyze New Releases
    '''
    client, db_collection = mongo_connect()

    analyze_new_releases(db_collection, new_release_ids)

    client.close()
