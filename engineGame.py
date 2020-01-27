# This code will later be integrated into the playGame function in run.py. Or maybe its own function. Depends on how we want to implement it.
import asyncio
import chess
import chess.engine

def convertMoveFromEngineToRobot(move):
    # The chess engine represents moves in algebraic notation. The robot wants x & y coordinates

async def main():
    # connecting to the stockfish engine
    transport, engine = await chess.engine.popen_uci("stockfish")

    # create a gui object to connect with the gui
    gui = Gui();

    # create board that will keep track of moves for the engine. The robot uses a separate board to track moves.
    board = chess.Board()

    # run game until the engine detects a checkmate
    while not board.is_game_over():
        while True:
            # get the next move from user input in the gui
            move = gui.getNextMove(); 

            # create a python-chess move object in order to check for legal moves
            move_object = chess.Move.from_uci(move)
            if move_object in board.legal_moves:
                board.push(move_object)
                start = Position(move[0], move[1])
                end = Position(move[2], move[3])
                if castle != 0:
                    robot.castle(castle,1)
                else:
                    robot.move(start,end)
                break
            else:
                gui.notLegalMove()
        result = await engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        robot_move = convertMoveFromEngineToRobot(move)
        start = Position(robot_move[0], robot_move[1])
        end = Position(robot_move[2], robot_move[3])
        print(result.move)

    await engine.quit()
    robot.clearRobotPieces()
    robot2.clearRobotPieces()
    robot.resetToOriginalPosition()
    robot2.resetToOriginalPosition()

asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())

get move from user
	feed to engine
	create start and end position object for the move
	if castle:
		robot.castle - 1 for rb1, 2 for rb2
	else:
		robot.move
get move from engine
	create start and end position object for the move
		if castle:
			robot.castle - 1 for rb1, 2 for rb2
		else:
			robot.move

robot.clearRobotPieces()
robot2.clearRobotPieces()
robot.resetToOriginalPosition()
robot2.resetToOriginalPosition()