import os
import sys
import time
from pathlib import Path

from videomanger import VideoManger
from rfidmanger import RFID
from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)

mediadir = str(Path(__file__).parents[0]) + "/media/"
player = VideoManger(mediadir, False)
rfidmanger = RFID()


@rfidmanger.scanned
def tag_scanned(id, text):
    player.play_video(text)


@player.close_callback
def requested_close():
    rfidmanger.stop()
    time.sleep(2)
    sys.exit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload-clue-file", methods=["POST"])
def upload_clue():
    if request.files:
        file = request.files["clue"]
        print(mediadir + file.filename)
        file.save(os.path.join(mediadir, file.filename))

    return redirect(url_for("index"))


if __name__ == "__main__":
    print(mediadir)
    serve(app, host="0.0.0.0", port=8080)
