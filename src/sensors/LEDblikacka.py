import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

count = 0
while True:
    print(count)
    time.sleep(0.5)
    GPIO.setup(13, GPIO.LOW)
    GPIO.setup(27, GPIO.LOW)
    GPIO.setup(5, GPIO.LOW)
    time.sleep(0.5)
    GPIO.setup(13, GPIO.HIGH)
    GPIO.setup(27, GPIO.HIGH)
    GPIO.setup(5, GPIO.HIGH)
    count += 1
    if count >= 5:
        break
