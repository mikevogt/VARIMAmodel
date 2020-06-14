import pytest

from PyQt5 import QtCore

import ArimaModelGui

# LOGIN
@pytest.fixture
def login(qtbot):
    test_Arima = ArimaModelGui.Login()
    qtbot.addWidget(test_Arima)
    return test_Arima

def test_loginEdit(login, qtbot):
    login.usernameLineEditLogin.clear()
    login.passwordLineEditLogin.clear()
    qtbot.keyClicks(login.usernameLineEditLogin, "encrypt")
    qtbot.keyClicks(login.passwordLineEditLogin, "encryptp")
    qtbot.mouseClick(login.loginButton, QtCore.Qt.LeftButton)
    assert True

def test_loginRegisterButton(login, qtbot):
    qtbot.mouseClick(login.registerButton, QtCore.Qt.LeftButton)
    assert True

def test_loginForgotButton(login, qtbot):
    qtbot.mouseClick(login.forgotButton, QtCore.Qt.LeftButton)
    assert True

#def test_loginQuitButton(login, qtbot):
#    qtbot.mouseClick(login.quitButton, QtCore.Qt.LeftButton)

# REGISTER
@pytest.fixture
def register(qtbot):
    test_Arima = ArimaModelGui.Register()
    qtbot.addWidget(test_Arima)
    return test_Arima

def test_registerEdit(register, qtbot):
    register.usernameLineEdit.clear()
    register.passwordLineEdit.clear()
    register.confirmPasswordLineEdit.clear()
    register.emailAddressLineEdit.clear()
    qtbot.keyClicks(register.usernameLineEdit, "username")
    qtbot.keyClicks(register.passwordLineEdit, "encryptp")
    qtbot.keyClicks(register.confirmPasswordLineEdit, "encryptp")
    qtbot.keyClicks(register.emailLineEdit, "encryptp")
    qtbot.mouseClick(register.registerButton, QtCore.Qt.LeftButton)
    assert True

def test_registerReturnButton(register, qtbot):
    qtbot.mouseClick(register.returnButton, QtCore.Qt.LeftButton)
    assert True

# ForgotPassword
@pytest.fixture
def forgot(qtbot):
    test_Arima = ArimaModelGui.ForgotPage()
    qtbot.addWidget(test_Arima)
    return test_Arima

def test_registerEdit(forgot, qtbot):
    forgot.usernameLineEdit.clear()
    forgot.passwordLineEdit.clear()
    forgot.confirmPasswordLineEdit.clear()
    forgot.emailLineEdit.clear()
    qtbot.keyClicks(forgot.usernameLineEdit, "encrypt")
    qtbot.keyClicks(forgot.passwordLineEdit, "encryptp")
    qtbot.keyClicks(forgot.confirmPasswordLineEdit, "encryptp")
    qtbot.keyClicks(forgot.emailLineEdit, "nicholasbaard30@gmail.com")
    qtbot.mouseClick(forgot.resetButton, QtCore.Qt.LeftButton)
    assert True

def test_forgotReturnMainButton(forgot, qtbot):
    qtbot.mouseClick(forgot.returnButton, QtCore.Qt.LeftButton)
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

def test_sliderPVal(myWindow, qtbot):
    myWindow.sliderPval.setValue(2)
    assert myWindow.pValSpinBox.value() == 2
    print("HELLO WORLD")

    myWindow.sliderDval.setValue(1)
    assert myWindow.dValSpinBox.value() == 1

    myWindow.sliderQval.setValue(1)
    assert myWindow.qValSpinBox.value() == 1

    assert myWindow.featuresListWidget.currentItem().text() == "Return on Investment"

    assert myWindow.dialSpinBox.value() == 27
    assert myWindow.dial.value() == 27

def test_myWindowLogout(myWindow, qtbot):
    qtbot.mouseClick(myWindow.logoutButton, QtCore.Qt.LeftButton)
