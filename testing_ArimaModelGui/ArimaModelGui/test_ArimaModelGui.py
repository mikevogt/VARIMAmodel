import pytest

from PyQt5 import QtCore

import ArimaModelGui


@pytest.fixture
def login(qtbot):
    test_Arima = ArimaModelGui.Login()
    qtbot.addWidget(test_Arima)

    return test_Arima

def test_loginButton_clicked(login, qtbot):
    qtbot.mouseClick(login.loginButton, QtCore.Qt.LeftButton)
    assert login.x == 5


@pytest.fixture
def register(qtbot):
    test_Arima = ArimaModelGui.Register()
    qtbot.addWidget(test_Arima)

    return test_Arima

def test_registerButton_clicked(register, qtbot):
    qtbot.mouseClick(register.registerButton, QtCore.Qt.LeftButton)
    assert register.x == 5


@pytest.fixture
def myWindow(qtbot):
    test_Arima = ArimaModelGui.MyWindow()
    qtbot.addWidget(test_Arima)

    return test_Arima

def test_myWindow_labels(myWindow):
    assert myWindow.sharesLabel.text() == "Shares"
    assert myWindow.labelPval.text() == "P-Value:"
