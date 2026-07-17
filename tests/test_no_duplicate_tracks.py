import pandas as pd
from src.preprocess import clean_data

def test_no_duplicate_songs_left():
    df = get_test_df()

    cleaned_df = clean_data(df)
    duplicates = cleaned_df.duplicated(subset = ["track_name", "artists"])
    assert duplicates.sum() == 0

def test_unique_songs_remain():
    df = get_test_df()


    cleaned_df = clean_data(df)
    #test_no_duplicate_songs_left already proved no duplicate songs are left after cleaning data
    unique_song_count_after = len(cleaned_df)

    assert unique_song_count_after == 3


def get_test_df():
    return pd.DataFrame({         
        "track_id": ["1", "1", "2", "3", "4"],
        "track_name": ["a", "a", "b", "b", "a"],
        "artists": ["q", "q", "q", "q", "r"],
        "popularity": [10, 10, 20, 30, 40],
        "duration_ms": [100, 100, 200, 300, 400],
        "explicit": [False, True, False, False, False],
        "danceability": [0.1, 0.1, 0.2, 0.3, 0.4],
        "energy": [0.1, 0.1, 0.2, 0.3, 0.4],
        "loudness": [-5, -5, -6, -7, -8],
        "speechiness": [0.1, 0.1, 0.2, 0.3, 0.4],
        "acousticness": [0.1, 0.1, 0.2, 0.3, 0.4],
        "instrumentalness": [0, 0, 0, 0, 0],
        "liveness": [0.1, 0.1, 0.2, 0.3, 0.4],
        "valence": [0.1, 0.1, 0.2, 0.3, 0.4],
        "tempo": [100, 100, 110, 120, 130]
    })