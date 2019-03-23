import spidev
import time
import sys

spi = spidev.SpiDev()
spi.open(0, 0)


def readadc(adcnum):
    r = spi.xfer2([1,8+adcnum<<4,0])
    adcout = ((r[1]&3)<< 8)+r[2]
    print(r)
    return adcout


for channel in range(8):
    print('Napatie kanal'+str((channel))+ 'je' + str(readadc(channel)))
