#!/usr/bin/env python3

import sys, os, logging
from position import Position
from config import Conf
from time import sleep
from uArmWrapper import uArmWrapper
from board import Board
from captureBoard import CaptureBoard


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
conf = Conf()


class Robot(object):

    """docstring for Robot"""
    def __init__(self,port,board):
        super(Robot, self).__init__()
        logging.debug('\tsetup self.swift ...')
        
        self.swift = uArmWrapper(port)

        self.board = board

        # Set to the inital resting position
        self.swift.setDefault(conf.I('robot','restX'), 0, conf.I('robot','restZ'), conf.I('robot','speed'))

        self.swift.reset()


    # This will take a little bit of work
    def resetBoard(self):
        # looks through board and move each peice back to its normal position
        # possibly we could trake this in the orignal peice class?
        logging.debug("resetBoard is not written yet!")
        return

        # reset every peice in the capture board to the right place
        capturePosition = self.board.popCapture()
        while capturePosition is not None:
            ### NEED TO UPDATE THIS TO GET ORIGINAL POSITION!
            originalPoisiton = Position(0,0) #capturePosition.getOrignalPosition?
            self.robotMove(capturePosition,originalPoisiton)
            capturePosition = self.board.popCapture()

    #wrapper for clarity
    def updateBoard(self,start,end):
        self.board.move(start,end)

    # Move the end peice onto the discard pile
    def handleCollision(self,start,peice):

        # TODO: Check for casteling
        # Unsure how to detect this at this point without looking at each of the peices

        # Insert peice into capture board and get position
        capturePosition = self.board.capture(peice)
        
        # If the coordinates on the capture poistion are correct this should work
        # but the debug information will report an incorrect board coodinate
        self.robotMove(start,capturePosition)


    def move(self,start,end):

        peice = self.board.isCollision(end)
        if peice:
            self.handleCollision(end,peice)

        self.updateBoard(start,end)

        self.robotMove(start,end)

        self.reedSwitchCheck()

    def robotMove(self,start,end):
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

