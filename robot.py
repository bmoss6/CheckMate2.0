#!/usr/bin/env python3

import sys, os, logging
from position import Position
from config import Conf
from time import sleep
from uArmWrapper import uArmWrapper


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
conf = Conf()


class Robot(object):

    curX = 0
    curY = 0
    curZ = 0

    """docstring for Robot"""
    def __init__(self,port):
        super(Robot, self).__init__()
        logging.debug('\tsetup self.swift ...')
        
        self.swift = uArmWrapper(port)


        self.swift.setDefault(conf.I('robot','restX'), 0, conf.I('robot','restZ'), conf.I('robot','speed'))
        # Set to the inital resting position

        self.curX = conf.I('robot','restX')
        self.curY = 0
        self.curZ = conf.I('robot','restZ')
        self.swift.reset()
        
    def getPos(self):
        return self.curX, self.curY ,self.curZ

    def setPos(self,x,y,z):
        self.curX = x
        self.curY = y
        self.curZ = z

    def move(self,start,end):

        #Up
        self.movUp()

        #Start Position
        logging.debug('\tSTART POS Board(%d,%d) Robot(%d:,%d)'%(start.getXBoard(),start.getYBoard(),start.getX(),start.getY()))
        x, y, z = self.getPos()
        x = start.getX()
        y = start.getY()
        self.swift.set_position(x,y,z)
        self.setPos(x,y,z)
        #sleep(2)

        #DOWN
        self.movDown()

        #Grip Peice
        self.swift.close()
        #sleep(1)

        #UP
        self.movUp()

        #End Posistion
        logging.debug('\tEND POS Board(%d,%d) robot(%d:,%d)'%(end.getXBoard(),end.getYBoard(),end.getX(),end.getY()))
        x, y, z = self.getPos()
        x = end.getX()
        y = end.getY()
        self.swift.set_position(x,y,z)
        self.setPos(x,y,z)
        #sleep(2)

        #DOWN
        self.movDown()

        #Release
        self.swift.open()

        #Up
        self.movUp()

        #RETURN TO RESTING
        logging.debug("\treset")
        self.swift.reset()

    def movUp(self):
        x, y, z = self.getPos()
        
        logging.debug('\tMOV UP z=%d zNew=%d'%(z,conf.I('offsets','maxHeight')))
        z = conf.I('offsets','maxHeight')
        self.swift.set_position(x,y,z)
        self.setPos(x,y,z)

    def movDown(self):
        x, y, z = self.getPos()
        logging.debug('\tMOV Down z=%d zNew=%d'%(z,conf.I('offsets','minHeight')))
        z = conf.I('offsets','minHeight')
        self.swift.set_position(x,y,z)
        self.setPos(x,y,z)

