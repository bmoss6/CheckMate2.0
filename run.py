#!/usr/bin/env python3
from time import sleep
import os
# This is a super hacky way to make sure python is ready before we start
if False:
   os.chdir("/home/pi/Documents/CheckMate2.0")
   tries = 0
   tmpFile ="test.txt"
   maxTries = 60
   while True:
      if (tries > 60):
         exit()
      try:
         f= open(tmpFile,"w+")
         f.write("script has run\n")
         f.close()
         os.remove(tmpFile)
         break
      except Exception as e:
         tries += 1
         sleep(1)

from robot import Robot 
from position import Position
from robotList import RobotList
from game import Game
from board import Board
from captureBoard import CaptureBoard
from itertools import zip_longest
from os import listdir
from os.path import isfile, join
import logging, sys
import RPi.GPIO as GPIO
from config import Conf
conf = Conf()
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Set to true to test off of the robots and PI. 
# also comment out "from gpio import GPIOBOARD" in board.py
testMode = False 

if not testMode:
   import RPi.GPIO as GPIO
   ##Setup GPIO PIN for Reset Button ##
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(1,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GameScripts = "GameScripts"

## play game read in for PGN file from the GameScirpts folder
#  @param robot:Robot first robot for game
#  @param robot2:Robot second robot for game
def playGame(game,robot,robot2):
   game = Game(game)
   robot1Moves, robot2Moves = game.getMoves()

   turn = 0
   for rb1Move, rb2Move in zip_longest(robot1Moves,robot2Moves,fillvalue=None):
      turn += 1
      logging.debug("Turn:%d"%turn)
      if rb1Move is not None:
         logging.debug("ROBOT1: Start[%d,%d] End[%d,%d]"% \
            (rb1Move[0][0],rb1Move[0][1],rb1Move[1][0],rb1Move[1][1]))
         start = Position(rb1Move[0][0],rb1Move[0][1])
         end = Position(rb1Move[1][0],rb1Move[1][1])
         castle = int(rb1Move[2])
         if castle != 0:
            robot.castle(castle,1)
         else:
            robot.move(start,end)
      if rb2Move is not None:
         logging.debug("ROBOT2: Start[%d,%d] End[%d,%d]"% \
            (rb2Move[0][0],rb2Move[0][1],rb2Move[1][0],rb2Move[1][1]))
         start = Position(rb2Move[0][0],rb2Move[0][1],True)
         end = Position(rb2Move[1][0],rb2Move[1][1],True)
         castle = int(rb2Move[2])
         if castle != 0:
            robot2.castle(castle,2)
         else:
            robot2.move(start,end)

   #The board is shared so it can be reset by either robot.
   robot.resetBoard(None)

def pauseGame():
   while True:
      time.sleep()

## initialize the robots and board used for the game
#  @return Robot1, Robot2
def setupRobots():

   retry_autostart = conf.I('game','retry_autostart')
   autostart = False
   if conf.S('game','autostart') == 'True':
      autostart = True

   #Both boards should just be in the same class.
   gameBoard = Board()
   captureBoard1 = CaptureBoard()
   captureBoard2 = CaptureBoard()

   #Setup Robots
   RL = RobotList(2)
   robotList = None
   while True:
      robotList = RL.getList()
      if robotList is False and autostart:
         retry_autostart -= 1
         #try again to get serial ports
         RL.serial_ports()
         if retry_autostart <= 0:
            logging.error("Unable to find robots on start")
            break
         sleep(3)
      elif not autostart:
         break
      else:
         break
     
   if robotList is False:
      print("Found to many or not enough robots to start." \
         "\nChange the number of robots in RobotList in run.py if testing.")
      quit()

   # Robots share the same board 
   robot = Robot(robotList[0],gameBoard,captureBoard1,"white")
   GPIO.add_event_detect(1, GPIO.BOTH, pauseGame)
   robot2 = Robot(robotList[1],gameBoard,captureBoard2, "black")

   # Check to verify the robots are not switched
   robot1ID = conf.S('robotIdents','robot1')
   logging.debug("Robot1 %s"%robot1ID)
   robot2ID = conf.S('robotIdents','robot2')
   logging.debug("Robot2 %s"%robot2ID)

   # Switch the robots if they look incorrect
   if not robot.checkID(robot1ID):
      logging.debug("switching robots")
      tmpRobot = robot2
      robot2 = robot
      robot = tmpRobot

   # Sanity check to make sure they match up after switch
   if robot.checkID(robot1ID):
      logging.error("Unable to identify robot 1!")
   if robot2.checkID(robot2ID):
      logging.error("Unable to identify robot 2!")

   return robot, robot2

## setup the robots without connection the API to test without the robots
#  @return Robot1, Robot2
def testRobotSetup():
   gameBoard = Board(test=True)
   captureBoard1 = CaptureBoard()
   captureBoard2 = CaptureBoard()

   # Robots share the same board 
   robot = Robot(None,gameBoard,captureBoard1,test=True)
   robot2 = Robot(None,gameBoard,captureBoard2,test=True)
   return robot, robot2

def testRobotRestart():
   robot, robot2 = setupRobots()
   robot.clearRobotPieces()
   robot2.clearRobotPieces()
   robot.resetToOriginalPosition()
   robot2.resetToOriginalPosition()
   
   
def main():

   # Setup board and capture board to share between robots
   if testMode:
      robot, robot2 = testRobotSetup()
   else:
      robot, robot2 = setupRobots()

   # Read all of the games from GameScript folder
   gameFiles = [join(GameScripts, f) for f in listdir(GameScripts) if isfile(join(GameScripts, f))]

   # Loop this forever
   for game in gameFiles:
      playGame(game,robot,robot2)

   if testMode:
      return

   logging.debug('Sleep Loop')
   while True:
      sleep(1)

if __name__ == "__main__":
   main()
   #testRobotRestart()
