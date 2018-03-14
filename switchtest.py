#!/usr/bin/python3
# script by Alex Eames http://RasPi.tv/  
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio  
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
  
GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	  
	  # now the program will do nothing until the signal on port 23   
	  # starts to fall towards zero. This is why we used the pullup  
	  # to keep the signal high and prevent a false interrupt  
	    
try:  
    GPIO.wait_for_edge(1, GPIO.FALLING)  
    print ("whatever was waiting for a button press.")  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    GPIO.cleanup()           # clean up GPIO on normal exit  
