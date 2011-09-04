import unittest
import coalitionsolver

class TestCoalitionSolver(unittest.TestCase):

  def setUp(self):
    return
      
  def test_4_3_2(self):
    coalition = coalitionsolver.Coalition([4,3,2])
    coalition.get_minimum_integer_solution()
    
    self.assertEqual(coalition._pulp_list, [(0,1),(0,2),(1,2)])
    self.assertEqual(coalition._tie_list, [])
    self.assertEqual(coalition._rank, [6,6,6])
    self.assertEqual(coalition._lp_vars[0].varValue, 1)
    self.assertEqual(coalition._lp_vars[1].varValue, 1)
    self.assertEqual(coalition._lp_vars[2].varValue, 1)
    
  def test_4_3_3_2_2(self):
    coalition = coalitionsolver.Coalition([4,3,3,2,2])
    coalition.get_minimum_integer_solution()
    
    self.assertEqual(coalition._pulp_list, [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4), (0, 3, 4), (1, 2, 3), (1, 2, 4)])
    self.assertEqual(coalition._tie_list, [(0, 1), (0, 2), (1, 3, 4), (2, 3, 4)])
    self.assertEqual(coalition._rank, [48, 40, 40, 32, 32])
    self.assertEqual(coalition._lp_vars[0].varValue, 4)
    self.assertEqual(coalition._lp_vars[1].varValue, 3)
    self.assertEqual(coalition._lp_vars[2].varValue, 3)
    self.assertEqual(coalition._lp_vars[3].varValue, 2)
    self.assertEqual(coalition._lp_vars[4].varValue, 2)
      
if __name__ == '__main__':
  unittest.main()
