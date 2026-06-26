### 15/06/2026
- planning on complete overview of project completed

### 16/06/2026
- Realised only removing same song IDs is not sufficient to remove all duplicates
had to also remove songs that had the same exact artist and same exact song name
- Chose standardisation rather than normalisation because some attributes contain outliers and KNN relies on distance calculations.

- Original dataset: 114000 songs
- Unique track IDs: 89741
- Significant number of duplicates removed

- reasoned about similaity features that should be taken into consideration for song recommendations 

### 17/06/2026
- Implemented version 1 of KNN song recommendation system
- Songs suggested were all mathematically similar
- Tested out model with wide range of songs such as Drake's One Dance and God's Plan, Mac Miller's cinderella and the songs suggested 
were all really good. Suggested songs broke the language barrier and even genre barrier that is usually faced
when trying to find similar songs - helped discover new artists and even new genres
    - Enter song name: One Dance
Enter artist name: Drake;Wizkid;Kyla
           track_name                                artists
41188       One Dance                      Drake;Wizkid;Kyla
33270        Badabing                   buller;LKN;El Chilli
18364     Your Matter                   Seyi Shay;Eugy;Efosa
44553  Cate's Brother                          Maisie Peters
51804   Somos Iguales  Ozuna;Tokischa;Louchie Lou;Michie One
321    Slow Down Time                             Us The Duo
- I found that equal weighting of all features produced reasonable results, but I plan to allow users to adjust feature importance to make it more tailored for the user
- using a small dataset that is 4 years old so perhaps using spotify's api later on will lead to better and more accurate song recommendations
    - noticed some songs suggested were not available on spotify anymore

- recommendation judged accurate for now
- starting off with smaller dataset leads to new discoveries of song taste

### 18/06/2026
- manual playlist style query, playlist embedding
    - find average song attribute values and find similar songs to average
    - setting up for future where user enters spotify public playlist link and program will find suggestions
    for the playlist
- implemented first version of streamlit application

- interesting recommendation: smack that by akon and eminem closest song being: Ich bin stark by rolf zuckowski which does not have the same vibe whatsoever one is rap the other a nursey rhyme
    - realised lyrics play an important role in music vibe and thus recommendation
    - they share the same danceability/tempo but differed heavily on genre context and lyrical mood
- added distance rounded to 3 dp to table on streamlit for user

### 19/06/2026
- first phase of feature scaling, user can adjust depending on preferences how they want to get recommended songs
- added sliders that user can adjust and fine tune to get more personalised recommendations
    - but it can be fiddly and having slider a few degrees off leads to different songs so user may miss out on songs, maybe have some presets for users who aren't as comfortable with music terminology or who don't know exactly what they like
- I started with equal weighting after standardisation, then added user-controlled feature weighting to let users customise the similarity metric instead of assuming one universal definition of vibe
- originally had all 9 sliders on screen, too overwhelming and too much finetuning may reduce to 3-4 instead
- added presets to make it easier for user to define how they want to get recommended songs
- similarity depends on the definition of similarity
- will need to further improve presets with user feedback perhaps
    - realised that feature weights do not mean “make this feature high or low.”  
    They mean “how important is it that this feature matches the query song?”
    For example, increasing the energy weight does not mean recommending high-energy songs. It means recommendations must have energy values closer to the query song’s energy
- added tickbox option for user to fine tune recommendation system themselves if they want to

### 20/06/2026
- integrating spotify web api via spotipy
- added spotify link to every song so can instantly go to spotify and play song
    - tested with Apocalypse by Cigarettes After Sex and all songs recommended were accurate and had accurate links to Spotify
- made whole app feel more polished and less of a dataframe website and more of a song recommendation website
- added corresponding album covers to make app feel more polished
- implemented simple match score as that's more useful than distance score for user, intentionally didn'y say accuracy or likelihood of liking song
- noticed bug: entered beautiful (feat. Camila Cabello) and it suggested ranked 1 song same song but with match of 99.4% distance of 0.006 - dataset has repeated song wasnt removed since one is without (feat. Camila Cabello) even though she is featured in the song so wasn't classified as a duplicate

### 21/06/2026
- added ability for user to choose from manually inputting song name and artist or pasting spotify link
    - added this feature since realised how common it is to have typo or not know everyone who is featured in a song, now it's easy to get recommendations via pasting spotify link
    - maybe add feature that shows the details of the song you pasted to make sure correct song was inputted
- annoying having relatively small dataset as more often than not the user's decided song to use as input will not be in the dataset
- planing to add spotify public playlist link capability for user, program will have to adapt depending on what link is sent, user shouldn't have to specify that its a playlist etc. so can have a cleaner UX design

### 24/06/2026
- added ability to enter spotify public playlist link, easier for user than manually entering all songs
    - songs from entered playlist that are also in the database are only used, the other songs are ignored as there is no data about the song's information
    - sign to perhaps increase dataset size
- trying to access more than 50 songs at a time from entered playlist

### 26/06/2026
- currently not calculating number of songs in playlist properly