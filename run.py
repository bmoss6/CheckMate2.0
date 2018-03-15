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
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Set to true to test off of the robots and PI. 
# also comment out "from gpio import GPIOBOARD" in board.py
testMode = False

GameScripts = "GameScripts"

if not testMode:
   import GPi.GPIO as GPIO
   ##Setup GPIO PIN for Reset Button ##
   GPIO.setup(1,GPIO.IN,pull_up_down=GPIO.PUD_UP)



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
         robot.move(start,end,castle)
      if rb2Move is not None:
         logging.debug("ROBOT2: Start[%d,%d] End[%d,%d]"% \
            (rb2Move[0][0],rb2Move[0][1],rb2Move[1][0],rb2Move[1][1]))
         start = Position(rb2Move[0][0],rb2Move[0][1],True)
         end = Position(rb2Move[1][0],rb2Move[1][1],True)
         castle = int(rb2Move[2])
         robot2.move(start,end,castle)

   #The board is shared so it can be reset by either robot.
   robot.resetBoard()

def setupRobots():
   #Both boards should just be in the same class.
   gameBoard = Board()

   #Setup Robots
   RL = RobotList(2)
   robotList = RL.getList()
   if robotList is False:
      quit()

   # Robots share the same board 
   robot = Robot(robotList[0],gameBoard)
   GPIO.add_event_detect(1, GPIO.BOTH, robot.reset())
   robot2 = Robot(robotList[1],gameBoard)
   return robot, robot2

def testRobotSetup():
   gameBoard = Board(test=True)

   # Robots share the same board 
   robot = Robot(None,gameBoard,True)
   robot2 = Robot(None,gameBoard,True)
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

   logging.debug('Sleep Loop')
   while True:
      sleep(1)

if __name__ == "__main__":
   main()