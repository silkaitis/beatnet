import json

from essentia.standard import Extractor, MonoLoader

class essentia_api(object):
    '''
    Interface to Essentia Extractor Algorithm. Configure desired summary
    statistics for applicable features (mean or median).

    INPUT
        fname - location of file to analyze, STR
    OUTPUT
        summary - Acoustic features for provided file, JSON
    '''

    def __init__(self, summary_file, feature_mean=True, feature_median=True):
        self.f_mean = feature_mean
        self.f_median = feature_median
        self.summary = {}
        self.fsum = summary_file

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

    def _feature_mean(self, label):
        '''
        Summarize feature using mean
        '''
        self.summary[label + '.mean'] = np.mean(self.features[label], axis=0)

        return

    def _feature_median(self, label):
        '''
        Summarize feature using median
        '''
        self.summary[label + '.median'] = np.median(self.features[label], axis=0)

        return

    def _summary(self):
        '''
        Collect all features
        '''
        for key in self.features.descriptorNames():

            #Essentia has a .isSingleValue method but it does not
            #function as intended.
            shape = len(np.array(self.features[key]).shape)

            if shape > 0:

                if self.f_mean:

                    self._feature_mean(key)

                if self.f_median:

                    self._feature_median(key)

            else:
                self.summary[key] = self.features[key]

        return

    def export(self):
        '''
        Save audio features to summary file
        '''
        self._summary()

        if os.path.exists(self.fsum):

            with open(self.fsum, 'a') as fin:

                fin.write("{}\n".format(json.dumps({self.title : self.summary})))

        else:

            print('Need to create empty summary JSON file first')

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
