from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages
from flask_session import Session
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

df = pd.read_csv('df.csv')
df.head(10)
# from helpers import apology, login_required, lookup, usd

# Configure application
# app = Flask(__name__)


# @app.route("/")
# def index():
#     lists = [i for i in range(1, 4)]
#     lists1 = [i for i in range(4, 7)]
#     return render_template("index.html", lists=lists, lists1=lists1)
