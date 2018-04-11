#!/usr/bin/env python3
import logging
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def confI(obj,var):
    return int(config[obj][var])

## Position
#  The main purpose of the position class is the abstact the MM coordiates used by
#  the robot to positions on the board. It is imporant to note that even though the 
#  robots are facing differnt directions that they will both used the same cooridate
#  posistions for each square on the board. This is relativly easy to accomplish in 
#  that for one of the robots all of the robot poistion coordinates 
#  need to be fliped. ie. the invert paramter
class Position(object):

    ## @var x:int
    #  x coordinate of MM of the peice (x direction away and toward the robot)
    x = 0
    ## @var y:int
    #  y coordinate of MM of the peice (y direction is left and right of the robot)
    y = 0
    ## @var xBoard:int
    #  the x position of the peice on the board
    xBoard = 0
    ## @var yBoard:int
    #  the y position of the peice on the board
    yBoard = 0 
    ## @var invert:bool
    #  value to flag in the robot poistion should be inverted for second robot
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

    ## get y poition of robot in mm
    #  @return type:int
    def getY(self):
        return self.y
        
    ## get x poition of robot in mm
    #  @return type:int
    def getX(self):
        return self.x

    ## get x board poition of robot
    #  @return type:int
    def getXBoard(self):
        return self.xBoard

    ## get y board poition of robot
    #  @return type:int
    def getYBoard(self):
        return self.yBoard

    ## convert and set the y board coordinate to the coordinate read by the robot
    def yConvert(self,y):
        yCoord = "c" + str(y)
        self.y = confI('board', yCoord)
    #    yPos = y - confI('board','threshHold')
    #    #logging.debug(yPos)
    #    self.y = (yPos * confI('offsets','inc')) + confI('offsets', 'y')

    ## convert and set the x board coordinate to the coordinate read by the robot
    def xConvert(self,x):
        xCoord = "r" + str(x)
        self.x = confI('board', xCoord)
    #    self.x = confI('offsets','x') + x * confI('offsets','inc')

    ## invert the coordinates for second robot
    #  @return type:int type:int inverted x, inverted y
    def invert(self,x,y):
        invertDict = {7:0, 6:1, 5:2, 4:3, 3:4, 2:5, 1:6, 0:7}
        return invertDict[x], invertDict[y]
