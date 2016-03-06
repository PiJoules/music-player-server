# music-player-server
Music player to run locally on your broswer.


## Usage
Audio files go in the `static/audio/` directory.

Only mp3 files are supported.


### Saving an image into an mp3
http://tuxpool.blogspot.com/2013/02/how-to-store-images-in-mp3-files-using.html


## TODO
- For given filename, if not in list of string.printable, remove character from file.
  - Lean On (feat. MØ) caused app to crash since whatever markdown program is used by Flask
    could not parse it and threw an error when printing the src.
  - This is done in association with the way for getting new songs.
- Add easy way to get new songs.
- Add way to sync songs in here to the app.
  - Do along side working on app.
- Add search and genres + tags to help search.
- Add shuffle button.


## Resources
- https://github.com/iainhouston/bootstrap3_player

