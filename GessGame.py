class BlackBoxGame:

  def __init__(self, atom_locations):
    board = []
    for x in range(0,10):
      row = []
      for y in range(0, 10):
        if (x,y) in atom_locations:
          row.append('o')
        else:
          row.append('')
      board.append(row)

    self._board = board
    self.points = 25
    self._guesses = []

  def _check_valid_ray_origin(self, row, col):
    if (row == 0 or row == 9) and col in range(1,9): # top and bottom
      return True
    if (col == 0 or col == 9) and row in range(1,9): # sides
      return True
    return False

  def shoot_ray(self, row, col):
    if not self._check_valid_ray_origin(row, col):
      return False


  def print_board(self):
    print(self._board)


# game = BlackBoxGame([(2,5), (7,8), (9,9), (7,7)])
# game.print_board()    
# print(game.shoot_ray(9,2))

