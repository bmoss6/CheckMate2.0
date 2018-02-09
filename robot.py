#!/usr/bin/env python3

import sys, os, logging
from position import Position
from config import Conf
from time import sleep
from uArmWrapper import uArmWrapper


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
conf = Conf()


class Robot(object):

    """docstring for Robot"""
    def __init__(self,port):
        super(Robot, self).__init__()
        logging.debug('\tsetup self.swift ...')
        
        self.swift = uArmWrapper(port)

        # Set to the inital resting position
        self.swift.setDefault(conf.I('robot','restX'), 0, conf.I('robot','restZ'), conf.I('robot','speed'))

        self.swift.reset()

    def move(self,start,end):

        #Check if collision (is board)

        #Up
        self.movUp()

        #Start Position
        logging.debug('\tSTART POS Board(%d,%d) Robot(%d:,%d)'%(start.getXBoard(),start.getYBoard(),start.getX(),start.getY()))
        self.swift.set_position(x = start.getX(), y = start.getY())

        #DOWN
        self.movDown()

        #Grip Peice
        self.swift.close()

        #UP
        self.movUp()

        #End Posistion
        logging.debug('\tEND POS Board(%d,%d) robot(%d:,%d)'%(end.getXBoard(),end.getYBoard(),end.getX(),end.getY()))
        self.swift.set_position(x = end.getX(), y = end.getY())

        #DOWN
        self.movDown()

        #Release
        self.swift.open()

        #Up
        self.movUp()

        #RETURN TO RESTING
        self.swift.reset()

    def movUp(self):
        logging.debug('\tMOV UP z%d'%(conf.I('offsets','maxHeight')))
        self.swift.set_position(z = conf.I('offsets','maxHeight'))

    def movDown(self):
        logging.debug('\tMOV Down z=%d'%(conf.I('offsets','minHeight')))
        self.swift.set_position(z = conf.I('offsets','minHeight'))

