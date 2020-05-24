import math
import pandas as pd
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf

class modelFunctions:

    def ifStationary(self, diffdata):
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



    def Parametres(self,shareFeatureData):
        pVal = 0
        dVal = 0  # should not be more then 2
        qVal = 0
        count1 = 0
        count2 = 0
        check = 0
        data = shareFeatureData
        acfArray = acf(data, nlags=30)
        pacfArray = pacf(data, nlags=30)

        for i in range(0, 30):
            if acfArray[i] >= 0.24 and acfArray[i] <= 0.25:
                count = i + 1
                print(acfArray[count - 1])
                pVal = count

        while check != -1:
            for i in range(0, 30):
                if pacfArray[i] < 0:
                    count2 = i
                    check = -1
                    qVal = count2
                    break

        values = [pVal, dVal, qVal]

        return values




    
 
