import pandas as pd
import numpy as np
import datetime
from flask import Flask, render_template
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('final.csv')

# Normalize the music features using Min-Max scaling
scaler = MinMaxScaler()
music_features = df[['danceability', 'energy', 'key', 'mode',
                     'loudness',  'speechiness', 'acousticness',
                     'instrumentalness', 'liveness', 'valence', 'tempo']].values
music_features_scaled = scaler.fit_transform(music_features)


def genre_recommendations(genre, num_recommendations=6):
    genre = genre[0].lower() + genre[1:]
    print(genre)
    same_genre = df.loc[df['track_genre'] == genre]
    if same_genre.empty:
        return
    same_genre = df.loc[df['track_genre'] == genre].sample(num_recommendations)
    return same_genre


def convert_release_date(release_date):

    try:
        # Check if the release_date is in %Y format.
        release_date_datetime = datetime.strptime(release_date, "%Y")
    except ValueError:
        # If it is not in %Y format, return the original release_date.
        return release_date

    # If the release_date is in %Y format, convert it to year_01_01 format.
    release_date_datetime = release_date_datetime.replace(month=1, day=1)
    release_date = release_date_datetime.strftime("%Y-%m-%d")

    return release_date


def calculate_weighted_popularity(release_date):
    # Convert the release date to datetime object
    release_date = convert_release_date(release_date)
    release_date = datetime.strptime(release_date, '%Y-%m-%d')

    # Calculate the time span between release date and today's date
    time_span = datetime.now() - release_date

    # Calculate the weighted popularity score based on time span (e.g., more recent releases have higher weight)
    weight = 1 / (time_span.days + 1)
    return weight


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    def trim_strings(x): return x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


df = trim_all_columns(df)


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

# a function to get hybrid recommendations based on weighted popularity


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


def printout(song_name, artist_name, num_recommendations=6):
    recommendations = hybrid_recommendations(
        song_name, artist_name, num_recommendations)
    # print(f"Hybrid recommended songs for '{song_name}':")
    # print(recommendations)
    return recommendations


def apology(message, code=400):
    """Render message as an apology to user."""
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    genre = df["track_genre"].unique()
    size = len(artists)
    sizegenre = len(genre)

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message),  names=names, artists=artists, size=size, genre=genre, sizegenre=sizegenre), code
