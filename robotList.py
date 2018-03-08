#! /usr/bin/python3

import serial, sys, glob

class RobotList(object):
    """docstring for RobotList"""
    def __init__(self,numRobots):
        super(RobotList, self).__init__()
        self.numOfRobots = numRobots
        self.robotList = []
        self.initialized = False
        self.serial_ports()

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """

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
        else:
            print("Found to many or not enough robots to start." \
                "\nChange the number of robots in RobotList in run.py if testing.")


    def getList(self):
        if self.initialized:
            return self.robotList
        return False
             



if __name__ == '__main__':
    rl = RobotList()
    print(rl.getList())
