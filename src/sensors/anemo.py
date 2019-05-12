import RPi.GPIO as GPIO
import math
import time

impulses = 0

def getWindSpeed():
    global impulses
    impulses = 0

    def interrupt(val):
        global impulses
        impulses += 1

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(13, GPIO.RISING, callback = interrupt, bouncetime = 5)

    time.sleep(1)

    if impulses == 0:
        windSpeed = 0.00
    else:
        windSpeed = (impulses*0.0875+0.1)

    return round(windSpeed, 2)
