15/06/2026
- planning on complete overview of project completed

16/06/2026
- Realised only removing same song IDs is not sufficient to remove all duplicates
had to also remove songs that had the same exact artist and same exact song name
- Chose standardisation rather than normalisation because some attributes contain outliers and KNN relies on distance calculations.

- Original dataset: 114000 songs
- Unique track IDs: 89741
- Significant number of duplicates removed

- reasoned about similaity features that should be taken into consideration for song recommendations 

17/06/2026
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

18/06/2026
- manual playlist style query, playlist embedding
    - find average song attribute values and find similar songs to average
    - setting up for future where user enters spotify public playlist link and program will find suggestions
    for the playlist
- implemented first version of streamlit application

- interesting recommendation: smack that by akon and eminem closest song being: Ich bin stark by rolf zuckowski which does not have the same vibe whatsoever one is rap the other a nursey rhyme
    - realised lyrics play an important role in music vibe and thus recommendation
    - they share the same danceability/tempo but differed heavily on genre context and lyrical mood
- added distance rounded to 3 dp to table on streamlit for user

19/06/2026
- first phase of feature scaling, user can adjust depending on preferences how they want to get recommended songs
- added sliders that user can adjust and fine tune to get more personalised recommendations
    - but it can be fiddly and having slider a few degrees off leads to different songs so user may miss out on songs, maybe have some presets for users who aren't as comfortable with music terminology or who don't know exactly what they like
- I started with equal weighting after standardisation, then added user-controlled feature weighting to let users customise the similarity metric instead of assuming one universal definition of vibe
- originally had all 9 sliders on screen, too overwhelming and too much finetuning may reduce to 3-4 instead
- added presets to make it easier for user to define how they want to get recommended songs
- added tickbox option for user to fine tune recommendation system themselves if they want to