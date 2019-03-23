import Adafruit_DHT as dht
h,t = dht.read_retry(dht.AM2302, 25)
print ('Snimac zdroj Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
h,t = dht.read_retry(dht.AM2302, 16)
print ('Snimac stol Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
h,t = dht.read_retry(dht.AM2302, 22)
print ('Snimac vzduch Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
h,t = dht.read_retry(dht.AM2302, 4)
print ('Snimac vzduch2 Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))

