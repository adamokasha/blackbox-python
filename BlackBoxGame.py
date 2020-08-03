# Author: Adam Okasha
# Date: 3 August 2020
# Description: Programs has Board, LaserController and 
# BlackBoxGame classes which together form the black box
# game implementation in Python as described here:
# https://en.wikipedia.org/wiki/Black_Box_(game)


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


class LaserController:
  """LaserController class contains trajectory data member that indicates the laser's trajectory. Contains methods
  that scan the positions ahead of the laser's tip, change direction based on the orbs found by scanning ahead and
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
        set_hit_location (function): passed from BlackBoxGame that sets the hit location (laser hitting orb)
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
    """Scans the positions north of the ray, sets the direction based on orbs ahead and returns
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
    """Scans the positions south of the ray, sets the direction based on orbs ahead and returns
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
    """Scans the positions east of the ray, sets the direction based on orbs ahead and returns
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
    """Scans the positions west of the ray, sets the direction based on orbs ahead and returns
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

class BlackBoxGame:
  """BlackBoxGame class has private data members to hold and update game state and calls
  methods that call other class instance methods (LaserController and Board) to perform functionality
  related to traversal and building the board.
  """  
  def __init__(self, atom_locations):
    self._board = Board(10, atom_locations).get_board()
    self._atom_locations = set(atom_locations)
    self._laser = LaserController()
    self._points = 25
    self._guesses = set()
    self._entry_exit_pairs = set()
    self._current_pos = None # (r, c)
    self._current_direction = None
    self._hit_location = None

  def shoot_ray(self, row, col):
    """Shoots a laser ray from a valid origin (borders)

    Args:
        row (int): the row from where the shot originates
        col (int): the column from where the row originates

    Returns:
        (tuple | boolean | None | string): 
        - If the row and column are invalid, False is returned. 
        - If a hit occurs, None is returned. 
        - If an exit occurs, a tuple (row, col) indicating the exit position is returned.
        - If there are insufficient points to shoot the ray a message is returned indicating so.
    """    
    self._reset_previous()
    if not self._in_ray_origin(row, col):
      return False

    self._current_direction = self._set_initial_direction(row, col)
    self._current_pos = (row, col)

    if self._check_border_reflection(): # check for initial reflection
      return self._current_pos

    self._traverse()
    self._add_laser_trajectory()
    while not self._in_ray_origin(self._current_pos[0],self._current_pos[1]) and not self._hit_location:
      self._add_laser_trajectory()
      self._scan_ahead() # returns correct scan method and invokes
      self._traverse()
    if self._hit_location:
      if not self._has_enough_points((row, col), None):
        return f"Not enough points to shoot from {str((row,col))}!"
      self._handle_add_entry_exit_pair((row, col))
      return None
    if not self._has_enough_points((row, col), self.get_current_pos()): # args: entry, exit
      return f"Not enough points to shoot from {str((row,col))}!"
    self._handle_add_entry_exit_pair((row, col), self.get_current_pos())
    return self._current_pos

  def get_board(self):
    """Gets the board

    Returns:
        Board: a board built by the Board instance
    """    
    return self._board

  def get_current_direction(self):
    """Gets the current direction the ray is traversing

    Returns:
        string: 'south' | 'north' | 'east' | 'west'
    """    
    return self._current_direction

  def set_current_direction(self, direction):
    """Sets the current direction the ray is traversing

    Args:
        direction (string): 'south' | 'north' | 'east' | 'west'
    """    
    self._current_direction = direction

  def get_current_pos(self):
    """Gets the ray tip's current position

    Returns:
        tuple: (row, col) indicating the position
    """    
    return self._current_pos

  def set_current_pos(self, new_pos):
    """Sets the current position of the ray tip

    Args:
        new_pos (tuple): (row, col) indicating the new position 
    """    
    self._current_pos = new_pos

  def get_score(self):
    """Gets the current points count

    Returns:
        int: the current points count
    """    
    return self._points

  def atoms_left(self):
    """The count of atoms not guessed correctly

    Returns:
        int: number of atoms not guessed correctly
    """    
    return len(self._atom_locations) - len(self._atom_locations.intersection(self._guesses)) 

  def set_hit_location(self, location):
    """Sets the location a hit on an orb occurred

    Args:
        location (tuple): (row, col) tuple indicating the position
    """    
    self._hit_location = location

  def guess_atom(self, row, col):
    """Method to guess the position of an atom

    Args:
        row (int): row of the guess
        col (int): column of the guess

    Returns:
        (boolean | string): returns True if correct, False if not and a message if points not sufficient to make a guess.
    """    
    if self._points < 5:
      return "Not enough points to make a guess!"
    if (row, col) in self._guesses:
      return self._board[row][col] == 'o'
    if self._board[row][col] == 'o':
      self._guesses.add((row, col))
      return True
    else:
      self._guesses.add((row, col))
      self._points -= 5
      return False

  def _reset_previous(self):
    """Resets the hit location and laser trajectory so that the next shot can be printed without previous data
    """    
    self._hit_location = None
    self._laser.get_trajectory().clear()

  def _set_initial_direction(self, row, col):
    """Wrapper function that sets the initial direction by calling the method on the LaserController instance.

    Args:
        row (int): the current row
        col (int): the current column

    Returns:
        string: 'south' | 'north' | 'east' | 'west' 
    """    
    return self._laser.set_initial_direction(row, col)

  def _has_enough_points(self, entry_pos, exit_pos):
    """Checks if plyer has enough points to shoot laser

    Args:
        entry_pos (tuple): the entry position of the ray
        exit_pos (tuple): the exit position of the ray

    Returns:
        boolean: True if there are enough points, false otherwise.
    """    
    points_required = 0
    if entry_pos not in self._entry_exit_pairs:
      points_required += 1
    if exit_pos not in self._entry_exit_pairs:
      points_required += 1
    return points_required < self._points

  def _handle_add_entry_exit_pair(self, entry_pos, exit_pos = None):
    """Adds entry/exit coords to the set tracking entry/exits if needed and updates point accordingly.

    Args:
        entry_pos (tuple): (row, col) indicating entry position
        exit_pos (tuple, optional): (row, col) indicating exit position. Defaults to None.
    """    
    if entry_pos not in self._entry_exit_pairs:
      self._points -= 1
      self._entry_exit_pairs.add(entry_pos)
    if exit_pos and exit_pos not in self._entry_exit_pairs:
      self._points -= 1
      self._entry_exit_pairs.add(exit_pos)

  def _in_ray_origin(self, row, col):
    """Calls Board static method 'check_valid_ray_origin'. Checks if the starting ray position is valid.
    Args:
        row (int): the laser's origin row
        col (int): the laser's origin column

    Returns:
        boolean: whether or not the position is a valid ray origin
    """    
    return Board.check_valid_ray_origin(self._board, row, col)

  def _check_border_reflection(self):
    """Wrapper function that calls LaserController instance method 'check_border_reflection' with bound arguments. 
    Checks if there is a potential deflection between the ray starting position and the next position.

    Returns:
        boolean: return True if reflection will occur, False if not.
    """    
    return self._laser.check_border_reflection(self._board, self.get_current_direction, self.get_current_pos, self.set_current_direction)
      
  def _traverse(self):
    """Wrapper function that calls LaserController instance method 'traverse' with bound arguments. Moves the laser ray one place in the proper direction.
    """    
    self._laser.traverse(self._board, self.get_current_direction, self.get_current_pos, self.set_current_pos, self.set_hit_location)

  def _scan_ahead(self):
    """Wrapper function that calls LaserController instance method 'get_scan_method' with bound arguments. Returns the proper scan method
    based on the laser's current direction.
    """    
    self._laser.get_scan_method(self.get_current_direction)(self._board, self.get_current_pos, self.set_current_direction)

  def _add_laser_trajectory(self):
    """Wrapper function that calls LaserController instance method 'get_trajectory' and adds the current position.
    """ 
    self._laser.get_trajectory().add(self._current_pos)

  def print_board(self):
    """Calls Board static method 'print_board' which will print the board.
    """    
    Board.print_board(self._board, self._laser.get_trajectory())


# game = BlackBoxGame([(7,7)])
# game = BlackBoxGame([(5,3),(6,3),(7,3)])
# game = BlackBoxGame([(7,6),(7,7),(7,8)])
# game = BlackBoxGame([(2,6),(7,6), (7, 8)])
# print(game.shoot_ray(3,9))
# game.print_board()    
# print(game.shoot_ray(4,9))
# game.print_board()    
