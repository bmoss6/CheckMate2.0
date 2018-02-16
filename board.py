class board:

    def __init__(self, width=8, height=8):
        self.name = "8x8 Chess Board"
        self.width, self.height = width, height
        self.board = [[] for x in range (0,self.height)]

            ##TODO Initialize starting board pieces for 8x8 grid.


    def construct_8x8_board(self):

        first_line = []
        blank_rows =[]
        first_line.append(piece("rook","black"))
        first_line.append(piece("knight", "black"))
        first_line.append(piece("bishop", "black"))
        first_line.append(piece("queen", "black"))
        first_line.append(piece("king", "black"))
        first_line.append(piece("bishop", "black"))
        first_line.append(piece("knight", "black"))
        first_line.append(piece("rook", "black"))
        second_line = []
        for x in range(0,self.width):
            second_line.append(piece("pawn","black"))
        self.board[0] = first_line
        self.board[1] = second_line
        self.board[6] = second_line
        self.board[7] = first_line
        for x in range(0,self.width):
            self.board[6][x].color = "white"
            self.board[7][x].color = "white"
        for x in range(0,self.width):
            blank_rows.append(piece())
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
class piece:
    def __init__(self, name="null", color="null"):
        self.name = name
        self.color = color



def test():
    testboard = board()
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