#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import itertools
import logging

## The GPIO Class for keeping track of where pieces are. Originally this was going to be an integral part of
#  error checking for the robots. However, as time went by it became clear that this functionality was going to be a mere
#  safety feature and not an actual critical function of the project.
#  However, we realized this after prototype boards and wiring had already been made. So it was decided that this feature
#  could actually be a forerunner to a more advanced system where robots are able to play against human counterparts.
#  The gpio class consists of the GPIO pins that are connected to each square of the board as well as logic that checks the
#  state of the gpios to determine whether a reed switch has been activated.
#  Magnets are placed at the bottom of each physical piece which should trigger a reed switch when placed on top of it.
class GPIOBOARD():
    ## The inital constructor creates the maps made for reading the gpio switches. Please refer to the wiring documentation
    #  for more details on the process. A gpioboard is also created, which is just a 2-d array of either 1's or 0's depending on
    #  whether a switch has been acgtivated.

    def __init__(self):
        ## @param Mux Tables: Maps a GPIO pin to the mux inputs. See wiring documentation for further details.
        self.Mux1= {'A': 24, 'B': 23, 'C': 18, 'D': 15, 'W': 14}
        self.Mux2= {'A': 16, 'B': 12, 'C': 7, 'D': 8, 'W': 25}
        self.Mux3= {'A': 4, 'B': 3, 'C': 2, 'D': 21, 'W': 20}
        self.Mux4= {'A': 19, 'B': 10, 'C': 22, 'D': 27, 'W': 17}
        ## @param MuxList: Combined list of all the muxmaps.
        self.MuxList = [self.Mux1, self.Mux2, self.Mux3, self.Mux4]
        ## @param gpioboard: Initial gpio board (2-d array) containing all 0's (default state)
        self.gpioboard=[ [0 for i in range(8)] for x in range(8)]
        ## @param MuxToCoordinateMap: Each square on the grid needs to match a particular mux and gpio reading (1-16). This map
        ## maps a square on the physical board to a mux and input number.
        self.MuxToCoordinateMap = {"1.0":"7,3","1.1":"7,1","1.2":"7,2","1.3":"7,0","1.4":"5,3","1.5":"5,1","1.6":"5,2","1.7":"5,0","1.8":"6,3","1.9":"6,1","1.10":"6,2","1.11":"6,0","1.12":"4,3","1.13":"4,1","1.14":"4,2","1.15":"4,0","2.0":"7,7","2.1":"7,5","2.2":"7,6","2.3":"7,4","2.4":"5,7","2.5":"5,5","2.6":"5,6","2.7":"5,4","2.8":"6,7","2.9":"6,5","2.10":"6,6","2.11":"6,4","2.12":"4,7","2.13":"4,5","2.14":"4,6","2.15":"4,4","3.0":"3,3","3.1":"3,1","3.2":"3,2","3.3":"3,0","3.4":"1,3","3.5":"1,1","3.6":"1,2","3.7":"1,0","3.8":"2,3","3.9":"2,1","3.10":"2,2","3.11":"2,0","3.12":"0,3","3.13":"0,1","3.14":"0,2","3.15":"0,0","4.0":"3,7","4.1":"3,5","4.2":"3,6","4.3":"3,4","4.4":"1,7","4.5":"1,5","4.6":"1,6","4.7":"1,4","4.8":"2,7","4.9":"2,5","4.10":"2,6","4.11":"2,4","4.12":"0,7","4.13":"0,5","4.14":"0,6","4.15":"0,4"}
        logging.debug("Initialize GPIOboard complete!!")


    ## Updates the GPIO board by iterating through every square on the physical board and getting to correct gpio value for
    #  that square.
    #  @param muxnumber: the mux the board is checking
    #  @param pinvalue: the value of the pins that relates to the square we are checking
    #  @param outputvalue: The output value that is read from the gpio pin relating to the square whether a piece is on (1) or off (0)
    def updateboard(self,muxnumber,pinvalue,outputvalue):
        MuxPinPosition = "{:d}.{:d}".format(muxnumber,pinvalue)
        BoardCoordinates = self.MuxToCoordinateMap.get(MuxPinPosition)
        BoardCoordinates = BoardCoordinates.split(",")
        x = BoardCoordinates[0]
        y = BoardCoordinates[1]
        self.gpioboard[int(x)][int(y)] = outputvalue
 


    ## Sets up the inital board by performing the setup functions for the gpio reads.
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for mux in self.MuxList:
            GPIO.setup(mux.get('A'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('B'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('C'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('D'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('W'),GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        logging.debug("Setup GPIO Board Complete!")

    ## Checkmux gets an output value after receving a binary input (0-16) which corresponds to the square that is being checked.
    #  @param MuxMap: the mux that is being checked
    #  @param inputs: The binary value (0-16) that relates to the square to be checked.
    def checkmux(self, MuxMap, inputs):
        GPIO.output(MuxMap.get('A'), inputs[0])
        GPIO.output(MuxMap.get('B'), inputs[1])
        GPIO.output(MuxMap.get('C'), inputs[2])
        GPIO.output(MuxMap.get('D'), inputs[3])
        return GPIO.input(MuxMap.get('W'))

    ## boardcheck iterates through the board and checks each square in each mux (0-16).
    #  once a square is properly checked, the state of the gpio pin is updated using the updateboard function.
    #  @param muxnumber: The mux that is being checked.
    def boardcheck(self,muxnumber=0):
        x = 0
        y = 0
        i = 1
        for mux in self.MuxList:
            #print (i)
            #print ("--------------")
            for num in range(0, 16):
                pin_values = list('{0:04b}'.format(num))
                pin_values = list(map(int, pin_values))
                self.updateboard(i,num,self.checkmux(mux,pin_values))
                #print ('{0} :  {1}'.format(str(pin_values),self.checkmux(mux, pin_values)))
            i= i+1


## Test function in order to test accuracy of gpio board. 

if __name__=='__main__':
    testgpio = GPIOBOARD()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--muxnumber", help="display only 1 particular MUX",
	                    type=int)
    args = parser.parse_args()
    testgpio.setup()
    print(str(testgpio.checkmux(testgpio.Mux4,[1,1,0,0])))
    print(str(testgpio.gpioboard))
    while(1):
        testgpio.boardcheck(args.muxnumber)
        print ("++++++++++++++++++++++++++++++++++++++++++")
        print(str(testgpio.gpioboard))
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        sleep(2)
