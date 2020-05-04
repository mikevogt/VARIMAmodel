from ARIMA import Models
import pandas as pd
import matplotlib.pylab as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
import datetime
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
import itertools
import csv

model = Models()  # the constructor

data = pd.read_csv('ProcessedStandardised.csv', ';')
ticker = str(input('What share do you wna predict:'))  # INPUT

share = model.Ticker(ticker, data)  # Getting choice for a share
lag = 1
feature = str(input(
    'Pick a feature from the following MonthReturn2:'))  # the input has to be in apostrophes like 'HCI' not just HCI (will figure it out later)

shareFeature_data = share[feature]  # Getting choice for a share
diffData = model.differecing(1, shareFeature_data)  # differecing it once
isStationary = model.ifStationary(diffData) # checks if series is stationary

# this loop checks if series is stationary and makes it stationary (not entirely sure if it works)
while isStationary == 0:
    diffData = model.differecing(lag, shareFeature_data)
    lag += 1

# this is a simple I/O system to check how and if the class functions are working
if isStationary == 1:
    lag += 1
    what_model = input('Would you like an ARIMA model or AR model prediction:')

    if what_model == 'ARIMA':
        p_value = int(input('enter p value:'))
        d_value = int(input('enter d value:'))
        q_value = int(input('enter q value:'))
        period = int(input('How many periods would you like to predict'))

        forcast = model.ARIMAmodel(shareFeature_data, p_value, d_value, q_value, period)
        print(forcast)

    if what_model == 'AR':
        predictions = model.ARmodel(shareFeature_data)
        print(predictions)

    if what_model == 'MA':
        order_value = int(input('enter MA order value value:'))
        prediction = model.MAmodel(order_value, shareFeature_data)
        print(prediction)
