#! /usr/bin/python3

from board import Board

def test():
    testboard = Board()
    testboard.construct_8x8_board()
    for x in range(0,len(testboard.board)):
        for y in range(0,testboard.width):
            print("||" +str(x)+str(y)+" " + testboard.board[x][y].color + " " + testboard.board[x][y].name +"||"),
        print("------------------------------------")
    i =0
    j =0

   # for x in testboard.board:
    #    for y in testboard.board[i]:
     #       print (str(i) + str(j) + "\n" + testboard.board[i][j].name +" "+ testboard.board[i][j].color)
      #      j= j+1
       # i = i+1
        #print("--------------------------------------------------------")


if __name__ == "__main__":
    test()