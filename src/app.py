import streamlit as st
from recommend import get_recommendations
import numpy as np
from spotify_utils import search_track, get_track_from_track_url, get_tracks_from_playlist


def display_suggested_tracks(row, url, album, cover, distance, rank, shown):
    col1, col2 = st.columns([1,2])
        
    with col1:
        st.write(f"### #{rank}")
        st.image(cover, width=220)
    
    with col2:
        artists = row['artists'].replace(";", ", ")
        st.markdown(
    f"### {row['track_name']} | {artists}")
        st.link_button("Open in Spotify", url)

        st.write(f"Album: {album}")
        st.write(f"Distance: {distance[0][i].round(3)}")
        match_score = round(100 / (1 + distance[0][i].round(3)), 1)
        st.write(f"Match Score: {match_score}%")
        st.progress(match_score/100)

    st.divider()
    return rank+1, shown+1

def display_section_header(title, subtitle, icon):
    st.markdown(
        f"""
        <div style="margin: 60px 0 25px 0;">
            <div style="
                display: flex;
                align-items: center;
                gap: 14px;
                margin-bottom: 6px;
            ">
                <span style="
                    color: #c77dff;
                    font-size: 28px;
                    filter: drop-shadow(0 0 10px rgba(199, 125, 255, 0.45));
                ">{icon}</span>
                <span style="
                    font-family: sans-serif;
                    font-size: 34px;
                    font-weight: 900;
                    letter-spacing: 3px;
                    text-transform: uppercase;
                    background: linear-gradient(135deg, #e0aaff, #c77dff, #7b2cbf);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">{title}</span>
            </div>
            <p style="
                margin: 0 0 0 43px;
                color: #8f96a8;
                font-family: monospace;
                font-size: 13px;
                letter-spacing: 2px;
                text-transform: uppercase;
            ">
                {subtitle}
            </p>
            <div style="
                height: 1px;
                margin-top: 18px;
                background: linear-gradient(90deg, rgba(199,125,255,0.6), rgba(199,125,255,0));
            "></div>
        </div>
        """,
        unsafe_allow_html=True
    )

#title
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
    st.write("Rhythm Focused: match movement/groove/danceability/tempo")
    st.write("Energy Focused: match intensity/punch/loudness")
    st.write("Acoustic Focused: match organic/acoustic texture")
    st.write("Vocals Focused: match speech/vocal-forward qualities")
    st.write("Mood Focused: match emotional tone, mainly valence")

match preset:
    case "Balanced":
        danceability_weight = 1.0
        energy_weight = 1.0
        loudness_weight = 1.0
        speechiness_weight = 1.0
        acousticness_weight = 1.0
        instrumentalness_weight = 1.0
        liveness_weight = 1.0
        valence_weight = 1.0
        tempo_weight = 1.0
    
    case "Rhythm Focused":
        danceability_weight = 2.5
        energy_weight = 1.3
        loudness_weight = 1.0
        speechiness_weight = 0.8
        acousticness_weight = 0.7
        instrumentalness_weight = 0.6
        liveness_weight = 0.6
        valence_weight = 1.2
        tempo_weight = 1.8

    case "Energy Focused":
        danceability_weight = 1.4
        energy_weight = 2.5
        loudness_weight = 1.8
        speechiness_weight = 0.8
        acousticness_weight = 0.6
        instrumentalness_weight = 0.6
        liveness_weight = 0.8
        valence_weight = 1.4
        tempo_weight = 1.5

    case "Acoustic Focused":
        danceability_weight = 0.8
        energy_weight = 0.8
        loudness_weight = 1.2
        speechiness_weight = 0.7
        acousticness_weight = 2.7
        instrumentalness_weight = 1.8
        liveness_weight = 0.6
        valence_weight = 1.1
        tempo_weight = 1.0

    case "Vocals Focused":
        danceability_weight = 1.0
        energy_weight = 1.0
        loudness_weight = 1.0
        speechiness_weight = 2.5
        acousticness_weight = 0.9
        instrumentalness_weight = 0.6
        liveness_weight = 0.7
        valence_weight = 1.2
        tempo_weight = 0.8

    case "Mood Focused":
        danceability_weight = 1.0
        energy_weight = 1.2
        loudness_weight = 1.2
        speechiness_weight = 0.7
        acousticness_weight = 1.2
        instrumentalness_weight = 0.8
        liveness_weight = 0.6
        valence_weight = 2.5
        tempo_weight = 1.0


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
link_chosen, no_access_playlist, invalid_link = None, False, False

