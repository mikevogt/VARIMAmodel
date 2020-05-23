from math import *

def rootMeanSquareError(self,forecastValues,actualValues): # Havent tested if this gives the correct output yet
    sum =0.0
    for i in range(0,7):
        sum = sum +(forecastValues[i]-actualValues[len(actualValues)-7+i])**2
    rMSE = sqrt(sum/7)
    return rMSE

def sum(arg):
    total = 0
    for val in arg:
        total += val
    return total
