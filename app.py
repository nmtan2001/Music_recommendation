from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages
from flask_session import Session
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from algo import test, printout

df = pd.read_csv('final.csv')

# Configure application
app = Flask(__name__)


@app.route("/recommendation", methods=["POST"])
def recommendation():
    # req = request.form.get('song-name')
    # songid = request.form.get('answer-hidden')
    returndf = printout(5)
    returnsongs = list(returndf['track_name'].values)
    returnartists = list(returndf['artists'].values)
    returnalbum = list(returndf['album_name'].values)
    returnid = list(returndf['track_id'].values)
    returnpop = list(returndf['popularity'].values)

    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    id = list(df['track_id'].values)
    size = len(artists)
    return render_template("result.html",  names=names, artists=artists, size=size, id=id, returnsongs=returnsongs,  returnartists=returnartists, returnalbum=returnalbum, returnid=returnid, returnpop=returnpop)


@app.route("/")
def index():
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    id = list(df['track_id'].values)
    size = len(artists)
    return render_template("index.html",  names=names, artists=artists, size=size, id=id)
