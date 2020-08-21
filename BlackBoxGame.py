# Author: Adam Okasha
# Date: 3 August 2020
# Description: Programs has Board, LaserController and 
# BlackBoxGame classes which together form the black box
# game implementation in Python as described here:
# https://en.wikipedia.org/wiki/Black_Box_(game)

from Board import Board
from LaserController import LaserController

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
      self._handle_add_entry_exit_pair((row, col))
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
    """Sets the location a hit on an atom occurred

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
