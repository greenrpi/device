from influxdb import InfluxDBClient
from config import config
from pathlib import Path
from os.path import isfile
from os import remove
from sys import exit
from time import sleep

#
####### Cycle consists of four phases and is run periodically every minute #######
#

####### Init #######
influx = InfluxDBClient(config['host'], config['port'], config['user'], config['password'], config['dbname'])
# We can't run more than one cycle at once so we end if previous didn't end
running = isfile("running")
if running:
    print("Previous cycle didn't end. Exiting!")
    exit()
Path('running').touch()

####### 1. PHASE - Get sensor data #######
temperatures = {
    'somename': 32,
    'othername': 28
}

####### 2. PHASE - Upload sensor data #######
for key, value in temperatures.items():
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

####### 3. PHASE - Download commands #######

####### 4. PHASE - Execute downloaded and automatic operations #######

####### Finish #######
remove("running")
