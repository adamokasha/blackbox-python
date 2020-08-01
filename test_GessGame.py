import unittest
from GessGame import BlackBoxGame

class BlackBoxGameTest(unittest.TestCase):

  def test_ray_origin(self):
    game = BlackBoxGame([(2,5), (7,8), (9,9), (7,7)])

    valid_origins = []
    for num in range(1,9):
      valid_origins.append((0, num))
      valid_origins.append((9, num))
      valid_origins.append((num, 9))
      valid_origins.append((num, 0))

    valid_test_results = []

    for origin in valid_origins:
      valid_test_results.append(game._check_valid_ray_origin(origin[0], origin[1]))

    invalid_inner_origins = []
    for row in range(1,9):
      for col in range(1,9):
        invalid_inner_origins.append((row, col))

    invalid_inner_test_results = []
    for origin in invalid_inner_origins:
      invalid_inner_test_results.append(game._check_valid_ray_origin(origin[0], origin[1]))

    invalid_boundaries = [(12,12), (-1, -10), (0,0), (0,9), (9,0), (9,9)]
    invalid_boundaries_results = []
    for origin in invalid_boundaries:
      invalid_boundaries_results.append(game._check_valid_ray_origin(origin[0], origin[1]))


    self.assertEqual(len(valid_origins), 32)
    self.assertEqual(len(valid_test_results), 32)
    self.assertNotIn(False, valid_test_results)
    self.assertNotIn(True, invalid_inner_test_results)
    self.assertNotIn(True, invalid_boundaries_results)

  def test_direct_hit(self):
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


if __name__ == '__main__':
  unittest.main()
