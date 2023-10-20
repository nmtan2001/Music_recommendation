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


@app.route("/")
def index():
    lists = [i for i in range(1, 4)]
    lists1 = [i for i in range(4, 7)]
    names = list(df['track_name'].values)
    artists = list(df['artists'].values)
    size = len(artists)
    return render_template("index.html",  names=names, artists=artists, size=size)
