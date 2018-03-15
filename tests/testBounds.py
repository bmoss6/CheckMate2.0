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

#log fails for future reference
toWrite = open("fullresults.txt", "a")
toWrite.write("Start of test 1")

toWrite.write("...........Testing close X bounds..........\n")
#test close bounds
for ex in range(106, 200):
  
  zee = 30
  
  while (1):
    cordsIn = str(str(ex) + " 0 " + str(zee))
    if cordsIn == "open":
      robot.open()

    elif cordsIn == "close":
      robot.close()

    cords = cordsIn.split()
#if len(cords) < 3:
#	break
    x = int(cords[0])
    y = int(cords[1])
    z = int(cords[2])
    robot.set_position(x,y,z)
    response = robot.get_position().strip().split(" ")
    print(response)
    if (response[4] != ("Z" + str(z) + ".00") or zee == 140):
      toWrite.write(str(response) + '\n')
      print("about to break")
      break
    zee = zee + 1

  if (zee == 140):
    break

toWrite.write("...........Testing far X bounds..........\n")
#Test far bounds
for ex in range(350, 300, -1):
  
  zee = 30
  
  while (1):
    cordsIn = str(str(ex) + " 0 " + str(zee))
    if cordsIn == "open":
      robot.open()

    elif cordsIn == "close":
      robot.close()

    cords = cordsIn.split()
#if len(cords) < 3:
#	break
    x = int(cords[0])
    y = int(cords[1])
    z = int(cords[2])
    robot.set_position(x,y,z)
    response = robot.get_position().strip().split(" ")
    print(response)
    if (response[4] != ("Z" + str(z) + ".00") or zee == 140):
      toWrite.write(str(response) + '\n')
      print("about to break")
      break
    zee = zee + 1

  if (zee == 140):
    break  


#This part is not yet working as intended.
toWrite.write("...........Testing far negative Y bounds..........\n")  
#Test far negative y bounds
for ex in range(350, 300, -1):
  
  why = -110
  
  while(1):
  
    zee = 30
    
    while (1):
      cordsIn = str(str(ex) + " " + str(why) + " " + str(zee))
      if cordsIn == "open":
        robot.open()
  
      elif cordsIn == "close":
        robot.close()
  
      cords = cordsIn.split()
  #if len(cords) < 3:
  #	break
      x = int(cords[0])
      y = int(cords[1])
      z = int(cords[2])
      robot.set_position(x,y,z)
      response = robot.get_position().strip().split(" ")
      print(response)
      if (response[4] != ("Z" + str(z) + ".00") or zee == 100):
        toWrite.write("command called: " + str(cordsIn) + '\n')
        print("about to break")
        break
      zee = zee + 1
  
    if (zee == 100):
      break
      
    why = why + 1
        
  if (why >= -80):
    break

toWrite.write("...........Testing far positive Y bounds..........\n")
#Test far positive y bounds
for ex in range(350, 300, -1):
  
  why = 110
  
  while(1):
  
    zee = 30
    
    while (1):
      cordsIn = str(str(ex) + " " + str(why) + " " + str(zee))
      if cordsIn == "open":
        robot.open()
  
      elif cordsIn == "close":
        robot.close()
  
      cords = cordsIn.split()
  #if len(cords) < 3:
  #	break
      x = int(cords[0])
      y = int(cords[1])
      z = int(cords[2])
      robot.set_position(x,y,z)
      response = robot.get_position().strip().split(" ")
      print(response)
      if (response[4] != ("Z" + str(z) + ".00") or zee == 100):
        toWrite.write("command called: " + str(cordsIn) + '\n')
        print("about to break")
        break
      zee = zee + 1
  
    if (zee == 100):
      break
      
    why = why - 1
        
  if (why <= 80):
    break  
  
toWrite.close()
robot.reset()

while(1):
	sleep(1)
