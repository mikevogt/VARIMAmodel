import unittest
from unittest import TestCase
import pandas as pd
from functions import Parametres   

class TestSum(unittest.TestCase):
    
    def test_Parametres(self):
        testData = pd.read_csv('unit_test.csv', ',')
        #c = modelFunctions()
        result = Parametres.Parametres(testData)
        resultString = str(result)
        self.assertEqual(resultString, "[0, 0, 1]")
 
if __name__ == '__main__':
    unittest.main()