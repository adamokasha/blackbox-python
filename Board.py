
class Board:
  """Board class builds and returns the board used for the BlackBoxGame class. Includes
  methods for validating input and printing the board.
  """  
  def __init__(self, length, atom_locations):
    board = []
    for x in range(0, length):
      row = []
      for y in range(0, length):
        if (x,y) in atom_locations:
          row.append('o')
        else:
          row.append('')
      board.append(row)
    self._board = board

  def get_board(self):
    """Returns a copy of the board

    Returns:
        list: the board
    """    
    return list(self._board)

  def get_atom_locations(self):
    """Returns a copy of set of atom locations

    Returns:
        set: set of tuples indicating atom locations
    """    
    return set(self._atom_locations)

  @staticmethod
  def check_valid_ray_origin(board, row, col):
    """Checks if the ray is being shot from a valid position

    Args:
        board (Board): board built by an instanceo f a Board class
        row (int): the row where the shot is placed
        col (int): the column where the shot is placed

    Returns:
        boolean: whether or not the position is a valid ray shot origin
    """    
    if (row == 0 or row == len(board) - 1) and col in range(1,len(board) - 1): # top and bottom
      return True
    if (col == 0 or col == len(board) - 1) and row in range(1,len(board) - 1): # sides
      return True
    return False

  @staticmethod
  def check_within_board(row, col, side_length):
    """Checks if a position falls within the inner boundaries of the board (excluding ray shot origins)

    Args:
        row (int): indicates the row
        col (int): indicates the column
        side_length (int): the length of a side of the board we are validating for (excluding ray origin). for 8x8 board, the arg would be 8.

    Returns:
        boolean: whether the position falls within the board (excluding ray origin).
    """    
    if 1 <= row <= side_length and 1 <= col <= side_length:
      return True
    return False

  @staticmethod
  def print_board(board, trajectory_coords):
    """Prints the board to the console.

    Args:
        board (Board): a board built by the Board class
        trajectory_coords (set): set of tuples indicating the trajectory the ray took
    """    
    for row in range(1, len(board) - 1):
      pretty_row = ""
      for col in range(1, len(board) - 1):
        if board[row][col] == 'o':
          pretty_row += ' o '
        elif (row, col) in trajectory_coords:
          pretty_row += " x "
        else:
          pretty_row += " _ "
      print(pretty_row)

