from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from datetime import datetime

import numpy as np
import pandas as pd

df = pd.read_csv('final.csv')

# Normalize the music features using Min-Max scaling
scaler = MinMaxScaler()
music_features = df[['danceability', 'energy', 'key', 'mode',
                     'loudness',  'speechiness', 'acousticness',
                     'instrumentalness', 'liveness', 'valence', 'tempo']].values
music_features_scaled = scaler.fit_transform(music_features)


def test(a, b):
    print(a)
    print(b)
    return a


def calculate_weighted_popularity(release_date):
    # Convert the release date to datetime object
    release_date = datetime.strptime(release_date, '%Y-%m-%d')

    # Calculate the time span between release date and today's date
    time_span = datetime.now() - release_date

    # Calculate the weighted popularity score based on time span (e.g., more recent releases have higher weight)
    weight = 1 / (time_span.days + 1)
    return weight


def content_based_recommendations(input_song_name, input_artist_name, num_recommendations=5):

    # Get the indices of the songs in the dataset that match the input song name.
    song = (df['track_name'].str.contains(
        input_song_name, case=False, na=False))
    art = (df['artists'].str.contains(
        input_artist_name, case=False, na=False))

    print(song.head())
    print(art.head())
    print(input_song_name)
    print(input_artist_name)

    matching_song_indices = df[song & art].index
    print(matching_song_indices[0])
    # If no songs match the input song name, return an empty list.
    # if not matching_song_indices.any() :
    #     return []

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


# def printoutt(song_name, artist_name, num_recommendations=5):
#     # song_name = 'Tief'
#     # artist_name = 'Paul Kalkbrenner'
#     recommendations = content_based_recommendations(
#         song_name, artist_name, num_recommendations)
#     return recommendations
#     # Print the recommendations.
#     print(f"CB recommended songs for '{song_name}':")
#     print(recommendations)


print(content_based_recommendations('Lolly', 'Rill'))


# a function to get hybrid recommendations based on weighted popularity


def hybrid_recommendations(input_song_name, input_artist_name, num_recommendations=5, alpha=0.5):

    # if input_song_name not in df['track_name'].values:
    #     print(
    #         f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
    #     return

    # Get content-based recommendations
    content_based_rec = content_based_recommendations(
        input_song_name, input_artist_name, num_recommendations)

    # Get the indices of the songs in the dataset that match the input song name.
    song = (df['track_name'].str.contains(
        input_song_name, case=False, na=False))
    art = (df['artists'].str.contains(
        input_artist_name, case=False, na=False))

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


def printout(song_name, artist_name, num_recommendations=5):
    # song_name = 'Into The Night'
    # artist_name = 'YOASOBI'
    recommendations = hybrid_recommendations(
        song_name, artist_name, num_recommendations)
    return recommendations
    # Print the recommendations.
    print(f"Hybrid recommended songs for '{song_name}':")
    print(recommendations)


# printout('Into The Night', 'YOASOBI')

# printout(5)
