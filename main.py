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

    # Opposite of current player wins (It gets switched with board.switch())
    white_wins = not board.white_turn
    # Print winner
    print("White wins!") if white_wins else print("Black wins!")


if __name__ == "__main__":
    main()

