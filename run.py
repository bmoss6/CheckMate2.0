#!/usr/bin/env python3
from robot import Robot 
from position import Position
from time import sleep
from robotList import RobotList
import logging,sys


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
   RL = RobotList(1)
   robotList = RL.getList()

   robot = Robot(robotList[0])
   if len(robotList) == 2:
      robot2 = Robot(robotList[1])

#   Test the capturing algorithm
   robot.move(Position(0,0),Position(7,4))
   robot.move(Position(0,1),Position(7,5))
   robot.move(Position(0,2),Position(7,6))
   robot.move(Position(0,3),Position(7,7))
#   robot.move(Position(0,4),Position(7,3))
#   robot.move(Position(0,5),Position(7,2))
#   robot.move(Position(0,6),Position(7,1))
#   robot.move(Position(0,7),Position(7,0))
   robot.move(Position(1,0),Position(6,4))
   robot.move(Position(1,1),Position(6,5))
   robot.move(Position(1,2),Position(6,6))
   robot.move(Position(1,3),Position(6,7))
#   robot.move(Position(2,0),Position(5,4))
#   robot.move(Position(2,1),Position(5,5))
#   robot.move(Position(2,2),Position(5,6))
#   robot.move(Position(2,3),Position(5,7))

#   Test the inverse functionality
   # robot.move(Position(0,0),Position(3,3))
   # robot2.move(Position(0,0, True),Position(3,3, True))
   # robot.move(Position(0,7),Position(3,4))
   # robot2.move(Position(0,7, True),Position(3,4, True))
   # robot.move(Position(0,2),Position(3,3))
   # robot2.move(Position(0,2, True),Position(3,3, True))

   logging.debug('Sleep Loop')
   while True:
      sleep(1)

if __name__ == "__main__":
   main()
