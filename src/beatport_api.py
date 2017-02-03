from __future__ import unicode_literals

import yaml
import requests
import urllib
import sys

from rauth import OAuth1Service
from IPython.core.display import clear_output

class beatport(object):

    def __init__(self, keys_filename):
        self.keys_fname = keys_filename
        self.base_url = 'https://oauth-api.beatport.com/catalog/3/'

    def _setup_progress_bar(self, num_pages):
        '''
        '''
        toolbar_width = 40

        # setup toolbar
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

        increment = num_pages / float(toolbar_width)

        return(increment)

    def _update_progress_bar(self, curr_page, increment):

        if curr_page > increment:
            # update the bar
            sys.stdout.write("-")
            sys.stdout.flush()

            increment += increment

        return(increment)

    def _escape_progress_bar(self):
        sys.stdout.write("\n")
        return

    def _access(self, fname):
        with open(fname, 'r') as f:
            keys = yaml.load(f)

        login = keys['Beatport_Login']
        pswd = keys['Beatport_Pass']
        key = keys['Beatport_Key']
        secret = keys['Beatport_Secret']

        return(login, pswd, key, secret)

    def _container(self, key, secret):

        OAuth = OAuth1Service(name = 'beatport',
                                    consumer_key = key,
                                    consumer_secret = secret,
                                    request_token_url= 'https://oauth-api.beatport.com/identity/1/oauth/request-token',
                                    access_token_url='https://oauth-api.beatport.com/identity/1/oauth/access-token',
                                    authorize_url='https://oauth-api.beatport.com/identity/1/oauth/authorize',
                                    base_url='https://oauth-api.beatport.com/json/catalog')
        return(OAuth)

    def _req_token_secret(self, OAuth):

        req_token, req_token_secret = OAuth.get_request_token(method = 'POST',
                                                         data = {'oauth_callback': 'http://www.ritcheydnb.com'})

        return(req_token, req_token_secret)

    def _auth_url(self, OAuth, req_token):

        return(OAuth.get_authorize_url(req_token))

    def _fetch_access(self, OAuth, req_token, req_token_secret, login, pswd):
        values = {'oauth_token': req_token,
                  'username': login,
                  'password': pswd,
                  'submit': 'Login'}

        r = requests.post('https://oauth-api.beatport.com/identity/1/oauth/authorize-submit',
                          data = values)

        verifier = r.url.split('oauth_verifier=', 1)[1]

        tokens = OAuth.get_raw_access_token(req_token,
                                               req_token_secret,
                                               method = 'POST',
                                               data = {'oauth_verifier': verifier})
        token_string = tokens.content

        access_token = token_string[token_string.find('=')+1:token_string.find('&')]
        access_token_secret = token_string[token_string.find('t=')+2:token_string.rfind('&s')]

        return(access_token, access_token_secret)

    def initialize(self):
        '''
        Start API session
        '''

        login, pswd, key, secret = self._access(self.keys_fname)

        OAuth = self._container(key, secret)

        req_token, req_token_secret = self._req_token_secret(OAuth)

        auth_url = self._auth_url(OAuth, req_token)

        acc_token, acc_token_secret = self._fetch_access(OAuth,
                                                         req_token,
                                                         req_token_secret,
                                                         login,
                                                         pswd)

        self.session = OAuth.get_session((acc_token, acc_token_secret))
        print('Session created')
        return

    def find_artist_id(self, artist):
        '''
        Find Beatport artist ID from their name

        INPUT:
            artist - artist name, STR
        OUTPUT:
            artist_id - INT
        '''
        qry = self.session.get(base_url+'artists',
                               params = {'facets': 'artistName:' + artist}).json()

        if len(qry) == 0:
            return('Artist not found')
        elif len(qry) > 1:
            return('Multiple artists found')
        else:
            return(qry[0]['id'])

    def find_tracks_by_artist_id(self, artist_id):
        '''
        Find all tracks by an artist using ID

        INPUT:
            artist_id - INT
        OUTPUT:
            tracks - track name and track id, DICT
        '''
        trks = self.session \
                   .get(self.base_url+'tracks',
                       params = {'facets': 'artistId:' + str(artist_id),
                                 'perPage': 150}) \
                   .json()

        pages = trks['metadata']['totalPages']

        trk_dict = {}

        for i in xrange(pages):

            trks = self.session \
                       .get(self.base_url + 'tracks',
                            params = {'facets': 'artistId:' + str(artist_id),
                                      'perPage': 150,
                                      'page': i + 1}) \
                       .json()

            for trk in trks['results']:

                trk_dict[trk['name']] = trk['id']

        return(trk_dict)

    def find_all_artists_by_genre_id(self, genre_id):
        artists = self.session \
                      .get(self.base_url+'artists',
                           params = {'facets': 'genreID:' + str(genre_id),
                                     'perPage': 150}) \
                      .json()

        pages = artists['metadata']['totalPages']

        incr = self._setup_progress_bar(pages)

        artist_dict = {}

        for i in xrange(pages):
            artists = self.session \
                          .get(self.base_url + 'artists',
                               params = {'facets': 'genreID:' + str(genre_id),
                                         'perPage': 150,
                                         'page': i + 1}) \
                          .json()

            for art in artists['results']:

                artist_dict[art['name'].lower()] = art['id']

            incr = self._update_progress_bar(i, incr)

        self._escape_progress_bar()

        return(artist_dict)
