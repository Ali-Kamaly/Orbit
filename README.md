<div style="text-align: center; margin: -20px 0 40px 0; width: 100%;">
        <p style="
            font-family: sans-serif; 
            font-size: 120px; 
            font-weight: 900; 
            letter-spacing: 12px; 
            margin: 0;
            background: linear-gradient(135deg, #e0aaff, #c77dff, #7b2cbf, #3c096c);
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0px 4px 20px rgba(199, 125, 255, 0.3));
            margin-right: -12px; 
        ">
            ORBIT
        </p>
        <p style="
            font-family: monospace; 
            letter-spacing: 6px; 
            color: #888888; 
            font-size: 14px; 
            margin: -20px 0 0 0; 
            text-transform: uppercase;
            margin-right: -6px;
        ">
            MUSIC THAT REVOLVES AROUND YOU
        </p>
    </div>

Orbit is a machine learning-powered music recommendation web application that generates personalised song recommendations from Spotify tracks and playlists.

Unlike traditional recommendation systems that only return the most similar songs, Orbit balances recommendation accuracy with music discovery by combining K-Means clustering and K-Nearest Neighbours (KNN).

Orbit combines **K-Means clustering** and **K-Nearest Neighbours (KNN)** to deliver two complementary recommendation modes:
- **Your Orbit** - highly similar songs based on existing taste and recommendation preference
- **Expand Your Orbit** - recommendations from the closest neighbouring musical region to encourage discovery while remaining stylistically relevant

Built using **Python**, **scikit-learn**, **pandas**, **Streamlit**, **Spotipy**, and the **Spotify Web API**.

## Application Preview
### Landing Page
![Landing Page](image.png)

### Your Orbit Songs
Recommendations generated from the closest musical cluster using weighted KNN similarity search.
![Entered song](image-7.png)
![Your Orbit Recs 1-3](image-4.png)
![Your Orbit Recs 3-5](image-5.png)

### Expand Your Orbit Songs
Recommendations generated from the closest neighbouring musical cluster to encourage music discovery while remaining stylistically similar.
![Expand Your Orbit Recs](image-6.png)
