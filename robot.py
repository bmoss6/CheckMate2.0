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
    def __init__(self,port,board,captureBoard,color,test=False):
        super(Robot, self).__init__()
        logging.debug('\tsetup self.swift ...')
        self.color = color
        self.board = board
        self.captureBoard = captureBoard

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

    def clearRobotPieces(self):
        for x in range (self.board.height):
            for y in range (self.board.width):
                if self.board.board[x][y].name!=None and self.board.board[x][y].color == self.color:
                    if self.color != "white":
                        self.handleCollision(Position(x,y,True))
                    else:
                        self.handleCollision(Position(x,y,False))
    def resetToOriginalPosition(self):
        capturePosition, peice = self.captureBoard.popLast()
        while capturePosition is not None:
            if self.color != "white":
                originalPoisiton = Position(peice.StartingX,peice.StartingY,True)
            else:
                originalPosition = Position(peice.StartingX,peice.StartyingY,False)
            self.robotMove(capturePosition,originalPoisiton)
            capturePosition, peice = self.captureBoard.popLast()

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
            logging.error("Collision king on castle?")
        self.updateBoard(start_king,end_king)
        self.robotMove(start_king,end_king)

        # sanity check for castle
        if self.board.isCollision(end_rook):
            logging.error("Collision roon on castle?")
        self.updateBoard(start_rook,end_rook)
        self.robotMove(start_rook,end_rook)

        if self.test:
            self.board.print_simple_no_gpio()
            self.captureBoard.printBoard()
            print("\n")


    # Move the end peice onto the discard pile
    def handleCollision(self,peicePosition):
        # Insert peice into capture board and get position
        peice = self.board.getPeice(peicePosition)

        capturePosition = self.captureBoard.insertNextPos(peice)
        
        # If the coordinates on the capture poistion are correct this should work
        # but the debug information will report an incorrect board coodinate
        self.robotMove(peicePosition,capturePosition)


    def move(self,start,end):
        
        if self.board.isCollision(end):
            self.handleCollision(end) 

        self.updateBoard(start,end)

        self.robotMove(start,end)

        if self.test:
            self.board.print_simple_no_gpio()
            self.captureBoard.printBoard()
            print("\n")

    def robotMove(self,start,end):
        # If testing the code without the robots setup just return
        if self.test:
            return

        self.movUp()

        #Start Position
        #logging.debug('\tSTART POS Board(%d,%d) Robot(%d:,%d)'%(start.getXBoard(),start.getYBoard(),start.getX(),start.getY()))
        self.swift.set_position(x = start.getX(), y = start.getY())

        self.movDown()

        #Grip Peice
        self.swift.close()

        self.movUp()

        #End Posistion
        #logging.debug('\tEND POS Board(%d,%d) robot(%d:,%d)'%(end.getXBoard(),end.getYBoard(),end.getX(),end.getY()))
        self.swift.set_position(x = end.getX(), y = end.getY())

        self.movDown()

        #Release
        self.swift.open()

        self.movUp()

        #RETURN TO RESTING
        self.swift.reset()

    def movUp(self):
        #logging.debug('\tMOV UP z%d'%(conf.I('offsets','maxHeight')))
        self.swift.set_position(z = conf.I('offsets','maxHeight'))

    def movDown(self):
        #logging.debug('\tMOV Down z=%d'%(conf.I('offsets','minHeight')))
        self.swift.set_position(z = conf.I('offsets','minHeight'))

