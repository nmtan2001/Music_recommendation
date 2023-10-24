from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages
from flask_session import Session
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from algo import printout

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

    returndf = printout(song_name, artist_name)

    # display result
    returnsongs = list(returndf['track_name'].values)
    returnartists = list(returndf['artists'].values)
    returnalbum = list(returndf['album_name'].values)
    returnid = list(returndf['track_id'].values)
    size1 = len(returnsongs)

    # display search
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    id = list(df['track_id'].values)
    size = len(artists)

    return render_template("result.html",  names=names, artists=artists, size=size, id=id, returnsongs=returnsongs,  returnartists=returnartists, returnalbum=returnalbum, returnid=returnid, size1=size1)


@app.route("/")
def index():
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    id = list(df['track_id'].values)
    size = len(artists)
    return render_template("index.html",  names=names, artists=artists, size=size, id=id)


def handleSplit(song_request):
    try:
        song_name, artist_name = song_request.split(" by ")
    except ValueError:
        song_name = None
        artist_name = None

    return song_name, artist_name


def apology(message, code=400):
    """Render message as an apology to user."""
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    id = list(df['track_id'].values)
    size = len(artists)

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message),  names=names, artists=artists, size=size, id=id), code
