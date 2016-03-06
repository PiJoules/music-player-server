#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import eyed3

from config import APP_ROOT


class Song(object):
    """Container for song info."""

    __slots__ = ("title", "artist", "album", "cover", "src", "base_src",
                 "server_src", "duration")

    def __init__(self, src, **kwargs):
        """
        title/artist/album:
            Strings that should be obvious of what they represent.
        cover:
            Binary image data (bot base64 encoded, but can be base64 encoded).
        src:
            The OS path of the file. Can be relative or absolute.
        base_src:
            The base filename.
        server_src:
            The server path of the file, where '/' is the root of the server,
            not the OS. Can be relative or absolute.
        duration:
            Length of the song in seconds.
        """
        for attr in self.__slots__:
            val = kwargs.get(attr, None)
            setattr(self, attr, val)
        self.src = src
        self.base_src = os.path.basename(src)

        src_real = os.path.realpath(src)
        self.server_src = os.path.join("/", src_real[len(APP_ROOT):])

    @classmethod
    def from_path(cls, path):
        """
        Create a song obj from the path to the file.

        This path must be the actual path of the computer this server is
        running on, not the flask server. If path starts with '/', this
        represents the OS root, not the flask root.
        """
        audio_file = eyed3.load(path)
        tag = audio_file.tag
        if tag.images:
            cover = tag.images[0]
        else:
            cover = None
        return cls(path, title=tag.title, artist=tag.artist, album=tag.album,
                   cover=cover, duration=audio_file.info.time_secs)

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

