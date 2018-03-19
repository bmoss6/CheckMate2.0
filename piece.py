#! /usr/bin/python3

class Piece:
    def __init__(self, name=None, color=None):
        self.name = name
        self.color = color
        self.gpio = 0
        self.StartingPosition = None
        

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

    def getGpio(self):
        return self.gpio

    def isEmpty(self):
        if (self.name is None) and (self.color is None) and (self.gpio is 0):
            return True
        return False

    def clear(self):
        self.name = None
        self.color = None
        self.gpio = 0

    def setGPIO(self, gpio):
        self.gpio = gpio

    def update(self,peice):
        self.name = peice.getName()
        self.color = peice.getColor()

