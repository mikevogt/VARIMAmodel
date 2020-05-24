import unittest
from unittest import TestCase
import pandas as pd
from functions import ifStationary

class TestifStationary(unittest.TestCase):

    def test_ifStationary(self):
        testData =  pd.read_csv('unit_test.csv',',')
        #a = ifStationary()
        result = ifStationary.ifStationary(testData)
        self.assertEqual(result, 0)
        
if __name__ == '__main__':
    unittest.main()
