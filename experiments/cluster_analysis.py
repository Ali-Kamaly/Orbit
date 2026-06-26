import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

df = pd.read_csv('data/processed/processed_dataset.csv')
similarity_features = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness',
                'liveness','valence','tempo']

song_vectors = df[similarity_features].values

k_values = [3,7,10,25]

for k in k_values:
    kmeans = KMeans(n_clusters = k, random_state = 217, n_init = 10)
    kmeans.fit(song_vectors)

    cluster_labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    inertia = kmeans.inertia_

    df['cluster'] = cluster_labels
    print(f"\n==== K = {k} ===")
    print(df['cluster'].value_counts().sort_index())
    print(f"Inertia {inertia}")