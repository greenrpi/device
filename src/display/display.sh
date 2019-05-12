#!/bin/sh
raspistill -ISO 800 -ex backlight -awb off -w 320 -h 240 -co 100 -sh 100 -sa 100 -ss 100000 -t 1 -e bmp -o /tmp/display.bmp
convert /tmp/display.bmp -rotate -1.5 -modulate 100,0 -level 25%,70% -negate -crop 140x70+80+100 /tmp/display-crop.jpg
gosser -i /tmp/display-crop.jpg -m manifest.json -p 3
convert /tmp/display.bmp -rotate -1.5 -modulate 100,0 -level 25%,70% -negate -crop 54x36+12+99 /tmp/display-crop.jpg
gosser -i /tmp/display-crop.jpg -m manifest-input.json -p 2
