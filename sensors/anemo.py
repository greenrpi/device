import RPi.GPIO as GPIO
import math
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

impulses = 0


def interrupt(val):
        global impulses
        impulses += 1
        print('piiip....navysujem')


GPIO.add_event_detect(5, GPIO.RISING, callback = interrupt, bouncetime = 5)

time.sleep(1)

wind_speed = (impulses*0.0875+0.1)

print('Rychlost vetra je ' + str(wind_speed))
