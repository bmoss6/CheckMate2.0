#! /usr/bin/python3

from position import Position
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def confI(obj,var):
   return int(config[obj][var])


## Capture Position
#  This class is used by the capture board to set the robot coordinates to place
#  the captured peices. It inherts from the poistion class and only needs to change
#  the y offset of the peice
class CapturePosition(Position):

   ## @var nextSide:bool
   #  use the other side of the capture board
   nextSide=False

   ## Constructor
   #  @param x:int x poistion used by parent class position
   #  @param y:int y poistion used by parent class position with an added offset
   #  @param ns:Bool if one side of the board is full use the other side with the second offset.
   #  @param invert:Bool invert peice poistion used by parent class
   def __init__(self,x,y,ns,invert):
      super(CapturePosition, self).__init__(x, y, invert)
      self.nextSide = ns
      if self.nextSide:
         self.y += confI('offsets','captureL')
      else:
         self.y += confI('offsets','captureR')

