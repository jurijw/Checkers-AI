import numpy as np

from piece import Piece
from board import Board


def main():
    # Create a new board
    board = Board()

    while not board.game_over:
        # Execute a move
        board.move()

        # Change players turn
        board.switch()


if __name__ == "__main__":
    main()

