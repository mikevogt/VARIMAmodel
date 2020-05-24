from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA, ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf

def MAmodel(order_value, shareFeature_data):

    dataSize = shareFeature_data.size
    #splitting of training and testing data
    trainSize = int(dataSize * 70 / 100 + 1)
    testSize = int(dataSize * 30 / 100)
    train = shareFeature_data[0:trainSize]
    test = shareFeature_data[trainSize + 1:]

    #the model fitting and forcasting
    model_ma = ARMA(shareFeature_data, order=(0, order_value))
    res = model_ma.fit()
    forcast = res.predict(start=trainSize, end=dataSize)

    return forcast