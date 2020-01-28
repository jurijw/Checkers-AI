import numpy as np

from piece import Piece
from board import Board


def main():
    # Create a new board
    board = Board()

    while not board.game_over:
        turn_over = False
        while not turn_over:
            board.show()
            print("White to move.") if board.white_turn else print("Black to move.")


if __name__ == "__main__":
    main()

