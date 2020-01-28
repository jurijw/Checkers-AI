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
        board.white_turn = not board.white_turn

        # board.must_capture = False
        board.capture_on_last_move = False
        # List to keep track of available valid moves given the game state
        # board.moves = None
        # DEBUG - remove
        # board.game_over = True


if __name__ == "__main__":
    main()