if input_mode == "Manual Entry":
    num_songs = st.number_input("How many songs would you like to enter: ", min_value = 1)

    for i in range(num_songs):
        song_name = st.text_input(f"Song {i+1} Name")
        artist_name = st.text_input(f"Artist {i+1} name(s) : ")
        song_names.append(song_name)
        artists.append(artist_name)

else:
    type_of_link = st.radio("Link type", ["Track link", "Playlist link"])

    link_chosen = type_of_link

    if type_of_link == "Track link":    
        num_songs = st.number_input("How many songs would you like to enter: ", min_value = 1)

        for i in range(num_songs):
            spotify_url = st.text_input(f"Paste spotify track {i+1} URL:")
            track_data = get_track_from_track_url(spotify_url)
            if track_data is None:
                #invalid track link
                continue
            track_name, artist = track_data
            song_names.append(track_name)
            artists.append(artist)
    else:
        spotify_url = st.text_input("Paste spotify public playlist URL: ")
        try:
            tracks_data = get_tracks_from_playlist(spotify_url)
        except Exception:
            st.error("⚠️ Playlist input is currently unavaible in the public demo.\nThe playlist recommendation engine is fully implemented" \
            "and can be used when running Orbit locally with your own Spotify Developer credentials.")
        first_val, _ = tracks_data
        if first_val is not None:
            no_access_playlist = False
            track_names, artists_names = tracks_data
            song_names = track_names.copy()
            artists = artists_names.copy()
        else:
            _, reason = tracks_data
            if reason == "no access":
                no_access_playlist = True
            elif reason == "invalid link":
                invalid_link = True


if st.button("Recommend"):
    result = get_recommendations(song_names, artists, weights)
    if result is None:
        if input_mode == "Spotify Link":
            if link_chosen == "Track link":
                st.error("All song links entered were invalid")
            else:
                if no_access_playlist:
                    st.error("Only upload playlists that you own/have collaborated with")
                elif invalid_link:
                    st.error("Playlist link entered was invalid")
                else:
                    st.error("Playlist has no valid songs")
        else:
            st.error("None of the inputted songs were found :(")
    else:
        exploitation_recs, exploitation_dist, exploration_recs, exploration_dist, valid_songs_count = result
        rank, shown_exploitation = 1, 0

        display_section_header("Your Orbit", "Closest matches based on your musical taste", "💫")
        for i, (_, row) in enumerate(exploitation_recs.iterrows()):
            if shown_exploitation == 5:
                #only recommend five songs for exploitation part of recommendation system
                break

            result = search_track(row["track_name"], row["artists"])
            if result is None:
                #song is no longer available on Spotify, skip it in the suggestions
                continue
                
            #if a song from database is no longer in spotify, display next best recommendations
            url, album, cover = result
            rank, shown_exploitation = display_suggested_tracks(row, url, album, cover, exploitation_dist, rank, shown_exploitation)

        shown_explore, rank = 0, 1

        display_section_header("Expand Your Orbit", "Discover music just beyond your usual taste", "🔭")
        for i, (_, row) in enumerate(exploration_recs.iterrows()):
            if shown_explore == 2:
                #only recommend two songs for exploration part of recommendation system
                break

            result = search_track(row["track_name"], row["artists"])
            if result is None:
                #song is no longer available on spotify, skip it in the suggestions
                continue

            url, album, cover = result
            rank, shown_explore = display_suggested_tracks(row, url, album, cover, exploration_dist, rank, shown_explore)


        st.caption(f"Recommendations based on {valid_songs_count}/{len(song_names)} songs given")


