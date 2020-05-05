import pandas as pd
import matplotlib.pylab as plt
import datetime
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
import warnings
import itertools
from statsmodels.tsa.arima_model import ARMA



class Models:

    def ARmodel(self, shareFeature_data):

        dataSize = shareFeature_data.size
        #splitting of training and testing data
        trainSize = int(dataSize * 70 / 100 + 1)
        testSize = int(dataSize * 30 / 100)
        train = shareFeature_data[0:trainSize]
        test = shareFeature_data[trainSize + 1:]
        predictions = []

        #the model fitting and forcasting
        model_ar = AR(shareFeature_data)
        model_ar_fit = model_ar.fit()
        predictions = model_ar_fit.predict(start=trainSize, end=dataSize)

        return predictions

    def MAmodel(self, order_value, shareFeature_data):

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

    def ARIMAmodel(self, shareFeature_data, p, d, q, futureSteps):

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

    def Ticker(self, ticker, data):
        TickerChoice = ticker
        dataticker = data[data.Ticker == TickerChoice]
        return dataticker

    def differecing(self, numDiff, shareFeature_data):

        data_diff = shareFeature_data.diff(periods=numDiff)
        data_diff = data_diff[numDiff:]
        return data_diff

    def ifStationary(self, diffdata):
        #checks if series is stationary by means of the autocorrelation and this can be tweaked and we can add other tests as well
        autocorrelation = diffdata.autocorr(lag=1)
        boolean = 0
        if autocorrelation <= 0.2:
           boolean=1
        else:
            boolean = 0
        return boolean
