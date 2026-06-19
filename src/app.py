import streamlit as st
from recommend import get_recommendations
import numpy as np

st.title("Orbit")
st.write("Music that revolves around you")

preset = st.selectbox("Choose a vibe preset",["Balanced", "Dance/Party"])
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

if preset == "Dance/Party":
    danceability_weight = 2.5
    energy_weight = 2.2
    loudness_weight = 1.3
    speechiness_weight = 1.0
    acousticness_weight = 1.0
    instrumentalness_weight = 1.0
    liveness_weight = 2.0
    valence_weight = 2.2
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

num_songs = st.number_input("How many songs would you like to enter: ", min_value = 1)

song_names = []
artists = []

for i in range(num_songs):
    song_name = st.text_input(f"Song {i+1} Name")
    artist_name = st.text_input(f"Artist {i+1} name(s) : ")
    song_names.append(song_name)
    artists.append(artist_name)

if st.button("Recommend"):
    result = get_recommendations(song_names, artists, weights)
    if result is None:
        st.error("Song not found :(")
    else:
        recommendations, distances = result
        recommendations = recommendations.copy()
        recommendations['distance'] = distances[0].round(3)
        st.dataframe(recommendations[["track_name","artists","distance"]])
        