import unittest
from unittest import TestCase

import numpy
import pandas as pd

from functions import ARIMAmodel
def differecing(numDiff, shareFeature_data):

    data_diff = shareFeature_data.diff(periods=numDiff)
    data_diff = data_diff[numDiff:]
    return data_diff

class TestARIMAmodel(unittest.TestCase):

    def test_ARIMAmodel():

        resultTestData =[-5.28963772,  1.6839004,  -2.01805453, -0.05284403, -1.09609074, -0.54227541,
         -0.83627243, -0.68020191, -0.76305311, -0.71907093, -0.7424192,  -0.7300246,
         -0.73660437, -0.73311145, -0.73496569, -0.73398135, -0.73450389, -0.7342265,
         -0.73437376, -0.73429558, -0.73433708, -0.73431505, -0.73432675, -0.73432054,
         -0.73432383, -0.73432208, -0.73432301, -0.73432252, -0.73432278, -0.73432264,
         -0.73432272, -0.73432268, -0.7343227,  -0.73432269, -0.73432269, -0.73432269,
         -0.73432269, -0.73432269, -0.73432269, -0.73432269, -0.73432269, -0.73432269,
         -0.73432269, -0.73432269, -0.73432269]

        resultTestData = str(numpy.array(resultTestData))
        testData = pd.read_csv('unit_test.csv', ',')
        diffdata = differecing(1, testData)
        result = ARIMAmodel.ARIMAmodel(diffdata,1,1,1,5)
        finalResult = str(result)

        self.assertEqual(resultTestData, finalResult)
        
if __name__ == '__main__':
    unittest.main()