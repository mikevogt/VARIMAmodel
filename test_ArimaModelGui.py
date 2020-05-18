import unittest
from unittest import TestCase
import ArimaModelGui
from ArimaModelGui import MyWindow


class TestMyWindow(unittest.TestCase):
    # testing importButton
    def setUp(self):
        self.app = ArimaModelGui.app.test_client()
        self.app.testing = True

    def test_button_import_function(self):
        check = ArimaModelGui.MyWindow.buttonImportFunction()
        self.assertEqual(check == "button import pressed")

    def test_rMSE(self):
        forecastValues = [0.0, 0.5, 0.0, 0.5, 0.0, 0.4, 0.9]
        actualValues = [0.2, 0.4, 0.1, 0.6, 0.2, 0.1, 0.6]
        result = ArimaModelGui.MyWindow.rootMeanSquareError(forecastValues,actualValues)
        self.assertEqual(result, 0.24083189157584592)

if __name__ == '__main__':
    unittest.main()
