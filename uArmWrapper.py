#! /usr/bin/python3
import serial, time, logging
import time
from time import sleep

## A simplified wrapper to the UARM robot.
#  The [original wrapper](https://github.com/uArm-Developer/pyuf) is currently
#  very unrealiable so this give a limited list of commands that our robot needs.
#
#  This wrapper communitates over a serial connection to the robot by sending
#  the raw API commands to the arduino on board the robot. To see a list of
#  commands view [their documentation](http://download.ufactory.cc/docs/en/uArm-Swift-Pro-Develper-Guide-171221.pdf).
#  
#  It is imporant to not that unlike the orignal wrapper all function calls are blocking.
#  all of the commands block on read on the serial connection until they recive a response 
#  that the robot has completed the command or it has errored. 
#
#  Lastley robot does have limits and so not all coordinates you input will work. The arduino API
#  is a little unreliable but set_position should print an error if something goes wrong. 
#
class uArmWrapper(object):

   ## The constructor to initlize defaults and establish a serial communcation 
   #  to the robot.
   #  @param devPort:string USB port to robot. /dev/ttyACM[0-9]*
   def __init__(self, devPort):
      ## @var defaultX:int
      #  defualt X (forward and backward from the robot perspective) resting position of the robot.
      self.defaultX = 120
      ## @var defaultY:int
      #  defualt Y (left to right from the robot perspective) resting position of the robot.
      self.defaultY = 0
      ## @var defaultZ:int
      #  defualt resting position of the robot.
      self.defaultZ = 60
      ## @var speed:int
      #  defualt resting position of the robot.
      self.speed = 10000
      ## @var debugNum:int
      #  You can assing a number to a command that is run to verify that it comes back correctly
      #  beuase we only run one command at a time and block this is not super helpful but we used it.
      self.debugNum = 0

      ## @var curX:int
      #  the current x position of the robot
      self.curX=0
      ## @var curY:int
      #  the current y position of the robot
      self.curY=0
      ## @var curZ:int
      #  the current z position of the robot
      self.curZ=0
      
      ## @var ser:Serial
      # serial connection to communcate with aurdino within the robot.
      self.ser = ser = serial.Serial(
         port=devPort,
         baudrate=115200,
      )
      self.start()

   ## Read in initilization data
   #  When we first connect to the robot it sends a bunch of data we need to read
   #  in order to read the commands we send later.
   def start(self):
      #Give time to intilize
      sleep(2)
      #read out all of the data currently waiting
      while self.ser.inWaiting() > 0:
         self.ser.read(1)
      self.ser.readline()

   ## Save the current position
   #  Save coordinate. This should only be used internally
   #  @param x:int X position
   #  @param y:int Y position
   #  @param z:int Z position
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

   ## Set  position of the robot.
   #  Move the robot to the specifed x,y,z coordiante and save the coordiante for later.
   #  You are able to specify only one axis is desired.
   #  @param x:int X position
   #  @param y:int Y position
   #  @param z:int Z position
   def set_position(self,x=None,y=None,z=None):

      x, y, z = self.savePos(x,y,z)

      self.debugNum += 1
      cmdStr = '#%sG0 X%s Y%s Z%s F%s\n'%(self.debugNum,x,y,z,self.speed)
      self.ser.write(str.encode(cmdStr))
      response = str(self.ser.readline(),'utf-8')
      #If its a bad request then we need to read the empty line
      if "unreachable" in response:
         logging.error("\tERROR!: Invalid command %s"%cmdStr)
         self.ser.readline()
      else:
         pass
         #logging.debug("\tRESPONSE:"+response)

   ## Get current position of the robot.
   #  Although we save the position this function asks the robot what it thinks its current position is
   #  to make sure the position is correct
   #  @return API response:string
   def get_position(self):
      logging.debug("\tChecking Current Position")
      cmdStr = '#%sP2220\n'%(self.debugNum)
      self.ser.write(str.encode(cmdStr))
      response = str(self.ser.readline(),'utf-8')
      logging.debug("\tRESPONSE:"+response)

      return response

   ##  Open gripper
   def open(self):
      self.ser.write(b'M2232 V0\n')
      response = str(self.ser.readline(),'utf-8')
      sleep(2)

   ## Close gripper
   def close(self):
      self.ser.write(b'M2232 V1\n')
      response = str(self.ser.readline(),'utf-8')
      sleep(2)

   ## Set default postion and speed
   #  @param x:int X resting position
   #  @param y:int Y resting position
   #  @param z:int Z resting position
   #  @param speed:int speed of robot. 
   def setDefault(self,x,y,z,speed):
      self.defaultX = x
      self.defaultY = y
      self.defaultZ = z
      self.speed = speed

   ## get set defaults
   #  @return x:int, y:int, z:int
   def getDefault(self):
      return self.defaultX, self.defaultY, self.defaultZ

   ## get UID
   #  get the unique identification number of the robot so that we are able to tell them apart.
   #  This is important becuase the ports they are assigned to may switch
   #  @return UID:string
   def getUID(self):
      self.ser.write(b'P2205\n') 
      ret = str(self.ser.readline(),'utf-8')
      return ret.split(" ")[-1].rstrip()

   ## Reset robot position
   #  move the robot back to the resting position
   def reset(self):
      self.savePos(self.defaultX,self.defaultY,self.defaultZ)
      logging.debug("\tMove to rest%d,%d,%d"%(self.defaultX,self.defaultY,self.defaultZ))
      self.set_position(self.defaultX,self.defaultY,self.defaultZ)
      logging.debug("\tDone Reset")
