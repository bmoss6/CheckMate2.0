#!/usr/bin/env python3
from robot import Robot 
from position import Position
from time import sleep
import logging,sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
   robot = Robot('/dev/ttyACM0')
   robot.move(Position(0,0),Position(0,7))
   robot.move(Position(1,0),Position(1,7))
   robot.move(Position(2,0),Position(2,7))
   robot.move(Position(3,0),Position(3,7))
   robot.move(Position(4,0),Position(4,7))
   robot.move(Position(5,0),Position(5,7))
   robot.move(Position(6,0),Position(6,7))
   robot.move(Position(7,0),Position(7,7))

   logging.debug('Sleep Loop')
   while True:
      sleep(1)

if __name__ == "__main__":
   main()
