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




