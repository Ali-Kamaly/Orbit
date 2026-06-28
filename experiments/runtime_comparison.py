import time, sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.recommend import find_closest_songs

similarity_features = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness',
                    'liveness','valence','tempo']
df = pd.read_csv('data/processed/clustered_dataset.csv')

song_vectors = df[similarity_features].values



#normal knn
def test_normal_knn_speed(query_vector, repetitions = 10):

    elapsed_times = []
    for _ in range(repetitions):
        start = time.perf_counter()

        find_closest_songs(query_vector, song_vectors, df)

        end = time.perf_counter()
        elapsed_time = end-start
        elapsed_times.append(elapsed_time)
    elapsed_avg_time = np.mean(elapsed_times)
    return elapsed_avg_time

#clustered knn
def test_clustered_knn_speed(query_index, query_vector, repetitions = 10):
    query_cluster = df.loc[query_index, 'cluster']
    cluster_df = df[df['cluster'] == query_cluster]
    cluster_vectors = cluster_df[similarity_features].values


    elapsed_times = []
    for _ in range(repetitions):
        start = time.perf_counter()

        find_closest_songs(query_vector=query_vector, song_vectors=cluster_vectors, df=cluster_df)


        end = time.perf_counter()
        elapsed_time = end-start
        elapsed_times.append(elapsed_time)
    elapsed_avg_time = np.mean(elapsed_times)
    return elapsed_avg_time

def compare_runtimes(iterations = 10):

    indices_tested = []
    speed_ups = []
    for _ in range(iterations):
        query_index = np.random.randint(0, len(df))
        while query_index in indices_tested:
            query_index = np.random.randint(0, len(df))
        indices_tested.append(query_index)
        print(f"--- Random query index: {query_index}---")

        query_vector = df.loc[[query_index], similarity_features].values


        normal_speed = test_normal_knn_speed(query_vector, 100)
        clustered_speed = test_clustered_knn_speed(query_index, query_vector, 100)
        speed_up = normal_speed/clustered_speed
        speed_ups.append(speed_up)

        print(f"Normal KNN Avg. Time: {normal_speed}")
        print(f"Clustered KNN Avg. Time: {clustered_speed}")
        print(f"Clustered KNN is {speed_up} faster")

    print(f"Cluster KNN speedups mean: {np.mean(speed_ups)}")
    print(f"Cluster KNN speedups median: {np.median(speed_ups)}")

compare_runtimes()