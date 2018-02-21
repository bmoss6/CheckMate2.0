<<<<<<< HEAD
from . import game
import os
from .Piece import Piece as piece

class board:

    def __init__(self, width=8, height=8):
        self.name = "8x8 Chess Board"
        self.width, self.height = width, height
        self.board = [[] for x in range (0,self.height)]

            ##TODO Initialize starting board pieces for 8x8 grid.
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
        second_line.append(piece("pawn",color))
        second_line.append(piece("pawn", color))
        second_line.append(piece("pawn", color))
        second_line.append(piece("pawn", color))
        second_line.append(piece("pawn", color))
        second_line.append(piece("pawn", color))
        second_line.append(piece("pawn", color))
        second_line.append(piece("pawn", color))
        return second_line
    def construct_8x8_board(self):
        self.board[0] = self.first_line("white")
        self.board[1] = self.second_line("white")
        self.board[6] = self.second_line("black")
        self.board[7] = self.first_line("black")
        for x in range(2, 6):
            self.board[x] = self.populate_blank()


    def move(self,startx,starty,endx,endy):
        self.board[endx][endy].color = self.board[startx][starty].color
        self.board[endx][endy].name = self.board[startx][starty].name
        self.board[startx][starty].name = "null"
        self.board[startx][starty].color = "null"
    def print_board(self):
        for x in range(0, len(self.board)):
            for y in range(0, self.width):
                print("||" + str(x) + " , " + str(y) + " " + self.board[x][y].color + " " + self.board[x][y].name + "||"),
            print("------------------------------------")
        
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
    fishergame = os.path.join(filepath,"Fischer.pgn")

    testboard = board()
    testboard.construct_8x8_board()
    testboard.print_board()
    testboard.print_board()

   # for x in testboard.board:
    #    for y in testboard.board[i]:
     #       print (str(i) + str(j) + "\n" + testboard.board[i][j].name +" "+ testboard.board[i][j].color)
      #      j= j+1
       # i = i+1
        #print("--------------------------------------------------------")


if __name__ == "__main__":
    test()
=======
#! /usr/bin/python3

from piece import Piece

class Board:

    def __init__(self, width=8, height=8):
        self.name = "8x8 Chess Board"
        self.width, self.height = width, height
        self.board = [[] for x in range (0,self.height)]

            ##TODO Initialize starting board Pieces for 8x8 grid.


    def construct_8x8_board(self):

        first_line = []
        blank_rows =[]
        first_line.append(Piece("rook","black"))
        first_line.append(Piece("knight", "black"))
        first_line.append(Piece("bishop", "black"))
        first_line.append(Piece("queen", "black"))
        first_line.append(Piece("king", "black"))
        first_line.append(Piece("bishop", "black"))
        first_line.append(Piece("knight", "black"))
        first_line.append(Piece("rook", "black"))
        second_line = []
        for x in range(0,self.width):
            second_line.append(Piece("pawn","black"))
        self.board[0] = first_line
        self.board[1] = second_line
        self.board[6] = second_line
        self.board[7] = first_line
        for x in range(0,self.width):
            self.board[6][x].color = "white"
            self.board[7][x].color = "white"
        for x in range(0,self.width):
            blank_rows.append(Piece())
        for x in range(2, 6):
            self.board[x] = blank_rows


        
# [[ rook, knight, bishop, queen, king, bishop, knight, rook ]
#   [pawn,  pawn,  pawn,   pawn,  pawn,  pawn,  pawn,  pawn]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [null,  null,  null,   null,  null,  null,  null,  null]
#   [pawn,  pawn,  pawn,   pawn,  pawn,  pawn,  pawn,  pawn]
#   [ rook, knight, bishop, queen, king, bishop, knight, rook ]




>>>>>>> 24f9654b8448a8cc1b4459e0514bbc6df4fe2006
