import Adafruit_DHT as dht

INDOOR_PIN = 4
CASE_PIN = 15

def readTemperatureHumidity(pin):
    h, t = dht.read_retry(dht.AM2302, pin)
    return [h, t]
