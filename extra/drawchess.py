#! /usr/bin/python
##HELLO THIS IS CHANGE
import turtle
import os
from PIL import Image

def showit(x,y):
    print (x)
    print (y)           # Allows us to use turtles
wn = turtle.Screen()      # Creates a playground for turtles
Tess = turtle.Turtle()
Tess.pensize(1)
Tess.speed(100000)
w = 40
print (__file__)

filepath =os.path.abspath(os.path.join(os.path.dirname( __file__ ) ,'pictures', 'chesstry.png'))
print (filepath)
im = Image.open(filepath)
im.show
def mysquare(who, thecolor, size):
    who.pendown()
    who.pencolor(thecolor)
    who.fillcolor(thecolor)
    who.begin_fill()
    who.setheading(0)
    for i in range(4):
        who.forward(size)
        who.left(90)
    who.end_fill()


for i in range(8):
    for j in range(8):
        #      print(i,j)
        if (i + j) % 2 == 0:
            scolor = 'red'
        else:
            scolor = 'blue'
        Tess.penup()
        Tess.goto((i - 4) * w, (j - 4) * w)
        mysquare(Tess, scolor, w)


wn.onscreenclick(showit)
wn.mainloop()             # Wait for user to close window
