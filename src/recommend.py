import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

SIMILARITY_FEATURES = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness',
                    'liveness','valence','tempo']

def initial_set_up():
    df = pd.read_csv('data/processed/clustered_dataset.csv')
    centroids = np.load('data/processed/centroids.npy').astype(float)
    #the greater the number of similarity features the worse the suggestion model will perform
    #as most songs will become uniformly distributed
    return df, centroids

def get_matches(song_name, artist_name, df):
    """
    Finds all songs that have the same song name and artist name - should ideally only be one match
    """
    matches = df[
        (df['track_name']== song_name) &
        (df['artists'] == artist_name)]
    return matches

def convert_songs_to_vectors(df):
    return df[SIMILARITY_FEATURES].values

def find_closest_songs(query_vector, song_vectors, df, exclude_query_song = False):
    knn = NearestNeighbors(n_neighbors = 10, metric = 'euclidean')
    #finding 10 songs even though only 5 will be shown to allow for room if songs must be skipped
    knn.fit(song_vectors)
    #just stores song_vectors
    distances, indices = knn.kneighbors(query_vector)
    #finds mathematically closests songs to query song using euclidean distance
    recommendations = df.iloc[indices[0]]

    if exclude_query_song:
        #closest song will inevitably be itself if query is one song - disregard that recommendation later
        recommendations = recommendations.iloc[1:]
        distances = distances[:, 1:]

    return recommendations, distances

def get_query_vectors(query_songs, query_artists, df):
    query_vectors = []
    valid_songs = 0

    for i in range (len(query_songs)):    
        matches = get_matches(query_songs[i], query_artists[i], df)
        
        if matches.empty:
            #the specific song was not found in the dataset
            pass
        else:
            valid_songs +=1
            query_song = matches.iloc[0]
            #converted to series- only want first match
            query_vector = query_song[SIMILARITY_FEATURES].values.astype(float)
            query_vectors.append(query_vector)
            #converted to numpy array, only interested in similarity features values

    if len(query_vectors) == 0:
        query_vectors = None
        #no songs were found in the database hence no data for query song
    return query_vectors, valid_songs

def get_query_vectors_avg(query_vectors):
    """
    Returns one vector that is the average of all query vectors - embedding
    """
    if query_vectors is None:
        return
    query_vectors_avg = np.mean(query_vectors, axis = 0).astype(float).reshape(1,-1)
    #getting average values for every similarity feature
    return query_vectors_avg

def get_closest_centroids(query_vector, centroids):
    """Finds closest centroid by calculating the euclidean distance of each centroid"""
    distances = np.linalg.norm(centroids-query_vector, axis = 1)
    return np.argsort(distances)
    #centroids are sorted in the order of closest to furthest


def get_recommendations(query_songs, query_artists, weights):
    df, centroids = initial_set_up()
    query_vectors, valid_songs_count = get_query_vectors(query_songs, query_artists, df)
    exclude_query_song = (valid_songs_count == 1)
    #if valid song count == 1 then query song exists in dataset so must be excluded in recommendations

    if query_vectors is None:
        #no query songs were found in the dataset
        return
    weighted_query_vectors = query_vectors * weights

    query_vectors_avg = get_query_vectors_avg(weighted_query_vectors)
    if query_vectors_avg is None:
        return    

    weighted_centroids = centroids * weights
    closest_centroids = get_closest_centroids(query_vectors_avg, weighted_centroids)

    #used for exploitation & exploration song recommendation
    nearest_centroid = closest_centroids[0]
    next_best_centroid = closest_centroids[1]

    #running knn on a smaller more refined dataset (recommending songs from same cluster)
    exploitation_cluster_df = df[df['cluster']==nearest_centroid]
    exploitation_song_vectors = convert_songs_to_vectors(exploitation_cluster_df)
    weighted_exploitation_song_vectors = exploitation_song_vectors * weights
    exploitation_recs, exploitation_dist = find_closest_songs(query_vectors_avg, weighted_exploitation_song_vectors, exploitation_cluster_df, exclude_query_song)

    exploration_cluster_df = df[df['cluster']==next_best_centroid]
    exploration_song_vectors = convert_songs_to_vectors(exploration_cluster_df)
    weighted_exploration_song_vectors = exploration_song_vectors * weights
    exploration_recs, exploration_dist = find_closest_songs(query_vectors_avg, weighted_exploration_song_vectors, exploration_cluster_df, exclude_query_song)


    return exploitation_recs, exploitation_dist, exploration_recs, exploration_dist, valid_songs_count

