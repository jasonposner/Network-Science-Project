# Spotipy Testing

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def kanyeAlbums():
    kanye_uri = 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.artist_albums(kanye_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])


def main():
    kanyeAlbums()

main()

# artist_top_tracks(artist_id, country = 'US') -> returns top tracks.
