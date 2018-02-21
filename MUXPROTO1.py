import RPi.GPIO as GPIO
from time import sleep
import itertools
GPIO.setmode(GPIO.BCM)

NUM_QUADS = 1
NUM_SQRS = 9
SEL_BITS = 4

PIN_A1 = 24
PIN_B1 = 23
PIN_C1 = 18
PIN_D1 = 15
PIN_W1 = 14 


PIN_A2 = 16
PIN_B2 = 12
PIN_C2 = 7
PIN_D2 = 8
PIN_W2 = 25


PIN_A3 = 4
PIN_B3 = 3
PIN_C3 = 2
PIN_D3 = 21
PIN_W3 = 20


PIN_A4 = 9
PIN_B4 = 10
PIN_C4 = 22
PIN_D4 = 27
PIN_W4 = 17

prev_board = []
curr_board = []
select = [];

def setup():
	for x in range(0,NUM_QUADS):
		row = []
		for y in range(0,NUM_SQRS):
			row.append(0)
		curr_board.append(row)
		prev_board.append(row)

	for x in range(0,SEL_BITS):
		select.append(0)

	GPIO.setup(PIN_A1, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_B1, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_C1, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_D1, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_W1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(PIN_A2, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_B2, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_C2, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_D2, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_W2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(PIN_A3, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_B3, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_C3, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_D3, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_W3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(PIN_A4, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_B4, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_C4, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_D4, GPIO.OUT, initial = 0)
	GPIO.setup(PIN_W4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	
def checkmux1():
	setup()
	GPIO.output(PIN_A1, 0)
	GPIO.output(PIN_B1,0)
	GPIO.output(PIN_C1, 0)
	GPIO.output(PIN_D1, 0)
	print str(GPIO.input(PIN_W1))
	
	
def checkmux2():
	setup()
	GPIO.output(PIN_A2, 0)
	GPIO.output(PIN_B2,0)
	GPIO.output(PIN_C2, 0)
	GPIO.output(PIN_D2, 0)
	print str(GPIO.input(PIN_W2))
	
def checkmux3():
	setup()
	GPIO.output(PIN_A3, 0)
	GPIO.output(PIN_B3,0)
	GPIO.output(PIN_C3, 0)
	GPIO.output(PIN_D3, 0)
	print str(GPIO.input(PIN_W3))
	
def checkmux4():
	setup()
	GPIO.output(PIN_A4,1)
	GPIO.output(PIN_B4,0)
	GPIO.output(PIN_C4, 0)
	GPIO.output(PIN_D4, 0)
	print str(GPIO.input(PIN_W4))
	
def check3x3():
	setup()
	
	curr = []
	for x in range(0,3):
		row = []
		
		for y in range(0,3):
			row.append(0)
		curr.append(row)
	#print (curr)		
	for i in range(0,NUM_SQRS):
		select[3] = i & (1 << 3)
		select[2] = i & (1 << 2)
		select[1] = i & (1 << 1)
		select[0] = i & 1
		GPIO.output(PIN_A, select[3])
		GPIO.output(PIN_B, select[2])
		GPIO.output(PIN_C, select[1])
		GPIO.output(PIN_D, select[0])
		stuff = (str(select[3]),str(select[2]),str(select[1]),str(select[0]))
		stuff = ''.join(stuff)
		##print stuff
		#print '-----------------'
		i, j = mapit(stuff)	
		curr[i][j] = GPIO.input(PIN_W)
	
	print3x3(curr)
		#print (str(GPIO.input(PIN_W)))
	#GPIO.output(PIN_A, 1)
	#GPIO.output(PIN_B, 0)
	#GPIO.output(PIN_C, 0)
	#GPIO.output(PIN_D, 0)
	#while 1:
	#	print('E0 : ' + str(GPIO.input(PIN_W)))

def print3x3(board):
	for x in range (0,3):
		print 
		for y in range(0,3):
			print str(board[x][y]) + ' ',
def mapit(s):
	if s=='0000':
		return 0,0
	if s=='0001':
		return 1,0
	if s=='0020':
		return 2,0
	if s=='0021':
		return 1,0
	if s=='0400':
		return 1,1
	if s=='0401':
		return 1,2
	if s=='0420':
		return 2,0
	if s=='0421':
		return 2,1
	if s=='8000':
		return 2,2	
def checkBoard():

	for i in range(0,NUM_SQRS):
		select[3] = i & (1 << 3)
		select[2] = i & (1 << 2)
		select[1] = i & (1 << 1)
		select[0] = i & 1
		print ('-------------')
                print (select[3])
                print (select[2])
                print (select[1])
                print (select[0])
                print ('----------------')
		GPIO.output(PIN_A, select[3])
		GPIO.output(PIN_B, select[2])
		GPIO.output(PIN_C, select[1])
		GPIO.output(PIN_D, select[0])
                #print('Here!!')
                #print(i)
		prev_board[0][i] = curr_board[0][i];
		prev_board[1][i] = curr_board[1][i];
		prev_board[2][i] = curr_board[2][i];
		prev_board[3][i] = curr_board[3][i];

		curr_board[0][i] = GPIO.input(PIN_W)
		#curr_board[1][i] = 1# read Din from mux1 for Q2 */;
		#curr_board[2][i] = 1# read Din from mux2 for Q3 */;
		#curr_board[3][i] = 1# read Din from mux3 for Q4 */;

	
def printBoard():
	#for i in range(0,4):
		#print("%d %d %d %d %d %d %d %d"% \
		#	(curr_board[0][i*4+0], curr_board[0][i*4+1], \
			#curr_board[0][i*4+2], curr_board[0][i*4+3], \
			#curr_board[1][i*4+0], curr_board[1][i*4+1], \
			#curr_board[1][i*4+2], curr_board[1][i*4+3]))

	#for i in range(0,4):
		#print("%d %d %d %d %d %d %d %d"% \
		#	(curr_board[2][i*4+0], curr_board[2][i*4+1], \
		#	curr_board[2][i*4+2], curr_board[2][i*4+3], \
		#	curr_board[3][i*4+0], curr_board[3][i*4+1], \
		#	curr_board[3][i*4+2], curr_board[3][i*4+3]))
	print(str(curr_board[0][0]))

def main():
	setup()

	while(1):
		checkBoard()
		printBoard()

		sleep(1)


if __name__=='__main__':
	while 1:
		checkmux4()

