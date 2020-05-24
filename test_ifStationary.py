import unittest
from unittest import TestCase
import pandas as pd

from functions import ifStationary

def test_ifStationary(self):
    testData =  pd.read_csv('unit_test.csv',',')
    a = modelFunctions()
    result = a.ifStationary(testData)
    self.assertEqual(result, 0)