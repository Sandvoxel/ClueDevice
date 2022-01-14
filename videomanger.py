import mpv
import time
from os.path import exists


class VideoManger:
    def __init__(self, mediadir, fullscreen=True):
        self.player = mpv.MPV(input_vo_keyboard=True)
        self.player._set_property("keep-open", 'always')
        self.mediaDir = mediadir
        self.idleImage = "/idle.jpg"
        self.player.fullscreen = fullscreen

        self.player.play(self.mediaDir + self.idleImage)

        self.running = True
        self.close_func = None

        @self.player.on_key_press('q')
        def close():
            print("Closing program goodbye!")
            self.close_func()

        time.sleep(2)

    def play_video(self, path):
        if not exists(self.mediaDir + path):
            print("The given path \"{0}\" dose not exist".format(self.mediaDir + path))
            return
        self.player.play(self.mediaDir + path)
        self.player._set_property("pause", False)
        self.player.wait_until_playing()
        self.player.wait_until_paused()
        self.player.play(self.mediaDir + self.idleImage)

    def close_callback(self, func):
        self.close_func = func
