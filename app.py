from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages
from flask_session import Session
# from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)


@app.route("/")
def index():
    # lists = [i for i in range(1, 4)]
    # lists1 = [i for i in range(4, 7)]
    return render_template("index.html", lists=lists, lists1=lists1)
