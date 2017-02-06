import psycopg2 as pg2

from beatport_api import beatport, sqlport

def build_artist_table(bprt, name):
    '''
    Build artist table
    '''
    artists = bprt.find_all_artists_by_genre_id(1)

    slpt = sqlport(name)
    slpt.build_artist_table(artists)
    return


if __name__ == '__main__':
    '''
    Build or rebuild Beatport SQL tables
    '''
    bprt = beatport('/Users/danius/galvanize/API/mykeys.yaml')
    bprt.initialize()

    build_artist_table(bprt, 'danius')
