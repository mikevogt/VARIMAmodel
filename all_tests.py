import pytest
import ArimaModelGui
from ArimaModelGui import MyWindow

def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

def test_rMSE():
    assert rootMeanSquareError(forecastValues, actualValues) == 0.24083189157584592, "Should be 0.24083189157584592"

if __name__ == "__main__":
    test_sum()
    test_rMSE()
    print("Everything passed")
