import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
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

    pca = PCA(n_components = 2)
    projected = pca.fit_transform(song_vectors)
    print(projected.shape)
    plt.scatter(projected[:,0],projected[:,1], c = cluster_labels, s = 5)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title(f"PCA Projection of Songs (K = {k})")
    plt.show()