import pandas as pd

original_df = pd.read_csv("data\\raw\dataset.csv")
new_df = original_df[['artists','track_name','popularity','duration_ms','explicit','danceability','energy',
                      'loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']].copy()

print(original_df)
print(new_df)
