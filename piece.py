#! /usr/bin/python3

## Peice Instance used in board classes
#  Each of the squares of the board are filled with a piece instance. If
#  A peice does not exsits it is filled with the none type.
class Piece:

    ## Constructor 
    #  @param name:string type of peice
    #  @param color:string color of peice
    #  @param x:string starting x position
    #  @param x:string starting y position
    def __init__(self, name=None, color=None,x=None,y=None):
        ## @var name 
        # peice name
        self.name = name
        ## @var color 
        # peice color
        self.color = color
        ## @var gpio 
        # XXX [BLAKE]
        self.gpio = 0
        ## @var StartingX 
        # inital x position of peice for reset
        self.StartingX = None
        ## @var StartingY
        # inital Y position of peice for reset
        self.StartingY = None
        
    # @return name:string
    def getName(self):
        return self.name

    # @return color:string
    def getColor(self):
        return self.color

    # @return XXX[BLAKE]
    def getGpio(self):
        return self.gpio

    ## Check if peice is empty
    #  @return Bool
    def isEmpty(self):
        if (self.name is None) and (self.color is None) and (self.gpio is 0):
            return True
        return False

    ## Clear the peice
    def clear(self):
        self.name = None
        self.color = None
        self.gpio = 0

    ## Set inital position of peice
    def setStartPos(self,x,y):
        self.StartingX = x
        self.StartingY = y

    ## XXX [BLAKE]
    def setGPIO(self, gpio):
        self.gpio = gpio

    # This function should not be used
    # def update(self,peice):
    #     self.name = peice.getName()
    #     self.color = peice.getColor()

    ## Print out the peice as part of a board for debugging
    def printPeice(self):
        color = self.color
        name = self.name
        if color is None:
            color = "  "
        if name is None:
            name = "  "
        if name[0] == 'k':
            print("%2s:%2s|"%( color[0], name[0:2]),end='')
        else:
            print("%2s:%2s|"%( color[0], name[0:1]),end='')
