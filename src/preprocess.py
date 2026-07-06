import load_data

from sklearn.preprocessing import StandardScaler

def clean_data():
    original_df = load_data.get_df()

    new_df = original_df[['artists','track_name','track_id','popularity','duration_ms','explicit','danceability','energy',
                'loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']].copy()
    
    #cleaning data - remove any null values 
    #there are repeated track_ids meaning duplicate songs 
    new_df = new_df.dropna()
    new_df = new_df.drop_duplicates(subset = 'track_id')
    new_df = new_df.drop_duplicates(subset = ['artists', 'track_name'])
    new_df = new_df.drop(columns = 'track_id')
    #track id now redundant after removing duplicates

    return new_df

#standardisation vs normalisation
"""
standardisation = normal distribution with mean = 0 std = 1
normalisation = scale 0 - 1
chose standardisation as there may be outliers 
"""
def standardise_data(new_df):
    continuous_attributes = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness',
                'liveness','valence','tempo']
    scaler = StandardScaler()
    new_df[continuous_attributes] = scaler.fit_transform(new_df[continuous_attributes])
    #standardising only relevant continuous numerical attributes
    return new_df

def save_df(df):
    df.to_csv('data/processed/processed_dataset.csv', index = False)


def preprocess():
    new_df = clean_data()
    preprocessed_df = standardise_data(new_df)
    save_df(preprocessed_df)

preprocess()