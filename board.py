#! /usr/bin/python3

import os, logging, sys, time
from piece import Piece as piece
from position import Position
#from gpio import GPIOBOARD

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

## Board class
#  In order to keep track of the various states the board is in during a particular game,
#  this class was designed. Essentially, the board object of this class is a 2-D array of
#  PIECE object (See piece.py for more information). The movements of the robot are replicated in the board class
#  so that state can be kept and collisions can be handled.
#  The board class also plays an important role in resetting the board to a default state (ie. for a new game)
class Board:
    ## The constructor which initializes the board object by constructing an initial (starting position) chessboard
    #  @param width:int Width of the game board. Default for chess games should always be 8.
    #  @param height:int Height of the game board. Default for chess games should always be 8.
    #  @param test:Bool Default=False set when testing the programs without the robots.
    #  WARNING: If width or height are set to number other than 8. Constructing of board will fail.
    def __init__(self, width=8, height=8,test=False):
        ## @var name
        #  Name of the chess board to be created.
        self.name = "8x8 Chess Board"
        ## @var width and height
        #  Width and heightof chessboard to be created
        self.width, self.height = width, height
        ## @var board
        #  Actual 2-D array created for creating an abstract board.
        self.board = [[] for x in range (0,self.height)]
        ## @var pieceCount
        #  Number of pieces created on the board.
        self.pieceCount = 0

        self.construct_8x8_board()
        ## @var GPIOerrors
        #  Keeps track of the number of GPIO errors. This function will merely track the number of errors the gpio class
        #  encounters. It will not change the execution of the program
        self.GPIOerrors =0
        ## @var test
        #  Flag to determine whether program will run in test (no robots) mode or performance mode.
        self.test = test
        if self.test:
            self.gpio = None
        else:
            self.gpio = GPIOBOARD()
            self.gpio.setup()

    ## Creates an array of blank PIECE objects.
    #  Only works for 8x8 board.
    #  @return type:Piece array. Array of blank Pieces
    def populate_blank(self):
        list = []
        for x in range (0,8):
            list.append(piece())
        return list

    ## Creates the first and last row of the chessboard with corresponding PIECE objects.
    #  @param color:string The color or team the piece corresponds to (ie black/white)
    #  @return type:Piece array. Array of first chess row
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

    ## Creates a row of all pawns to be placed in front of the first and last rows of the board
    #  @param color:string The color or team the piece corresponds to (ie black/white)
    #  @return type:Piece array. Array of second chess row
    def second_line(self,color):
        second_line = []
        for x in range(0,self.width):
            second_line.append(piece("pawn",color))
        return second_line

    ## Reset function that creates a new board with the default positioning of pieces.
    def reset(self):
        self.construct_8x8_board()

    ## Returns a specific piece on the board when given x/y coordinates
    #  @param position: a POSITION object with x and y coordinates.
    #  @return type:Piece
    def getPeice(self,position):
        x = position.getXBoard()
        y = position.getYBoard()
        return self.board[x][y]

    ## Constructs the 8x8 board by using the first_line() and second_line() and populate_blank() functions
    #  Also sets the piece count and the original positions (to be used when resetting the board)
    def construct_8x8_board(self):
        self.board[0] = self.first_line("white")
        self.board[1] = self.second_line("white")
        self.board[6] = self.second_line("black")
        self.board[7] = self.first_line("black")
        self.pieceCount = 4 * self.width
        # Populate empty coordinates with empty piece objects
        for x in range(2, 6):
            self.board[x] = self.populate_blank()
        # Set the original positions for the currently existing pieces.
        for x in range (8):
            for y in range(8):
                  if x < 2 or x > 5:
                      self.board[x][y].setStartPos(x,y)

    ## Checks if a collision will occur before a move function
    #  @param end:Position A position object relating to the position the piece is to move to.
    #  @return type:bool
    def isCollision(self,end):
        endx = end.getXBoard()
        endy = end.getYBoard()
        # Check the board to make sure that where the piece is moving to does not have a piece.
        # If there is a piece that exists in that ending square, return true. If not return false.
        if self.board[endx][endy].getName() is not None:
            # return the piece for application to use
            logging.debug('\tCollsion! %s'%self.board[endx][endy].getName())
            return True
        return False

    ## Remove function sets a PIECE object on the board to empty. Used when setting a piece to empty during the move.
    #  @param position:Position Position object corresponding to the square on the board that needs to be cleared.
    def remove(self,position):
        posx = position.getXBoard()
        posy = position.getYBoard()
        # Check and make sure that there is an actual piece
        if not self.isCollision(position):
            logging.error('\tRemoving none existant piece?')
        self.board[posx][posy].clear()

    ## GPIO Check will iterate through the board and update each piece object with it's GPIO tag
    # GPIO tag: 1 if physical piece is on square, 0 if physical piece not on square (as determined by reed switches)
    # WARNING: Not always reliable. See GPIO Error Threshold for more information.
    def GPIOUpdate(self):
        #For testing off PI just return
        if self.test:
            return
        self.gpio.boardcheck()
        # Updates each PIECE object in the board with the actual GPIO values
        for x in range(8):
            for y in range(8):
                self.board[x][y].setGPIO(self.gpio.gpioboard[x][y])

    ## Used to move pieces around on the board Use position objects for start and end
    # Pieces will inherently get removed as the overwrite
    # @param start:Position starting poistion
    # @param end:Position ending position
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

    ## Checks a piece object to ensure that a GPIO (Reed Switch) is activated, which means that a magnet (attached to the piece)
    # is in the square relating to the piece object.
    #  @param startx:int x-coordinate of square to check on the board.
    #  @param starty:int y-coordinate of square to check on the board.
    def GPIOError(self,startx,starty):
        if self.test:
            return
        # If not in test mode, make sure that piece has a magnet. IF not, increment the gpio error count.
        if self.board[startx][starty].gpio!=1:
            logging.error('\tGPIO Check Failed, GPIO Says no piece exists at this move')
            self.GPIOerrors += 1


    ## Print board function that will print board and it's piece objects + attributes.
    #  Used mainly to test the gpio function to ensure that gpio tracking is working properly
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

    ## Simplified print function for showing board state throughout a chess game. Does not display GPIO information.
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


    ## Test function that creates a new board and displays initial print objects
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
