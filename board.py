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
    def __init__(self, board=None, white_turn=True, game_over=False, must_capture=False, capture_on_last_move=False):
        # Set passed arguments as Board properties
        self.white_turn = white_turn
        self.game_over = game_over
        self.must_capture = must_capture
        self.capture_on_last_move = capture_on_last_move
        # List to keep track of available valid moves given the game state
        self.moves = None

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
        else valid_moves -> List[Tuple(Tuple(x, y), List[Tuple(x, y), ..])]
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
                new_x2, new_y2 = piece.x + 2 * dx, piece.y + 2 * dy

                # Check if square is on the board
                if pos_on_board((new_x1, new_y1)):
                    neighbor = self.board[new_y1][new_x1]
                    # Check if square is occupied by a piece of opposite color
                    if neighbor.white != self.white_turn and not neighbor.empty:
                        # Check if square behind it is on the board
                        if pos_on_board((new_x2, new_y2)):
                            # If so check if that square is free
                            if self.board[new_y2][new_x2].empty:
                                capturing_pos = new_x1, new_y1
                                final_pos = new_x2, new_y2
                                two_square_moves.append([final_pos, capturing_pos])
                    # Otherwise, if the neighboring square is free and no capturing move was made on the last turn
                    elif neighbor.empty and not self.capture_on_last_move:
                        final_pos = new_x1, new_y1
                        single_square_moves.append([final_pos])
                
            # If the piece can make capturing moves set these as the piece.moves 
            # property and change the must_capture attribute of the board
            if two_square_moves != []:
                piece.can_move = True
                piece.can_capture = True
                piece.two_square_moves = two_square_moves
                self.must_capture = True
            # Otherwise just set the single square moves as that piece's moves
            elif single_square_moves != []:
                piece.can_move = True
                piece.can_capture = False
                piece.single_square_moves = single_square_moves

        valid_moves = []
        # If the player must make a capturing move return all the two square moves of the pieces
        # This occurs either when a capturing move is available or if a capturing move was made 
        # on the last turn.
        for piece in pieces:
            piece_pos = piece.x, piece.y

            if self.capture_on_last_move or self.must_capture:
                # Check if double square moves exist
                if piece.two_square_moves != []:
                    valid_moves.append((piece_pos, piece.two_square_moves))
            elif piece.can_move:
                valid_moves.append((piece_pos, piece.single_square_moves))
        
        # FIX: perhaps implement this elsewhere
        # # If there are no valid moves for the player whose turn it is the game is over
        # # In this case update the game_over status of the board and return None
        # if valid_moves == []:
        #     self.game_over = True
        #     return None

        # Otherwise, return a list of valid moves 
        self.moves = valid_moves
        return valid_moves

    def move(self):
        """
        Move a piece and remove a piece in the event of a capture.
        The indexes refer to a piece and move in the board's 
        board.moves list.
        Args:
        piece_index, move_index -> Int
        Returns:
        True if turn completed
        else False
        """
        # Display the board
        self.show()

        # Get valid moves (also updates self.moves in the process)
        valid_moves = self.valid_moves()

        # Base case - no valid moves available 
        if valid_moves == []:
            return True

        # Recursive case - capturing move has been made and subsequent capturing moves exist or no capture has been made
        #                  but capturing moves exist

        # Get user input
        print("White to move.") if self.white_turn else print("Black to move.")

        # Print moves and get input
        moveable_pieces = [move[0] for move in valid_moves]
        print("Moveable pieces: ", moveable_pieces)
        piece_index = int(input(f"Choose a piece by index (0 - {len(moveable_pieces) - 1}) : "))
        # Get the moves for that piece
        potential_moves = [move[0] for move in valid_moves[piece_index][1]]
        print("Potential Moves: ", potential_moves)
        move_index = int(input(f"Choose a move by index (0 - {len(potential_moves) - 1}) : "))


        # Get piece position
        piece_x, piece_y = valid_moves[piece_index][0]
        # Get the piece reference
        piece = self.board[piece_y][piece_x] 
        # Get the desired move
        new_x, new_y = self.moves[piece_index][1][move_index][0]
        # Move the piece to the new location
        self.board[new_y][new_x] = piece
        # Remove its reference in the old position
        self.board[piece.y][piece.x] = Piece((piece.x, piece.y), empty=True)

        # Update the pieces location
        piece.x, piece.y = new_x, new_y

        # Check for crowning
        if piece.white and piece.y == 0 or not piece.white and piece.y == 7:
            piece.crowned = True

        # If capturing move, remove the captured piece
        if piece.can_capture:
            captured_x, captured_y = self.moves[piece_index][1][move_index][1]
            self.board[captured_y][captured_x] = Piece((captured_x, captured_y), empty=True)
            # Update the capture_on_last_move attribute
            self.capture_on_last_move = True

            # Recurse
            if self.move():
                return True
            else:
                return False
        
    
        return False



def main():
    test_board = Board()
    for j, row in enumerate(test_board.board):
        for i, _ in enumerate(row):
            test_board.board[j][i] = Piece((i, j), empty=True)
    
    test_board.board[1][1] = Piece((1, 1), white=False)
    test_board.board[1][5] = Piece((5, 1), white=False)

    test_board.board[3][3] = Piece((3, 3), white=True)
    test_board.board[4][2] = Piece((2, 4), white=True)
    test_board.board[4][4] = Piece((4, 4), white=True)
    test_board.board[6][2] = Piece((2, 6), white=True)


    game_over = False
    while not game_over:
        test_board.move()
        test_board.white_turn = not test_board.white_turn
        test_board.must_capture = False
        test_board.capture_on_last_move = False
        # List to keep track of available valid moves given the game state
        test_board.moves = None

    



if __name__ == "__main__":
    main()
