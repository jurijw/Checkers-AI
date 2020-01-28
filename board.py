import numpy as np
from piece import Piece

def pos_on_board(pos):
    """
    Args:
    pos -> Tuple(x, y)
    Returns:
    True if pos on board
    else False
    """
    x, y = pos

    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    else:
        return True


class Board:
    def __init__(self, board=None, white_turn=True, game_over=False, must_capture=False):
        # Set passed arguments as Board properties
        self.white_turn = white_turn
        self.game_over = game_over
        self.must_capture = must_capture
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
        turn it is and the current board configuration. Updates the properties
        of some pieces to indicate which moves (if any) they can make. 
        Returns:
        None if game over
        else valid_moves -> List[Tuple((x, y), List[Tuple(x, y)])]
        """ 
        # Assume no capturing moves must be made
        self.must_capture = False

        # Get the current player's pieces in a 1d array
        pieces = [piece for piece in self.board.flatten() if piece.white == self.white_turn and not piece.empty]
        
        # List of vectors to neighboring pieces based on player's turn
        # and whether or not a piece is crowned
        direction = -1 if self.white_turn else 1
        vectors_not_crowned = [(-1, direction), (1, direction)]
        # If the piece is crowned it can move in all directions
        vectors_crowned = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        
        # Loop through pieces and check for potential moves
        for piece in pieces:
            # Reset some piece properties
            piece.can_move = False
            piece.can_capture = False
            piece.single_square_moves = []
            piece.two_square_moves = []

            # Lists for storing potential moves seperated by single and two square (capturing) moves
            single_square_moves = []
            two_square_moves = []

            # Get correct list of vectors depending on whether or not piece is crowned
            vectors = vectors_crowned if piece.crowned else vectors_not_crowned

            for vector in vectors:
                # Calculate position of neighbor
                dx, dy = vector
                # New position for single square move
                new_x1, new_y1 = piece.x + dx, piece.y + dy
                # New position for a double square (capturing) move
                new_x2, new_y2 = piece.x + 2*dx, piece.y + 2*dy

                # Check if square is on the board
                if pos_on_board((new_x1, new_y1)):
                    neighbor = self.board[new_y1][new_x1]
                    # Check if square is occupied by a piece of opposite color
                    if neighbor.white != self.white_turn:
                        # Check if square behind it is on the board
                        if pos_on_board((new_x2, new_y2)):
                            # If so check if that square is free
                            if self.board[new_y2][new_x2].empty:
                                capturing_pos = new_x1, new_y1
                                final_pos = new_x2, new_y2
                                two_square_moves.append((final_pos, capturing_pos))
                    # Otherwise, if the neighboring square is free
                    elif neighbor.empty:
                        final_pos = new_x1, new_y1
                        single_square_moves.append((final_pos))
                
                # If the piece can make capturing moves set these as the piece.moves 
                # property and change the must_capture attribute of the board
                if two_square_moves != []:
                    piece.can_move = True
                    piece.can_capture = True
                    piece.two_square_moves = two_square_moves
                    self.must_capture = True
                # Otherwise just set the single square moves as that pieces moves
                elif single_square_moves != []:
                    piece.can_move = True
                    piece.can_capture = False
                    piece.single_square_moves = single_square_moves

        valid_moves = []
        # If the player must make a capturing move return all the two square moves of the pieces
        for piece in pieces:
            if piece.can_move:
                piece_pos = piece.x, piece.y
                if self.must_capture:
                    valid_moves.append((piece_pos, piece.two_square_moves))
                else:
                    valid_moves.append((piece_pos, piece.single_square_moves))
        
        # If there are no valid moves for the player whose turn it is the game is over
        # In this case update the game_over status of the board and return None
        if valid_moves == []:
            self.game_over = True
            return None
        # Otherwise, return a list of valid moves 
        return valid_moves

            



def main():
    test_board = Board()
    test_board.show()
    print(test_board.valid_moves())


if __name__ == "__main__":
    main()
