import serial
import time
import random
import urllib2
import json
import sys

class NixieState:

    def __init__(self, number=0, left=False, right=False, brightness=128,
                 red=64, green=16, blue=32):
        self.number = number
        self.left = left
        self.right = right
        self.brightness = brightness
        self.red = red
        self.green = green
        self.blue = blue

    def getCommand(self):
        yesno = {True:'Y', False:'N'}
        return "$%d,%s,%s,%03d,%03d,%03d,%03d!" % (
            self.number,
            yesno[self.left],
            yesno[self.right],
            self.brightness,
            self.red,
            self.green,
            self.blue)

class Nixie:

    def __init__(self):
        self.state = NixieState()
        self.serial = serial.Serial('/dev/cu.usbserial-A9E997F7', 115200)
        self.update()

    def update(self):
        self.serial.write(self.state.getCommand())

    def setNumber(self, num):
        self.state.number = num
        self.update()

    def pulse(self):
        for i in xrange(32,256):
            self.state.brightness = i
            self.update()
            time.sleep(0.004)

        for i in xrange(256, 32, -1):
            self.state.brightness = i
            self.update()
            time.sleep(0.004)


def get_notifs_count(token):
    url = 'https://graph.facebook.com/me/notifications?access_token=%s' % token
    res = urllib2.urlopen(url).read()
    data = json.loads(res)

    summary = data['summary']
    if len(summary) == 0:
        return 0
    return summary['unseen_count']

nixie = Nixie()
last_count = -1
time_to_update = 15
while True:
    count = get_notifs_count(sys.argv[1])
    nixie.setNumber(count)
    if count != last_count:
        start = time.time()
        while time.time() - start < time_to_update:
            nixie.pulse()
    else:
        time.sleep(time_to_update)
    last_count = count

