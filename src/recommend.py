import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

def initial_set_up():
    df = pd.read_csv('data/processed/processed_dataset.csv')
    similarity_features = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness',
                    'liveness','valence','tempo']
    #the greater the number of similarity features the worse the suggestiong model will perform
    #most songs will become uniformly distributed
    return df, similarity_features

def get_matches(song_name, artist_name, df):
    """
    Find all songs that have same song name and artist name - should ideally only be one match
    """
    matches = df[
        (df['track_name']== song_name) &
        (df['artists'] == artist_name)]
    return matches

def convert_songs_to_vectors(df, similarity_features):
    song_vectors = df[similarity_features].values
    #1 row and however many cols needed
    #print(f"Song vectors:\n{song_vectors}")
    return song_vectors

def find_closest_songs(query_vector, song_vectors, df):
    knn = NearestNeighbors(n_neighbors = 6, metric = 'euclidean')
    knn.fit(song_vectors)
    #just stores song_vectors
    distances, indices = knn.kneighbors(query_vector)
    #finds mathematically closests songs to query song using euclidean distance
    recommendations = df.iloc[indices[0]]
    recommendations = recommendations.iloc[1:6]
    #closest song will inevitably be itself if query is one song - disregard that recommendation later
    return recommendations, distances


def get_query_songs():
    num_songs = int(input("How many songs to enter: "))
    query_songs = []
    query_artists = []
    for i in range(num_songs):
        query_song_name = input("Enter song name: ")
        query_artist_name = input("Enter artist name: ")
        query_songs.append(query_song_name)
        query_artists.append(query_artist_name)
    return query_songs,query_artists

def get_query_vectors(query_songs, query_artists, df, similarity_features):
    query_vectors = []
    valid_songs = 0

    for i in range (len(query_songs)):    
        matches = get_matches(query_songs[i], query_artists[i], df)
        print(matches)
        #index of song in the df
        if matches.empty:
            #print(f"The song {query_songs[i]} by {query_artists[i]} was not found.")
            pass
        else:
            valid_songs +=1
            query_song = matches.iloc[0]
            #converted to series- only want first match
            query_vector = query_song[similarity_features].values
            query_vectors.append(query_vector)
            #converted to numpy array, only interested in similarity features values
            #print(f"Queried song:\n{query_song}")
            #print(f"Query vector:\n{query_vector}")

            #print(matches)
    if len(query_vectors) == 0:
        query_vectors = None
    return query_vectors, valid_songs

def get_query_vectors_avg(query_vectors):
    """
    Returns one vector that is the average of all query vectors
    """
    if query_vectors is None:
        #print("No valid songs found.")
        return
    query_vectors_avg = np.mean(query_vectors, axis = 0).reshape(1,-1)
    #getting average values for every similarity feature
    return query_vectors_avg


def get_recommendations(query_songs, query_artists, weights):
    df, similarity_features = initial_set_up()
    query_vectors, valid_songs_count = get_query_vectors(query_songs, query_artists, df, similarity_features)
    if query_vectors is None:
        return
    weighted_query_vectors = query_vectors * weights

    print(f"Default: {query_vectors}")
    print(f"Weighted: {weighted_query_vectors}")
    query_vectors_avg = get_query_vectors_avg(weighted_query_vectors)
    if query_vectors_avg is None:
        #print("All songs entered are invalid.")
        return    

    #print(query_vectors_avg)

    song_vectors = convert_songs_to_vectors(df, similarity_features)
    weighted_song_vectors = song_vectors * weights
    recommendations, distances = find_closest_songs(query_vectors_avg, weighted_song_vectors, df)

    return recommendations, distances, valid_songs_count



#recommendations, distances = get_recommendations(query_songs, )
#print(recommendations[['track_name','artists']])
#print(recommendations[similarity_features])
#printed in ascending order of distance i.e. closest similarity at top 
#print(distances)

if __name__ == "__main__":
    danceability_weight, energy_weight, loudness_weight,speechiness_weight = 1,1,1,1
    acousticness_weight,instrumentalness_weight, liveness_weight, valence_weight, tempo_weight = 1,1,1,1,1
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

    #need to have weights defined here
    query_songs, query_artists = get_query_songs()
    recommendations, distances = get_recommendations(query_songs, query_artists, weights)
    print(recommendations[["track_name", "artists"]])
    print(distances)

