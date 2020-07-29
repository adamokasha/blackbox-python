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


if __name__ == '__main__':
  unittest.main()
