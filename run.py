#!/usr/bin/env python3
from robot import Robot 
from position import Position
from time import sleep
import logging,sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
   robot = Robot('/dev/ttyACM0')
   robot.move(Position(0,0),Position(6,6))
   robot.move(Position(0,0),Position(7,7))
   robot.move(Position(0,3),Position(7,0))
   robot.move(Position(0,7),Position(7,0))
   robot.move(Position(7,7),Position(0,0))
   robot.move(Position(0,3),Position(7,0))
   robot.move(Position(0,3),Position(7,7))
   robot.move(Position(0,4),Position(7,0))
   robot.move(Position(0,4),Position(7,7))
   robot.move(Position(1,1),Position(6,6))
   robot.move(Position(2,2),Position(5,5))
   robot.move(Position(5,5),Position(2,2))

   logging.debug('Sleep Loop')
   while True:
      sleep(1)

if __name__ == "__main__":
   main()
