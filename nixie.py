import serial
import time
import random

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

nixie = Nixie()
for i in xrange(0, 10):
    nixie.setNumber(i)
    time.sleep(1)

