import os

import numpy as np

from essentia.standard import Extractor, MonoLoader
from pymongo import MongoClient

class essentia_api(object):
    '''
    Interface to Essentia Extractor Algorithm. Configure desired summary
    statistics for applicable features (mean or median).

    INPUT
        fname - location of file to analyze, STR
    OUTPUT
        summary - Acoustic features for provided file, JSON
    '''

    def __init__(self, feature_mean=True, feature_median=True):
        self.f_mean = feature_mean
        self.f_median = feature_median
        self.summary = {}

    def _mongo(self):
        '''
        Initialize MongoDB connection
        '''
        client = MongoClient()
        db = client['beatport']
        audio_feat = db['audio_features']

        return(client, audio_feat)

    def _mongo_close(self, client):
        '''
        Close MongoDB connection
        '''
        client.close()
        return

    def load(self, fname):
        '''
        Load audio file
        '''
        loader = MonoLoader(filename=fname)

        self.audio = loader()

        self.title = fname.split('/')[-1].replace('.mp3', '')

        return

    def extract(self):
        '''
        Extract features from audio using Extractor algorithm
        '''
        ext_algo = Extractor()

        self.features = ext_algo(self.audio)

        return

    def _feature_mean(self, old_key, new_key):
        '''
        Summarize feature using mean
        '''
        self.summary[new_key + '_mean'] = np.mean(self.features[old_key], axis=0).tolist()

        return

    def _feature_median(self, old_key, new_key):
        '''
        Summarize feature using median
        '''
        self.summary[new_key + '_median'] = np.median(self.features[old_key], axis=0).tolist()

        return

    def _summary(self):
        '''
        Collect all features
        '''
        for key in self.features.descriptorNames():
            new_key = key.replace('.', '_')

            #Essentia has a .isSingleValue method but it does not
            #function as intended.
            length = len(np.array(self.features[key]).shape)

            if (length > 0) and (key != 'tonal.chords_progression'):

                if self.f_mean:

                    self._feature_mean(key, new_key)

                if self.f_median:

                    self._feature_median(key, new_key)

            else:

                self.summary[new_key] = self.features[key]

        return

    def export(self):
        '''
        Save audio features to summary file
        '''
        self._summary()

        client, tbl = self._mongo()

        tbl.insert_one({'track_id':self.title , 'details' : self.summary})

        self._mongo_close(client)

        return

    def reset(self):
        '''
        Reset variables
        '''
        self.summary = {}
        self.title = None
        self.audio = None
        self.features = None

        return

    def execute(self, fname):
        '''
        Execute entire process for extracting audio features
        '''
        self.load(fname)

        self.extract()

        self.export()

        self.reset()

        return
