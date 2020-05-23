import unittest
from functions import rootMeanSquareError

class TestRMSE(unittest.TestCase):

    def test_RMSE(self):
        """test RMSE on  two lists of floats"""
        forecastValues = [0.0, 0.5, 0.0, 0.5, 0.0, 0.4, 0.9]
        actualValues = [0.2, 0.4, 0.1, 0.6, 0.2, 0.1, 0.6]
        result = rootMeanSquareError(self, forecastValues, actualValues)
        self.assertEqual(result,  0.20354009783964297)

if __name__ == '__main__':
    unittest.main()
