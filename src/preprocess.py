import pandas as pd
import load_data

def clean_data():
    original_df = load_data.get_df()

    new_df = original_df[['artists','track_name','track_id','popularity','duration_ms','explicit','danceability','energy',
                'loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']].copy()
    
    #cleaning data - remove any null values 
    #there are repeated track_ids meaning duplicate songs 
    new_df.dropna(inplace = True)
    new_df.drop_duplicates(subset = 'track_id', inplace = True)

    print(original_df)
    print(new_df)
