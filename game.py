#!/usr/bin/env python3
import chess.pgn
from collections import namedtuple

## A class that reads a PGN formatted game and translates it into a series of moves for the robots.
#
# PGN, or portable game notation, and a commonly used format for digitized chess games. 
# PGN formatted games include information on the location of the game when it was played,
# who the participants were, the various moves stored in different formats, and also 
# rankings on the quality of move made. 
#
# The most useful format that moves are stored in is called algebraic notation. Information
# on the specifics can be found online. This class will read through the PGN formatted game
# and retrieve the moves for each player.

class Game(object):

   ## Retrieve every other move starting with the first move in index 0.
   # This represents the moves made by the first robot.
   #@param a:string array of all moves in this game.
   def altElement(self, a):
      return a[::2]

   ## Retrieve every other move starting with the second move in index 1.
   # This represent the moves made by the second robot.
   #@param b:string array of all moves in this game.
   def otheraltelement(self, b):
      return b[1::2]

   ## Convert the move we have retrived from PGN format into something the
   # robot class will be able to interpret and use for movement.
   #@param move:string move retrieved from PGN file.
   def convertMove(self, move):
      ## @var startposy
      # The first character of the move string is the y coordinate of the
      # starting position.
      startposy = move[0]
      ## @var startposx
      # The second character of the move string is the x coordinate of the
      # starting position.
      startposx = move[1]
      ## @var endposy
      # The third character of the move string is the y coordinate of the
      # ending position.
      endposy = move[2]
      ## @var endposx
      # The fourth character of the move string is the x coordinate of the
      # ending position.
      endposx = move[3]
      ## @var castle
      # The fifth character of the move string is a special character we have
      # added to keep track of whether or not the move is a castling move.
      castle = move[4]
      ## @var mapping
      # translate the "file" or y coordinates into a number we can pass to the
      # robot class.
      mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
      ## @var mapping2
      # translate the "rank" or x coordinates into a number we can pass to the
      # robot class.
      mapping2 = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

      ## @var start
      # The starting position, stored in a nameTuple with x and y coordinates
      start = self.Square(x=mapping2.get(startposx), y=mapping.get(startposy))
      ## @var end
      # The ending position, stored in a nameTuple with x and y coordinates
      end = self.Square(x=mapping2.get(endposx), y=mapping.get(endposy))

      ## @var move
      # The complete move from start to end, stored as a namedTuple with nested
      # namedTuples for each individual position for easy access. Can reference 
      # coordinates with move.start.x, for example.
      move = self.Move(start, end, castle)

      return (move)
   ## The constructor to initialize and define the different datastructures that hold
   # the moves, as well as read the file containing the PGN formatted game.
   #@param filename:string the name of the file that holds the PGN formatted game.
   def __init__(self, filename):

      ## @var robot1_moves
      # an array that will hold all of the moves for robot 1
      self.robot1_moves = []
      ## @var robot2_moves
      # an array that will hold all of the moves for robot 2
      self.robot2_moves = []
      ## @var all_moves
      # an array that will temporarily hold all of the moves in the game while we
      # assign moves to each of the robots.
      self.all_moves = []
      ## @var pgn
      # The game file with the PGN game information
      self.pgn = open(filename)
      ## @var game
      # The actual game, translated from the PGN file we received during
      # initialization. This holds all of the information about the game such
      # as moves, as well as metadata about the chess players and location and
      # time of play.
      self.game = chess.pgn.read_game(self.pgn)

      ## @var Square
      # A namedTuple to hold the x and y coordinates of a single position or square.
      self.Square = namedtuple('Square', ['x', 'y'])
      ## @var Move
      # A namedTuple to hold the starting and ending postion of a whole move, as well as
      # keep track of whether or not the move is a castling move.
      self.Move = namedtuple('Move', ['start', 'stop', 'castle'])

      ## @var node
      # A copy of game needed to keep track of more difficult moves, such as castle. It is
      # necessary to keep track of the algebraic notation using the chess library's node structure
      # to account for odd moves like castling, which do not show up correctly in the easier to translate
      # moves we get from the main_line. If we find a castle, add the correct castling form onto the end
      # of the move so we can account for it in the robot class.
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

      ## @var all_moves1
      # A poorly named and temporary variable needed to hold all of the moves
      # so robot2 can retrieve the ones it needs.
      all_moves1 = self.all_moves

      ## @var robot1
      # A temporary variable to hold the raw moves for robot1 prior to translating them
      # into robot readable moves.
      robot1 = self.altElement(self.all_moves)
      ## @var robot2
      # A temporary variable to hold the raw moves for robot2 prior to translating them
      # into robot readable moves.
      robot2 = self.otheraltelement(all_moves1)

      for move1 in robot1:
         self.robot1_moves.append(self.convertMove(str(move1)))

      for move2 in robot2:
         self.robot2_moves.append(self.convertMove(str(move2)))

      ## A get function to retrieve the translated moves for each robot.
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
