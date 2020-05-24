import math
import pandas as pd
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf

def ifStationary(diffdata):
    # checks if series is stationary by means of the Augmented Dicky-Fuller Test (adfuller)
    # returns a 1 if the series is stationary and 0 if not

    adfResult = adfuller(diffdata, autolag='AIC')
    adfStat = adfResult[0]
    adfPValue = adfResult[1]
    Dictionary = dict(adfResult[4].items())
    significanceLevel = 0.05
    stationary = 0
    criticalValues1percentage = Dictionary['1%']
    criticalValues5percentage = Dictionary['5%']
    criticalValues10percentage = Dictionary['10%']

    # https://www.machinelearningplus.com/time-series/augmented-dickey-fuller-test/ for more info on how the
    # stationarity is decided and meaning to the following comparisons

    if adfPValue > significanceLevel:
        stationary = 0
    else:
        stationary = 1
    if adfStat > criticalValues1percentage or adfStat > criticalValues5percentage or adfStat > criticalValues10percentage:
        stationary = 0
    elif adfStat < criticalValues1percentage or adfStat < criticalValues5percentage or adfStat < criticalValues10percentage:
        stationary = 1

    return stationary