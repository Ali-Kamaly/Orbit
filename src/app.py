import streamlit as st
from recommend import get_recommendations
import numpy as np
from spotify_utils import search_track, get_track_from_track_url, get_tracks_from_playlist

st.markdown(
    """
    <div style="text-align: center; margin: -20px 0 40px 0; width: 100%;">
        <p style="
            font-family: sans-serif; 
            font-size: 120px; 
            font-weight: 900; 
            letter-spacing: 12px; 
            margin: 0;
            background: linear-gradient(135deg, #e0aaff, #c77dff, #7b2cbf, #3c096c);
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0px 4px 20px rgba(199, 125, 255, 0.3));
            margin-right: -12px; 
        ">
            ORBIT
        </p>
        <!-- Slogan -->
        <p style="
            font-family: monospace; 
            letter-spacing: 6px; 
            color: #888888; 
            font-size: 14px; 
            margin: -20px 0 0 0; 
            text-transform: uppercase;
            margin-right: -6px;
        ">
            MUSIC THAT REVOLVES AROUND YOU
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)



preset = st.selectbox("Choose what aspect of the song should matter most",["Balanced", "Rhythm Focused", "Energy Focused", "Acoustic Focused", "Vocals Focused", "Mood Focused"])

with st.expander("What do the presets mean?"):
    st.write("Rhythm Focused = match movement/groove/danceability/tempo")
    st.write("Energy Focused = match intensity/punch/loudness")
    st.write("Acoustic Focused = match organic/acoustic texture")
    st.write("Vocals Focused = match speech/vocal-forward qualities")
    st.write("Mood Focused = match emotional tone, mainly valence")




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

#advanced = st.checkbox("Advanced Controls")

with st.expander("Advanced Controls"):
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
            print(len(song_names))
            artists = artists_names.copy()
        



if st.button("Recommend"):
    result = get_recommendations(song_names, artists, weights)
    if result is None:
        st.error("Song not found :(")
    else:
        exploitation_recs, exploitation_dist, exploration_recs, exploration_dist, valid_songs_count = result
        #print(recommendations)
        #index i = 0 is the song itself hence dist = 0.0
        rank = 1
        shown = 0
        #defensive programming: if a song from database is no longer
        #in spotify, display next best recommendations

        st.write("Closest Songs...")
        for i, (_, row) in enumerate(exploitation_recs.iterrows()):
            if shown == 5:
                break
            result = search_track(row["track_name"], row["artists"])
            if result is None:
                print(f"recommended song {row['track_name']} by {row['artists']} is no longer on spotify")
                continue
            
            print(i, row['track_name'], row['artists'], exploitation_dist[0][i])

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
                st.write(f"Distance: {exploitation_dist[0][i].round(3)}")
                match_score = round(100 / (1 + exploitation_dist[0][i].round(3)), 1)
                st.write(f"Match Score: {match_score}%")
                st.progress(match_score/100)
            rank+=1
            shown+=1
            st.divider()

        shown_exp = 0
        st.write("Expand Your Orbit")
        for i, (_, row) in enumerate(exploration_recs.iterrows()):
            if shown_exp == 2:
                break
            result = search_track(row["track_name"], row["artists"])
            if result is None:
                print(f"recommended song {row['track_name']} by {row['artists']} is no longer on spotify")
                continue
            
            print(i, row['track_name'], row['artists'], exploration_dist[0][i])

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
                st.write(f"Distance: {exploration_dist[0][i].round(3)}")
                match_score = round(100 / (1 + exploration_dist[0][i].round(3)), 1)
                st.write(f"Match Score: {match_score}%")
                st.progress(match_score/100)
            rank+=1
            shown_exp+=1
            st.divider()

        #refactor code above too messy

        st.write(f"Recommendations based on {valid_songs_count}/{len(song_names)} songs from playlist given.")
