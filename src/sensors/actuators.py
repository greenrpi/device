import RPi.GPIO as GPIO
import time

def open50():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    GPIO.output(22, GPIO.HIGH)
    GPIO.output(25, GPIO.LOW)
    time.sleep(1.7)

    GPIO.output(22, GPIO.HIGH)
    GPIO.output(25, GPIO.HIGH)

def open():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    GPIO.output(22, GPIO.HIGH)
    GPIO.output(25, GPIO.LOW)
    time.sleep(7)

    GPIO.output(22, GPIO.HIGH)
    GPIO.output(25, GPIO.HIGH)

def close():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    GPIO.output(22, GPIO.LOW)
    GPIO.output(25, GPIO.HIGH)
    time.sleep(7)

    GPIO.output(22, GPIO.HIGH)
    GPIO.output(25, GPIO.HIGH)
