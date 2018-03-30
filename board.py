#! /usr/bin/python3

import os, logging, sys, time
from piece import Piece as piece
from position import Position
from gpio import GPIOBOARD

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class Board:

    def __init__(self, width=8, height=8,test=False):
        self.name = "8x8 Chess Board"
        self.width, self.height = width, height
        self.board = [[] for x in range (0,self.height)]
        self.pieceCount = 0
        self.construct_8x8_board()
        self.GPIOerrors =0
        self.test = test
        if self.test:
            self.gpio = None
        else:
            self.gpio = GPIOBOARD()
            self.gpio.setup()

    def populate_blank(self):
        list = []
        for x in range (0,8):
            list.append(piece())
        return list

    def first_line(self,color):
        first_line = []
        first_line.append(piece("rook",color))
        first_line.append(piece("knight", color))
        first_line.append(piece("bishop", color))
        first_line.append(piece("queen", color))
        first_line.append(piece("king", color))
        first_line.append(piece("bishop", color))
        first_line.append(piece("knight", color))
        first_line.append(piece("rook", color))
        return first_line

    def second_line(self,color):
        second_line = []
        for x in range(0,self.width):
            second_line.append(piece("pawn",color))
        return second_line

    #wrapper for clarity for external user
    def reset(self):
        self.construct_8x8_board()

    # get the peice from a position
    def getPeice(self,position):
        x = position.getXBoard()
        y = position.getYBoard()
        return self.board[x][y]

    def construct_8x8_board(self):
        self.board[0] = self.first_line("white")
        self.board[1] = self.second_line("white")
        self.board[6] = self.second_line("black")
        self.board[7] = self.first_line("black")
        self.pieceCount = 4 * self.width
        for x in range(2, 6):
            self.board[x] = self.populate_blank()
        for x in range (8):
            for y in range(8):
                  if x < 2 or x > 5:
                      self.board[x][y].setStartPos(x,y)

    # Check if where we are moving to results in a collision
    def isCollision(self,end):
        endx = end.getXBoard()
        endy = end.getYBoard()
        if self.board[endx][endy].getName() is not None:
            # return the piece for application to use
            logging.debug('\tCollsion! %s'%self.board[endx][endy].getName())
            return True
        return False

    def remove(self,position):
        posx = position.getXBoard()
        posy = position.getYBoard()
        if not self.isCollision(position):
            logging.error('\tRemoving none existant piece?')
        self.board[posx][posy].clear()

    # GPIO Check will iterate through the board and update each piece object with it's GPIO tag
    # GPIO tag: 1 if physical piece is on square, 0 if physical piece not on square (as determined by reed switches)
    # WARNING: Not always reliable. See GPIO Error Threshold for more information.
    def GPIOUpdate(self):
        #For testing off PI just return
        if self.test:
            return
        self.gpio.boardcheck()
        for x in range(8):
            for y in range(8):
                self.board[x][y].setGPIO(self.gpio.gpioboard[x][y])

    # Use position objects for start and end
    # Pieces will inherently get removed as the overwrite
    def move(self,start,end):
        self.GPIOUpdate()
        startx = start.getXBoard()
        starty = start.getYBoard()
        endx = end.getXBoard()
        endy = end.getYBoard()
        self.GPIOError(startx,starty)
        # sanity check to make sure we are moving a piece we think exists.
        if self.board[startx][starty].isEmpty():
            logging.error('\tMoving non-existant piece?')
            return

        # we should have handled the phiscal collision by now but 
        # here we decrement cour count
        if not self.isCollision(end):
            self.pieceCount -= 1

        # Update piece
        self.board[endx][endy] = self.board[startx][starty]
        # set the piece to null again.
        self.board[startx][starty] = piece()

        # self.board[endx][endy].color = self.board[startx][starty].color
        # self.board[endx][endy].name = self.board[startx][starty].name
        # self.board[startx][starty].name = "null"
        # self.board[startx][starty].color = "null"

    def GPIOError(self,startx,starty):
        if self.test:
            return
        if self.board[startx][starty].gpio!=1:
            logging.error('\tGPIO Check Failed, GPIO Says no piece exists at this move')
            self.GPIOerrors += 1

    def print_board(self):
        self.GPIOUpdate()
        for x in range(0, len(self.board)):
            for y in range(0, self.width):
                color = self.board[x][y].getColor()
                name = self.board[x][y].getName()
                gpio = self.board[x][y].gpio
                StartingPosition = self.board[x][y].StartingPosition
                if color is None:
                    color = "null"
                if name is None:
                    name = "null"
                if StartingPosition is None:
                    StartingPosition= "null"
                print ("|%s %s %s|"%( color, name, str(gpio)),StartingPosition, end='')
            print("\n------------------------------------")

    def print_simple_no_gpio(self):
        print("      [0]   [1]   [2]   [3]   [4]   [5]   [6]   [7]")
        for x in range(0, len(self.board)):
            print("[%d] |"%x,end='')
            for y in range(0, self.width):
                if self.board[x][y] is None:
                    print("  :  |",end='')
                    continue
                self.board[x][y].printPeice()
            print()
        
        
# [[ rook, knight, bishop, queen, king, bishop, knight, rook ]
#   [pawn,  pawn,  pawn,   pawn,  pawn,  pawn,  pawn,  pawn]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [pawn,  pawn,  pawn,   pawn,  pawn,  pawn,  pawn,  pawn]
#   [ rook, knight, bishop, queen, king, bishop, knight, rook ]


def test():
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'GameScripts'))
    fishergame = os.path.join(filepath,"GameScripts/Fischer.pgn")
    testboard = Board(test=True)
    while (1):
        print()
        testboard.print_board()
        time.sleep(2)


if __name__ == "__main__":
    test()
