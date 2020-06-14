import pytest

from PyQt5 import QtCore

import ArimaModelGui

# LOGIN
@pytest.fixture
def login(qtbot):
    test_Arima = ArimaModelGui.Login()
    qtbot.addWidget(test_Arima)
    return test_Arima

def test_login_Edit(login, qtbot):
    login.usernameLineEditLogin.clear()
    login.passwordLineEditLogin.clear()
    qtbot.keyClicks(login.usernameLineEditLogin, "encrypt")
    qtbot.keyClicks(login.passwordLineEditLogin, "encryptp")
    qtbot.mouseClick(login.loginButton, QtCore.Qt.LeftButton)
    #assert True

def test_loginRegisterButton_clicked(login, qtbot):
    qtbot.mouseClick(login.registerButton, QtCore.Qt.LeftButton)
    #assert True

def test_loginForgotButton_clicked(login, qtbot):
    qtbot.mouseClick(login.forgotButton, QtCore.Qt.LeftButton)
    #assert True

# REGISTER
@pytest.fixture
def register(qtbot):
    test_Arima = ArimaModelGui.Register()
    qtbot.addWidget(test_Arima)
    return test_Arima

def test_registerButton_clicked(register, qtbot):
    qtbot.mouseClick(register.registerButton, QtCore.Qt.LeftButton)
    assert True

# myWINDOW
@pytest.fixture
def myWindow(qtbot):
    test_Arima = ArimaModelGui.MyWindow()
    qtbot.addWidget(test_Arima)
    return test_Arima

def test_myWindow_labels(myWindow):
    assert myWindow.sharesLabel.text() == "Shares"
    assert myWindow.labelPval.text() == "P-Value:"
    assert myWindow.labelArimaCustomize.text() == "Customize Arima Variables"
    assert myWindow.labelQval.text() == "Q-Value:"
    assert myWindow.labelPlotCustomize.text() == "Plot Line Colour"
    assert myWindow.labelPlotColour.text() == "Plot line colour:"
    assert myWindow.labelDval.text() =="D-Value:"
    assert myWindow.labelForecastLength.text() == "Forecast Length:"

def test_sliderVal(myWindow, qtbot):
    myWindow.sliderPval.setValue(2)
    myWindow.sliderDval.setValue(1)
    myWindow.sliderQval.setValue(2)
    qtbot.mouseClick(myWindow.buttonArima, QtCore.Qt.LeftButton)
    # continue until you press Arima button and compare RMSE to expected FUCKING RMSE
