#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask server for music player.
"""

from __future__ import print_function

import os
import eyed3

from flask import Flask, render_template
from uuid import uuid4


# Flask app
app = Flask(__name__)
app.secret_key = str(uuid4())
app.jinja_env.filters["path_join"] = os.path.join

# Config
WORKING_DIR = "static/audio"


@app.route("/")
def index_route():
    return render_template("index.html",
                           title="Home",
                           audio_files=os.listdir(WORKING_DIR))


@app.route("/<filename>")
def song_route(filename):
    relpath = os.path.join(WORKING_DIR, filename)
    fullpath = os.path.join("/", relpath)
    audio_file = eyed3.load(relpath)
    print(audio_file.tag)
    print(audio_file.tag.artist)
    print(audio_file.tag.album)
    print(audio_file.tag.album_artist)
    print(audio_file.tag.title)
    print(list(audio_file.tag.images))

    return render_template("play.html",
                           title=filename,
                           audio_file=fullpath)


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")

