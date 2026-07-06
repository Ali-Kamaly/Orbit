from dotenv import load_dotenv
import os, spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-private"
    )
)

def search_track(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q = query, type = 'track')
    items = results["tracks"]["items"]
    if len(items)==0:
        return 
    track = results["tracks"]["items"][0]

    song_name = track["name"]
    artist = track["artists"][0]["name"]
    spotify_url = track["external_urls"]["spotify"]
    album = track["album"]["name"]
    cover = track["album"]["images"][0]["url"]

    return spotify_url, album, cover

def extract_track_id(spotify_url):
    if "track/" not in spotify_url:
        print("not valid")
        return None
    
    track_id = spotify_url.split('track/')[1].split('?')[0]
    return track_id

def extract_playlist_id(spotify_url):
    if "playlist/" not in spotify_url:
        print("invalid playlist link")
        return None
    
    playlist_id = spotify_url.split('playlist/')[1].split('?')[0]
    return playlist_id

def get_tracks_from_playlist(spotify_url):
    playlist_id = extract_playlist_id(spotify_url)
    print(playlist_id)
    if playlist_id is None:
        return None, "invalid link"
    
    try:
        results = sp.playlist_items(playlist_id)
    except spotipy.exceptions.SpotifyException:
        return None, "no access"
    song_names = []
    artists = []

    while results: 

        for song in results['items']:
            print(song)
            if song is None:
                continue
            track = song['item']
            song_names.append(track['name'])
            artist_names = ';'.join([artist['name'] for artist in track['artists']])
            artists.append(artist_names)

        if results['next']:
            results = sp.next(results)
        else:
            break
    return song_names, artists

def get_track_from_track_url(spotify_url):
    track_id = extract_track_id(spotify_url)
    print(track_id)
    if track_id is None:
        return None
    
    track = sp.track(track_id)
    track_name = track['name']
    artists = ';'.join([artist['name'] for artist in track['artists']])
    print(track_name, artists)
    return track_name, artists

get_tracks_from_playlist("https://open.spotify.com/playlist/0UpZYECCrXxyoprMaSAX9R")