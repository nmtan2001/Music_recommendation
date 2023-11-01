# MUSIC RECOMENDATIONG SYSTEM USING MACHINE LEARNING
### Video Demo:  <https://youtu.be/2nKFh2oCTbU>
### Description:
A music recommendation webapp using Machine Learning. The backend use Flask, the frontend use HTML, CSS with Bootstrap;the Machine Learning logics use Scikit-learn and numpy, data manipulation use Pandas 

#### Explore data:
Data is taken from [Kaggle](https://www.kaggle.com/datasets/jashanjeetsinghhh/songs-dataset). The data consists of ~110k songs from **Spotify**, include the song's name, song's features,... 
The reason I chose this dataset is:
- The data is from Spotify, comes with a lot of useful features about the songs.
- Data's from 2022 so it's pretty relevant
- The songs come with the track_genre feature, which the Spotify API doesn't provide.

The downside of this dataset is that it lacks the release date of the songs. That's why I need to crawl data from the Spotify using *Spotipy* - a library in Python that interact with Spotify. Inside the folder ***datas*** is the code for crawling and concat all the data together, then merge them with the old dataset. 

Inside the *gatheryear.py* is how it gets the data: 
```
def get_release_date(dataset, access_token):
    sp = spotipy.Spotify(auth=access_token)
    release_dates = []
    for trackid in dataset:
        info = sp.track(trackid)
        # time.sleep(5)
        release_date = info['album']['release_date']
        if release_date is not None:
            print(release_date)
            release_dates.append(
                {'track_id': trackid, 'release': release_date})
    return release_dates


df = pd.read_csv('df.csv')
df10 = df['track_id'][87000:89741]
```
Then it concat all the data using ***concatdf.py*** and then merge with the old dataset using ***merge.py***. The final dataset is ***final.csv***

#### The algorithms
The webapp has 2 recommending methods: by *song* or by *genre*.

The genre recommendation function take the select genre and give random songs that have the same genre:
```
def genre_recommendations(genre, num_recommendations=6):
    genre = genre[0].lower() + genre[1:]
    print(genre)
    same_genre = df.loc[df['track_genre'] == genre]
    if same_genre.empty:
        return
    same_genre = df.loc[df['track_genre'] == genre].sample(num_recommendations)
    return same_genre
```

The song recommendation function first take the features of the song and do a cosine similarity check:
```
def content_based_recommendations(input_song_name, input_artist_name, num_recommendations=5):

    # Get the indices of the songs in the dataset that match the input song name.

    song = (df['track_name'].str.contains(
        input_song_name, case=False, na=False, regex=False))
    art = (df['artists'].str.contains(
        input_artist_name, case=False, na=False, regex=False))

    matching_song_indices = df[song & art].index
    # If no songs match the input song name, return an empty list.
    if len(matching_song_indices) == 0:
        return

    # Get the index of the input song in the dataset.
    input_song_index = matching_song_indices[0]

    """ https://towardsdatascience.com/using-cosine-similarity-to-build-a-movie-recommendation-system-ae7f20842599"""

    # Calculate the similarity scores based on music features (cosine similarity).
    similarity_scores = cosine_similarity(
        [music_features_scaled[input_song_index]], music_features_scaled)

    # Get the indices of the most similar songs.
    similar_song_indices = similarity_scores.argsort(
    )[0][::-1][1:num_recommendations + 1]

    # Get the names of the most similar songs based on content-based filtering.
    content_based_recommendations = df.iloc[similar_song_indices][[
        'track_name', 'artists', 'album_name', 'track_id', 'popularity']]

    return content_based_recommendations
```

Song relevance can be measured using two factors: release date and popularity. Newer songs are more likely to be relevant to the user's taste, as they are more representative of current trends. More popular songs are also more likely to be relevant to the user's taste, as they have been enjoyed by a larger number of people. Therefore, a song's relevance can be calculated using a formula that take account of the release date freshness and the popularity of the song. The release date freshness is a measure of how new a song is, while the popularity is a measure of how well-liked a song is.

The song recommendation function then combines the results of that and content-based recommendation function to generate a final list of recommendations.


```
def hybrid_recommendations(input_song_name, input_artist_name, num_recommendations=5, alpha=0.5):

    # Get content-based recommendations
    content_based_rec = content_based_recommendations(
        input_song_name, input_artist_name, num_recommendations)

    if content_based_rec is None:
        return

    # Get the indices of the songs in the dataset that match the input song name.
    song = (df['track_name'].str.contains(
        input_song_name, case=False, na=False, regex=False))
    art = (df['artists'].str.contains(
        input_artist_name, case=False, na=False, regex=False))

    matching_song_indices = df[song & art].index[0]
    # # Get the popularity score of the input song
    popularity_score = df.loc[matching_song_indices, 'popularity']
    # Calculate the weighted popularity score
    weighted_popularity_score = popularity_score * calculate_weighted_popularity(
        df.loc[matching_song_indices, 'release'])
    # Combine content-based and popularity-based recommendations based on weighted popularity
    hybrid_recommendations = content_based_rec
    hybrid_recommendations = pd.concat([hybrid_recommendations,  pd.DataFrame.from_records([{
        'track_name': input_song_name,
        'artists': df.loc[df['track_name'] == input_song_name, 'artists'].values[0],
        'album_name': df.loc[df['track_name'] == input_song_name, 'album_name'].values[0],
        'track_id': df.loc[df['track_name'] == input_song_name, 'track_id'].values[0],
        'popularity': weighted_popularity_score
    }])])

    # Sort the hybrid recommendations based on weighted popularity score
    hybrid_recommendations = hybrid_recommendations.sort_values(
        by='popularity', ascending=False)

    # Remove the input song from the recommendations
    hybrid_recommendations = hybrid_recommendations[hybrid_recommendations['track_name'] != input_song_name]

    return hybrid_recommendations
```

