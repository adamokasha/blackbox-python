from Board import Board

class LaserController:
  """LaserController class contains trajectory data member that indicates the laser's trajectory. Contains methods
  that scan the positions ahead of the laser's tip, change direction based on the atoms found by scanning ahead and
  performing traversal based on computed direction. 
  """  
  def __init__(self):
    self._trajectory = set()

  def add_trajectory_coord(self, coord):
    """Adds a coord to the trajectory data member

    Args:
        coord (set): (row, col) tuple set indicating the movement a ray made
    """    
    self._trajectory.add(coord)

  def get_trajectory(self):
    """Gets the trajectory set

    Returns:
        set: the trajectory the laser made for a particular shot
    """    
    return self._trajectory

  def check_border_reflection(self, board, get_current_direction, get_current_pos, set_direction):
    """Checks if there is a reflection between the ray's starting point and the next position that
    the ray should travel to

    Args:
        board (Board): board built by the Board class
        get_current_direction (function): passed in by BlackBoxGame that gets the current direction of the ray
        get_current_pos (function): passed in by BlackBoxGame that gets the current position of the ray
        set_direction (function): passed in by BlackBoxGame that sets the current direction of the ray

    Returns:
        boolean: whether there is a reflection between the ray origin and the next position
    """    
    if get_current_direction() == 'east':
      north_east, south_east, east_pos = self._scan_east_and_compute_direction(board, get_current_pos, set_direction)
      if (north_east == 'o' or south_east == 'o') and east_pos != 'o':
        return True

    if get_current_direction() == 'west':
      north_west, south_west, west = self._scan_west_and_compute_direction(board, get_current_pos, set_direction)
      if (north_west == 'o' or south_west == 'o') and west != 'o':
        return True

    if get_current_direction() == 'north':
      north_west, north_east, north = self._scan_north_and_compute_direction(board, get_current_pos, set_direction)
      if (north_west == 'o' or north_east == 'o') and north != 'o':
        return True

    if get_current_direction() == 'south':
      south_west, south_east, south = self._scan_south_and_compute_direction(board, get_current_pos, set_direction)
      if (south_west == 'o' or south_east == 'o') and south != 'o':
        return True
    
  def set_initial_direction(self, origin_row, origin_col):
    """Sets the initial direction of the ray

    Args:
        origin_row (int): the row where the laser was initially placed
        origin_col (int): the column where the laser was initially placed

    Returns:
        string: 'south' | 'north' | 'east' | 'west' 
    """    
    if origin_row == 0:
      return 'south'
    elif origin_row == 9:
      return 'north'
    elif origin_col == 0:
      return 'east'
    else:
      return 'west'

  def traverse(self, board, get_current_direction, get_current_pos, set_current_pos, set_hit_location):
    """Moves the laser ray one place in the proper direction

    Args:
        board (Board): the board created by the Board instance
        get_current_direction (function): passed from BlackBoxGame that gets the current direction
        get_current_pos (function): passed from BlackBoxGame that gets the current position as (row, col)
        set_current_pos (function): passed from BlackBoxGame that sets the current pos (row, col)
        set_hit_location (function): passed from BlackBoxGame that sets the hit location (laser hitting atom)
    """    
    direction = get_current_direction()
    current_row = get_current_pos()[0]
    current_col = get_current_pos()[1]

    if direction == 'north':
      set_current_pos((current_row - 1, current_col))
    elif direction == 'south':
      set_current_pos((current_row + 1, current_col))
    elif direction == 'east':
      set_current_pos((current_row, current_col + 1))
    else: # west
      set_current_pos((current_row, current_col - 1))
    # hit registered
    new_row = get_current_pos()[0]
    new_col = get_current_pos()[1]
    if board[new_row][new_col] == 'o':
      set_hit_location(get_current_pos)

  def get_scan_method(self, get_current_direction):
    """Gets the appropriate scan ahead method from current direction

    Args:
        get_current_direction (function): passed from BlackBoxGame that gets the current direction the ray is travelling in

    Returns:
        function: the function that scans ahead relative to the direction the ray is traversing in
    """    
    direction = get_current_direction()
    if direction == 'north':
      return self._scan_north_and_compute_direction
    elif direction == 'south':
      return self._scan_south_and_compute_direction
    elif direction == 'east':
      return self._scan_east_and_compute_direction
    else: # west
      return self._scan_west_and_compute_direction


  def _scan_north_and_compute_direction(self, board, get_current_pos, set_direction):
    """Scans the positions north of the ray, sets the direction based on atoms ahead and returns
    a tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)

    Args:
        board (Board): the board created by the Board instance
        get_current_pos (function): passed from BlackBoxGame that gets the current position as (row, col)
        set_direction (function): passed in by BlackBoxGame that sets the current direction of the ray

    Returns:
        tuple: tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)
    """ 
    current_row = get_current_pos()[0]
    current_col = get_current_pos()[1]
    north_west = None
    north_east = None
    next_pos = None
    
    if Board.check_within_board(current_row - 1, current_col - 1, len(board) - 2):
      north_west = board[current_row - 1][current_col - 1]

    if Board.check_within_board(current_row - 1, current_col + 1, len(board) - 2):
      north_east = board[current_row - 1][current_col + 1]

    if Board.check_within_board(current_row - 1, current_col, len(board) - 2):
      next_pos = board[current_row - 1][current_col]

    if north_west == 'o' and north_east == 'o' and next_pos != 'o':
      set_direction('south')

    if north_west == 'o' and (north_east == '' or not north_east) and next_pos != 'o':
      set_direction('east')
    
    if north_east == 'o' and (north_west == '' or not north_west) and next_pos != 'o':
      set_direction('west')
    
    return (north_west, north_east, next_pos)

  def _scan_south_and_compute_direction(self, board, get_current_pos, set_direction):
    """Scans the positions south of the ray, sets the direction based on atoms ahead and returns
    a tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)

    Args:
        board (Board): the board created by the Board instance
        get_current_pos (function): passed from BlackBoxGame that gets the current position as (row, col)
        set_direction (function): passed in by BlackBoxGame that sets the current direction of the ray

    Returns:
        tuple: tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)
    """    
    current_row = get_current_pos()[0]
    current_col = get_current_pos()[1]
    south_west = None
    south_east = None
    next_pos = None
    
    if Board.check_within_board(current_row + 1, current_col - 1, len(board) - 2):
      south_west = board[current_row + 1][current_col - 1]

    if Board.check_within_board(current_row + 1, current_col + 1, len(board) - 2):
      south_east = board[current_row + 1][current_col + 1]

    if Board.check_within_board(current_row + 1,current_col, len(board) - 2):
      next_pos = board[current_row + 1][current_col] 

    if south_west == 'o' and south_east == 'o' and next_pos != 'o':
      set_direction('north')

    if south_west == 'o' and (south_east == '' or not south_east) and next_pos != 'o':
      set_direction('east')
    
    if south_east == 'o' and (south_west == '' or not south_west) and next_pos != 'o':
      set_direction('west')
    
    return (south_west, south_east, next_pos)

  def _scan_east_and_compute_direction(self, board, get_current_pos, set_direction):
    """Scans the positions east of the ray, sets the direction based on atoms ahead and returns
    a tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)

    Args:
        board (Board): the board created by the Board instance
        get_current_pos (function): passed from BlackBoxGame that gets the current position as (row, col)
        set_direction (function): passed in by BlackBoxGame that sets the current direction of the ray

    Returns:
        tuple: tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)
    """     
    current_row = get_current_pos()[0]
    current_col = get_current_pos()[1]
    north_east = None
    south_east = None
    next_pos = None
    
    if Board.check_within_board(current_row - 1, current_col + 1, len(board) - 2):
      north_east = board[current_row - 1][current_col + 1]

    if Board.check_within_board(current_row + 1, current_col + 1, len(board) - 2):
      south_east = board[current_row + 1][current_col + 1]

    if Board.check_within_board(current_row, current_col + 1, len(board) - 2):
      next_pos = board[current_row][current_col + 1]
    
    if north_east == 'o' and south_east == 'o' and next_pos != 'o':
      set_direction('west')

    if north_east == 'o' and (south_east == '' or not south_east) and next_pos != 'o':
      set_direction('south')
    
    if south_east == 'o' and (north_east == '' or not north_east) and next_pos != 'o':
      set_direction('north')

    return (north_east, south_east, next_pos)

  def _scan_west_and_compute_direction(self, board, get_current_pos, set_direction):
    """Scans the positions west of the ray, sets the direction based on atoms ahead and returns
    a tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)

    Args:
        board (Board): the board created by the Board instance
        get_current_pos (function): passed from BlackBoxGame that gets the current position as (row, col)
        set_direction (function): passed in by BlackBoxGame that sets the current direction of the ray

    Returns:
        tuple: tuple showing what was found ahead ('o' or empty or None, None being outside of the inner board)
    """     
    current_row = get_current_pos()[0]
    current_col = get_current_pos()[1]

    north_west = None
    south_west = None
    next_pos = None
    
    if Board.check_within_board(current_row - 1, current_col - 1, len(board) - 2):
      north_west = board[current_row - 1][current_col - 1]

    if Board.check_within_board(current_row + 1, current_col - 1, len(board) - 2):
      south_west = board[current_row + 1][current_col - 1]
    
    if Board.check_within_board(current_row, current_col - 1, len(board) - 2):
      next_pos = board[current_row][current_col - 1]

    if north_west == 'o' and south_west == 'o' and next_pos != 'o':
      set_direction('east')

    if north_west == 'o' and (south_west == '' or not south_west) and next_pos != 'o':
      set_direction('south')
    
    if south_west == 'o' and (north_west == '' or not north_west) and next_pos != 'o':
      set_direction('north')
    
    return (north_west, south_west, next_pos)
