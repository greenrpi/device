from influxdb import InfluxDBClient
from config import config
from pathlib import Path
from os.path import isfile
from os import remove
from os import system
import sys
from time import sleep
import traceback
import RPi.GPIO as GPIO
import json
import random

from sensors.led import setLeds, clearLeds, changeLeds
from sensors import iptemp
from sensors.anemo import getWindSpeed
from sensors.display import readControllerDisplay
from sensors import dht
from sensors import adc
from sensors import actuators
from sensors import pump

def handleException(exc_type, exc_value, exc_traceback):
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    changeLeds((200, 0, 0))
    GPIO.cleanup()
    sys.exit(1)
sys.excepthook = handleException

#
####### Cycle consists of four phases and is run periodically every minute #######
#

####### Init #######
influx = InfluxDBClient(config['host'], config['port'], config['user'], config['password'], config['dbname'], ssl=config['ssl'], verify_ssl=True)
# We can't run more than one cycle at once so we end if previous didn't end
running = isfile("running")
if running:
    print("Previous cycle didn't end. Exiting!")
    sys.exit()
Path('running').touch()
clearLeds()

####### 1. PHASE - Get sensor data #######
setLeds(first=(200, 200, 200))

temperature = {}
wind = {}
rain = {}
power = {}
humidity = {}

dhtIndoor = dht.readTemperatureHumidity(dht.INDOOR_PIN)
dhtCase = dht.readTemperatureHumidity(dht.CASE_PIN)

# Temperatures
temperature["outdoor"] = iptemp.readTemp(iptemp.SENSOR_OUTDOOR)
temperature["soill"] = (iptemp.readTemp(iptemp.SENSOR_SOIL_1) + iptemp.readTemp(iptemp.SENSOR_SOIL_2)) / 2
temperature["soilu"] = iptemp.readTemp(iptemp.SENSOR_SOIL_3)
temperature["barrel"] = iptemp.readTemp(iptemp.SENSOR_BARREL)
temperature["indoor"] = dhtIndoor[1]
temperature["case"] = dhtCase[1]

# Outdoor wind speed
wind["outdoor"] = getWindSpeed()

# Rain sensor
rain["first"] = adc.readRaw(adc.RAIN_1_PIN)
rain["second"] = adc.readRaw(adc.RAIN_2_PIN)

# Soil humidity, Indoor and case humidity
humidity["indoor"] = dhtIndoor[0]
humidity["case"] = dhtCase[0]
humidity["soill"] = (adc.readRaw(adc.SOIL_SOUTH_1_PIN) + adc.readRaw(adc.SOIL_SOUTH_2_PIN)) / 2
humidity["soilu"] = (adc.readRaw(adc.SOIL_NORTH_1_PIN) + adc.readRaw(adc.SOIL_NORTH_2_PIN)) / 2

# Solar controller values
power["controller"] = readControllerDisplay()

####### 2. PHASE - Upload sensor data #######
setLeds(first=(200, 200, 200), second=(200, 200, 200))

for key, value in temperature.items():
    influx.write_points([
        {
            "measurement": "temperature",
            "tags": {
                "sensor": key
            },
            "fields": {
                "celsius": value
            }
        }
    ])

for key, value in wind.items():
    influx.write_points([
        {
            "measurement": "wind",
            "tags": {
                "sensor": key
            },
            "fields": {
                "mps": value
            }
        }
    ])

for key, value in rain.items():
    influx.write_points([
        {
            "measurement": "rain",
            "tags": {
                "sensor": key
            },
            "fields": {
                "raw": value
            }
        }
    ])

for key, value in power.items():
    influx.write_points([
        {
            "measurement": "power",
            "tags": {
                "sensor": key
            },
            "fields": {
                "voltage": value[0],
                "input": value[1]
            }
        }
    ])

for key, value in humidity.items():
    influx.write_points([
        {
            "measurement": "humidity",
            "tags": {
                "sensor": key
            },
            "fields": {
                "raw": value
            }
        }
    ])

####### 3. PHASE - Download commands #######
setLeds(first=(200, 200, 200), second=(200, 200, 200), third=(200, 200, 200))

manualCommands = influx.query('SELECT LAST(type) as "type", COUNT(*) as "count" FROM "greenrpi"."autogen"."action" WHERE "manual"=\'yes\' GROUP BY id').raw["series"]

####### 4. PHASE - Execute downloaded and automatic operations #######
setLeds(first=(200, 200, 200), second=(200, 200, 200), third=(200, 200, 200), fourth=(200, 200, 200))

for command in manualCommands:
    if (command["values"][0][2] != 1):
        continue

    if (command["values"][0][1] == 'WINDOWS_OPEN_50'):
        print("Opening windows to 50%")
        actuators.open50()
    elif (command["values"][0][1] == 'WINDOWS_OPEN'):
        print("Opening windows")
        actuators.open()
    elif (command["values"][0][1] == 'WINDOWS_CLOSE'):
        print("Closing windows")
        actuators.close()
    elif (command["values"][0][1] == 'PUMP_ON'):
        print("Pump on")
        pump.start()
    elif (command["values"][0][1] == 'PUMP_OFF'):
        print("Pump off")
        pump.stop()
    elif (command["values"][0][1] == 'REBOOT'):
        print("Rebooting")
        remove("running")
        system('sudo shutdown -r now')
    elif (command["values"][0][1] == 'SHUTDOWN'):
        print("Shutdown")
        remove("running")
        system('sudo shutdown now')
    else:
        continue

    influx.write_points([
        {
            "measurement": "action",
            "tags": {
                "id": command["tags"]["id"],
                "manual": "yes"
            },
            "fields": {
                "type": command["values"][0][1]
            }
        }
    ])

lastWindowAction = influx.query('SELECT type FROM "greenrpi"."autogen"."action" WHERE type = \'WINDOWS_OPEN\' OR type = \'WINDOWS_CLOSE\' OR type = \'WINDOWS_OPEN_50\' ORDER BY DESC LIMIT 1').get_points()
for action in lastWindowAction:
    randId = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(16))
    if (action["type"] == "WINDOWS_CLOSE" and temperature["indoor"] >= 30):
        print("Automatically opening windows")
        actuators.open()
        influx.write_points([
            {
                "measurement": "action",
                "tags": {
                    "id": randId,
                    "manual": "no"
                },
                "fields": {
                    "type": "WINDOWS_OPEN"
                }
            }
        ])
    elif ((action["type"] == "WINDOWS_OPEN" or action["type"] == "WINDOWS_OPEN_50") and temperature["indoor"] <= 25):
        print("Automatically closing windows")
        actuators.close()
        influx.write_points([
            {
                "measurement": "action",
                "tags": {
                    "id": randId,
                    "manual": "no"
                },
                "fields": {
                    "type": "WINDOWS_CLOSE"
                }
            }
        ])

# TODO: Automate water pump

####### Finish #######
setLeds(first=(0, 50, 0), second=(0, 50, 0), third=(0, 50, 0), fourth=(0, 50, 0))
GPIO.cleanup()
remove("running")
