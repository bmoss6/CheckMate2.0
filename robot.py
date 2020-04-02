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

## Robot Class
#  This class is at the center of where all of the classes interaction starts.
#  The core code and functionaility of this class is to controll the robot and move
#  the peices into the correct spot. As it moves peices it is reponsible for updating
#  the board classes. This class is the logic for moving a peies into position and 
#  handeling any collisions that maay occur. The acutall communcation with the robot is
#  defined within the uArmWrapper
class Robot(object):

    ## Constructor 
    #  @param port:string path to the TTY of the robot
    #  @param board:Board Board class the both robots share
    #  @param captureBoard:CaptureBoard Capture board for this robot.
    #  @param color:string color of peices the robot is responsible for
    #  @param test:Bool Default:False Set to true if you want to run test without robots so they dont try to send commnds
    def __init__(self,port,board,captureBoard,color,test=False):
        super(Robot, self).__init__()
        logging.debug('\tsetup self.swift ...')
        ## @var color:string
        #  the color of peices used by the robot.
        self.color = color
        ## @var board:Board
        #  Board class used by robot. This is shared between robots
        self.board = board
        ## @var captureBoard:CaptureBoard
        #  Capture board used by robot. This board is not shared.
        self.captureBoard = captureBoard

        ## @var color:bool
        #  Set the robot in test mode to run without being connected
        self.test = test
        
        if test:
            #connect the API becuase the robots are not connected
            self.swift = None
            return

        ## @var swift:uArmWrapper
        #  instance of the API to interact with the robot.
        self.swift = uArmWrapper(port)
        ## @var uid:string
        #  uid of robot as reported by the API
        self.uid = self.swift.getUID()
        # Set to the inital resting position
        self.swift.setDefault(conf.I('robot','restX'), conf.I('robot','restY'), conf.I('robot','restZ'), conf.I('robot','speed'))
        self.swift.reset()

    ## If the robots switch you need to change their color os they are correct
    #  @param color:string
    def setColor(self,color):
        self.color = color

    ## After a game is complete send all of the peices to the captureboard to reset them.
    def clearRobotPieces(self):
        for x in range (self.board.height):
            for y in range (self.board.width):
                # You only capture peices that are not your own so those are the ones to reset.
                if self.board.board[x][y].name!=None and self.board.board[x][y].color != self.color:
                    # The second robot which is black should be inverted
                    position = None
                    if self.color != "white":
                        position = Position(x,y,True)
                    else:
                        position = Position(x,y,False)
                    self.handleCollision(position)
                    self.board.clearPosition(position)

    ## Pop all of the capture peices off of the capture board and reset them to their orignal position
    def resetToOriginalPosition(self):
        capturePosition, peice = self.captureBoard.popLast()
        while capturePosition is not None:
            if self.color != "white":
                originalPosition = Position(peice.StartingX,peice.StartingY,True)
            else:
                originalPosition = Position(peice.StartingX,peice.StartingY,False)
            self.robotMove(capturePosition,originalPosition)
            self.board.setPosition(originalPosition,peice)
            capturePosition, peice = self.captureBoard.popLast()

    ## Check to see if the uid of the robot is what we think it is
    #  @param uid:string uid to verify
    #  @return type:Bool to say if matched or not.
    def checkID(self,uid):
        if self.uid == uid:
            return True
        return False

    ## Wrapper to update the board class for clarity
    #  @param start:Position starting position of peice
    #  @param end:Position ending position of peice
    def updateBoard(self,start,end):
        self.board.move(start,end)

    ## Castleing moves are always the same so they are hardcoded depending on the robot.
    #  @param castle:int 1 = king side castle  2 = queenside castle
    #  @param robot:int Robot 1 or 2 depending what side of the board it is on.
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


    ## Move the end peice onto the capture board and update it.
    #  @param peicePosition:Position Position of the peice that needs to be discarded
    def handleCollision(self,peicePosition):
        # get the peice at the given position
        peice = self.board.getPeice(peicePosition)

        capturePosition = self.captureBoard.insertNextPos(peice)
        
        # If the coordinates on the capture poistion are correct this should work
        # but the debug information will report an incorrect board coodinate
        self.robotMove(peicePosition,capturePosition)

    ## External move function that should be called outside the class to move a peice. It will
    #  do any collision handling if nessisary and update the board.
    #  @param start:Position starting position of peice
    #  @param end:Position ending position of peice
    def move(self,start,end):
        
        if self.board.isCollision(end):
            self.handleCollision(end) 

        self.updateBoard(start,end)

        self.robotMove(start,end)

        if self.test:
            self.board.print_simple_no_gpio()
            self.captureBoard.printBoard()
            print("\n")

    ## Internal move function that will use the serial API from one position to the other.
    #  There is not error handling at this point.
    #  @param start:Position starting position of peice
    #  @param end:Position ending position of peice
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

    ## Move the robot up to the hight sent in the configuration 
    def movUp(self):
        #logging.debug('\tMOV UP z%d'%(conf.I('offsets','maxHeight')))
        self.swift.set_position(z = conf.I('offsets','maxHeight'))

    ## Move the robot up to the hight sent in the configuration
    def movDown(self):
        #logging.debug('\tMOV Down z=%d'%(conf.I('offsets','minHeight')))
        self.swift.set_position(z = conf.I('offsets','minHeight'))
        
    def movDownQuit(self):
        #logging.debug('\tMOV Down z=%d'%(conf.I('offsets','minHeight')))
        self.swift.set_position(z = conf.I('offsets','quitHeight'))

    ## Print the board for debugging
    def printBoard(self):
        self.board.print_simple_no_gpio()

    ## Print the the capture board for debugging
    def printCaptureBoard(self):
        print(self.color)
        self.captureBoard.printBoard()
