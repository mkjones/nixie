import serial
import time
import random
import urllib2
import json
import sys

class NixieState:

    def __init__(self, number=0, left=False, right=False, brightness=128,
                 red=32, green=4, blue=16):
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

    def setLeft(self, value):
        self.state.left = value
        self.update()

    def setRight(self, value):
        self.state.right = value
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
    try:
        res = urllib2.urlopen(url)
    except Error as e:
        print e
        return 0
    print res.info()
    print res.getcode()
    data = json.loads(res.read())

    summary = data['summary']
    if len(summary) == 0:
        return 0
    return summary['unseen_count']

nixie = Nixie()
last_count = -1
time_to_update = 15
while True:
    count = get_notifs_count(sys.argv[1])
    if count > 29:
        nixie.setLeft(True)
        nixie.setRight(True)
        nixie.setNumber(9)
    elif count > 19:
        nixie.setLeft(True)
        nixie.setRight(True)
        nixie.setNumber(count - 20)
    elif count > 9:
        nixie.setLeft(True)
        nixie.setRight(False)
        nixie.setNumber(count - 10)
    else:
        nixie.setLeft(False)
        nixie.setRight(False)
        nixie.setNumber(count)

    if count != last_count:
        start = time.time()
        while time.time() - start < time_to_update:
            nixie.pulse()
    else:
        time.sleep(time_to_update)
    last_count = count

