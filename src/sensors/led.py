import board
import neopixel
import time
import random

pixels = neopixel.NeoPixel(board.D12, 30)

def setLeds(first = None, second = None, third = None, fourth = None):
    if first:
        pixels[0] = first
    if second:
        pixels[1] = second
    if third:
        pixels[2] = third
    if fourth:
        pixels[3] = fourth

def changeLeds(color):
    pixels[0] = color if ((0, 0, 0) != pixels[0]) else pixels[0]
    pixels[1] = color if ((0, 0, 0) != pixels[1]) else pixels[1]
    pixels[2] = color if ((0, 0, 0) != pixels[2]) else pixels[2]
    pixels[3] = color if ((0, 0, 0) != pixels[3]) else pixels[3]

def clearLeds():
    pixels[0] = (0, 0, 0)
    pixels[1] = (0, 0, 0)
    pixels[2] = (0, 0, 0)
    pixels[3] = (0, 0, 0)
