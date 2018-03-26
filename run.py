#!/usr/bin/env python3
from robot import Robot 
from position import Position
from time import sleep
from robotList import RobotList
from game import Game
from board import Board
from captureBoard import CaptureBoard
from itertools import zip_longest
from os import listdir
from os.path import isfile, join
from config import Conf
import logging, sys
import RPi.GPIO as GPIO
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
conf = Conf()

# Set to true to test off of the robots and PI. 
# also comment out "from gpio import GPIOBOARD" in board.py
testMode = False 

if not testMode:
   import RPi.GPIO as GPIO
   ##Setup GPIO PIN for Reset Button ##
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(1,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GameScripts = "GameScripts"

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

def setupRobots():
   #Both boards should just be in the same class.
   gameBoard = Board()
   captureBoard1 = CaptureBoard()
   captureBoard2 = CaptureBoard()

   #Setup Robots
   RL = RobotList(2)
   robotList = RL.getList()
   if robotList is False:
      quit()

   # Robots share the same board 
   robot = Robot(robotList[0],gameBoard,captureBoard1)
   GPIO.add_event_detect(1, GPIO.BOTH, robot.resetBoard)
   robot2 = Robot(robotList[1],gameBoard,captureBoard2)

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

def testRobotSetup():
   gameBoard = Board(test=True)
   captureBoard1 = CaptureBoard()
   captureBoard2 = CaptureBoard()

   # Robots share the same board 
   robot = Robot(None,gameBoard,captureBoard1,test=True)
   robot2 = Robot(None,gameBoard,captureBoard2,test=True)
   return robot, robot2

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
