#! /usr/bin/python

#from position import Position
from capturePosition import CapturePosition

class CaptureBoard(object):

   COLUMN_SIZE=8
   ROW_SIZE=2
   #2x8 to hold all peices. Top half the right side. Bottom the left.
   board=[]
   peiceCount=0
   #A hack to get the first index correctly...
   lastRowI=0
   lastColI=0
   invert = False

   """docstring for CaptureBoard"""
   def __init__(self,invert=False):
      super(CaptureBoard, self).__init__()

      self.invert = invert
      # We will make 2x4 capture areas for each of the captured peices
      for x in range(0,self.COLUMN_SIZE):
         row = []
         for y in range(0,self.ROW_SIZE):
            row.append(None)
         self.board.append(row)
      

   #GPIO check
   def selfCheck(self):
      pass

   def convIndexPos(self,row,col):
      # Check if we are on the other half 
      nextSide = True if row >= self.COLUMN_SIZE/2 else False
      if nextSide:
         row = row % int(self.COLUMN_SIZE/2)
      return CapturePosition(row,col,nextSide,self.invert)

   #This function inserts an object into the array at index
   #Return the next position
   def insertNextPos(self,peice):
      
      if self.peiceCount == 0:
         self.lastRowI = 0
         self.lastColI = 0
      else:
         # Increament to next avalible position
         self.lastColI += 1
         if ( (self.lastColI % self.ROW_SIZE) == 0):
            self.lastRowI += 1
            self.lastColI = 0
            assert(self.lastRowI<self.COLUMN_SIZE)
      # insert peice
      self.board[self.lastRowI][self.lastColI] = peice
      self.peiceCount += 1

      return self.convIndexPos(self.lastRowI,self.lastColI)
   
   #Return a list of all of the captured pecies so that we can rest board
   def captureList(self,piece):
      pass

   #There may be times we will want to hold a peice in the discard pile and need to get it back.
   #return last index
   def popLast(self):
      if self.peiceCount == 0:
         return None
      pos = self.convIndexPos(self.lastRowI,self.lastColI)
      #Reset index we pop to none
      self.board[self.lastRowI][self.lastColI]=None
      if self.peiceCount != 1:
         self.lastColI -= 1
      if ( self.lastColI < 0):
         self.lastRowI -= 1 
         self.lastColI = self.ROW_SIZE-1
         assert(self.lastRowI>=0)
      self.peiceCount -= 1
      #print(self.board[row][col])
      return pos

   def resetBoard(self):
      self.lastRowI = 0
      self.lastColI = 0
      self.peiceCount = 0
      for x in range(0,self.COLUMN_SIZE):
         for y in range(0,self.ROW_SIZE):
            self.board[x][y] = None

   def getBoard(self):
      return self.board