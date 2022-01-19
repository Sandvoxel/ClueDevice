import os
import sys
import time
import socket
import threading
from pathlib import Path
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageDraw, ImageFont

from videomanger import VideoManger
from rfidmanger import RFID
from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)

mediadir = str(Path(__file__).parents[0]) + "/media"
configdir = str(Path(__file__).parents[0]) + "/config.json"
player = VideoManger(mediadir)
rfidmanger = RFID()


@rfidmanger.scanned
def tag_scanned(id, text):
    player.play_video(text)


@app.route("/")
def index():
    files = [f for f in listdir(mediadir) if isfile(join(mediadir, f))]
    files.remove("ip.jpg")
    files.remove("paircard.jpg")
    files.remove("pairedcard.jpg")

    return render_template("index.html", files=files)


@app.route("/invalid-upload")
def invalid_upload():
    return render_template("invalid_upload.html")


@app.route("/upload-clue-file", methods=["POST"])
def upload_clue():
    if request.files:
        file = request.files["clue"]

        if file.filename == "" or not file.filename.lower().endswith(('.jpg', '.mp4', '.avi', '.mov')):
            return redirect(url_for("invalid_upload"))

        print(mediadir + "/" + file.filename)
        file.save(os.path.join(mediadir, file.filename))
        player.display_idle_image()

    return redirect(url_for("index"))


@app.route("/remove-cluefile", methods=["POST"])
def remove_clue():
    if request.form:
        os.remove(mediadir + "/" + (request.form.get("files")))

    return redirect(url_for("index"))


@app.route("/pair-rfidCard", methods=["POST"])
def pair_card():
    if request.form:
        player.display_img("/paircard.jpg")

        rfidmanger.pair_card((request.form.get("files")), lambda: player.display_img("/pairedcard.jpg", 3))

    return redirect(url_for("index"))


def init():
    is_file = os.path.exists(mediadir)
    if not is_file:
        os.mkdir(mediadir)

    idle_img_file = os.path.isfile(mediadir + "/idle.jpg")
    if not idle_img_file:
        img = Image.new('RGB', (1920, 1080), color=(73, 73, 73))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype('/usr/share/fonts/opentype/cantarell/Cantarell-Regular.otf', 80)
        d.text((10, 10), "Example Idle Image", font=font, fill=(255, 255, 255))
        d.text((10, 500), "Upload a new image with the name idle.png", font=font, fill=(255, 255, 255))
        img.save(mediadir + "/idle.jpg")

    idle_img_file = os.path.isfile(mediadir + "/paircard.jpg")
    if not idle_img_file:
        img = Image.new('RGB', (1920, 1080), color=(73, 73, 73))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype('/usr/share/fonts/opentype/cantarell/Cantarell-Regular.otf', 80)
        d.text((500, 10), "Tap card on scanner...", font=font, fill=(255, 255, 255))
        img.save(mediadir + "/paircard.jpg")
    idle_img_file = os.path.isfile(mediadir + "/pairedcard.jpg")
    if not idle_img_file:
        img = Image.new('RGB', (1920, 1080), color=(73, 73, 73))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype('/usr/share/fonts/opentype/cantarell/Cantarell-Regular.otf', 80)
        d.text((500, 10), "Card Paired", font=font, fill=(255, 255, 255))
        img.save(mediadir + "/pairedcard.jpg")

    ipfile = os.path.isfile(mediadir + "/ip.jpg")
    if ipfile:
        os.remove(mediadir + "/ip.jpg")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()

    img = Image.new('RGB', (1920, 1080), color=(73, 73, 73))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/opentype/cantarell/Cantarell-Regular.otf', 80)
    d.text((10, 10), local_ip + ":8080", font=font, fill=(255, 255, 255))
    img.save(mediadir + "/ip.jpg")

    player.display_img("/ip.jpg", 20)


def start_website():
    serve(app, host="0.0.0.0", port=8080)


website_thread = threading.Thread(target=start_website)
website_thread.start()


@player.close_callback
def requested_close():
    rfidmanger.stop()
    time.sleep(2)
    player.quit_player()
    os._exit(os.EX_OK)


init()
