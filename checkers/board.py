import pygame
from checkers.constants import Constants
from checkers.piece import Piece
from checkers.angry_piece import AngryPiece

class Board:
    def __init__(self):
        """Initialize a new game board.
        """
        self.c = Constants()
        self.board = []
        self.grey_left = self.white_left = 12
        self.grey_kings = self.white_kings = 0
        self.build_board()

    def make_squares(self, window):
        """Draw the squares on the game board.

        Args:
            window (Surface): The Pygame surface on which to draw the game board.
        """
         # Fill the window with the color BLACK
        window.fill(self.c.BLACK)

        # Loop through all rows and columns of the game board
        for r in range(self.c.ROWS):
            for c in range(r % 2, self.c.COLS, 2):
                # Draw a square at the current row and column
                self.square(window, r, c)
    def square(self, window, r, c):
        """Draw a single square on the game board.

    Args:
        window (Surface): The Pygame surface on which to draw the game board.
        r (int): The row of the square to draw.
        c (int): The column of the square to draw.
    """
        #draws square
        pygame.draw.rect(window, self.c.GREY, (r * self.c.SQUARE, c * self.c.SQUARE,
                                                   self.c.SQUARE, self.c.SQUARE))

    def move(self, piece, r, c, window=None):
        """Move a piece on the game board.

    Args:
        piece (Piece): The piece to move.
        r (int): The row to move the piece to.
        c (int): The column to move the piece to.
        window (Surface, optional): The Pygame surface on which to draw the move.
            Defaults to None.
    """
        # Swap the piece at the current position with the piece at the new position
        self.board[piece.row][piece.col], self.board[r][c] = self.board[r][c], self.board[piece.row][piece.col]
        # Move the piece to the new position on the game board
        piece.move_piece(r, c, window)
        # If the moved piece reaches the opposite side of the board, make it a king
        self.make_king(piece, r)

    def make_king(self, piece, r):
        """Make a piece a king if it reaches the opposite end of the board.

    Args:
        piece (Piece): The piece to potentially promote.
        row (int): The row that the piece moved to.
    """
        # Check if the piece reached the top or bottom row of the board
        if r == self.c.ROWS - 1 or r == 0:
            # Promote the piece to a king
            piece.promote_king()

            # Increment the number of kings for the piece's color
            if piece.color == self.c.WHITE:
                self.white_kings += 1
            else:
                self.grey_kings += 1

    def find_piece(self, r, c):
        """Get the piece at the given position on the game board.

    Args:
        r (int): The row of the piece to get.
        c (int): The column of the piece to get.

    Returns:
        Piece: The piece at the given position, or 0 if there is no piece.
    """
        # Return the piece at the given position on the board
        return self.board[r][c]

    def build_board(self):
        """Create the initial state of the game board.
    """
        # Loop through all rows and columns of the game board
        for r in range(self.c.ROWS):
            # Append an empty list to represent the current row of the board
            self.board.append([])

            # Loop through all columns of the current row
            for c in range(self.c.COLS):
                # Create a piece at the current position on the board
                self.create_piece(r,c)

    def create_piece(self, r, c):
        """Create a piece at the given position on the game board.

    Args:
        r (int): The row of the piece to create.
        c (int): The column of the piece to create.
    """
         # Check if the current position should contain a piece
        if c % 2 == ((r + 1) % 2):
            # If the row is in the top three rows, create a white piece
            if r < 3:
                self.board[r].append(AngryPiece(r, c, self.c.WHITE))
            # If the row is in the bottom three rows, create a grey piece
            elif r > 4:
                self.board[r].append(AngryPiece(r, c, self.c.GREY))
            # Otherwise, append 0 to represent an empty position
            else:
                self.board[r].append(0)
        # If the current position should not contain a piece, append 0 to represent an empty position
        else:
            self.board[r].append(0)
        

    def draw_board(self, window):
        """Draw the game board and all of the pieces on it.

    Args:
        window (Surface): The Pygame surface on which to draw the game board.
    """
         # Draw the squares on the game board
        self.make_squares(window)

        # Loop through all rows and columns of the game board
        for r in range(self.c.ROWS):
            for c in range(self.c.COLS):
                # Get the piece at the current position on the board
                piece = self.board[r][c]

                # If there is a piece at the current position, draw it on the window
                if piece != 0:
                    piece.draw_piece(window)

    def remove_piece(self, pieces):
        """Remove a list of pieces from the game board.

    Args:
        pieces (list): A list of pieces to remove.
    """
        # Loop through all pieces in the list
        for piece in pieces:
            # Set the position of the piece on the board to 0 to represent an empty position
            self.board[piece.row][piece.col] = 0

            # If the piece is not 0 (i.e. it is a valid piece)
            if piece != 0:
                # Decrement the number of pieces for the piece's color
                if piece.color == self.c.GREY:
                    self.grey_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        """Determine the winner of the game.

    Returns:
        str: The color of the winning player, or None if the game is not over.
    """
        # If there are no more grey pieces, white wins
        if self.grey_left <= 0:
            return self.c.WHITE
        # If there are no more white pieces, grey wins
        elif self.white_left <= 0:
            return self.c.GREY

        # If there are still pieces of both colors, the game is not over
        return None

    def possible_moves(self, piece):
        """Get a dictionary of valid moves for a given piece.

    Args:
        piece (Piece): The piece to get valid moves for.

    Returns:
        dict: A dictionary of valid moves, where the keys are tuples representing
            positions on the game board, and the values are the pieces that will
            be skipped if the move is made.
    """
        # Initialize an empty dictionary to store valid moves
        posible_moves = {}

        # Get the left and right columns relative to the current piece's position
        left_col = piece.col - 1
        right = piece.col + 1

        # Get the current piece's row
        r = piece.row

        # If the current piece is a grey piece or a king,
        # check for possible moves in the upward direction
        if piece.color == self.c.GREY or piece.king:
            # Update the dictionary of valid moves with the moves that are found
            posible_moves.update(self.move_left(r - 1, max(r - 3, -1), -1, piece.color, left_col))
            posible_moves.update(self.move_right(r - 1, max(r - 3, -1), -1, piece.color, right))

        # If the current piece is a white piece or a king,
        # check for possible moves in the downward direction
        if piece.color == self.c.WHITE or piece.king:
            # Update the dictionary of valid moves with the moves that are found
            posible_moves.update(self.move_left(r + 1, min(r + 3, self.c.ROWS), 1, piece.color, left_col))
            posible_moves.update(self.move_right(r + 1, min(r + 3, self.c.ROWS), 1, piece.color, right))
        # Return the dictionary of valid moves
        return posible_moves

    def move_left(self, start, stop, step, color, left, passed=[]):
        """Recursively traverse the game board in the left direction.

    This method is used to find all of the valid moves for a given piece.

    Args:
        row (int): The row to start traversing from.
        end (int): The row to end traversing at.
        direction (int): The direction in which to traverse (-1 for up, 1 for down).
        color (str): The color of the piece for which to find valid moves.
        col (int): The column to traverse from.

    Returns:
        dict: A dictionary of valid moves that were found during traversal, where the keys
            are tuples representing positions on the game board, and the values are the pieces
            that will be skipped if the move is made.
    """
         # Initialize an empty dictionary to store valid moves
        posible_moves = {}

        # Initialize a list to store pieces that have been skipped
        removed = []

        # Loop through the rows starting at the start position and moving in the direction specified by step
        for r in range(start, stop, step):
            # If the left column is out of bounds, break out of the loop
            if left < 0:
                break

            # Get the piece at the current position on the board
            # Get the piece at the current position on the board
            current = self.board[r][left]

            # If the current position is empty,
            if current == 0:
                # If there are pieces that have been skipped and there are no previous pieces that were skipped, break out of the loop
                if passed and not removed:
                    break
                # If there are pieces that have been skipped, add the previous pieces that were skipped to the current move
                elif passed:
                    posible_moves[(r, left)] = removed + passed
                # If there are no pieces that have been skipped, add the previous pieces that were skipped to the current move
                else:
                    posible_moves[(r, left)] = removed

                # If there are previous pieces that were skipped,
                if removed:
                    # If the direction is upward, set the new starting row to the maximum of the current row minus 3, or 0
                    if step == -1:
                        r = max(r - 3, 0)
                    # If the direction is downward, set the new starting row to the minimum of the current row plus 3, or the number of rows on the board
                    else:
                        r = min(r + 3, self.c.ROWS)
                    # Recursively check for valid moves in the left direction starting at the new starting row and moving in the same direction as before
                    posible_moves.update(self.move_left(r + step, r, step, color, left - 1, passed=removed))
                    # Recursively check for valid moves in the right direction starting at the new starting row and moving in the same direction as before
                    posible_moves.update(self.move_right(r + step, r, step, color, left + 1, passed=removed))
                break
            # If the current position is occupied by a piece of the same color as the current piece, break out of the loop
            elif current.color == color:
                break
            # If the current position is occupied by a piece of the opposite color, add the piece to the list of pieces that have been skipped
            else:
                removed = [current]

            # Decrement the left column to move to the next position in the left direction
            left -= 1

            # Return the dictionary of valid moves
        return posible_moves


    #same as move_left function but in right direction
    def move_right(self, start, stop, step, color, right, passed=[]):
        """Recursively traverse the game board in the right direction.

    This method is used to find all of the valid moves for a given piece.

    Args:
        r (int): The row to start traversing from.
        end (int): The row to end traversing at.
        direction (int): The direction in which to traverse (-1 for up, 1 for down).
        color (str): The color of the piece for which to find valid moves.
        c (int): The column to traverse from.

    Returns:
        dict: A dictionary of valid moves that were found during traversal, where the keys
            are tuples representing positions on the game board, and the values are the pieces
            that will be skipped if the move is made.
    """
        # Initialize the dictionary of valid moves
        posible_moves = {}
        # Initialize the list of pieces that have been skipped
        removed = []

        # For each row in the given direction starting at the starting row and ending at the ending row,
        for r in range(start, stop, step):
            # If the current column is equal to or greater than the number of columns on the board, break out of the loop
            if right >= self.c.COLS:
                break

            # Get the piece at the current position on the board
            current = self.board[r][right]

            # If the current position is empty,
            if current == 0:
                # If there are pieces that have been skipped and there are no previous pieces that were skipped, break out of the loop
                if passed and not removed:
                    break
                # If there are pieces that have been skipped, add the previous pieces that were skipped to the current move
                elif passed:
                    posible_moves[(r, right)] = removed + passed
                # If there are no pieces that have been skipped, add the previous pieces that were skipped to the current move
                else:
                    posible_moves[(r, right)] = removed

                # If there are previous pieces that were skipped,
                if removed:
                    # If the direction is upward, set the new starting row to the maximum of the current row minus 3, or 0
                    if step == -1:
                        r = max(r - 3, 0)
                    # If the direction is downward, set the new starting row to the minimum of the current row plus 3, or the number of rows on the board
                    else:
                        r = min(r + 3, self.c.ROWS)
                    # Recursively check for valid moves in the left direction starting at the new starting row and moving in the same direction as before
                    posible_moves.update(self.move_left(r + step, r, step, color, right - 1, passed=removed))
                    # Recursively check for valid moves in the right direction starting at the new starting row and moving in the same direction as before
                    posible_moves.update(self.move_right(r + step, r, step, color, right + 1, passed=removed))
                # If there are no previous pieces that were skipped, break out of the loop
                break
            # If the current position is occupied by a piece of the same color as the current piece, break out of the loop
            elif current.color == color:
                break
            # If the current position is occupied by a piece of the opposite color, add the piece to the list of pieces that have been skipped
            else:
                removed = [current]

            # Decrement the left column to move to the next position in the left direction
            right += 1

            # Return the dictionary of valid moves
        return posible_moves


        
        
