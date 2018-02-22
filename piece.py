#! /usr/bin/python3

class Piece:
    def __init__(self, name=None, color=None):
        self.name = name
        self.color = color

    def getName(self):
        return self.name

    def getColor(self):
        return self.color 

    def isEmpty(self):
        if (self.name is None) and (self.color is None):
            return True
        return False

    def clear(self):
        self.name = None
        self.color = None

    def update(self,peice):
        self.name = peice.getName()
        self.color = peice.getColor()

