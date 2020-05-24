import unittest
from unittest import TestCase

import numpy
import pandas as pd

from functions import ARmodel

class TestARmodel(unittest.TestCase):

    def differecing(numDiff, shareFeature_data):

        data_diff = shareFeature_data.diff(periods=numDiff)
        data_diff = data_diff[numDiff:]
        return data_diff
        

    def test_ARmodel(self):

        resultTestData = [-14.67057602, -68.04512658,  20.74505794,  -1.86955487,
        -24.3323447 ,  44.0012286 ,  41.11481005, -55.95581696,
        57.77831485,  27.50358171, -44.57683099,  44.40557306,
        -40.59844835, -60.32359577,  14.33915377]
        resultTestData = str(numpy.array(resultTestData))
        
        testData = pd.read_csv('unit_test.csv', ',')
        diffdata = differecing(1,testData)
        result = ARmodel.ARmodel(diffdata)
        finalResult = str(result.to_numpy())

        self.assertEqual(resultTestData, finalResult)
        
if __name__ == '__main__':
    unittest.main()
