from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from recommend import convert_songs_to_vectors

df = pd.read_csv('data/processed/processed_dataset.csv')
similarity_features = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness',
                'liveness','valence','tempo']

song_vectors = convert_songs_to_vectors(df, similarity_features)

kmeans = KMeans(n_clusters = 20, random_state = 217, n_init = 10)

kmeans.fit(song_vectors)

cluster_labels = kmeans.labels_
centroids = kmeans.cluster_centers_
inertia = kmeans.inertia_
# sum of squared song vectors from respective centroid

df['cluster'] = cluster_labels
df.to_csv('data/processed/clustered_dataset.csv', index = False)
np.save('data/processed/centroids.npy', centroids)

centroids = np.load('data/processed/centroids.npy')
print(centroids.shape)
print(centroids)
print(df['cluster'].value_counts())