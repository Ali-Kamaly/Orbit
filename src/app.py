import streamlit as st
from recommend import get_recommendations
import numpy as np
from spotify_utils import search_track, get_track_from_track_url, get_tracks_from_playlist

st.title("Orbit")
st.subheader("Music that revolves around you.")

preset = st.selectbox("Choose what aspect of the song should matter most",["Balanced", "Rhythm Focused", "Energy Focused", "Acoustic Focused", "Vocals Focused", "Mood Focused"])

st.info(
"""Rhythm Focused = match movement/groove/danceability/tempo\n
Energy Focused = match intensity/punch/loudness\n
Acoustic Focused = match organic/acoustic texture\n
Vocals Focused = match speech/vocal-forward qualities\n
Mood Focused = match emotional tone, mainly valence\n"""
)

advanced = st.checkbox("Advanced Controls")


if preset == "Balanced":
    danceability_weight = 1.0
    energy_weight = 1.0
    loudness_weight = 1.0
    speechiness_weight = 1.0
    acousticness_weight = 1.0
    instrumentalness_weight = 1.0
    liveness_weight = 1.0
    valence_weight = 1.0
    tempo_weight = 1.0

if preset == "Rhythm Focused":
    danceability_weight = 2.5
    energy_weight = 1.3
    loudness_weight = 1.0
    speechiness_weight = 0.8
    acousticness_weight = 0.7
    instrumentalness_weight = 0.6
    liveness_weight = 0.6
    valence_weight = 1.2
    tempo_weight = 1.8

if preset == "Energy Focused":
    danceability_weight = 1.4
    energy_weight = 2.5
    loudness_weight = 1.8
    speechiness_weight = 0.8
    acousticness_weight = 0.6
    instrumentalness_weight = 0.6
    liveness_weight = 0.8
    valence_weight = 1.4
    tempo_weight = 1.5

if preset == "Acoustic Focused":
    danceability_weight = 0.8
    energy_weight = 0.8
    loudness_weight = 1.2
    speechiness_weight = 0.7
    acousticness_weight = 2.7
    instrumentalness_weight = 1.8
    liveness_weight = 0.6
    valence_weight = 1.1
    tempo_weight = 1.0

if preset == "Vocals Focused":
    danceability_weight = 1.0
    energy_weight = 1.0
    loudness_weight = 1.0
    speechiness_weight = 2.5
    acousticness_weight = 0.9
    instrumentalness_weight = 0.6
    liveness_weight = 0.7
    valence_weight = 1.2
    tempo_weight = 0.8

if preset == "Mood Focused":
    danceability_weight = 1.0
    energy_weight = 1.2
    loudness_weight = 1.2
    speechiness_weight = 0.7
    acousticness_weight = 1.2
    instrumentalness_weight = 0.8
    liveness_weight = 0.6
    valence_weight = 2.5
    tempo_weight = 1.0



if advanced:
    danceability_weight = st.slider("Danceability", 0.0, 3.0, danceability_weight)
    energy_weight = st.slider("Energy", 0.0, 3.0, energy_weight)
    loudness_weight = st.slider("Loudness", 0.0, 3.0, loudness_weight)
    speechiness_weight = st.slider("Speechiness", 0.0, 3.0, speechiness_weight)
    acousticness_weight = st.slider("Acousticness", 0.0, 3.0, acousticness_weight)
    instrumentalness_weight = st.slider("Instrumentalness", 0.0, 3.0, instrumentalness_weight)
    liveness_weight = st.slider("Liveness", 0.0, 3.0, liveness_weight)
    valence_weight = st.slider("Valence", 0.0, 3.0, valence_weight)
    tempo_weight = st.slider("Tempo", 0.0, 3.0, tempo_weight)




weights = np.array([
    danceability_weight,
    energy_weight,
    loudness_weight,
    speechiness_weight,
    acousticness_weight,
    instrumentalness_weight,
    liveness_weight,
    valence_weight,
    tempo_weight
])

input_mode = st.radio("Input type", ["Manual Entry", "Spotify Link"])

song_names = []
artists = []

if input_mode == "Manual Entry":
    num_songs = st.number_input("How many songs would you like to enter: ", min_value = 1)

    for i in range(num_songs):
        song_name = st.text_input(f"Song {i+1} Name")
        artist_name = st.text_input(f"Artist {i+1} name(s) : ")
        song_names.append(song_name)
        artists.append(artist_name)


else:
    type_of_link = st.radio("Link type", ["Track link", "Playlist link"])

    if type_of_link == "Track link":
        num_songs = st.number_input("How many songs would you like to enter: ", min_value = 1)

        for i in range(num_songs):
            spotify_url = st.text_input(f"Paste spotify track {i+1} URL:")
            track_data = get_track_from_track_url(spotify_url)
            if track_data is None:
                continue
            track_name, artist = track_data
            song_names.append(track_name)
            artists.append(artist)
    else:
        spotify_url = st.text_input("Paste spotify public playlist URL: ")
        tracks_data = get_tracks_from_playlist(spotify_url)
        if tracks_data is not None:
            track_names, artists_names = tracks_data
            song_names = track_names.copy()
            artists = artists_names.copy()
        



if st.button("Recommend"):
    result = get_recommendations(song_names, artists, weights)
    if result is None:
        st.error("Song not found :(")
    else:
        recommendations, distances, valid_songs_count = result
        print(recommendations)
        i, rank= 1,1
        #index i = 0 is the song itself hence dist = 0.0
        for _, row in recommendations.iterrows():
            result = search_track(row["track_name"], row["artists"])
            if result is None:
                continue
            
            url, album, cover = result
            col1, col2 = st.columns([1,2])
            
            with col1:
                st.write(f"### #{rank}")
                st.image(cover, width=220)
            
            with col2:
                st.markdown(
            f"### {row['track_name']} | {row['artists']}")
                st.link_button("Open in Spotify", url)

                st.write(f"Album: {album}")
                st.write(f"Distance: {distances[0][i].round(3)}")
                match_score = round(100 / (1 + distances[0][i].round(3)), 1)
                st.write(f"Match Score: {match_score}%")
                i+=1
                rank+=1
            st.divider()
        st.write(f"Recommendations based on {valid_songs_count}/{len(song_names)} songs from playlist given.")
