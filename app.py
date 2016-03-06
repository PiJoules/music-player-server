#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask server for music player.
"""

from __future__ import print_function

import os
import eyed3

from flask import Flask, render_template, request
from uuid import uuid4


# Flask app
app = Flask(__name__)
app.secret_key = str(uuid4())
app.jinja_env.filters["path_join"] = os.path.join

# Config
WORKING_DIR = "static/audio"


class Song(object):
    """Container for song info."""

    __slots__ = ("title", "artist", "album", "cover", "src", "base_src")

    def __init__(self, src, **kwargs):
        for attr in self.__slots__:
            val = kwargs.get(attr, None)
            setattr(self, attr, val)
        self.src = src
        self.base_src = os.path.basename(src)

    @classmethod
    def from_path(cls, path):
        """
        Create a song obj from the path to the file.

        This path must be the actual path of the computer this server is
        running on, not the relative flask server. '/' represents the OS root,
        not the flask root.
        """
        tag = eyed3.load(path).tag
        if tag.images:
            cover = tag.images[0]
        else:
            cover = None
        return cls(path, title=tag.title, artist=tag.artist, album=tag.album,
                   cover=cover)

    @property
    def base64_cover(self):
        """base64 encoded cover image data."""
        cover = self.cover
        if cover:
            return self.cover.image_data.encode("base64")
        return None

    def __str__(self):
        return str({attr: getattr(self, attr, None)
                    for attr in self.__slots__})


@app.route("/")
def index_route():
    audio_files = os.listdir(WORKING_DIR)
    songs = [Song.from_path(os.path.join(WORKING_DIR, f)) for f in audio_files]
    return render_template("index.html",
                           songs=songs)


@app.route("/<filename>/edit", methods=["GET", "POST"])
def edit_song_route(filename):
    """Route for editing song info."""
    relpath = os.path.join(WORKING_DIR, filename)
    if request.method == "GET":
        song = Song.from_path(relpath)
        print(song)
        return render_template("edit.html", song=song)

    # POST
    print(request.form)
    print(request.files)
    cover = request.files.get("cover", None)
    tag = eyed3.load(relpath).tag
    tag.artist = request.form["artist"]
    tag.album = request.form["album"]
    tag.title = request.form["title"]
    if cover:
        tag.images.set(3, cover.read(), cover.mimetype)
    tag.save()
    return ""


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
    print(audio_file.info.time_secs)

    return render_template("play.html",
                           title=filename,
                           audio_file=fullpath)


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")

