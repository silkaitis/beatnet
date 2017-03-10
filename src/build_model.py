import psycopg2 as pg2
import cPickle as pkl
import pandas as pd

from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import log_loss, roc_curve

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
        n = 'details.' + n
        name_dict[n] = 1

    return(collection.find({}, name_dict))

def trk_label(track_id, rkbx_set):
    '''
    Label track data with either purchased (1) or not purchased (0)
    '''
    if track_id in rkbx_set:
        return(1)
    else:
        return(0)

def extract_data(rkbx_set, names):
    '''
    Extract audio features from MongoDB

    INPUT
        names - audio feature names, LIST
        rkbx_set - track ids purchased, SET
    OUTPUT
        soln - track_id, features and label, LIST
    '''
    client, audio_features = db_connect()

    soln = []
    for doc in mongo_docs(audio_features, names):
        row = []

        row.append(int(doc['track_id']))

        row.extend([doc['details'][n] for n in names])

        row.append(trk_label(row[0], rkbx_set))

        soln.append(row)

    client.close()

    return(soln)

def expand_dataframe(row, df):
    '''
    Expand any columns that contain lists
    '''
    for r, col in zip(row, df.columns):
        if type(r) == list:
            n = len(r)

            df = df.join(pd.DataFrame(df[col].tolist(),
                                      columns = [col + str(i) for i in range(n)]))
            df = df.drop(col, axis=1)

    return(df)

def extract_features(rkbx_set, names):
    '''
    Extract data and format into DataFrame

    INPUT
        names - audio feature names, LIST
        rkbx_set - track ids purchased, SET
    OUTPUT
        soln - track_id, features and label, LIST
    '''
    cols = ['track_id']
    cols.extend(names)
    cols.append('label')

    data = extract_data(rkbx_set, names)

    df = pd.DataFrame(data, columns = cols)

    df = expand_dataframe(data[0], df)

    return(df)

def audio_keys(db_collection):
    '''
    Select audio features to use in the model
    '''
    client, audio_features = db_connect()

    feat_keys = {}

    for i, key in enumerate(sorted(audio_features.find_one()['details'].keys())):
        feat_keys[i] = key

    sub_keys = []

    single_doc = audio_features.find_one()['details']
    for key, val in feat_keys.iteritems():
        if type(single_doc[val]) == float:
            if val.split('_')[-1] != 'median':
                sub_keys.append(key)

    sub_keys.remove(88)
    sub_keys.append(13)
    sub_keys.append(104)
    sub_keys.append(3)

    cols = [feat_keys[v] for v in sub_keys]

    client.close()

    return(cols)

def collect_rkbx_tracks():
    '''
    Collect purchased track ids
    '''
    conn = pg2.connect('dbname=beatport user=danius')
    cur = conn.cursor()

    cur.execute('''
                SELECT id
                FROM rkbx_tracks;
                ''')

    data = cur.fetchall()

    return(set([val[0] for val in data]))

def save_data(obj, name):
    '''
    Pickle necessary information
    '''
    with open(name, 'w') as f:
        pkl.dump(obj, f)

    return

if __name__ == '__main__':
    cols = audio_keys()

    rkbx_set = collect_rkbx_tracks()

    df = extract_features(rkbx_set, cols)

    Xtr, Xte, ytr, yte = train_test_split(df.drop(['label', 'track_id'], axis=1), df['label'])

    model = GradientBoostingClassifier(max_features='auto',
                                       learning_rate=0.025,
                                       max_depth=3,
                                       n_estimators=400)

    model.fit(Xtr, ytr)

    y_pred = model.predict_proba(Xte)

    print('Model log loss: {:0.4f}'.format(log_loss(yte, y_pred)))

    fpr, tpr, thres = roc_curve(yte, y_pred)

    fpr_target = 0.18

    thres_select = max(thres[fpr > fpr_trgt])

    print('Positive Threshold: {}'.format(thres_select))

    save_data(thres_select, 'thres_select.pkl')
    save_data(model, 'model.pkl')
