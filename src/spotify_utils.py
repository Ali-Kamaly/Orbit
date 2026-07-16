from dotenv import load_dotenv
import os, spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

INVALID_LINK = "invalid_link"
NO_ACCESS = "no_access"
PLAYLISTS_DISABLED = "playlists_diabled"


load_dotenv()

def get_secret(name):
    """
    Get a credential from Streamlit cloud when deployed, or from the
    local .env file when running locally
    """
    try:
        value = st.secrets[name]
    except (FileNotFoundError, KeyError):
        value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required credential {name}"
        )

    return value

CLIENT_ID = get_secret("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = get_secret("SPOTIPY_CLIENT_SECRET")

#public spotify catalogue client - works locally and on streamlit cloud without a user login
catalogue_sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET
    )
)

def create_user_client():
    return spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=get_secret("SPOTIPY_CLIENT_ID"),
        client_secret=get_secret("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=get_secret("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private playlist-read-collaborative",
        )
    )

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=get_secret("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private playlist-read-collaborative",
        cache_path = ".cache"
    )
)


def search_track(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    results = catalogue_sp.search(q = query, type = 'track')
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
        return None
    
    track_id = spotify_url.split('track/')[1].split('?')[0]
    return track_id

def extract_playlist_id(spotify_url):
    if "playlist/" not in spotify_url:
        return None
    
    playlist_id = spotify_url.split('playlist/')[1].split('?')[0]
    return playlist_id

def playlists_enabled():
    try:
        return st.secrets.get("ENABLE_PLAYLISTS", False)
    except FileNotFoundError:
        return True

def get_tracks_from_playlist(spotify_url):
    playlist_id = extract_playlist_id(spotify_url)
    if playlist_id is None:
        return None, "invalid link"
    
    if not playlists_enabled():
        return None, "playlists disabled"
    
    user_sp = create_user_client()

    try:
        results = user_sp.playlist_items(playlist_id)
    except (Exception, spotipy.exceptions.SpotifyException):
        return None, "no access"
    song_names = []
    artists = []

    while results: 

        for song in results['items']:
            if song is None:
                continue
            track = song['item']
            song_names.append(track['name'])
            artist_names = ';'.join([artist['name'] for artist in track['artists']])
            artists.append(artist_names)

        if results['next']:
            results = user_sp.next(results)
        else:
            break
    return song_names, artists

def get_track_from_track_url(spotify_url):
    track_id = extract_track_id(spotify_url)
    if track_id is None:
        return None
    
    try:
        track = catalogue_sp.track(track_id)
    except spotipy.exceptions.SpotifyException:
        return None
    track_name = track['name']
    artists = ';'.join([artist['name'] for artist in track['artists']])
    return track_name, artists
