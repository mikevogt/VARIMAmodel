import unittest
from unittest import TestCase

import numpy
import pandas as pd
import numpy as np

from functions import ARIMAmodel
def differecing(numDiff, shareFeature_data):

    data_diff = shareFeature_data.diff(periods=numDiff)
    data_diff = data_diff[numDiff:]
    return data_diff

class TestARIMAmodel(unittest.TestCase):

    def test_ARIMAmodel(self):

        resultTestData =[-5.29 ,  1.684, -2.018, -0.053, -1.096, -0.542, -0.836, -0.68 ,
       -0.763, -0.719, -0.742, -0.73 , -0.737, -0.733, -0.735, -0.734,
       -0.735, -0.734, -0.734, -0.734, -0.734, -0.734, -0.734, -0.734,
       -0.734, -0.734, -0.734, -0.734, -0.734, -0.734, -0.734, -0.734,
       -0.734, -0.734, -0.734, -0.734, -0.734, -0.734, -0.734, -0.734,
       -0.734, -0.734, -0.734, -0.734, -0.734]

        resultTestData = str(numpy.array(resultTestData))
        testData = pd.read_csv('unit_test.csv', ',')
        diffdata = differecing(1, testData)
        result = ARIMAmodel.ARIMAmodel(diffdata,1,1,1,5)
        finalResult = str(np.around(result, decimals=3))

        self.assertEqual(resultTestData, finalResult)
        
if __name__ == '__main__':
    unittest.main()
