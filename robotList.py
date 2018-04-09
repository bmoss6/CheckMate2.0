#! /usr/bin/python3

import serial, sys, glob

## Dynamicly locate the list serial ports avalible
class RobotList(object):
    
    ## Constructor
    #  @param numRobots Number of robots that are expected to be found
    def __init__(self,numRobots):
        super(RobotList, self).__init__()
        self.numOfRobots = numRobots
        self.robotList = []
        self.initialized = False
        self.serial_ports()

    ## Check for a list of avaliable serial ports. 
    #  It will set initilized to true if all you find the number of robots you expect.
    def serial_ports(self):
        self.robotList=[]
        if sys.platform.startswith('linux'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyACM[0-9]*')
        else:
            raise EnvironmentError('Unsupported platform')

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.robotList.append(port)
            except (OSError, serial.SerialException):
                print("Unable to connect to serial port %s"%port)
        if(len(self.robotList) == self.numOfRobots):
            self.initialized = True
        
    ## Get a list of the avabliable serial ports if avaliable
    #  @return Type:Bool or Type:string array. Thats gross... 
    def getList(self):
        if self.initialized:
            return self.robotList
        return False
             

if __name__ == '__main__':
    rl = RobotList()
    print(rl.getList())
