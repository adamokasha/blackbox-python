class Board:

  def __init__(self, length, atom_locations):
    board = []
    atom_locations_set = set() 
    for x in range(0, length):
      row = []
      for y in range(0, length):
        if (x,y) in atom_locations:
          row.append('o')
          atom_locations_set.add((x,y))
        else:
          row.append('')
      board.append(row)
    self._board = board
    self._atom_locations = atom_locations_set

  def get_board(self):
    return list(self._board)

  def get_atom_locations(self):
    return set(self._atom_locations)

  @staticmethod
  def check_within_board(row, col, side_length):
    if 1 <= row <= side_length and 1 <= col <= side_length:
      return True
    return False

  @staticmethod
  def print_board(board, trajectory_coords):
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

  def __init__(self):
    self._trajectory = set()

  def add_trajectory_coord(self, coord):
    self._trajectory.add(coord)

  def get_trajectory(self):
    return self._trajectory

  def check_border_reflection(self, board, get_current_direction, get_current_pos, set_direction):
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
    if origin_row == 0:
      return 'south'
    elif origin_row == 9:
      return 'north'
    elif origin_col == 0:
      return 'east'
    else:
      return 'west'

  def _traverse(self, board, get_current_direction, get_current_pos, set_current_pos, set_hit_location):
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
    """[summary]

    Returns:
        tuple: the items at (north_west, north_east, next_pos) 
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
    """[summary]

    Returns:
        tuple: the items at (south_west, south_east, next_pos)
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
    """[summary]

    Returns:
        tuple: the items at (north_east, south_east, next_pos)
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
    """[summary]

    Returns:
        tuple: the items at (north_west, south_west, next_pos)
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


  def __init__(self, atom_locations):
    board = Board(10, atom_locations)
    self._board = board.get_board()
    self._atom_locations = board.get_atom_locations()
    self._laser = LaserController()
    self._points = 25
    self._guesses = set()
    self._entry_positions = set()
    self._exit_positions = set()
    self._current_pos = None # (r, c)
    self._current_direction = None
    self._laser_trajectory = set()
    self._hit_location = None

  def _check_valid_ray_origin(self, row, col):
    if (row == 0 or row == 9) and col in range(1,9): # top and bottom
      return True
    if (col == 0 or col == 9) and row in range(1,9): # sides
      return True
    return False

  def shoot_ray(self, row, col):
    self._hit_location = None
    self._laser.get_trajectory().clear()

    if not self._check_valid_ray_origin(row, col):
      return False
    if (row, col) not in self._entry_positions:
      self._entry_positions.add((row,col))
      self._points -= 1

    self._current_direction = self._laser.set_initial_direction(row, col)
    self._current_pos = (row, col)

    if self._laser.check_border_reflection(self._board, self.get_current_direction, self.get_current_pos, self.set_current_direction): # check for initial reflection
      return self._current_pos

    self._laser._traverse(self._board, self.get_current_direction, self.get_current_pos, self.set_current_pos, self.set_hit_location)
    self._laser.get_trajectory().add(self._current_pos)
    while not self._check_valid_ray_origin(self._current_pos[0],self._current_pos[1]) and not self._hit_location:
      self._laser.get_trajectory().add(self._current_pos)
      self._laser.get_scan_method(self.get_current_direction)(self._board, self.get_current_pos, self.set_current_direction) # return correct scan method and invoke
      self._laser._traverse(self._board, self.get_current_direction, self.get_current_pos, self.set_current_pos, self.set_hit_location)
    if self._hit_location:
      return None
    exit_pos = self.get_current_pos()
    if exit_pos not in self._exit_positions:
      self._exit_positions.add(exit_pos)
      self._points -= 1
    return self._current_pos

  def get_current_direction(self):
    return self._current_direction

  def set_current_direction(self, direction):
    self._current_direction = direction

  def get_current_pos(self):
    return self._current_pos

  def set_current_pos(self, new_pos):
    self._current_pos = new_pos

  def guess_atom(self, row, col):
    if (row, col) in self._guesses:
      return self._board[row][col] == 'o'
    if self._board[row][col] == 'o':
      self._guesses.add((row, col))
      return True
    else:
      self._guesses.add((row, col))
      self._points -= 5
      return False

  def get_score(self):
    return self._points

  def atoms_left(self):
    return len(self._atom_locations) - len(self._atom_locations.intersection(self._guesses)) 


  def set_hit_location(self, location):
    self._hit_location = location

  def _check_within_board(self, row, col):
    if 1 <= row <= 8 and 1 <= col <= 8:
      return True
    return False
      
  def register_entry_position(self, row, col):
    self._entry_positions.add((row, col))

  def register_exit_position(self, row, col):
    self._exit_positions.add((row, col))

  def print_board(self):
    Board.print_board(self._board, self._laser.get_trajectory())


# game = BlackBoxGame([(7,7)])
# game = BlackBoxGame([(5,3),(6,3),(7,3)])
# game = BlackBoxGame([(7,6),(7,7),(7,8)])
# game = BlackBoxGame([(2,6),(7,6), (7, 8)])
# print(game.shoot_ray(3,9))
# game.print_board()    
# print(game.shoot_ray(4,9))
# game.print_board()    
