#!/usr/bin/env python3
from robot import Robot 
from position import Position
from time import sleep
import logging,sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
   robot = Robot('/dev/ttyACM0')
   robot.move(Position(6,4),Position(4,4))
   robot.move(Position(1,3),Position(2,2))
   robot.move(Position(7,5),Position(3,1))
   robot.move(Position(2,2),Position(4,4))

   logging.debug('Sleep Loop')
   while True:
      sleep(1)

if __name__ == "__main__":
   main()
