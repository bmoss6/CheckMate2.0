#! /usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

A1 = 0
A2 = 0
A3 = 0
B1 = 0
B2 = 0
B3 = 0
C1 = 0
C2 = 0
C3 = 0

sensorA1 = 24
sensorA2 = 4 #15
sensorA3 = 6 #23
sensorB1 = 7
sensorB2 = 5 #8
sensorB3 = 8 #25
sensorC1 = 16
sensorC2 = 12
sensorC3 = 18

count = 0

#Setup GPIO pin
#GPIO.setup(sensorA1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
A1active = True
GPIO.setup(sensorA2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
A2active = True
GPIO.setup(sensorA3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
A3active = True
#GPIO.setup(sensorB1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
B1active = True
GPIO.setup(sensorB2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
B2active = True
GPIO.setup(sensorB3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
B3active = True
#GPIO.setup(sensorC1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
C1active = True
#GPIO.setup(sensorC2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
C2active = True
#GPIO.setup(sensorC3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
C3active = True
while count == 0:
    try:
#            A1active = GPIO.input(sensorA1)
            if A1active == False:
                A1 = 1
                sleep(.1)
            elif A1active == True:
                A1 = 0
                sleep(.1)
            A2active = GPIO.input(sensorA2)
            if A2active == False:
                A2 = 1
                sleep(.1)
            elif A2active == True:
                A2 = 0
                sleep(.1)
            A3active = GPIO.input(sensorA3)
            if A3active == False:
                A3 = 1
                sleep(.1)
            elif A3active == True:
                A3 = 0
                sleep(.1)
#            B1active = GPIO.input(sensorB1)
            if B1active == False:
                B1 = 1
                sleep(.1)
            elif B1active == True:
                B1 = 0
                sleep(.1)
            B2active = GPIO.input(sensorB2)
            if B2active == False:
                B2 = 1
                sleep(.1)
            elif B2active == True:
                B2 = 0
                sleep(.1)
            B3active = GPIO.input(sensorB3)
            if B3active == False:
                B3 = 1
                sleep(.1)
            elif B3active == True:
                B3 = 0
                sleep(.5)
#            C1active = GPIO.input(sensorC1)
            if C1active == False:
                C1 = 1
                sleep(.1)
            elif C1active == True:
                C1 = 0
                sleep(.1)
#            C2active = GPIO.input(sensorC2)
            if C2active == False:
                C2 = 1
                sleep(.1)
            elif C2active == True:
                C2 = 0
                sleep(.1)
#            C3active = GPIO.input(sensorC3)
            if C3active == False:
                C3 = 1
                sleep(.1)
            elif C3active == True:
                C3 = 0
                sleep(.1)
            print A3, B3, C3
            print A2, B2, C2
            print A1, B1, C1
            print ''
            sleep(0.1)
    except KeyboardInterrupt:
            print('End of program')
            GPIO.cleanup()
            break

    
