import psycopg2 as pg2

from beatport_api import beatport, sqlport

def build_artist_table(btpt):
    '''
    Build artist table
    '''
    artists = btpt.find_all_artists_by_genre_id(1)

    slpt = sqlport()
    slpt.build_artist_table(artists)
    return


if __name__ == '__main__':
    '''
    Build or rebuild Beatport SQL tables
    '''
    btpt = beatport('/home/ubuntu/beatnet/mykeys.yaml')
    btpt.initialize()

    build_artist_table(btpt)
