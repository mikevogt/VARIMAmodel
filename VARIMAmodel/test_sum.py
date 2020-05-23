import unittest
from functions import my_sum

class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(my_sum.sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(my_sum.sum((1, 2, 3)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()
