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
    def __init__(self,port,board,test=False):
        super(Robot, self).__init__()
        logging.debug('\tsetup self.swift ...')
        
        self.board = board

        self.test = test
        # testing functionality lets you run the robots without having them hooked up
        if test:
            self.swift = None
            return

        self.swift = uArmWrapper(port)
        self.uid = self.swift.getUID()
        # Set to the inital resting position
        self.swift.setDefault(conf.I('robot','restX'), 0, conf.I('robot','restZ'), conf.I('robot','speed'))
        self.swift.reset()

#    def ResetStartingPositionRows(self):
#        for x in range (8):
#            for y in range (8):
#                if x < 2 or x > 5:
#                    if self.board[x][y] is not None: 
#                        origin = self.board[x][y].StartingPosition.split(",")
#                        originx = origin[0]
#                        originy = origin[1]
#                        self.move(Position(x,y),Position(originx,originy)
# This will take a little bit of work
    def resetBoard(self,channel):
        # looks through board and move each peice back to its normal position
        # possibly we could trake this in the orignal peice class?
        logging.debug("resetBoard is not written yet!")
        return
        self.ResetStartingPositionRows()
        exit(1)
        return

        # reset every peice in the capture board to the right place
        capturePosition = self.board.popCapture()
        while capturePosition is not None:
            ### NEED TO UPDATE THIS TO GET ORIGINAL POSITION!
            originalPoisiton = Position(0,0) #capturePosition.getOrignalPosition?
            self.robotMove(capturePosition,originalPoisiton)
            capturePosition = self.board.popCapture()

    def checkID(self,uid):
        if self.uid == uid:
            return True
        return False

    #wrapper for clarity
    def updateBoard(self,start,end):
        self.board.move(start,end)


    def castle(self,castle,robot):

        # King side castle
        if robot == 1:
            if castle == 1:
                logging.debug("Robot 1:King side castle")
                start_king = Position(0,4)
                end_king = Position(0,6)
                start_rook = Position(0,7)
                end_rook = Position(0,5)
            # Queen side castle
            elif castle == 2:
                logging.debug("Robot 1:Queen side castle")
                start_king = Position(0,4)
                end_king = Position(0,2)
                start_rook = Position(0,0)
                end_rook = Position(0,3)

        if robot == 2:
            if castle == 1:
                logging.debug("Robot 2:King side castle")
                start_king = Position(7,4,True)
                end_king = Position(7,6,True)
                start_rook = Position(7,7,True)
                end_rook = Position(7,5,True)
            # Queen side castle
            elif castle == 2:
                logging.debug("Robot 2:Queen side castle")
                start_king = Position(7,4,True)
                end_king = Position(7,2,True)
                start_rook = Position(7,0,True)
                end_rook = Position(7,3,True)

        # sanity check for castle
        if self.board.isCollision(end_king):
            logging.debug("Collision king on castle?")
        self.updateBoard(start_king,end_king)
        self.robotMove(start_king,end_king)

        # sanity check for castle
        if self.board.isCollision(end_rook):
            logging.debug("Collision roon on castle?")
        self.updateBoard(start_rook,end_rook)
        self.robotMove(start_rook,end_rook)

        if self.test:
            self.board.print_simple_no_gpio()


    # Move the end peice onto the discard pile
    def handleCollision(self,peice):

        # Insert peice into capture board and get position
        capturePosition = self.board.capture(peice)
        
        # If the coordinates on the capture poistion are correct this should work
        # but the debug information will report an incorrect board coodinate
        self.robotMove(peice,capturePosition)


    def move(self,start,end):
        
        if self.board.isCollision(end):
            self.handleCollision(end) 

        self.updateBoard(start,end)

        self.robotMove(start,end)

        if self.test:
            self.board.print_simple_no_gpio()

    def robotMove(self,start,end):
        # If testing the code without the robots setup just return
        if self.test:
            return

        #Up
        self.movUp()

        #Start Position
        #logging.debug('\tSTART POS Board(%d,%d) Robot(%d:,%d)'%(start.getXBoard(),start.getYBoard(),start.getX(),start.getY()))
        self.swift.set_position(x = start.getX(), y = start.getY())

        #DOWN
        self.movDown()

        #Grip Peice
        self.swift.close()

        #UP
        self.movUp()

        #End Posistion
        #logging.debug('\tEND POS Board(%d,%d) robot(%d:,%d)'%(end.getXBoard(),end.getYBoard(),end.getX(),end.getY()))
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
        #logging.debug('\tMOV UP z%d'%(conf.I('offsets','maxHeight')))
        self.swift.set_position(z = conf.I('offsets','maxHeight'))

    def movDown(self):
        #logging.debug('\tMOV Down z=%d'%(conf.I('offsets','minHeight')))
        self.swift.set_position(z = conf.I('offsets','minHeight'))

