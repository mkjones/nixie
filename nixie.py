import serial
import time
import random

ser = serial.Serial('/dev/cu.usbserial-A9E997F7', 115200)
for i in xrange(0, 10):
    for brightness in xrange(0, 256):
        ser.write("$%d,N,Y,%03d,064,032,016!" % (i, brightness))
    time.sleep(1)
