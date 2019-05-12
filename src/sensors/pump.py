import RPi.GPIO as GPIO
import time

def start():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.LOW)
    time.sleep(15)

def stop():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.HIGH)
