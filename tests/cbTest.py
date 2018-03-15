#! /usr/bin/python3

from captureBoard import CaptureBoard
cp = CaptureBoard()

print("==========INSERT==========")
for x in range(0,16):
	pos = cp.insertNextPos("king%d"%x)
	print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
print(cp.getBoard())

print("==========POPPING==========")
for x in range(0,16):
	pos = cp.popLast()
	print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
print(cp.getBoard())

print("==========INSERT==========")
for x in range(0,16):
	pos = cp.insertNextPos("king%d"%x)
	print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
print(cp.getBoard())

print("==========RESET==========")
cp.resetBoard()
print(cp.getBoard())

print("==========INSERT==========")
for x in range(0,16):
	pos = cp.insertNextPos("king%d"%x)
	print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
print(cp.getBoard())

print("==========POPPING==========")
for x in range(0,16):
	pos = cp.popLast()
	print("x:%d y:%d cBoardX:%d cBoardY:%d"%(pos.getX(),pos.getY(),pos.getXBoard(),pos.getYBoard()))
print(cp.getBoard())
