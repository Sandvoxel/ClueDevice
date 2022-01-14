import time
from RPi import GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

towrite = "/grass.mp4"


time.sleep(2)
try:
    while True:

        print("Hold a tag near the reader")
        reader.write(towrite)
        print("written")
        # delay after clue given
        time.sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise


