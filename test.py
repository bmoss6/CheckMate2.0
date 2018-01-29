#! /usr/bin/python3

from uArmWrapper import uArmWrapper
from time import sleep
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

devPort= '/dev/ttyACM0'

#ROBOT TESTING LOOP
try:
	robot = uArmWrapper(devPort)
except Exception as e:
	print("[FAILED]\tUsing devPort '%s'. \nMake sure the robot is turned on and using the correct dev port "%devPort)
	quit()

while(1):
	cordsIn = input("Input Cordinates: ")
	if cordsIn == "open":
		robot.open()
		continue
	elif cordsIn == "close":
		robot.close()
		continue
	cords = cordsIn.split()
	if len(cords) < 3:
  		break
	x = int(cords[0])
	y = int(cords[1])
	z = int(cords[2])
	robot.set_position(x,y,z)
	response = robot.get_position().split(" ")
	print (response)

robot.reset()

while(1):
	sleep(1)
