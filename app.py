#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask server for music player.
"""

from __future__ import print_function

import os
import eyed3

from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4
from config import WORKING_DIR
from song import Song

# Flask app
app = Flask(__name__)
app.secret_key = str(uuid4())


@app.route("/")
def index_route():
    audio_files = os.listdir(WORKING_DIR)
    songs = [Song.from_path(os.path.join(WORKING_DIR, f)) for f in audio_files]
    return render_template("index.html",
                           songs=songs)


@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit_song_route(filename):
    """Route for editing song info."""
    relpath = os.path.join(WORKING_DIR, filename)
    if request.method == "GET":
        song = Song.from_path(relpath)
        return render_template("edit.html", song=song)

    # POST
    cover = request.files.get("cover", None)
    tag = eyed3.load(relpath).tag
    tag.artist = request.form["artist"]
    tag.album = request.form["album"]
    tag.title = request.form["title"]
    if cover:
        # 3 for front cover, 4 for back, 0 for other.
        # This is specified in the eyed3 docs.
        tag.images.set(3, cover.read(), cover.mimetype)
    tag.save()
    return redirect(url_for("index_route"))


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")

