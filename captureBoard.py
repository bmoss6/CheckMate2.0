#! /usr/bin/python3

#from position import Position
from capturePosition import CapturePosition

## CaptureBoard
#  The capture board is an exections of the playing board for each robot in order to keep
#  track and place the disgarded peices. You can think of it like a stack that you push and
#  pop pecies on and off of. Structurally it is just a 2D array in which the 1st half of the
#  rows represent one half of the board and the second. Running the test cases should give a
#  pretty clear demenstration of how the data structure works 
class CaptureBoard(object):

   ## Constructor
   #  @param invert:bool invert:bool store if returned peices should be inverted for this capture board.
   def __init__(self,invert=False):
      super(CaptureBoard, self).__init__()

      self.COLUMN_LENGTH=8
      self.ROW_LENGTH=2
      #2x8 to hold all peices. Top half the right side. Bottom the left.
      self.board=[]
      self.peiceCount=0
      #A hack to get the first index correctly...
      self.lastRowI=0
      self.lastColI=0
      self.invert = False

      self.invert = invert
      # We will make 2x4 capture areas for each of the captured peices
      for x in range(0,self.COLUMN_LENGTH):
         row = []
         for y in range(0,self.ROW_LENGTH):
            row.append(None)
         self.board.append(row)

   ## Convert the index of the array on the board to a Position on the capture board
   #  @param row:int index of row
   #  @param col:int index of column
   #  @return type:CapturePoisiton poistion on capture board
   def convIndexPos(self,row,col):
      # Check if we are on the other half 
      nextSide = True if row >= self.COLUMN_LENGTH/2 else False
      if nextSide:
         row = row % int(self.COLUMN_LENGTH/2)
      return CapturePosition(row,col,nextSide,self.invert)

   ## Insert a peice on the the next avaliable space of the CaptureBorad
   #  @param peice:Piece Piece to store in capture board
   #  @return type:CapturePosition poistion of the empty space found
   def insertNextPos(self,peice):
      if self.peiceCount == 0:
         self.lastRowI = 0
         self.lastColI = 0
      else:
         # Increament to next avalible position
         self.lastColI += 1
         if ( (self.lastColI % self.ROW_LENGTH) == 0):
            self.lastRowI += 1
            self.lastColI = 0
            # print("test %d"%self.peiceCount)
            # self.printBoard()
            assert(self.lastRowI<self.COLUMN_LENGTH)
      # insert peice
      self.board[self.lastRowI][self.lastColI] = peice
      self.peiceCount += 1

      return self.convIndexPos(self.lastRowI,self.lastColI)

   ## Get the last peice placed on the capture board. You can think of the board as a stack 
   ##  that you popping the next peice off of.
   #  @return type:CapturePoistion, type:Piece The poistion and piece that are popped off.
   def popLast(self):
      if self.peiceCount == 0:
         return None, None
      pos = self.convIndexPos(self.lastRowI,self.lastColI)
      peice = self.board[self.lastRowI][self.lastColI]
      #Reset index we pop to none
      self.board[self.lastRowI][self.lastColI]=None
      if self.peiceCount != 1:
         self.lastColI -= 1
      if ( self.lastColI < 0):
         self.lastRowI -= 1 
         self.lastColI = self.ROW_LENGTH-1
         assert(self.lastRowI>=0)
      self.peiceCount -= 1
      return pos, peice

   ## Clear all of the pieces from the capture board.
   def resetBoard(self):
      self.lastRowI = 0
      self.lastColI = 0
      self.peiceCount = 0
      for x in range(0,self.COLUMN_LENGTH):
         for y in range(0,self.ROW_LENGTH):
            self.board[x][y] = None

   ## get the board array
   #  @return type:2D array of pieces
   def getBoard(self):
      return self.board

   ## Used to debug and print the contents of the board.
   def printBoard(self):
      print("RIGHT")
      self.printRight()
      print("LEFT")
      self.printLeft()

   ## Used to debug and print the right side of the board.
   def printRight(self):
      print("      [0]   [1]")
      for x in range(0,int(self.COLUMN_LENGTH/2)):
         print("[%d] |"%x,end='')
         for y in range(0,self.ROW_LENGTH):
            if self.board[x][y] is None:
               print("  :  |",end='')
               continue
            self.board[x][y].printPeice()
         print()

    ## Used to debug and print the left side of the board.
   def printLeft(self):
      print("      [0]   [1]")
      for x in range(int(self.COLUMN_LENGTH/2),self.COLUMN_LENGTH):
         print("[%d] |"%(x-int(self.COLUMN_LENGTH/2)),end='')
         for y in range(0,self.ROW_LENGTH):
            if self.board[x][y] is None:
               print("  :  |",end='')
               continue
            self.board[x][y].printPeice()
         print()


def test():
   # imbracing the grossness of python with dynmaic imports
   from piece import Piece
   cp = CaptureBoard()
   cp.printBoard()

   print("==========INSERT==========")
   for x in range(0,16):
      name = "k%d"%x
      pos = cp.insertNextPos(Piece(name,"white"))
      print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
      cp.printBoard()
      print()

   print("==========POPPING==========")
   for x in range(0,16):
      pos, peice = cp.popLast()
      print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
      print("%s:%s"%(peice.getName(),peice.getColor()))
      cp.printBoard()
   #print(cp.getBoard())

   print("==========INSERT==========")
   for x in range(0,16):
      name = "k%d"%x
      pos = cp.insertNextPos(Piece(name,"white"))
      print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
      cp.printBoard()
   #print(cp.getBoard())

   print("==========RESET==========")
   cp.resetBoard()
   cp.printBoard()
   #print(cp.getBoard())

   print("==========INSERT==========")
   for x in range(0,16):
      name = "k%d"%x
      pos = cp.insertNextPos(Piece(name,"white"))
      print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
      cp.printBoard()
   #print(cp.getBoard())

   print("==========POPPING==========")
   for x in range(0,16):
      pos, peice = cp.popLast()
      print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
      cp.printBoard()
   #print(cp.getBoard())


if __name__ == "__main__":
   test()
