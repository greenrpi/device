import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

SOIL_SOUTH_1_PIN = MCP.P1
SOIL_SOUTH_2_PIN = MCP.P2
SOIL_NORTH_1_PIN = MCP.P3
SOIL_NORTH_2_PIN = MCP.P4
RAIN_1_PIN = MCP.P5
RAIN_2_PIN = MCP.P6

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

def readRaw(pin):
    # create an analog input channel
    channel = AnalogIn(mcp, pin)

    return channel.value
