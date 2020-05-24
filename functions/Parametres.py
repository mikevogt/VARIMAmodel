import math
import pandas as pd
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf

def Parametres(shareFeatureData):
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
