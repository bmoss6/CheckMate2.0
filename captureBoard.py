#! /usr/bin/python

#from position import Position

class CaptureBoard(object):

	#2x8 to hold all peices. Top half the right side. Bottom the left.
	board=[]
	peiceCount=0

	"""docstring for CaptureBoard"""
	def __init__(self):
		super(CaptureBoard, self).__init__()

		for x in xrange(0,8):
			row = []
			for y in xrange(0,2):
				row.append(None)
			self.board.append(row)

	# We will make 2x4 capture areas for each of the captured peices


	#GPIO check
	def selfCheck(self):
		pass

	#Get next open postion
	def getOpenPos(self):
		pass
	
	#Return a list of all of the captured pecies so that we can rest board
	def captureList(self):
		pass

	#There may be times we will want to hold a peice in the discard pile and need to get it back.
	def getLast(self):
		pass

	def retBoard(self):
		return self.board