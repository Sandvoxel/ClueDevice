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
            self.player.fullscreen = False
            print("Closing program goodbye!")
            self.close_func()

        time.sleep(2)

    def play_video(self, path):
        try:
            if not exists(self.mediaDir + path):
                print("The given path \"{0}\" dose not exist".format(self.mediaDir + path))
                return
        except:
            print("The given path \"{0}\" dose not exist".format(self.mediaDir + path))
            return
        
        self.player.play(self.mediaDir + path)
        self.player._set_property("pause", False)
        self.player.wait_until_playing()
        self.player.wait_until_paused()
        self.display_idle_image()

    def display_img(self, path, delay=0):
        if not exists(self.mediaDir + path):
            print("The given path \"{0}\" dose not exist".format(self.mediaDir + path))
            return
        self.player.play(self.mediaDir + path)
        if delay != 0:
            time.sleep(delay)
            self.display_idle_image()

    def display_idle_image(self):
        self.player.play(self.mediaDir + self.idleImage)

    def quit_player(self):
        self.player.quit()

    def close_callback(self, func):
        self.close_func = func
