from threading import Thread
import time
from RPi import GPIO
from mfrc522 import SimpleMFRC522


class RFID(Thread):
    def __init__(self, scandelay=5):
        GPIO.setwarnings(False)
        self.callbackFunc = None
        self.scanDelay = scandelay
        self.running = True
        self.reader = SimpleMFRC522()
        Thread.__init__(self)
        self.start()

    def scanned(self, func):
        self.callbackFunc = func

    def run(self):
        while True:
            print("Hold a tag near the reader")

            id, text = self.reader.read_no_block()
            while not id and self.running:
                id, text = self.reader.read_no_block()

            if not id:
                break
            print("ID: %s\nText: %s" % (id, text))

            self.callbackFunc(id, text.strip())

            # delay after clue given
            time.sleep(5)

    def stop(self):
        self.running = False
        GPIO.cleanup()
