#! /usr/bin/python3

import serial, time, logging
import time
from time import sleep

class uArmWrapper(object):
   """docstring for uArmWrapper"""

   defaultX = 108
   defaultY = 0
   defaultZ = 40
   speed = 10000

   debugNum = 0

   curX=0
   curY=0
   curZ=0

   def __init__(self, devPort):
      
      self.ser = ser = serial.Serial(
         port=devPort,
         baudrate=115200,
      )
      self.start()
      # self.arg = arg

   def start(self):
      sleep(2)
      #Need to read out device info from serial
      while self.ser.inWaiting() > 0:
         self.ser.read(1)
      self.ser.readline()

   def savePos(self,x,y,z):
      if x is None:
         x = self.curX
      else:
         self.curX = x
      if y is None:
         y = self.curY
      else:
         self.curY = y
      if z is None:
         z = self.curZ
      else:
         self.curZ = z

      return x, y, z

   
   def set_position(self,x=None,y=None,z=None):

      x, y, z = self.savePos(x,y,z)

      logging.debug("\tSet Position X:%d Y:%d Z:%d Speed:%d"%(x,y,z,self.speed))
      self.debugNum += 1
      cmdStr = '#%sG0 X%s Y%s Z%s F%s\n'%(self.debugNum,x,y,z,self.speed)
      self.ser.write(str.encode(cmdStr))
      response = str(self.ser.readline(),'utf-8')
      #If its a bad request then we need to read the empty line
      if "unreachable" in response:
         logging.error("\tERROR!: Invalid command %s"%cmdStr)
         self.ser.readline()
      else:
         logging.debug("\tRESPONSE:"+response)
      #sleep(1)
      
   def get_position(self):

      logging.debug("\tChecking Current Position")
      cmdStr = '#%sP2220\n'%(self.debugNum)
      self.ser.write(str.encode(cmdStr))
      response = str(self.ser.readline(),'utf-8')
      logging.debug("\tRESPONSE:"+response)
      #sleep(1)
      return response

   def open(self):
      self.ser.write(b'M2232 V0\n')
      response = str(self.ser.readline(),'utf-8')
      sleep(2)

   def close(self):
      self.ser.write(b'M2232 V1\n')
      response = str(self.ser.readline(),'utf-8')
      sleep(2)

   def setDefault(self,x,y,z,speed):
      self.defaultX = x
      self.defaultY = y
      self.defaultZ = z
      self.speed = speed

   def getDefault(self):
      return self.defaultX, self.defaultY, self.defaultZ

   def reset(self):
      #use defaults here
      self.savePos(self.defaultX,self.defaultY,self.defaultZ)
      logging.debug("\tMove to rest%d,%d,%d"%(self.defaultX,self.defaultY,self.defaultZ))
      self.set_position(self.defaultX,self.defaultY,self.defaultZ)
      logging.debug("\tDone Reset")
