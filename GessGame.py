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

  def print_board(self):
    print(self._board)


game = BlackBoxGame([(2,5), (7,8), (9,9), (7,7)])
game.print_board()    
