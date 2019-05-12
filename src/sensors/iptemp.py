import os
import glob
import time

SENSOR_SOIL_1 = '28-01131be4a556';
SENSOR_SOIL_2 = '28-021313ce94aa';
SENSOR_SOIL_3 = '28-021312d2aeaa';
SENSOR_SOIL_4 = '28-020b92459057';
SENSOR_BARREL = '28-01131a8107d9';
SENSOR_OUTDOOR = '28-021312ef98aa';

base_dir = '/sys/bus/w1/devices/'

def readTempRaw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readTemp(sensor):
    device_folder = base_dir + sensor
    file = device_folder + '/w1_slave'

    lines = readTempRaw(file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempRaw(file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
