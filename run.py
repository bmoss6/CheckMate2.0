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
import RPi.GPIO as GPIO
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

GameScripts = "GameScripts"
##Setup GPIO PIN for Reset Button ##
GPIO.setmode(GPIO.BCM)
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
         robot.move(start,end)
      if rb2Move is not None:
         logging.debug("ROBOT2: Start[%d,%d] End[%d,%d]"% \
            (rb2Move[0][0],rb2Move[0][1],rb2Move[1][0],rb2Move[1][1]))
         start = Position(rb2Move[0][0],rb2Move[0][1],True)
         end = Position(rb2Move[1][0],rb2Move[1][1],True)
         robot2.move(start,end)

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
   GPIO.add_event_detect(1, GPIO.BOTH, robot.resetBoard)
   robot2 = Robot(robotList[1],gameBoard)
   return robot, robot2

def main():

   # Setup board and capture board to share between robots
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


# #   Test the capturing algorithm
#    robot.move(Position(0,0),Position(7,4))
#    robot.move(Position(0,1),Position(7,5))
#    robot.move(Position(0,2),Position(7,6))
#    robot.move(Position(0,3),Position(7,7))
# #   robot.move(Position(0,4),Position(7,3))
# #   robot.move(Position(0,5),Position(7,2))
# #   robot.move(Position(0,6),Position(7,1))
# #   robot.move(Position(0,7),Position(7,0))
#    robot.move(Position(1,0),Position(6,4))
#    robot.move(Position(1,1),Position(6,5))
#    robot.move(Position(1,2),Position(6,6))
#    robot.move(Position(1,3),Position(6,7))
# #   robot.move(Position(2,0),Position(5,4))
# #   robot.move(Position(2,1),Position(5,5))
# #   robot.move(Position(2,2),Position(5,6))
# #   robot.move(Position(2,3),Position(5,7))

#   Test the inverse functionality
#    robot.move(Position(0,0),Position(3,3))
#    robot2.move(Position(0,0, True),Position(3,3, True))
#    robot.move(Position(0,7),Position(3,4))
#    robot2.move(Position(0,7, True),Position(3,4, True))
#    robot.move(Position(0,2),Position(3,3))
#    robot2.move(Position(0,2, True),Position(3,3, True))
