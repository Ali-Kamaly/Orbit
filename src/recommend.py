import pandas as pd
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('data/processed/processed_dataset.csv')
similarity_features = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness',
                'liveness','valence','tempo']

def get_query_vector(song_name, artist_name):
    """
    Find all songs that have same song name and artist name - should ideally only be one match
    """
    matches = df[
        (df['track_name']== song_name) &
        (df['artists'] == artist_name)]
    return matches

def convert_songs_to_vectors():
    song_vectors = df[similarity_features].values
    #1 row and however many cols needed
    #print(f"Song vectors:\n{song_vectors}")
    return song_vectors

def find_closest_songs(query_vector, song_vectors):
    knn = NearestNeighbors(n_neighbors = 6, metric = 'euclidean')
    knn.fit(song_vectors)
    #just stores song_vectors
    distances, indices = knn.kneighbors(query_vector)
    #finds mathematically closests songs to query song
    recommendations = df.iloc[indices[0]]
    recommendations = recommendations.iloc[1:6]
    print(recommendations[['track_name','artists']])

def recommend():
    query_song_name = input("Enter song name: ")
    query_artist_name = input("Enter artist name: ")
    matches = get_query_vector(query_song_name, query_artist_name)
    #index of song in the df
    if matches.empty:
        print(f"The song {query_song_name} by {query_artist_name} was not found.")
    else:
        query_song = matches.iloc[0]
        #converted to series
        query_vector = query_song[similarity_features].values.reshape(1,-1)
        #converted to numpy array
        #print(f"Queried song:\n{query_song}")
        #print(f"Query vector:\n{query_vector}")

        #print(matches)
    song_vectors = convert_songs_to_vectors()
    find_closest_songs(query_vector, song_vectors)
    


recommend()