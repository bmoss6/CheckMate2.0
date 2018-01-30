#!/usr/bin/env python3
from robot import Robot 
from position import Position
from time import sleep
import logging,sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
   robot = Robot('/dev/ttyACM0')
   robot.move(Position(1,1),Position(6,6))
	# robot.move(Position(2,2),Position(5,5))
	# robot.move(Position(5,5),Position(2,2))
	# robot.move(Position(5,5),Position(2,2))
   robot.move(Position(3,2),Position(6,5))

   logging.debug('Sleep Loop')
   while True:
      sleep(1)

if __name__ == "__main__":
   main()
