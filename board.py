import numpy as np
from piece import Piece


class Board:
    def __init__(self, board=None, white_turn=True):
        # Set passed arguments as Board properties
        self.white_turn = white_turn
        # If no baord is passed generate one
        if board == None:
            # Placeholder array
            board = np.zeros((8, 8), dtype=Piece)

            for j in range(8):
                for i in range(8):
                    # Fill the empty squares
                    if j == 3 or j == 4:
                        board[j][i] = Piece((i, j), empty=True)
                    elif i % 2 == 0 and j % 2 == 0:
                        board[j][i] = Piece((i, j), empty=True)
                    elif i % 2 != 0 and j % 2 != 0:
                        board[j][i] = Piece((i, j), empty=True)

                    # Loop through odd rows and even columns
                    if i % 2 == 0 and j % 2 != 0:
                        if j == 1:
                            board[j][i] = Piece((i, j), white=False)
                        if j == 5 or j == 7:
                            board[j][i] = Piece((i, j), white=True)
                    # Loop through even rows and odd columns
                    if i % 2 != 0 and j % 2 == 0:
                        if j == 0 or j == 2:
                            board[j][i] = Piece((i, j), white=False)
                        if j == 6:
                            board[j][i] = Piece((i, j), white=True)
            # Set the board attribute to the 2d array of pieces
            self.board = board
        else:
            self.board = board

    def show(self):
        """
        Prints the current board configuration in the commandline.
        (X)s represent white pieces while (O)s represent red ones.
        Returns:
        None
        """
        # Loop through rows and columns
        for row in self.board:
            for piece in row:
                if piece.empty:
                    print("| |", end="")
                else:
                    if piece.crowned:
                        if piece.white:
                            print("|X^", end="")
                        else:
                            print("|O^", end="")
                    else:
                        if piece.white:
                            print("|X|", end="")
                        else:
                            print("|O|", end="")
            print()

    def valid_moves(self):
        """
        Returns a list of valid moves based on which player's
        turn it is and the current board configuration.
        """ 
        # Get the current player's pieces in a 1d array
        pieces = [piece for piece in self.board.flatten() if piece.white == self.white_turn and not piece.empty]
        
        # List of vectors to neighboring pieces based on player's turn
        # and whether or not a piece is crowned
        direction = -1 if self.white_turn else 1
        vectors_not_crowned = [(1, direction), (-1, direction)]
        # If the piece is crowned it can move in all directions
        vectors_crowned = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

        # Loop through pieces and check for potential moves
        for piece in pieces:
            # Get correct list of vectors depending on whether or not piece is crowned
            vectors = vectors_crowned if piece.crowned else vectors_not_crowned

            for vector in vectors:
                # Calculate position of neighbor
                dx, dy = vector
                # New position for single square move
                new_x1, new_y1 = piece.x + dx, piece.y + dy
                # New position for a double square (capturing) move
                new_x2, new_y2 = piece.x + 2*dx, piece.y + 2*dy
                # Check if square is occupied by a piece of opposite color
                if self.board[new_y][new_x].white != self.white_turn:
                    # If so check if the square behind it is free
                    if se
            



def main():
    test_board = Board()
    test_board.show()
    print(len(test_board.valid_moves()))


if __name__ == "__main__":
    main()
