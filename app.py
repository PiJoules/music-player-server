#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask server for music player.
"""

from __future__ import print_function

import os

from flask import Flask, render_template
from uuid import uuid4


# Flask app
app = Flask(__name__)
app.secret_key = str(uuid4())
app.jinja_env.filters["path_join"] = os.path.join


@app.route("/")
def index_route():
    return render_template("index.html",
                           title="Home",
                           audio_files=os.listdir("static/audio"))


@app.route("/<filename>")
def song_route(filename):
    return render_template("play.html",
                           title=filename,
                           audio_file=filename)


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")

