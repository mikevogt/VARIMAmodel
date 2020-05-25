from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA, ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf


def ARIMAmodel(shareFeature_data, p, d, q, futureSteps):

    dataSize = shareFeature_data.size
    #splitting of training and testing data
    trainSize = int(dataSize * 70 / 100)
    testSize = int(dataSize * 30 / 100)
    train = shareFeature_data[0:trainSize]
    test = shareFeature_data[trainSize + 1:]
    futureSteps = futureSteps + testSize

    #the model fitting and forcasting
    model_arima = ARIMA(train, order=(1, 0, 1))
    model_arima_fit = model_arima.fit()
    forcasted = model_arima_fit.forecast(steps=45)[0]
    print(model_arima_fit.aic)

    return forcasted