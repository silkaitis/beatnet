from collections import defaultdict

class tracklister(object):
    '''
    Class to build track list from M3U8 generated by Rekordbox
    '''

    def __init__(self, fname):
        self.filename = fname

    def read_file(self):
        '''
        Read lines of file and store
        '''
        self.lines = []
        string = ''
        with open(self.filename, 'r') as f:

            for line in f.read():

                string += line

                if line == '\n':
                    self.lines.append(string)
                    string = ''

        return

    def read_tracks(self):
        '''
        Transform file into better format
        '''
        soln = []

        for track in self.lines:
            if track[0:7] == '#EXTINF':
                pos = track.find(',') + 1
                soln.append(track[pos:])

        self.tracks = self.strip_return(soln)

        return

    def strip_last_return(self, tracks):
        '''
        Remove the carriage return from last track
        '''
        tracks = [track.strip('\r\n') for track in tracks]

        return(tracks)

    def build(self):
        '''
        Build track list and return list
        '''
        self.collection = defaultdict(list)

        for track in self.tracks:
            trk = track.split(' - ')
            self.collection[trk[0]].append(trk[1])

        return
