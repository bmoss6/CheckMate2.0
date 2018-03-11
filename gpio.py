#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import itertools

class GPIOBOARD():
    def __init__(self):
        self.gpioboard = [[] for x in range (0,8)]
        self.Mux1= {'A': 24, 'B': 23, 'C': 18, 'D': 15, 'W': 14}
        self.Mux2= {'A': 16, 'B': 12, 'C': 7, 'D': 8, 'W': 25}
        self.Mux3= {'A': 4, 'B': 3, 'C': 2, 'D': 21, 'W': 20}
        self.Mux4= {'A': 19, 'B': 10, 'C': 22, 'D': 27, 'W': 17}
        self.MuxList = [self.Mux1, self.Mux2, self.Mux3, self.Mux4]


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
    def boardcheck1(self,muxnumber=0):
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
                        print ('{0} :  {1}'.format(str(pin_values),self.checkmux(mux, pin_values)))
                else:
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
        print ("HK:KLKLJ:++++++++++++++++++++++++++++++++++++++++++")
        sleep(2)
