import cPickle as pkl
from beatport_api import beatport

if __name__ == '__main__':

    bprt = beatport('/Users/danius/galvanize/API/mykeys.yaml')
    bprt.initialize()

    yrs = range(1990,2017)

    trk_ids = set()
    for yr in yrs:
        print 'Processing {}'.format(yr)

        start = str(yr) + '-01-01'
        stop = str(yr) + '-12-31'

        result = bprt.tracks_w_dates(start, stop)

        for key in result.keys():
            trk_ids.add(key)

    with open('track_id_set.pkl', 'w') as fin:
        pkl.dump(trk_ids, fin)
