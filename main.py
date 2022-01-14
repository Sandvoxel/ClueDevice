import os
import sys
import time

from videomanger import VideoManger
from rfidmanger import RFID
from flask import Flask, render_template, request, redirect
from waitress import serve

app = Flask(__name__)

mediadir = os.getcwd() + "/media"
player = VideoManger(mediadir, True)
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
        file.save(os.path.join(mediadir, file.filename))

        redirect("/")

    return ""


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
