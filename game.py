#!/usr/bin/env python3
import chess.pgn
from collections import namedtuple


class Game(object):

   def altElement(self, a):
      return a[::2]

   def otheraltelement(self, b):
      return b[1::2]

   def convertMove(self, move):
      startposy = move[0]
      startposx = move[1]
      endposy = move[2]
      endposx = move[3]
      castle = move[4]
      mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
      mapping2 = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

      start = self.Square(x=mapping2.get(startposx), y=mapping.get(startposy))
      end = self.Square(x=mapping2.get(endposx), y=mapping.get(endposy))

      move = self.Move(start, end, castle)

      return (move)

   def __init__(self, filename):

      self.robot1_moves = []
      self.robot2_moves = []
      self.all_moves = []
      self.pgn = open(filename)
      self.game = chess.pgn.read_game(self.pgn)

      self.Square = namedtuple('Square', ['x', 'y'])
      self.Move = namedtuple('Move', ['start', 'stop', 'castle'])

      #have to keep track of the algebraic notation using the chess library's node structure
      #to account for odd moves like castling, which do not show up correctly in move.
      node = self.game
      for move in self.game.main_line():
         castle = ""
         if node.variations:
            next = node.variation(0)
            mov = node.board().san(next.move)
            node = next
            if mov == "O-O":
               castle = "kingCastle"
            elif mov == "O-O-O":
               castle = "queenCastle"
         
         if castle == "kingCastle":   
            move = str(move) + '1'
         elif castle == "queenCastle":
            move = str(move) + '2'
         else:
            move = str(move) + '0'
            
         self.all_moves.append(move)

      all_moves1 = self.all_moves

      robot1 = self.altElement(self.all_moves)
      robot2 = self.otheraltelement(all_moves1)

      for move1 in robot1:
         self.robot1_moves.append(self.convertMove(str(move1)))

      for move2 in robot2:
         self.robot2_moves.append(self.convertMove(str(move2)))

   def getMoves(self):
      return self.robot1_moves, self.robot2_moves


  ## Headers for Game Information
#   >>> game.headers["Event"]

#        >>> game.headers["Site"]

#        >>> game.headers["Date"]

#        >>> game.headers["Round"]

#        >>> game.headers["White"]

#        >>> game.headers["Black"]

#        >>> game.headers["Result"]

def test():
   newgame = Game("GameScripts/Fischer.pgn")
   # print(newgame.game.headers["Event"])
   # print(newgame.game.headers["Site"])
   # print(newgame.game.headers["Date"])
   # for move in newgame.all_moves:
   #    print (move)
   print ("Robot 1 Moves: ")
   for move in newgame.robot1_moves:
      print (move)

   print("-----------------------")
   print("Robot 2 Moves: ")
   for move in newgame.robot2_moves:
      print (move)

if __name__ == "__main__":
   test()
