
from time import sleep
import itertools

class GPIO():
    def __init__(self):
        self.gpioboard = [[] for x in range (0,8)]
        self.Mux1= {'A': 24, 'B': 23, 'C': 18, 'D': 15, 'W': 14}
        self.Mux2= {'A': 16, 'B': 12, 'C': 7, 'D': 8, 'W': 25}
        self.Mux3= {'A': 4, 'B': 3, 'C': 2, 'D': 21, 'W': 20}
        self.Mux4= {'A': 9, 'B': 10, 'C': 22, 'D': 27, 'W': 17}
        self.MuxList = [].append(Mux1, Mux2, Mux3, Mux4)


    def setup(self):
        for mux in self.MuxList:
            GPIO.setup(mux['A'], GPIO.OUT, initial=0)
            GPIO.setup(mux['B'], GPIO.OUT, initial=0)
            GPIO.setup(mux['C'], GPIO.OUT, initial=0)
            GPIO.setup(mux['D'], GPIO.OUT, initial=0)

    def checkmux(self, MuxMap, inputs):
        self.setup()
        GPIO.output(MuxMap['A'], inputs[0])
        GPIO.output(MuxMap['B'], inputs[1])
        GPIO.output(MuxMap['C'], inputs[2])
        GPIO.output(MuxMap['D'], inputs[3])
        return GPIO.input(MuxMap['W'])
## Workign on boardcheck currently
    def boardcheck1(self):
        x = 0
        y = 0
        for mux in self.MuxList:
            for num in range(0, 16):
                pin_values = list('{0:04b}'.format(num))
                pin_values = list(map(int, pin_values))
                if y > 3:
                    y = 0
                else:
                    y += 1

                self.checkmux(mux, pin_values)




##0000
##0001
##0010
##0011
##0100
##0101
##0110
##0111
##1000
##1001
##1010
##1011
##1100
##1101
##1110
##1111










def main():
    setup()

    while(1):
        checkBoard()
        printBoard()

        sleep(1)


if __name__=='__main__':
    boardcheck1()

