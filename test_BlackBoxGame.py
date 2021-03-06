import unittest

from Board import Board
from LaserController import LaserController
from BlackBoxGame import BlackBoxGame

class BlackBoxGameTest(unittest.TestCase):
  """Unit tests for BlackBoxGame class
  """  
  def test_ray_origin(self):
    """Test for valid and invalid ray origin input
    """    
    game = BlackBoxGame([(2,5), (7,8), (9,9), (7,7)])

    valid_origins = []
    for num in range(1,9):
      valid_origins.append((0, num))
      valid_origins.append((9, num))
      valid_origins.append((num, 9))
      valid_origins.append((num, 0))

    valid_test_results = []

    for origin in valid_origins:
      valid_test_results.append(Board.check_valid_ray_origin(game.get_board(),origin[0], origin[1]))

    invalid_inner_origins = []
    for row in range(1,9):
      for col in range(1,9):
        invalid_inner_origins.append((row, col))

    invalid_inner_test_results = []
    for origin in invalid_inner_origins:
      invalid_inner_test_results.append(Board.check_valid_ray_origin(game.get_board(),origin[0], origin[1]))

    invalid_boundaries = [(12,12), (-1, -10), (0,0), (0,9), (9,0), (9,9)]
    invalid_boundaries_results = []
    for origin in invalid_boundaries:
      invalid_boundaries_results.append(Board.check_valid_ray_origin(game.get_board(),origin[0], origin[1]))


    self.assertEqual(len(valid_origins), 32)
    self.assertEqual(len(valid_test_results), 32)
    self.assertNotIn(False, valid_test_results)
    self.assertNotIn(True, invalid_inner_test_results)
    self.assertNotIn(True, invalid_boundaries_results)

  def test_direct_hit(self):
    """Test a direct hit from all directions
    """    
    game = BlackBoxGame([(4,4)])
    north_shot = game.shoot_ray(0,4)
    south_shot = game.shoot_ray(4, 9)
    west_shot = game.shoot_ray(4,0)
    east_shot = game.shoot_ray(4,9)

    self.assertIsNone(north_shot)
    self.assertIsNone(south_shot)
    self.assertIsNone(west_shot)
    self.assertIsNone(east_shot)

  def test_single_reflection(self):
    """Test a reflection from every direction
    """    
    game = BlackBoxGame([(4,4)])
    # naming convention is incoming trajectory relative to 'o'
    north_east_shot = game.shoot_ray(0, 3)
    north_west_shot = game.shoot_ray(0, 5)
    south_east_shot = game.shoot_ray(9, 3)
    south_west_shot = game.shoot_ray(9, 5)
    west_north_shot = game.shoot_ray(3,9)
    west_south_shot = game.shoot_ray(5,9)
    east_north_shot = game.shoot_ray(3,0)
    east_south_shot = game.shoot_ray(5,0)

    self.assertEqual(north_east_shot, (3,0))
    self.assertEqual(north_west_shot, (3,9))
    self.assertEqual(south_east_shot, (5,0))
    self.assertEqual(south_west_shot, (5,9))
    self.assertEqual(west_north_shot, (0,5))
    self.assertEqual(west_south_shot, (9,5))
    self.assertEqual(east_north_shot, (0,3))
    self.assertEqual(east_south_shot, (9,3))

  def test_west_border_reflection(self):
    """Test reflection between west ray origin and next position
    """    
    game = BlackBoxGame([(5,1),(6,1),(7,1)])

    fourth_row_shot = game.shoot_ray(4,0)
    fifth_row_shot = game.shoot_ray(5,0)
    sixth_row_shot = game.shoot_ray(6,0)
    seventh_row_shot = game.shoot_ray(7,0)
    eighth_row_shot = game.shoot_ray(8,0)
    current_points = game.get_score()
    # game.print_board()

    self.assertEqual(fourth_row_shot, (4,0))
    self.assertIsNone(fifth_row_shot)
    self.assertIsNone(sixth_row_shot)
    self.assertIsNone(seventh_row_shot)
    self.assertEqual(eighth_row_shot, (8,0))
    self.assertEqual(current_points, 20)

  def test_east_border_reflection(self):
    """Test reflection between east ray origin and next position
    """
    game = BlackBoxGame([(5,8),(6,8),(7,8)])

    fourth_row_shot = game.shoot_ray(4,9)
    fifth_row_shot = game.shoot_ray(5,9)
    sixth_row_shot = game.shoot_ray(6,9)
    seventh_row_shot = game.shoot_ray(7,9)
    eighth_row_shot = game.shoot_ray(8,9)
    current_points = game.get_score()
    # game.print_board()

    self.assertEqual(fourth_row_shot, (4,9))
    self.assertIsNone(fifth_row_shot)
    self.assertIsNone(sixth_row_shot)
    self.assertIsNone(seventh_row_shot)
    self.assertEqual(eighth_row_shot, (8,9))
    self.assertEqual(current_points, 20)

  
  def test_north_border_reflection(self):
    """Test reflection between north ray origin and next position
    """
    game = BlackBoxGame([(1,5),(1,6),(1,7)])

    fourth_column_shot = game.shoot_ray(0,4)
    fifth_column_shot = game.shoot_ray(0,5)
    sixth_column_shot = game.shoot_ray(0, 6)
    seventh_column_shot = game.shoot_ray(0,7)
    eighth_column_shot = game.shoot_ray(0,8)
    current_points = game.get_score()
    # game.print_board()

    self.assertEqual(fourth_column_shot, (0,4))
    self.assertIsNone(fifth_column_shot)
    self.assertIsNone(sixth_column_shot)
    self.assertIsNone(seventh_column_shot)
    self.assertEqual(eighth_column_shot, (0,8))
    self.assertEqual(current_points, 20)

  def test_south_border_reflection(self):
    """Test reflection between north ray origin and next position
    """
    game = BlackBoxGame([(8,5),(8,6),(8,7)])

    fourth_column_shot = game.shoot_ray(9,4)
    fifth_column_shot = game.shoot_ray(9,5)
    sixth_column_shot = game.shoot_ray(9, 6)
    seventh_column_shot = game.shoot_ray(9,7)
    eighth_column_shot = game.shoot_ray(9,8)
    current_points = game.get_score()
    # game.print_board()

    self.assertEqual(fourth_column_shot, (9,4))
    self.assertIsNone(fifth_column_shot)
    self.assertIsNone(sixth_column_shot)
    self.assertIsNone(seventh_column_shot)
    self.assertEqual(eighth_column_shot, (9,8))
    self.assertEqual(current_points, 20)

  def test_double_deflection(self):
    """Tests a double deflection scenario"""
    game = BlackBoxGame([(6,4), (6,6)])

    shot = game.shoot_ray(0, 5)
    # game.print_board()

    self.assertEqual(shot, (0,5))

  def test_miss(self):
    """Tests a miss scenario"""
    game = BlackBoxGame([(6,4), (6,6)])

    shot = game.shoot_ray(1, 9)
    # game.print_board()

    self.assertEqual(shot, (1, 0))

  def test_detour(self):
    """Tests a detour scenario"""
    game = BlackBoxGame([(3,2), (3,7), (8, 7)])

    north_shot = game.shoot_ray(0, 3)
    # game.print_board()
    east_shot = game.shoot_ray(4, 9)
    # game.print_board()

    self.assertEqual(north_shot, (0, 6))
    self.assertEqual(east_shot, (7, 9))

  def test_twisted_trajectory(self):
    """Tests a more complex twisted laser trajectory"""
    game = BlackBoxGame([(3,2), (3,7), (6,4), (8, 7)])

    west_shot = game.shoot_ray(5, 0)
    # game.print_board()

    self.assertEqual(west_shot, (9,5))

  def test_deflection_and_reflection(self):
    """Tests a deflection then a reflection"""
    game = BlackBoxGame([(2,6), (7,6), (7, 8)])

    east_shot = game.shoot_ray(3, 9)
    # game.print_board()

    self.assertEqual(east_shot,(3,9))

  def test_deflect_and_hit(self):
    """Tests a deflection which then causes a hit"""
    game = BlackBoxGame([(2,6), (3,3), (7,6)])

    west_shot = game.shoot_ray(6,0)
    # game.print_board()

    self.assertIsNone(west_shot)


  def test_get_score(self):
    """Tests getting score after guessing and shooting rays"""
    game = BlackBoxGame([(2,6), (3,3), (7,6)])

    score = game.get_score()

    self.assertEqual(score, 25)

    game.guess_atom(2,7)
    score_after_guess_one = game.get_score()

    self.assertEqual(score_after_guess_one, 20)
    game.guess_atom(2,7)
    score_after_same_guess = game.get_score()

    self.assertEqual(score_after_same_guess, 20)

    game.shoot_ray(8,9)
    # game.print_board()
    score_after_ray_shot = game.get_score()

    game.shoot_ray(8,9)
    score_after_repeat_shot = game.get_score()

    self.assertEqual(score_after_ray_shot, 18)
    self.assertEqual(score_after_repeat_shot, 18)

  def test_one_hit_one_miss(self):
    """Tests a hit and a miss and the resulting score"""
    game = BlackBoxGame([(3,3)])

    hit = game.shoot_ray(3,0)
    game.shoot_ray(3,0)
    # game.print_board()
    miss = game.shoot_ray(1,0)
    game.shoot_ray(1,0)
    # game.print_board()

    score = game.get_score()

    self.assertIsNone(hit)
    self.assertEqual(miss, (1, 9))
    self.assertEqual(score, 22)

  def test_atoms_left(self):
    """Tests the number of atoms left after correct and incorrect guesses"""
    game = BlackBoxGame([(2,6), (3,3), (7,6)])

    game.guess_atom(2,6) # correct
    game.guess_atom(3,3) # correct
    game.guess_atom(1,2) # incorrect
    
    atoms_left = game.atoms_left()

    self.assertEqual(atoms_left, 1)

  def test_insufficient_points_for_guess(self):
    """Tests that the correct message is displayed when there are insufficient points for a guess"""
    game = BlackBoxGame([(2,6)])

    game.guess_atom(1,1)
    game.guess_atom(1,2)
    game.guess_atom(1,3)
    game.guess_atom(1,4)
    game.guess_atom(1,5)
    message = game.guess_atom(1,6)

    self.assertEqual(message, "Not enough points to make a guess!")

  def test_insufficient_points_for_shot(self):
    """Tests that the correct message is displayed when there are insufficient points for a shot"""
    game = BlackBoxGame([(8,8)])
    game.guess_atom(1,1)
    game.guess_atom(2,1)
    game.guess_atom(1,2)
    game.guess_atom(1,3)
    game.guess_atom(1,4)
    game.guess_atom(1,5)


    self.assertEqual(game.get_score(), 0)
    message = game.shoot_ray(8,0)
    self.assertEqual(message, "Not enough points to shoot from (8, 0)!")


if __name__ == '__main__':
  unittest.main()
