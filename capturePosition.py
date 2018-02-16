#! /usr/bin/python

from position import Position
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def confI(obj,var):
    return int(config[obj][var])

class CapturePosition(Position):

   nextSide=False

   def __init__(self,x,y,ns,invert):
      super(CapturePosition, self).__init__(x, y, invert)
      self.nextSide = ns
      if self.nextSide:
         self.y += confI('offsets','captureR')
      else:
         self.y += confI('offsets','captureL')


      #print("INVERT %d x:%d"%(invert,self.x))
      #print(super(CapturePosition, self).getXBoard())

