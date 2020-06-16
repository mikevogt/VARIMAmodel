import unittest
from unittest import TestCase

import numpy
import pandas as pd
import numpy as np

from functions import MAmodel


def differecing(numDiff, shareFeature_data):
    data_diff = shareFeature_data.diff(periods=numDiff)
    data_diff = data_diff[numDiff:]
    return data_diff


class TestMAmodel(unittest.TestCase):

    def test_MAmodel(self):
        resultTestData = [-9.31472891, -32.23434828, 3.98038566, -19.73325264, -16.2288928,32.92674818, 21.60659107, -31.17029119, 40.60667671, -3.08135266,-36.39569186, 42.79855021, -40.67890097, -33.89217772, 19.28623018]
        resultTestData = str(np.around(numpy.array(resultTestData), decimals=3))
        testData = pd.read_csv('unit_test.csv', ',')
        diffdata = differecing(1, testData)
        result = MAmodel.MAmodel(1, diffdata)
        finalResult = str(np.around(result.to_numpy(), decimals=3))
        self.assertEqual(resultTestData, finalResult)   

if __name__ == '__main__':
    unittest.main()
