#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import itertools

class GPIOBOARD():
    def __init__(self):
        self.Mux1= {'A': 24, 'B': 23, 'C': 18, 'D': 15, 'W': 14}
        self.Mux2= {'A': 16, 'B': 12, 'C': 7, 'D': 8, 'W': 25}
        self.Mux3= {'A': 4, 'B': 3, 'C': 2, 'D': 21, 'W': 20}
        self.Mux4= {'A': 19, 'B': 10, 'C': 22, 'D': 27, 'W': 17}
        self.MuxList = [self.Mux1, self.Mux2, self.Mux3, self.Mux4]
        self.gpioboard=[ [0 for i in range(8)] for x in range(8)]

        self.MuxToCoordinateMap = {"1.0":"7,3","1.1":"7,1","1.2":"7,2","1.3":"7,0","1.4":"5,3","1.5":"5,1","1.6":"5,2","1.7":"5,0","1.8":"6,3","1.9":"6,1","1.10":"6,2","1.11":"6,0","1.12":"4,3","1.13":"4,1","1.14":"4,2","1.15":"4,0","2.0":"7,7","2.1":"7,5","2.2":"7,6","2.3":"7,4","2.4":"5,7","2.5":"5,5","2.6":"5,6","2.7":"5,4","2.8":"6,7","2.9":"6,5","2.10":"6,6","2.11":"6,4","2.12":"4,7","2.13":"4,5","2.14":"4,6","2.15":"4,4","3.0":"3,3","3.1":"3,1","3.2":"3,2","3.3":"3,0","3.4":"1,3","3.5":"1,1","3.6":"1,2","3.7":"1,0","3.8":"2,3","3.9":"2,1","3.10":"2,2","3.11":"2,0","3.12":"0,3","3.13":"0,1","3.14":"0,2","3.15":"0,0","4.0":"3,7","4.1":"3,5","4.2":"3,6","4.3":"3,4","4.4":"1,7","4.5":"1,5","4.6":"1,6","4.7":"1,4","4.8":"2,7","4.9":"2,5","4.10":"2,6","4.11":"2,4","4.12":"0,7","4.13":"0,5","4.14":"0,6","4.15":"0,4"}

    def updateboard(self,muxnumber,pinvalue,outputvalue):
        MuxPinPosition = "{:d}.{:d}".format(muxnumber,pinvalue)
        BoardCoordinates = test.get(MuxPinPosition)
        BoardCoordinates = testobject.split(",")
        x = BoardCoordinates[0]
        y = BoardCoordinates[1]
        self.gpioboard[int(x)][int(y)] = outputvalue
 


    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for mux in self.MuxList:
            GPIO.setup(mux.get('A'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('B'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('C'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('D'), GPIO.OUT, initial=0)
            GPIO.setup(mux.get('W'),GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def checkmux(self, MuxMap, inputs):
        GPIO.output(MuxMap.get('A'), inputs[0])
        GPIO.output(MuxMap.get('B'), inputs[1])
        GPIO.output(MuxMap.get('C'), inputs[2])
        GPIO.output(MuxMap.get('D'), inputs[3])
        return GPIO.input(MuxMap.get('W'))
    def boardcheck(self,muxnumber=0):
        x = 0
        y = 0
        i = 1
        for mux in self.MuxList:
            print (i)
            print ("--------------")
            for num in range(0, 16):
                pin_values = list('{0:04b}'.format(num))
                pin_values = list(map(int, pin_values))
                if muxnumber is not None:
                    if i==muxnumber:
                        self.updateboard(i,num,self.checkmux(mux,pin_values))
                        print ('{0} :  {1}'.format(str(pin_values),self.checkmux(mux, pin_values)))
                else:
                        self.updateboard(i,num,self.checkmux(mux,pin_values))
                    print ('{0} :  {1}'.format(str(pin_values),self.checkmux(mux, pin_values)))
            i= i+1




def main():
    setup()

    while(1):
        checkBoard()
        printBoard()

        sleep(1)


if __name__=='__main__':
    testgpio = GPIOBOARD()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--muxnumber", help="display only 1 particular MUX",
	                    type=int)
    args = parser.parse_args()
    testgpio.setup()
    while(1):
        testgpio.boardcheck1(args.muxnumber)
        print ("++++++++++++++++++++++++++++++++++++++++++")
        sleep(2)
