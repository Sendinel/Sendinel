import unittest

class SimpleTest(unittest.TestCase):
  def test_always_true(self):
    pass
    
  def test_always_false(self):
    unittest.TestCase.assertTrue(self,True)