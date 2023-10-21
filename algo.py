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


def test():
    print("hello world")


def calculate_weighted_popularity(release_date):
    # Convert the release date to datetime object
    release_date = datetime.strptime(release_date, '%Y-%m-%d')

    # Calculate the time span between release date and today's date
    time_span = datetime.now() - release_date

    # Calculate the weighted popularity score based on time span (e.g., more recent releases have higher weight)
    weight = 1 / (time_span.days + 1)
    return weight


def content_based_recommendations(input_song_name, num_recommendations=5):
    # Convert the input song name to lowercase.
    input_song_name = input_song_name.lower()

    # Get the indices of the songs in the dataset that match the input song name.
    matching_song_indices = df[df['track_name'].str.lower(
    ) == input_song_name].index

    # If no songs match the input song name, return an empty list.
    if not matching_song_indices.any():
        return []

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
def hybrid_recommendations(input_song_name, num_recommendations=5, alpha=0.5):

    if input_song_name not in df['track_name'].values:
        print(
            f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return

    # Get content-based recommendations
    content_based_rec = content_based_recommendations(
        input_song_name, num_recommendations)

    # Get the popularity score of the input song
    popularity_score = df.loc[df['track_name'] ==
                              input_song_name, 'popularity'].values[0]
    # Calculate the weighted popularity score
    weighted_popularity_score = popularity_score * calculate_weighted_popularity(
        df.loc[df['track_name'] == input_song_name, 'release'].values[0])

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


def printout(song_id, num_recommendations=5):
    song_name = df.loc[song_id, 'track_name']
    recommendations = hybrid_recommendations(song_name, num_recommendations)
    return recommendations
    # Print the recommendations.
    # print(f"Hybrid recommended songs for '{song_name}':")
    # print(recommendations)


# printout(5)

# Identify the rows that have the value 'YOASOBI' in the 'artist' column
rows_to_print = df[df['artists'].isin(['YOASOBI'])].index

# Select the identified rows
df_filtered = df.loc[rows_to_print]

# Print the selected rows
# print(df_filtered['track_name'])
