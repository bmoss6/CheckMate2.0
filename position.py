#!/usr/bin/env python3
import logging
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def confI(obj,var):
    return int(config[obj][var])

class Position(object):

    #Robot Cordinates in MM
    x = 0
    y = 0
    #Position on Board
    xBoard = 0
    yBoard = 0
    #Oppisiate 
    invert = False

    """docstring for position"""
    def __init__(self, x, y, invert=False):
        super(Position, self).__init__()
        if invert:
            x, y = self.invert()
        self.xBoard = x
        self.yBoard = y
        self.xConvert(self.xBoard)
        self.yConvert(self.yBoard)

    def getY(self):
        return self.y
        
    def getX(self):
        return self.x

    def getXBoard(self):
        return self.xBoard

    def getYBoard(self):
        return self.yBoard

    def yConvert(self,y):
        yPos = y - confI('board','threshHold')
        #logging.debug(yPos)
        self.y = (yPos * confI('offsets','inc')) + confI('offsets', 'y')

    def xConvert(self,x):
        self.x = confI('offsets','x') + x * confI('offsets','inc')

    def invert(self,x,y):
        invertDict = {2:0, 1:1, 0:2}
        return invertDict[x], invertDict[y]
