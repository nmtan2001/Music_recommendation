from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages
import pandas as pd
import numpy as np
from algo import printout, apology, genre_recommendations

df = pd.read_csv('final.csv')

# Configure application
app = Flask(__name__)


@app.route("/recommendation", methods=["POST"])
def recommendation():
    # handle errors
    if not request.form.get("song-name"):
        return apology("missing name", 400)
    song_request = request.form.get("song-name")

    song_name, artist_name = handleSplit(song_request)

    if song_name is None:
        return apology("wrong format", 400)

    if printout(song_name, artist_name) is None:
        return apology("no match")

    returndf = printout(song_name, artist_name)
    # display result
    returnsongs = list(returndf['track_name'].values)
    returnartists = list(returndf['artists'].values)
    returnalbum = list(returndf['album_name'].values)
    returnid = list(returndf['track_id'].values)
    sizeres = len(returnsongs)

    # display search
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    genre = df["track_genre"].unique()
    size = len(artists)
    sizegenre = len(genre)

    return render_template("result.html",  names=names, artists=artists, size=size, genre=genre, sizegenre=sizegenre, returnsongs=returnsongs,  returnartists=returnartists, returnalbum=returnalbum, returnid=returnid, sizeres=sizeres)


@app.route("/genre", methods=["POST"])
def genre():
    # handle errors
    if not request.form.get("genre-name"):
        return apology("missing genre", 400)
    genre_request = request.form.get('genre-name')

    if genre_recommendations(genre_request) is None:
        return apology("no match")
    returndf = genre_recommendations(genre_request)

    # display result
    returnsongs = list(returndf['track_name'].values)
    returnartists = list(returndf['artists'].values)
    returnalbum = list(returndf['album_name'].values)
    returnid = list(returndf['track_id'].values)
    sizeres = len(returnsongs)

    # display search
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    genre = df["track_genre"].unique()
    size = len(artists)
    sizegenre = len(genre)
    return render_template("result.html",  names=names, artists=artists, size=size, genre=genre, sizegenre=sizegenre, returnsongs=returnsongs,  returnartists=returnartists, returnalbum=returnalbum, returnid=returnid, sizeres=sizeres)


@app.route("/")
def index():
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    genre = df["track_genre"].unique()
    size = len(artists)
    sizegenre = len(genre)
    return render_template("index.html",  names=names, artists=artists, size=size, genre=genre, sizegenre=sizegenre)


def handleSplit(song_request):
    try:
        song_name, artist_name = song_request.split(" by ")
    except ValueError:
        song_name = None
        artist_name = None

    return song_name, artist_name
