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
    invert = False

    """docstring for position"""
    def __init__(self, x, y, invert=False):
        super(Position, self).__init__()
        # The board position must stay true to its coordinates.
        # This is because we need to map the coordinates to the board.
        # Although we invert the robot coordinates so that the robot
        # picks up the right peice.
        self.xBoard = x
        self.yBoard = y
        if invert:
            x, y = self.invert(x, y)
        self.xConvert(x)
        self.yConvert(y)

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
        invertDict = {7:0, 6:1, 5:2, 4:3, 3:4, 2:5, 1:6, 0:7}
        return invertDict[x], invertDict[y]
