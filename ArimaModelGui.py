from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QFrame,QGridLayout,
	QSplitter, QStyleFactory, QApplication,QVBoxLayout,QStyle, QSizePolicy,QSpacerItem,QMessageBox,QAction)
from PyQt5.QtCore import (Qt,QSize)
from PyQt5.QtGui import (QPalette,QColor,QPixmap,QIcon)



import sys
import math
import datetime
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
import numpy as np
import pandas as pd

from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf

import mysql.connector
from sshtunnel import SSHTunnelForwarder
from numpy.linalg import LinAlgError

import bcrypt
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#from sklearn.metrics import mean_squared_error


class MyWindow(QMainWindow):
	#MainWindow constructor. Most of the actual construction takes place in the function initUi(self) when it is called
	def __init__(self):

		super(MyWindow,self).__init__()#This can be written as super().__init__() i think which would make more sense but leave it as is for now
		self.setWindowIcon(QIcon("Logo.ico"))
		self.data =pd.read_csv('ProcessedStandardised.csv',';')#Reads in the standardized data from ProcessedStandardised.csv. This file must be in the same directory as varimaGui.py
		self.pVal=2
		self.dVal=1
		self.qVal=1
		self.forecastLength=27
		self.initUi()


	def initUi(self):

		#The gui for main window is built below. It consists of a central widget called widgetBox which has a gridlayout (called grid) set to it

		widgetBox = QWidget(self)
		grid = QGridLayout()
		grid.setSpacing(10)
		widgetBox.setLayout(grid)
		self.setMinimumSize(900, 700);
		self.setCentralWidget(widgetBox)
		self.setWindowTitle("Arima Model")

		bar = self.menuBar()
		file = bar.addMenu("File")
		
		save = QAction("Save Plot",self)
		save.setShortcut("Ctrl+S")
		file.addAction(save)
		
		
		
		logout = QAction("Logout",self)
		file.addAction(logout)
		quit = QAction("Quit",self) 
		file.addAction(quit)

		

		view = bar.addMenu("View")
		view.addAction("Themes")
		helpMenu = bar.addMenu("Help")
		helpMenu.addAction("About")
      	#file.triggered[QAction].connect(self.processtrigger)
		"""self.menuBar().addMenu("&File")
		close=QtWidgets.QAction("&Close")
		#close.triggered.connect(window.close)
		self.menuBar().addAction(close)
	"""
		#Next, 3 QFrames are built to provide the primary framework of the window

		#############################################################################################################################################
		############################################## The top left frame is built and populated below below ########################################
		#############################################################################################################################################

		
		topLeft = QFrame(self,objectName="innerFrame2")#Objectname is only used for stylesheet purposes and hence is not needed for declaring most widgets
		topLeft.setFrameShape(QFrame.Panel)
		topLeft.setFrameShadow(QFrame.Raised)
		#builds layout for top left QFrame.
		gridTopLeft = QGridLayout(topLeft)
		gridTopLeft.setSpacing(10)
		topLeft.setLayout(gridTopLeft)

		#Widgets to be added to top left are made
		#import button made
		buttonImport= QtWidgets.QPushButton("Click herer",objectName="button")
		buttonImport.setText("Import Data")
		buttonImport.clicked.connect(self.buttonImportFunction)


		#Shares label is now made
		
		sharesLabel = QtWidgets.QLabel("Shares")
		sharesLabel.setStyleSheet("""font-size: 15px;""")
		sharesLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		sharesLabel.setSizePolicy(sharesLabelSizePolicy)

		#comboBox is now made


		self.comboBox= QtWidgets.QComboBox()
		self.comboBox.setStyleSheet("""font-size:13px;
										""")
		"""self.comboBox.setStyleSheet(
						border-radius:16px;
						font-size: 15px;
						
						color: rgba(60,70,89,225);
						background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
						stop:0 rgba(178, 182, 194,200), stop:1 rgba(215,218,230,225));
						border-width: 1px;	
						border-style: outset;
						border-color: rgba(240,240,240,200);)
"""
		for share in self.data.Ticker.unique():#For loop that iterates through the unique values in the column called  "Ticker" of self.data
			#Still need to fix this so that it does not add appostrophes around each share name
			self.comboBox.addItem(share)



		#Ignore the block of commets below here
		#Features scroll area is now made
		#innerGroupBox is made first. This will have a VBoxLayout containing list of hello worlds.
		#it will then be added to a scrollarea via setWidget
		'''innerGroupBox=QtWidgets.QGroupBox(objectName="featureBox")

		scrollVLayout=QVBoxLayout()
		featureList=[]

		for i in range(0,35):

			featureList.append(QtWidgets.QLabel("Hello World "+str(i)))
			scrollVLayout.addWidget(featureList[i])


		innerGroupBox.setLayout(scrollVLayout)
		#Scroll area made and its widget is set to group box
		scrollArea=QtWidgets.QScrollArea()
		scrollArea.setWidget(innerGroupBox)
		#OUter group made and layout set for it so scor
		groupBoxOuterScroll=QtWidgets.QGroupBox("Features")
		outerGroupBoxLayout=QtWidgets.QVBoxLayout()
		outerGroupBoxLayout.addWidget(scrollArea)
		groupBoxOuterScroll.setLayout(outerGroupBoxLayout)
'''				#Ignore up until here


		#Next, the features scroll list (called featuresListWidget) is made using a QListWidget() within a QGroupBox()

		self.featuresListWidget = QtWidgets.QListWidget()
		self.featuresListWidget.setStyleSheet("""font-size: 15px;""")
		self.featuresListWidget.setAlternatingRowColors(True)

		for column in self.data.columns[3:-2]:#For loop that iterates through all column names in data populating the featuresListWidget
			#Still need to fix this so that it does not add the first 3 column names (namely DateStamps, Shares and Ticker) to the features list
			self.featuresListWidget.addItem(column)



		listWidgetGroupBox=QtWidgets.QGroupBox("Features")#Outer groupBox to house the features list widget
		listWidgetGroupBox.setStyleSheet("""font-size:15px;
											""")
		listWidgetGroupBoxLayout=QtWidgets.QVBoxLayout()
		listWidgetGroupBox.setLayout(listWidgetGroupBoxLayout)
		listWidgetGroupBoxLayout.addWidget(self.featuresListWidget)#featuresListWidget is first added to the groupbox

		#All widgets are then added to the top left grid
		#gridTopLeft.addWidget(buttonImport,0,0,1,4)
		gridTopLeft.addWidget(sharesLabel,0,0,1,1)
		gridTopLeft.addWidget(self.comboBox,0,1,1,4)
		gridTopLeft.addWidget(listWidgetGroupBox,1,0,3,5)# the groupbox (listWidgetGroupBox) is added to the top left grid completing the placement of the features list


		#############################################################################################################################################
		############################################### Bottom left frame is built and populated below ##############################################
		#############################################################################################################################################

		#builds bottom left QFrame and creates a grid layout for it
		bottomLeft = QFrame(self,objectName="innerFrame2")
		bottomLeft.setFrameShape(QFrame.Panel)
		bottomLeft.setFrameShadow(QFrame.Raised)
		bottomLeftGridLayout= QGridLayout()
		bottomLeft.setLayout(bottomLeftGridLayout)

		#Next, each item in the bottom left frame is created without adding it to the layout just yet

		labelPlotCustomize = QtWidgets.QLabel("Plot Line Colour")
		labelPlotCustomize.setStyleSheet("""font-size: 15px""")
		
		#customizeLabelWidget = QWidget()
		#layout1=QHBoxLayout()
		#customizeLabelWidget.setLayout(layout1)
		#layout1.addWidget(labelPlotCustomize,Qt.AlignCenter)

		labelPlotColour = QtWidgets.QLabel("Plot line colour:")

		self.radioButtonGreen = QtWidgets.QRadioButton("Green")
		self.radioButtonGreen.setStyleSheet("""font-size: 13px""")
		self.radioButtonGreen.setStyle(QStyleFactory.create('windows'))
		self.radioButtonPurple = QtWidgets.QRadioButton("Purple")
		self.radioButtonPurple.setStyleSheet("""font-size: 13px""")
		self.radioButtonPurple.setStyle(QStyleFactory.create('windows'))
		self.radioButtonOrange = QtWidgets.QRadioButton("Orange")
		self.radioButtonOrange.setStyleSheet("""font-size: 13px""")
		self.radioButtonOrange.setStyle(QStyleFactory.create('windows'))
		"""
		buttonPlot = QtWidgets.QPushButton("Plot Data")
		buttonPlot.clicked.connect(self.plotDataClicked)"""

		labelArimaCustomize = QtWidgets.QLabel("Customize Arima Variables")
		labelArimaCustomize.setStyleSheet("""font-size: 15px""")

		labelPval= QtWidgets.QLabel("P-Value:")
		labelPval.setStyleSheet("""font-size: 13px""")
		lineEditPval = QtWidgets.QLineEdit()
		self.sliderPval = QtWidgets.QSlider(Qt.Horizontal)
		self.sliderPval.setMinimum(0)
		self.sliderPval.setMaximum(5)
		self.sliderPval.setValue(2)
		self.sliderPval.setTickPosition(3)
		self.sliderPval.setTickInterval(1)
		self.sliderPval.valueChanged.connect(self.sliderChangedPvalue)

		self.pValSpinBox = QtWidgets.QSpinBox()
		self.pValSpinBox.setStyleSheet("""font-size: 13px""")
		self.pValSpinBox.setValue(2)
		self.pValSpinBox.setMinimum(0)
		self.pValSpinBox.setMaximum(5)
		self.pValSpinBox.valueChanged.connect(self.spinboxChangedPvalue)

		labelDval= QtWidgets.QLabel("D-Value:")
		labelDval.setStyleSheet("""font-size: 13px""")
		lineEditDval = QtWidgets.QLineEdit()
		self.sliderDval = QtWidgets.QSlider(Qt.Horizontal)
		self.sliderDval.setMinimum(0)
		self.sliderDval.setMaximum(2)
		self.sliderDval.setValue(1)
		self.sliderDval.setTickPosition(3)
		self.sliderDval.setTickInterval(1)
		self.sliderDval.valueChanged.connect(self.sliderChangedDvalue)

		self.dValSpinBox = QtWidgets.QSpinBox()
		self.dValSpinBox.setStyleSheet("""font-size: 13px""")
		self.dValSpinBox.setValue(1)
		self.dValSpinBox.setMinimum(0)
		self.dValSpinBox.setMaximum(2)
		self.dValSpinBox.valueChanged.connect(self.spinboxChangedDvalue)

		labelQval= QtWidgets.QLabel("Q-Value:")
		labelQval.setStyleSheet("""font-size: 13px""")
		lineEditQval = QtWidgets.QLineEdit()
		self.sliderQval = QtWidgets.QSlider(Qt.Horizontal)
		self.sliderQval.setMinimum(0)
		self.sliderQval.setMaximum(5)
		self.sliderQval.setValue(1)
		self.sliderQval.setTickPosition(QtWidgets.QSlider.TicksBothSides)
		self.sliderQval.setFocusPolicy(Qt.StrongFocus)
		self.sliderQval.setTickInterval(1)
		self.sliderQval.setSingleStep(1)
		self.sliderQval.valueChanged.connect(self.sliderChangedQvalue)


		self.qValSpinBox = QtWidgets.QSpinBox()
		self.qValSpinBox.setStyleSheet("""font-size: 13px""")
		self.qValSpinBox.setValue(1)
		self.qValSpinBox.setMinimum(0)
		self.qValSpinBox.setMaximum(5)
		self.qValSpinBox.valueChanged.connect(self.spinboxChangedQvalue)

		labelForecastLength = QtWidgets.QLabel("Forecast Length:")
		labelForecastLength.setStyleSheet("""font-size: 13px""")
		


		self.dialSpinBox = QtWidgets.QSpinBox()
		self.dialSpinBox.setStyleSheet("""font-size: 13px""")
		self.dialSpinBox.setValue(27)
		self.dialSpinBox.setMaximum(37)
		self.dialSpinBox.setMinimum(7)
		self.dialSpinBox.valueChanged.connect(self.dialSpinBoxValueChanged)
		self.dial = QtWidgets.QDial()
		self.dial.setMinimum(7)
		self.dial.setMaximum(37)
		self.dial.setValue(27)
		self.dial.setNotchesVisible(True)
		self.dial.setStyle(QStyleFactory.create('Plastique'))
		self.dial.valueChanged.connect(self.dialValueChanged)

		"""optimizeButton=QtWidgets.QPushButton("Optimize Model Order")
		optimizeButton.clicked.connect(self.optimizeModelOrder)"""
		buttonArima = QtWidgets.QPushButton("Estimate using ARIMA",objectName="button")
		buttonArima.clicked.connect(self.varButtonClicker)

		logoutButton = QtWidgets.QPushButton("Logout",objectName="button")
		logoutButton.clicked.connect(self.logoutButtonClicked)


		#Now each item created above is added to the grid layout for the bottom left frame

		bottomLeftGridLayout.addWidget(labelPlotCustomize,0,0,1,7,Qt.AlignCenter)

		#bottomLeftGridLayout.addWidget(labelPlotColour,1,0,1,1)
		bottomLeftGridLayout.addWidget(self.radioButtonPurple,1,0,1,3,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.radioButtonGreen,1,3,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.radioButtonOrange,1,4,1,3,Qt.AlignCenter)

		#bottomLeftGridLayout.addWidget(buttonPlot,2,0,1,7)

		bottomLeftGridLayout.addWidget(labelArimaCustomize,2,0,1,7,Qt.AlignCenter)

		bottomLeftGridLayout.addWidget(labelPval,3,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.pValSpinBox,3,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderPval,3,2,1,5)

		bottomLeftGridLayout.addWidget(labelDval,4,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.dValSpinBox,4,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderDval,4,2,1,5)

		bottomLeftGridLayout.addWidget(labelQval,5,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.qValSpinBox,5,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderQval,5,2,1,5)

		bottomLeftGridLayout.addWidget(labelForecastLength,6,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.dialSpinBox,6,1,1,5)
		bottomLeftGridLayout.addWidget(self.dial,6,6,1,1)

		#bottomLeftGridLayout.addWidget(optimizeButton,,0,1,7)
		bottomLeftGridLayout.addWidget(buttonArima,7,0,1,7)
		
		bottomLeftGridLayout.addWidget(logoutButton,8,0,1,7)



		############################################################################################################################################
		################################################# Right frame is now built and populated ###################################################
		############################################################################################################################################

		#builds right QFrame and sets a grid layout for it
		right = QFrame(self,objectName="innerFrame2")
		right.setFrameShape(QFrame.Panel)
		right.setFrameShadow(QFrame.Raised)
		self.rightFrameGridLayout=QGridLayout()
		right.setLayout(self.rightFrameGridLayout)
		# Note that no widgets have been added to the right frame and thus it is initially merely empty space. This is because a widget (namely a plot)
		# is only added to it when the estimate using var button is pressed. Perhaps we should change this so that initially, there are grid lines and axis
		# without a plot to begin with.


		#All 3 frames are then added to their respective positions on the  the main grid of the central widget

		grid.addWidget(topLeft,0,0,2,1)
		grid.addWidget(bottomLeft,2,0,1,1)
		grid.addWidget(right,0,1,3,3)


		self.plotEmptyAxis()
		#Now each on-button-click function is created
		

	def plotEmptyAxis(self):

		fig, ax =plt.subplots()

		ax.grid(linestyle="--")
		ax.patch.set_facecolor('#282828')
		fig.patch.set_facecolor("None")


		ax.spines['bottom'].set_color('#ffffff')
		ax.spines['top'].set_color('#ffffff')
		ax.spines['right'].set_color('#ffffff')
		ax.spines['left'].set_color('#ffffff')
		ax.tick_params(axis='x', colors='#ffffff')
		ax.tick_params(axis='y', colors='#ffffff')
		#ax.set_xlabel("Date",fontsize=15)
		#ax.set_ylabel(self.featuresListWidget.currentItem().text(),fontsize=15)
		ax.yaxis.label.set_color('white')
		ax.xaxis.label.set_color('white')
		#fig.suptitle(self.comboBox.currentText(),fontsize=20,color='white')

		self.plotWidget = FigureCanvas(fig)#FigureCanvas is an matplotlib object that can act as a pyqt5 widget
		self.plotWidget.setStyleSheet("background-color:transparent;")
		
		self.rightFrameGridLayout.addWidget(self.plotWidget)

	def optimizeModelOrder(self):


		if(self.featuresListWidget.currentItem() == None):
			#Makes sure a feature is selected. should maybe have this open an alert box instead of printing to the console
			#If this removed, program will crash if no item is selected
			print("No feature selected, please select one above")
			return


		shareData = self.data[self.data.Ticker == self.comboBox.currentText()] #Stores a dataFrame of all shares with the selected ticker
		featureColumnName =self.featuresListWidget.currentItem().text()
		data= shareData[featureColumnName]
		pVal = 0
		dVal = 0  # should not be more then 2
		qVal = 0
		count1 = 0
		count2 = 0
		check = 0
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
		print(values)
		#return values


	def dialSpinBoxValueChanged(self):

		self.dial.setValue(self.dialSpinBox.value())
		self.forecastLength=self.dial.value()

	def dialValueChanged(self):

		self.dialSpinBox.setValue(self.dial.value())
		self.forecastLength=self.dial.value()


	def sliderChangedPvalue(self):


		self.pValSpinBox.setValue(self.sliderPval.value())
		self.pVal =self.sliderPval.value()

	def sliderChangedDvalue(self):

		self.dValSpinBox.setValue(self.sliderDval.value())
		self.dVal =self.sliderDval.value()

	def sliderChangedQvalue(self):

		self.qValSpinBox.setValue(self.sliderQval.value())
		self.qVal =self.sliderQval.value()

	def spinboxChangedPvalue(self):
		self.sliderPval.setValue(self.pValSpinBox.value())
		self.pVal = self.pValSpinBox.value()

	def spinboxChangedDvalue(self):

		self.sliderDval.setValue(self.dValSpinBox.value())
		self.dVal = self.dValSpinBox.value()

	def spinboxChangedQvalue(self):

		self.sliderQval.setValue(self.qValSpinBox.value())
		self.qVal = self.qValSpinBox.value()


	def buttonImportFunction(self):
		#So far there is no purpose to this button however we may be able to think of one or replace it etc
		#self.data =pd.read_csv('ProcessedNonStandardised.csv',';')
		print("button import pressed")


	def rootMeanSquareError(self,forecastValues,actualValues): # Havent tested if this gives the correct output yet

		sum =0.0

		for i in range(0,7):

			sum = sum +(forecastValues[i]-actualValues[len(actualValues)-7+i])**2

		rMSE =math.sqrt(sum/7)

		return rMSE

	def exponentiate(self,inVal):

		return (1.02)**(inVal)-1


	def plotDataClicked(self):

		#Determine the colour of the plot bases on user preference

		colourString = "#BF1AED" #Default purple
		if self.radioButtonPurple.isChecked():

			colourString = "#BF1AED"
		elif self.radioButtonGreen.isChecked():
			colourString = "#00E600"

		elif self.radioButtonOrange.isChecked():

			colourString = "#E46B3C"

		#If no feature has been select then return and display message box
		if(self.featuresListWidget.currentItem() == None):
			#Makes sure a feature is selected. should maybe have this open an alert box instead of printing to the console
			#If this removed, program will crash if no item is selected
			print("No feature selected, please select one above")
			return


		plt.clf()
		self.plotWidget.deleteLater()#Not fully sure if this is neccessary however we should only potentially remove it during polishing

		shareData = self.data[self.data.Ticker == self.comboBox.currentText()] #Stores a dataFrame of all shares with the selected ticker


		dateColumn = shareData['DateStamps']# takes and stores all the required date stamps

		pythonDateList =[] #This will store all the date stamps from dateColumn in python datetime format

		for i in range (0,len(dateColumn)) :

			pythonDateList.append(datetime.datetime.strptime(str(dateColumn.iloc[i]),"%Y%m%d"))


		#Now we convert all the python datetime objects into matplotlib date format
		dates = matplotlib.dates.date2num(pythonDateList)

		#We then access the selected feature column and copy its entire column into y.
		featureColumnName =self.featuresListWidget.currentItem().text()
		y= shareData[featureColumnName]

		print(self.comboBox.currentText())
		print(self.featuresListWidget.currentItem().text())

		#Plot of y vs dates is now created below
		fig, ax =plt.subplots()
		#color='#1AB1ED' for blue
		#ax.plot(y,linewidth=3,color='#BF1AED')
		ax.plot_date(dates,y,linewidth = 3,color=colourString,fmt='-', label ="Actual")
		plt.legend(loc="upper right")
		ax.grid(linestyle="--")
		ax.patch.set_facecolor('#282828')
		fig.patch.set_facecolor("None")
		#fig.patch.set_alpha(0.0)
		#ax.patch.set_alpha(0.0)

		ax.spines['bottom'].set_color('#ffffff')
		ax.spines['top'].set_color('#ffffff')
		ax.spines['right'].set_color('#ffffff')
		ax.spines['left'].set_color('#ffffff')
		ax.tick_params(axis='x', colors='#ffffff')
		ax.tick_params(axis='y', colors='#ffffff')
		ax.set_xlabel("Date",fontsize=15)
		ax.set_ylabel(self.featuresListWidget.currentItem().text(),fontsize=15)
		ax.yaxis.label.set_color('white')
		ax.xaxis.label.set_color('white')
		fig.suptitle(self.comboBox.currentText(),fontsize=20,color='white')

		self.plotWidget = FigureCanvas(fig)#FigureCanvas is an matplotlib object that can act as a pyqt5 widget
		self.plotWidget.setStyleSheet("background-color:transparent;")
		self.rightFrameGridLayout.addWidget(self.plotWidget)




	#Currently, this function does not perform a varima model on the selected stock and feature but rather plots the selected stock and feature
	def varButtonClicker(self):

		#self.featuresListWidget.currentItem().text() is the text of the item selected in the featuresList widget
		#self.comboBox.currentText() is the text of the item selected in the drop down list. namely the share

		colourString = "#E46B3C" #Default Orange
		if self.radioButtonPurple.isChecked():

			colourString = "#BF1AED"
		elif self.radioButtonGreen.isChecked():
			colourString = "#00E600"

		elif self.radioButtonOrange.isChecked():

			colourString = "#E46B3C"


		if(self.featuresListWidget.currentItem() == None):
			#Makes sure a feature is selected. should maybe have this open an alert box instead of printing to the console
			#If this removed, program will crash if no item is selected
			print("No feature selected, please select one above")
			return



		if self.rightFrameGridLayout.itemAt(0) == None : #Checks if there is a plot already there

			plt.clf()
			shareData = self.data[self.data.Ticker == self.comboBox.currentText()] #Stores a dataFrame of all shares with the selected ticker


			dateColumn = shareData['DateStamps']# takes and stores all the required date stamps

			pythonDateList =[] #This will store all the date stamps from dateColumn in python datetime format

			for i in range (0,len(dateColumn)) :

				pythonDateList.append(datetime.datetime.strptime(str(dateColumn.iloc[i]),"%Y%m%d"))

			#Now we create a date list called pythonForecastDatelist which will contain the last 7 dates plus 20 future dates
			#in increments of length dateDelta
			dateDelta = pythonDateList[len(pythonDateList)-1]-pythonDateList[len(pythonDateList)-2]# this date difference varies throughout each share date set and hence may lead to problems
			pythonDateListLast7 =pythonDateList[-7:]
			pythonDateListFuture =[]
			inDate = pythonDateList[len(pythonDateList)-1]#Start date for all future dates

			for i in range(0,20):

				pythonDateListFuture.append(inDate)
				inDate=inDate+dateDelta

			pythonForecastDateList = pythonDateListLast7+pythonDateListFuture

			print("python last 7:")
			print(pythonDateListLast7)
			print("DateDelta:")
			print(dateDelta)
			print("dateList original")
			print(pythonDateList)
			print("datelist future")
			print(pythonDateListFuture)



			#Now we convert all the python datetime objects into matplotlib date format
			dates = matplotlib.dates.date2num(pythonDateList)
			datesInFuture = matplotlib.dates.date2num(pythonDateListFuture)
			forcastDates = matplotlib.dates.date2num(pythonForecastDateList)
			#We then access the selected feature column and copy its entire column into y.
			string =self.featuresListWidget.currentItem().text()
			y= shareData[string]

			xValArray = shareData[string].values
			print(xValArray)
			train = xValArray[0:len(xValArray)-7]#This may yield an array index out of bounds error if xValArray is size<5 so try fix it later
			#test= xValArray[26:]

			print(self.comboBox.currentText())
			print(self.featuresListWidget.currentItem().text())

			model_arima = ARIMA(train,order=(self.pVal,self.dVal,self.qVal))
			print("got past Arima(train,order=(2,1,1))")
			model_arima_fit = model_arima.fit()
			print("got past model_arima.fit()")
			forcasted=[]
			forcasted= model_arima_fit.forecast(steps=27)[0]           #What is this zero here meant to signify
			print("got past forecast")
			rmse = self.rootMeanSquareError(forcasted,xValArray)
			print("RMSE calculated:")
			print(rmse)
			#Plot of y vs dates is now created below
			fig, ax =plt.subplots()
			#color='#1AB1ED' for blue
			#ax.plot(y,linewidth=3,color='#BF1AED')
			forecastUpperError = forcasted + rmse
			forecastLowerError = forcasted - rmse
			ax.plot_date(dates,y,linewidth = 3,color=colourString,fmt='-', label ="Actual")
			ax.plot_date(forcastDates,forcasted,linewidth = 3,color='#1AB1ED',fmt='-', label="Forecasted")
			ax.plot_date(forcastDates,forecastUpperError,linewidth = 2,color='#ff0066',fmt='--', label="Error")
			ax.plot_date(forcastDates,forecastLowerError,linewidth = 2, color='#ff0066', fmt='--')
			plt.legend(loc="upper right")
			ax.grid(linestyle="--")
			ax.patch.set_facecolor('#323232')
			fig.patch.set_facecolor('#191919')
			#fig.patch.set_alpha(0.0)
			#ax.patch.set_alpha(0.0)

			ax.spines['bottom'].set_color('#ffffff')
			ax.spines['top'].set_color('#ffffff')
			ax.spines['right'].set_color('#ffffff')
			ax.spines['left'].set_color('#ffffff')
			ax.tick_params(axis='x', colors='#ffffff')
			ax.tick_params(axis='y', colors='#ffffff')
			ax.set_xlabel("Date",fontsize=15)
			ax.set_ylabel(self.featuresListWidget.currentItem().text(),fontsize=15)
			ax.yaxis.label.set_color('white')
			ax.xaxis.label.set_color('white')
			fig.suptitle(self.comboBox.currentText(),fontsize=20,color='white')
			#fig.savefig('temp.png', transparent=True)

			self.plotWidget = FigureCanvas(fig) #FigureCanvas is an matplotlib object that can act as a pyqt5 widget
			self.rightFrameGridLayout.addWidget(self.plotWidget)

		else :# This is entered if there is a plot already in the frame



			plt.clf()
			self.plotWidget.deleteLater() #existing plot widget is initially deleted. not sure if this actually works or not. TEst later. Also, the
											#existing figure should be deleted here as well. Not quite sure how to do this though but i think making
											#ax and fig into class variables and then calling plt.clf() should do it.


			#Stores a dataFrame of all shares with the selected ticker
			shareData = self.data[self.data.Ticker == self.comboBox.currentText()]

			# takes and stores all the required date stamps
			dateColumn = shareData['DateStamps']

			#This will store all the date stamps from dateColumn in python datetime format
			pythonDateList =[]
			for i in range (0,len(dateColumn)) :

				pythonDateList.append(datetime.datetime.strptime(str(dateColumn.iloc[i]),"%Y%m%d"))


			dateDelta = pythonDateList[len(pythonDateList)-1]-pythonDateList[len(pythonDateList)-2]# this date difference varies throughout each share date set and hence
																									#may lead to problems

			pythonDateListFuture =[]
			pythonDateListLast7 =pythonDateList[-7:]

			inDate = pythonDateList[len(pythonDateList)-1]
			print("self.forecast Length-7")
			print(self.forecastLength-7)
			for i in range(0,self.forecastLength-7):

				pythonDateListFuture.append(inDate)
				inDate=inDate+dateDelta

			pythonForecastDateList = pythonDateListLast7+pythonDateListFuture
			#Now we convert all the python datetime objects into matplotlib date format
			dates = matplotlib.dates.date2num(pythonDateList)
			forecastDates = matplotlib.dates.date2num(pythonForecastDateList)



			#We then access the selected feature column and copy its entire row into y.
			string =self.featuresListWidget.currentItem().text()
			y= shareData[string]

			xValArray = shareData[string].values
			print(xValArray)
			train = xValArray[0:len(xValArray)-7]#This may yield an array index out of bounds error if xValArray is size<5 so try fix it later
			#test= xValArray[26:]




			print(self.comboBox.currentText())
			print(self.featuresListWidget.currentItem().text())
			try:

				model_arima = ARIMA(train,order=(self.pVal,self.dVal,self.qVal))
				print("got past Arima(train,order=(2,1,1))")
				model_arima_fit = model_arima.fit()
				print("got past model_arima.fit()")

				forcasted=[]
				forcasted= model_arima_fit.forecast(steps=self.forecastLength)[0]           #What is this zero here meant to signify
				print("got past forecast")

				rmse = self.rootMeanSquareError(forcasted,xValArray)
				print("RMSE calculated:")
				print(rmse)

				forecastUpperError=[]
				forecastLowerError=[]
				
				
				for i in range(0,len(forcasted)):
					
				
					forecastUpperError.append(forcasted[i]+rmse +self.exponentiate(i))
					forecastLowerError.append(forcasted[i]-rmse -self.exponentiate(i))
					


				print("after")
				print(forecastUpperError)
				#Plot of y vs dates is now created below
				fig, ax =plt.subplots()#Fig must be deleted  later so as not consume memory
				#color='#1AB1ED' for blue
				#ax.plot(y,linewidth=4,color='#BF1AED')
				ax.plot_date(dates,y,linewidth = 3,color=colourString,fmt='-',label="Actual Data")
				ax.plot_date(forecastDates,forcasted,linewidth = 3,color='#1AB1ED',fmt='-', label="Forecasted")
				ax.plot_date(forecastDates,forecastUpperError,linewidth = 3,color='#ff0066',fmt='--', label="Error")
				ax.plot_date(forecastDates,forecastLowerError,linewidth = 3, color='#ff0066', fmt='--')
				plt.legend(loc="upper right")
				ax.grid(linestyle="--")
				ax.patch.set_facecolor('#282828')
				fig.patch.set_facecolor("None")
				#fig.patch.set_alpha(0.0)
				#ax.patch.set_alpha(0.0)
				ax.spines['bottom'].set_color('#ffffff')
				ax.spines['top'].set_color('#ffffff')
				ax.spines['right'].set_color('#ffffff')
				ax.spines['left'].set_color('#ffffff')
				ax.tick_params(axis='x', colors='#ffffff')
				ax.tick_params(axis='y', colors='#ffffff')
				ax.set_xlabel("Date",fontsize=15)
				ax.set_ylabel(self.featuresListWidget.currentItem().text(),fontsize=15)
				fig.suptitle(self.comboBox.currentText(),fontsize=20,color='white')
				ax.yaxis.label.set_color('white')
				ax.xaxis.label.set_color('white')

				#fig.savefig('temp.png', transparent=True)

				self.plotWidget = FigureCanvas(fig)#FigureCanvas is an matplotlib object that can act as a pyqt5 widget
				self.plotWidget.setStyleSheet("background-color:transparent;")
				self.rightFrameGridLayout.addWidget(self.plotWidget)

			except LinAlgError as err:

				print(err)

				alertMessage=QMessageBox()
				alertMessage.setWindowTitle("Data Invalid")
				alertMessage.setText("The Singular Value Decomposition(SVG) did not converge.\nPlease choose a different model order or data set")
				alertMessage.setIcon(QMessageBox.Warning)
				alertMessage.setWindowIcon(QIcon("Logo.ico"))
				x=alertMessage.exec_()

				self.plotEmptyAxis()

			except ValueError as err:

				alertMessage=QMessageBox()
				alertMessage.setWindowTitle("Data Invalid")
				alertMessage.setText("The Singular Value Decomposition(SVG) did not converge.\nPlease choose a different model order or data set")
				alertMessage.setIcon(QMessageBox.Warning)
				alertMessage.setWindowIcon(QIcon("Logo.ico"))
				x=alertMessage.exec_()

				self.plotEmptyAxis()
				print(err)
			#right.setLayout(self.rightFrameGridLayout)



	def logoutButtonClicked (self):

		self.next=Login()
		self.next.showMaximized()
		self.close()

class Register(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowIcon(QIcon("Logo.ico"))
		self.setStyleSheet('''
						 QLabel{
						 font-size: 20px;
						 }
						''')
		self.initUi()

	def initUi(self):

		
		outerFrame = QtWidgets.QFrame()
		outerFrame.setFrameShape(QFrame.Panel)
		outerFrame.setFrameShadow(QFrame.Raised)
		outerFrameLayout = QHBoxLayout()

		outerFrame.setLayout(outerFrameLayout)
		outerFrameLayout.setSpacing(10)
		#outerFrameLayout.setContentsMargins(20,20,20,20)# Left top right then bottom

		frameDouble = QtWidgets.QFrame()
		doubleFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		doubleFrameSizePolicy.setHorizontalStretch(1)
		frameDouble.setSizePolicy(doubleFrameSizePolicy)

		frameDoubleVLayout = QVBoxLayout()
		frameDouble.setLayout(frameDoubleVLayout)

		innerFrame = QtWidgets.QFrame(self,objectName="innerFrame")
		innerFrame.setFrameShape(QFrame.Panel)
		innerFrame.setFrameShadow(QFrame.Raised)
		innerFrameLayout= QVBoxLayout()
		innerFrameLayout.setSpacing(15)
		innerFrameLayout.setContentsMargins(1,1,1,1)
		innerFrame.setLayout(innerFrameLayout)

		
		formBlock = QtWidgets.QWidget()
		formBlockSizePolicy =QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
		formBlock.setSizePolicy(formBlockSizePolicy)
		formBlockLayout = QGridLayout()
		formBlockLayout.setSpacing(15)
		formBlock.setLayout(formBlockLayout)



		loginLabel= QtWidgets.QLabel("STC2",objectName="loginLabel")
		loginLabel.setAlignment(Qt.AlignCenter)
		loginLabel.setStyleSheet("""font-size: 80px;""")
		loginLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)
		loginLabel.setSizePolicy(loginLabelSizePolicy)

		

		#Makes logo label and places logo image inside it
		logoLabel = QtWidgets.QLabel()
		logoLabel.setStyleSheet("""background: rgba(90,90,90,0);
									border-color: rgba(140,140,140,0);""")
		logoLabelSizePolicy=QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)#Horizontal,vertical
		logoLabel.setSizePolicy(logoLabelSizePolicy)
		pixmap = QPixmap("logotest.png")
		logoLabel.setPixmap(pixmap)
		logoLabel.setAlignment(Qt.AlignCenter)

		widgetUsername = QtWidgets.QWidget(objectName="groupWidget")#below border-radius 35px works but onnly for username

		widgetUsernameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetUsername.setSizePolicy(widgetUsernameSizePolicy)
		usernameLayout = QHBoxLayout()
		widgetUsername.setLayout(usernameLayout)
		bodyShadow = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow.setBlurRadius(9.0)
		bodyShadow.setColor(QColor(0, 0, 0, 160))
		bodyShadow.setOffset(-2)
		widgetUsername.setGraphicsEffect(bodyShadow)


		widgetEmail = QtWidgets.QWidget(objectName="groupWidget")
		
		widgetEmailSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetEmail.setSizePolicy(widgetEmailSizePolicy)
		emailLayout = QHBoxLayout()
		widgetEmail.setLayout(emailLayout)
		bodyShadow1 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow1.setBlurRadius(9.0)
		bodyShadow1.setColor(QColor(0, 0, 0, 160))
		bodyShadow1.setOffset(-2)
		widgetEmail.setGraphicsEffect(bodyShadow1)


		widgetPassword = QtWidgets.QWidget(objectName="groupWidget")
		
		widgetPasswordSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetPassword.setSizePolicy(widgetPasswordSizePolicy)
		passwordLayout = QHBoxLayout()
		widgetPassword.setLayout(passwordLayout)
		bodyShadow2 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow2.setBlurRadius(9.0)
		bodyShadow2.setColor(QColor(0, 0, 0, 160))
		bodyShadow2.setOffset(-2)
		widgetPassword.setGraphicsEffect(bodyShadow2)

		widgetConfirmPassword = QtWidgets.QWidget(objectName="groupWidget")
		
		widgetConfirmPasswordSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetConfirmPassword.setSizePolicy(widgetConfirmPasswordSizePolicy)
		confirmPasswordLayout = QHBoxLayout()
		widgetConfirmPassword.setLayout(confirmPasswordLayout)
		bodyShadow3 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow3.setBlurRadius(9.0)
		bodyShadow3.setColor(QColor(0, 0, 0, 160))
		bodyShadow3.setOffset(-2)
		widgetConfirmPassword.setGraphicsEffect(bodyShadow3)
	
		self.usernameLineEdit = QtWidgets.QLineEdit()
		
		self.usernameLineEdit.setPlaceholderText("Username")

		self.emailAddressLineEdit = QtWidgets.QLineEdit()
		
		self.emailAddressLineEdit.setPlaceholderText("Email Address") 

		self.passwordLineEdit=QtWidgets.QLineEdit()
		self.passwordLineEdit.setPlaceholderText("Password") 
		self.passwordLineEdit.setEchoMode(2)
	

		self.confirmPasswordLineEdit=QtWidgets.QLineEdit()
		self.confirmPasswordLineEdit.setPlaceholderText("Confirm Password") 
		self.confirmPasswordLineEdit.setEchoMode(2)
		
		

		usernameLogoLabel = QtWidgets.QLabel()
		usernameLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											padding:5px;
											border-radius: 19px;""")
		usernameLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical
		usernameLogoLabel.setSizePolicy(usernameLogoLabelSizePolicy)
		pixmap = QPixmap("account32px.png")
		usernameLogoLabel.setPixmap(pixmap)
		usernameLogoLabel.setAlignment(Qt.AlignCenter)

		emailLogoLabel = QtWidgets.QLabel()
		emailLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											padding:5px;
											border-radius: 19px;""")
		emailLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		emailLogoLabel.setSizePolicy(emailLogoLabelSizePolicy)
		pixmap = QPixmap("email32px.png")
		emailLogoLabel.setPixmap(pixmap)
		emailLogoLabel.setAlignment(Qt.AlignCenter)


		passwordLogoLabel = QtWidgets.QLabel()
		passwordLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											padding:5px;
											border-radius: 19px;""")
		passwordLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		passwordLogoLabel.setSizePolicy(passwordLogoLabelSizePolicy)
		pixmap = QPixmap("lock32px.png")
		passwordLogoLabel.setPixmap(pixmap)
		passwordLogoLabel.setAlignment(Qt.AlignCenter)

		confirmPasswordLogoLabel = QtWidgets.QLabel()
		confirmPasswordLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											padding:5px;
											border-radius: 19px;""")
		confirmPasswordLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		confirmPasswordLogoLabel.setSizePolicy(confirmPasswordLogoLabelSizePolicy)
		pixmap = QPixmap("lock32px.png")
		confirmPasswordLogoLabel.setPixmap(pixmap)
		confirmPasswordLogoLabel.setAlignment(Qt.AlignCenter)

		usernameLayout.addWidget(usernameLogoLabel)
		usernameLayout.addWidget(self.usernameLineEdit)
		emailLayout.addWidget(emailLogoLabel)
		emailLayout.addWidget(self.emailAddressLineEdit)
		passwordLayout.addWidget(passwordLogoLabel)
		passwordLayout.addWidget(self.passwordLineEdit)
		confirmPasswordLayout.addWidget(confirmPasswordLogoLabel)
		confirmPasswordLayout.addWidget(self.confirmPasswordLineEdit)

		showPasswordCheck=QtWidgets.QCheckBox("Show Password")
		

		registerButton = QtWidgets.QPushButton("Register")
		registerButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		registerButton.setSizePolicy(registerButtonSizePolicy)
		#max-height:35px;
		registerButton.setStyleSheet("""	QPushButton{font-size: 15px;
										color: rgba(60,70,89,225);
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(188, 192, 204,200), stop:1 rgba(205,208,220,225));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(240,240,240,200);
										border-radius: 16px;
										min-height:30px;
										}
										QPushButton:hover {
    									background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(205,208,220,225), stop:1 rgba(188, 192, 204,200));
											}
										QPushButton:pressed {
    									background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(185,188,200,225), stop:1 rgba(168, 172, 184,200));  
										border-style: inset;  
											}
										""")
		bodyShadow4 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow4.setBlurRadius(9.0)
		bodyShadow4.setColor(QColor(0, 0, 0, 160))
		bodyShadow4.setOffset(-2)
		registerButton.setGraphicsEffect(bodyShadow4)
		registerButton.clicked.connect(self.registerButtonClicked)

		returnButton = QtWidgets.QPushButton("Return to Mainpage")
		returnButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		returnButton.setSizePolicy(returnButtonSizePolicy)
		returnButton.setStyleSheet("""	QPushButton{font-size: 15px;
										color: rgba(60,70,89,225);
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(188, 192, 204,200), stop:1 rgba(205,208,220,225));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(240,240,240,200);
										border-radius: 16px;
										min-height:30px;
										}
										QPushButton:hover {
    									background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(205,208,220,225), stop:1 rgba(188, 192, 204,200));
											}
										QPushButton:pressed {
    									background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(185,188,200,225), stop:1 rgba(168, 172, 184,200));  
										border-style: inset;  
											}
										""")
		bodyShadow5 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow5.setBlurRadius(9.0)
		bodyShadow5.setColor(QColor(0, 0, 0, 160))
		bodyShadow5.setOffset(-2)
		returnButton.setGraphicsEffect(bodyShadow5)
		returnButton.clicked.connect(self.returnButtonClicked)


		formBlockLayout.addWidget(widgetUsername,0,0,1,2)

		formBlockLayout.addWidget(widgetEmail,1,0,1,2)

		formBlockLayout.addWidget(widgetPassword,2,0,1,2)

		formBlockLayout.addWidget(widgetConfirmPassword,3,0,1,2)

		formBlockLayout.addWidget(showPasswordCheck,4,0,1,2,Qt.AlignRight)
		formBlockLayout.addWidget(registerButton,5,0,1,1)
		formBlockLayout.addWidget(returnButton,5,1,1,1)
		

		innerFrameLayout.addWidget(logoLabel,Qt.AlignCenter)
		innerFrameLayout.addWidget(formBlock)

		
		frameDoubleVLayout.addWidget(loginLabel,Qt.AlignCenter)
		frameDoubleVLayout.addWidget(innerFrame,Qt.AlignCenter)
		outerFrameLayout.insertStretch(0,1)
		outerFrameLayout.addWidget(frameDouble)
		outerFrameLayout.addStretch(1)
		

		mainGrid = QGridLayout()
		mainGrid.setSpacing(10)
		mainGrid.addWidget(outerFrame)


		outerWidgetBox=QtWidgets.QWidget()
		outerWidgetBox.setLayout(mainGrid)

		self.setCentralWidget(outerWidgetBox)		
		self.setWindowTitle("Register")
		self.setMinimumSize(900, 700);
		self.showMaximized()


	def registerButtonClicked(self):

		
		inUserName= self.usernameLineEdit.text()
		inUserPassword = self.passwordLineEdit.text()
		inUserEmail = self.emailAddressLineEdit.text()
		hashUserPassword = bcrypt.hashpw(inUserPassword.encode('utf-8'), bcrypt.gensalt())

		if(len(inUserPassword)==0 or len(inUserName)==0):

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Registration Failed")
			alertMessage.setText("Please enter a username, password and email address to register.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			return

		server = SSHTunnelForwarder(
			'146.141.21.92',
			ssh_username='s1533169',
			ssh_password='dingun123',
			remote_bind_address=('127.0.0.1', 3306)
		)
		server.start()

		print("Got here")


		mydb =mysql.connector.connect(host="localhost",user="s1533169",passwd="dingun123" ,port=server.local_bind_port)
		mycursor= mydb.cursor()

		mycursor.execute("USE d1533169")
		print(inUserName)
		print(":::test")
		mycursor.execute("SELECT * FROM ARIMA_USERS WHERE USERNAME=%s",(inUserName.strip(),))
		myresult=mycursor.fetchall()
		print("fetchall result")
		print(myresult)

		if(len(myresult)==0):

			sqlInsertCommand ="INSERT INTO ARIMA_USERS VALUES(%s,%s,%s)"
			usernamePasswordPair=(inUserName,hashUserPassword,inUserEmail)
			mycursor.execute(sqlInsertCommand,usernamePasswordPair)

			mydb.commit()

			print("got past create table")
			mydb.close()
			print("got past mydb.close")
			server.close()


			self.next=MyWindow()
			self.next.showMaximized()
			self.close()
		else:

			mydb.close()
			server.close()
			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Registration Failed")
			alertMessage.setText("The username you have requested already exists. Please try another one.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			print("UserName already exists, Please try another")
			print("got past create table")

	def returnButtonClicked(self):

		self.next=Login()
		self.next.showMaximized()
		self.close()



class Login(QMainWindow):

	def __init__(self):#Constructor for the login page. All the construction takes place in self.initUi()
	#background: qradialgradient(cx: 0.5, cy: 0.5, radius: 2, fx: 0.5, fy: 0.5, stop: 0 rgba(228,107,60,50) , stop: 0.2 rgba(25,25,25,255) , stop: 0.4 rgba(55,55,55,255) );
	#background-image: url(b7.jpg);
		super().__init__()
		self.setWindowIcon(QIcon("Logo.ico"))
		self.setStyleSheet('''	
						QLabel{
						font-size: 20px;
						}	
						''')
		self.initUi()

	def initUi(self) :

		outerFrame = QtWidgets.QFrame()
		outerFrame.setFrameShape(QFrame.Panel)
		outerFrame.setFrameShadow(QFrame.Raised)
		outerFrameLayout = QHBoxLayout()

		outerFrame.setLayout(outerFrameLayout)
		#outerFrameLayout.setSpacing(10)
		#outerFrameLayout.setContentsMargins(20,20,20,20)# Left top right then bottom

		frameDouble = QtWidgets.QFrame()
		doubleFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		doubleFrameSizePolicy.setHorizontalStretch(1)
		frameDouble.setSizePolicy(doubleFrameSizePolicy)

		frameDoubleVLayout = QVBoxLayout()
		frameDouble.setLayout(frameDoubleVLayout)

		innerFrame = QtWidgets.QFrame(objectName="innerFrame")
		bodyShadowT = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadowT.setBlurRadius(15.0)
		bodyShadowT.setColor(QColor(0, 0, 0, 255))
		bodyShadowT.setOffset(0)
		innerFrame.setGraphicsEffect(bodyShadowT)

		innerFrameLayout= QVBoxLayout()
		innerFrameLayout.setSpacing(30)
		#innerFrameLayout.setContentsMargins(20,20,20,20)
		innerFrame.setLayout(innerFrameLayout)

		
		formBlock = QtWidgets.QWidget()
		formBlockSizePolicy =QSizePolicy(QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)
		formBlock.setSizePolicy(formBlockSizePolicy)
		formBlockLayout = QGridLayout()
		formBlockLayout.setSpacing(15)
		formBlock.setLayout(formBlockLayout)



		loginLabel= QtWidgets.QLabel("STC2")
		loginLabel.setAlignment(Qt.AlignCenter)
		loginLabel.setStyleSheet("""font-size: 80px;""")
		loginLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)
		loginLabel.setSizePolicy(loginLabelSizePolicy)

		

		#Makes logo label and places logo image inside it
		logoLabel = QtWidgets.QLabel()
		logoLabel.setStyleSheet("""background: rgba(90,90,90,0);
									border-color: rgba(140,140,140,0);""")
		logoLabelSizePolicy=QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)#Horizontal,vertical
		logoLabel.setSizePolicy(logoLabelSizePolicy)
		pixmap = QPixmap("logotest.png")
		logoLabel.setPixmap(pixmap)
		logoLabel.setAlignment(Qt.AlignCenter)

		widgetUsername = QtWidgets.QWidget(objectName="groupWidget")
		widgetUsernameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetUsername.setSizePolicy(widgetUsernameSizePolicy)
		widgetUsername.setFocusPolicy(Qt.StrongFocus)
		usernameLayout = QHBoxLayout()

		widgetUsername.setLayout(usernameLayout)
		bodyShadow = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow.setBlurRadius(9.0)
		bodyShadow.setColor(QColor(0, 0, 0, 160))
		bodyShadow.setOffset(-2)
		widgetUsername.setGraphicsEffect(bodyShadow)

		widgetPassword = QtWidgets.QWidget(objectName="groupWidget")		
		widgetPasswordSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)#Horizontal,vertical
		widgetPassword.setSizePolicy(widgetPasswordSizePolicy)
		passwordLayout = QHBoxLayout()
		widgetPassword.setLayout(passwordLayout)
		bodyShadow2 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow2.setBlurRadius(9.0)
		bodyShadow2.setColor(QColor(0, 0, 0, 160))
		bodyShadow2.setOffset(-2)
		widgetPassword.setGraphicsEffect(bodyShadow2)
	
		self.usernameLineEditLogin = QtWidgets.QLineEdit()
		usernameLineEditSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)#Horizontal,vertical
		self.usernameLineEditLogin.setSizePolicy(logoLabelSizePolicy)
		
		self.usernameLineEditLogin.setPlaceholderText("Username") 

		self.passwordLineEditLogin=QtWidgets.QLineEdit()
		self.passwordLineEditLogin.setPlaceholderText("Password") 
		
		
		self.passwordLineEditLogin.setEchoMode(2)

		usernameLogoLabel = QtWidgets.QLabel()
		usernameLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											padding:5px;
											border-radius: 19px;""")
		usernameLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical
		usernameLogoLabel.setSizePolicy(usernameLogoLabelSizePolicy)

		pixmap = QPixmap("account32px.png")
		usernameLogoLabel.setPixmap(pixmap)
		usernameLogoLabel.setAlignment(Qt.AlignCenter)

		passwordLogoLabel = QtWidgets.QLabel()
		passwordLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											padding:5px;
											border-radius: 19px;""")
		passwordLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		passwordLogoLabel.setSizePolicy(passwordLogoLabelSizePolicy)

		pixmap = QPixmap("lock32px.png")
		passwordLogoLabel.setPixmap(pixmap)
		passwordLogoLabel.setAlignment(Qt.AlignCenter)


		usernameLayout.addWidget(usernameLogoLabel)
		usernameLayout.addWidget(self.usernameLineEditLogin)
		passwordLayout.addWidget(passwordLogoLabel)
		passwordLayout.addWidget(self.passwordLineEditLogin)
		self.showPasswordCheck=QtWidgets.QCheckBox("Show Password")
		self.showPasswordCheck.stateChanged.connect(self.showPasswordChecked)

		loginButton = QtWidgets.QPushButton("Login",objectName="button")
		loginButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		loginButton.setSizePolicy(loginButtonSizePolicy)
		#min-height:65px;
		#max-height:68px;
		loginButton.setStyleSheet("""min-height:45px;
									
									font-size: 25px;
									border-radius: 20px;""")
		loginButton.clicked.connect(self.loginButtonFunction)
		bodyShadow3 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow3.setBlurRadius(9.0)
		bodyShadow3.setColor(QColor(0, 0, 0, 160))
		bodyShadow3.setOffset(-2)
		loginButton.setGraphicsEffect(bodyShadow3)

		forgotButton = QtWidgets.QPushButton("Forgot Password?",objectName="button")
		forgotButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		forgotButton.setSizePolicy(forgotButtonSizePolicy)
		bodyShadow4 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow4.setBlurRadius(9.0)
		bodyShadow4.setColor(QColor(0, 0, 0, 160))
		bodyShadow4.setOffset(-2)
		forgotButton.setGraphicsEffect(bodyShadow4)		
		forgotButton.clicked.connect(self.forgotPasswordClicked)



		registerButton = QtWidgets.QPushButton("Register",objectName="button")
		registerButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		registerButton.setSizePolicy(registerButtonSizePolicy)
		bodyShadow5 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow5.setBlurRadius(9.0)
		bodyShadow5.setColor(QColor(0, 0, 0, 160))
		bodyShadow5.setOffset(-2)
		registerButton.setGraphicsEffect(bodyShadow5)
		registerButton.clicked.connect(self.goRegisterButtonFunction)

		quitButton = QtWidgets.QPushButton("Quit Program",objectName="button")
		quitButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		quitButton.setSizePolicy(quitButtonSizePolicy)
		bodyShadow6 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow6.setBlurRadius(9.0)
		bodyShadow6.setColor(QColor(0, 0, 0, 160))
		bodyShadow6.setOffset(-2)
		quitButton.setGraphicsEffect(bodyShadow6)
		quitButton.clicked.connect(self.quitButtonFunction)


		formBlockLayout.addWidget(widgetUsername,0,0,1,2)

		
		formBlockLayout.addWidget(widgetPassword,1,0,1,2)
		formBlockLayout.addWidget(self.showPasswordCheck,2,0,1,2,Qt.AlignRight)
		formBlockLayout.addWidget(loginButton,3,0,1,2)
		formBlockLayout.addWidget(forgotButton,4,0,1,1)
		formBlockLayout.addWidget(registerButton,4,1,1,1)
		formBlockLayout.addWidget(quitButton,5,0,1,2)

		innerFrameLayout.addWidget(logoLabel,Qt.AlignCenter)
		innerFrameLayout.addWidget(formBlock)
		
		frameDoubleVLayout.addWidget(loginLabel,Qt.AlignCenter)
		frameDoubleVLayout.addWidget(innerFrame,Qt.AlignCenter)
		outerFrameLayout.insertStretch(0,1)
		outerFrameLayout.addWidget(frameDouble)
		outerFrameLayout.addStretch(1)
		

		mainGrid = QGridLayout()
		mainGrid.setSpacing(10)
		mainGrid.addWidget(outerFrame)


		outerWidgetBox=QtWidgets.QWidget()
		outerWidgetBox.setLayout(mainGrid)

		self.setCentralWidget(outerWidgetBox)
		#self.setGeometry(0,0,1500,900)
		self.setMinimumSize(900, 700);
		self.setWindowTitle("Login")

		self.showMaximized()

	def loginButtonFunction(self):

		if (True):

			self.next=MyWindow()
			self.next.showMaximized()
			self.close()
			return

		inUserName= self.usernameLineEditLogin.text()
		inUserPassword = self.passwordLineEditLogin.text()

		if(len(inUserPassword)==0 or len(inUserName)==0):

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Login Failed")
			alertMessage.setText("Please enter both a username and password to login.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			return



		server = SSHTunnelForwarder(
			'146.141.21.92',
			ssh_username='s1533169',
			ssh_password='dingun123',
			remote_bind_address=('127.0.0.1', 3306)
		)
		server.start()

		print("Got here")


		mydb =mysql.connector.connect(host="localhost",user="s1533169",passwd="dingun123" ,port=server.local_bind_port)
		mycursor= mydb.cursor()

		mycursor.execute("USE d1533169")
		print(inUserName)
		print(":::test")
		mycursor.execute("SELECT * FROM ARIMA_USERS WHERE USERNAME=%s",(inUserName.strip(),))
		myresult=mycursor.fetchall()
		print("fetchall result")
		print(myresult)


		if(len(myresult)==0):

			mydb.close()
			server.close()
			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Login Failed")
			alertMessage.setText("The username or password you entered is incorrect.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			print("The account you entered does not exist, Please try again")




		else:

			hashedPwd = myresult[0][1]
			hp = bcrypt.hashpw(inUserPassword.encode('utf8'), hashedPwd.encode('utf8'))

			if(hp == hashedPwd.encode('utf-8')):

				mydb.close()
				server.close()

				self.next=MyWindow()
				self.next.showMaximized()
				self.close()

			else:

				mydb.close()
				server.close()
				alertMessage=QMessageBox()
				alertMessage.setWindowTitle("Login Failed")
				alertMessage.setText("The username or password you entered is incorrect.")
				alertMessage.setIcon(QMessageBox.Information)
				alertMessage.setWindowIcon(QIcon("Logo.ico"))
				x=alertMessage.exec_()
				print("incorrect password, please try again")


	def showPasswordChecked(self):

		if (self.showPasswordCheck.isChecked()):

			self.passwordLineEditLogin.setEchoMode(0)

		else:

			self.passwordLineEditLogin.setEchoMode(2)	
		

	def goRegisterButtonFunction(self):

		self.next=Register()
		self.next.showMaximized()
		self.close()

	def forgotPasswordClicked(self):
		self.next=ForgotPage()
		self.next.showMaximized()
		self.close()
		print("Forgot password clicked")

	def quitButtonFunction(self):
		sys.exit()
		print("quit clicked")


class ForgotPage(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowIcon(QIcon("Logo.ico"))
		self.setStyleSheet('''		 
						 QLabel{
						 font-size: 20px;
						 }
						''')
		self.initUi()

	def initUi(self):

		
		outerFrame = QtWidgets.QFrame()
		outerFrame.setFrameShape(QFrame.Panel)
		outerFrame.setFrameShadow(QFrame.Raised)
		outerFrameLayout = QHBoxLayout()

		outerFrame.setLayout(outerFrameLayout)
		outerFrameLayout.setSpacing(10)
		outerFrameLayout.setContentsMargins(20,1,20,1)# Left top right then bottom

		frameDouble = QtWidgets.QFrame()
		doubleFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		doubleFrameSizePolicy.setHorizontalStretch(1)
		frameDouble.setSizePolicy(doubleFrameSizePolicy)

		frameDoubleVLayout = QVBoxLayout()
		frameDouble.setLayout(frameDoubleVLayout)

		innerFrame = QtWidgets.QFrame(self,objectName="innerFrame")
		innerFrame.setFrameShape(QFrame.Panel)
		innerFrame.setFrameShadow(QFrame.Raised)
		
		innerFrameLayout= QVBoxLayout()
		innerFrameLayout.setSpacing(1)
		innerFrameLayout.setContentsMargins(1,1,1,1)
		innerFrame.setLayout(innerFrameLayout)

		
		formBlock = QtWidgets.QWidget()
		formBlockSizePolicy =QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		formBlock.setSizePolicy(formBlockSizePolicy)
		formBlockLayout = QGridLayout()
		#formBlockLayout.setSpacing(1)
		formBlock.setLayout(formBlockLayout)



		loginLabel= QtWidgets.QLabel("Forgot it Huh?",objectName="loginLabel")
		loginLabel.setAlignment(Qt.AlignCenter)
		loginLabel.setStyleSheet("""font-size: 80px;""")
		loginLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)
		loginLabel.setSizePolicy(loginLabelSizePolicy)

		

		#Makes logo label and places logo image inside it
		logoLabel = QtWidgets.QLabel()
		logoLabel.setStyleSheet("""background: rgba(90,90,90,0);
									border-color: rgba(140,140,140,0);""")
		logoLabelSizePolicy=QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)#Horizontal,vertical
		logoLabel.setSizePolicy(logoLabelSizePolicy)
		pixmap = QPixmap("logotest.png")
		logoLabel.setPixmap(pixmap)
		logoLabel.setAlignment(Qt.AlignCenter)

		widgetExplanation = QtWidgets.QWidget(objectName="groupWidget")#below border-radius 35px works but onnly for username
	
		widgetExplanationSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetExplanation.setSizePolicy(widgetExplanationSizePolicy)
		explanationLayout = QHBoxLayout()
		widgetExplanation.setLayout(explanationLayout)
		explanationLabel = QtWidgets.QLabel("Type in your credentials below to reset your password. You will recieve an email \n                      confirmation if the procedure is successfull.")
		explanationLabel.setStyleSheet("""color: rgba(255,255,255,255);
													background:rgba(69, 83, 105,0);
													border-color: rgba(14,14,14,0);
													border-radius: 20px;
													font-size: 15px;""")
		explanationLayout.addWidget(explanationLabel)

		widgetUsername = QtWidgets.QWidget(objectName="groupWidget")#below border-radius 35px works but onnly for username
		widgetUsernameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetUsername.setSizePolicy(widgetUsernameSizePolicy)
		usernameLayout = QHBoxLayout()
		widgetUsername.setLayout(usernameLayout)
		bodyShadow = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow.setBlurRadius(9.0)
		bodyShadow.setColor(QColor(0, 0, 0, 160))
		bodyShadow.setOffset(-2)
		widgetUsername.setGraphicsEffect(bodyShadow)


		widgetEmail = QtWidgets.QWidget(objectName="groupWidget")
		widgetEmailSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetEmail.setSizePolicy(widgetEmailSizePolicy)
		emailLayout = QHBoxLayout()
		widgetEmail.setLayout(emailLayout)
		bodyShadow1 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow1.setBlurRadius(9.0)
		bodyShadow1.setColor(QColor(0, 0, 0, 160))
		bodyShadow1.setOffset(-2)
		widgetEmail.setGraphicsEffect(bodyShadow1)

		widgetPassword = QtWidgets.QWidget(objectName="groupWidget")
		widgetPasswordSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetPassword.setSizePolicy(widgetPasswordSizePolicy)
		passwordLayout = QHBoxLayout()
		widgetPassword.setLayout(passwordLayout)
		bodyShadow2 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow2.setBlurRadius(9.0)
		bodyShadow2.setColor(QColor(0, 0, 0, 160))
		bodyShadow2.setOffset(-2)
		widgetPassword.setGraphicsEffect(bodyShadow2)

		widgetConfirmPassword = QtWidgets.QWidget(objectName="groupWidget")
		
		widgetConfirmPasswordSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetConfirmPassword.setSizePolicy(widgetConfirmPasswordSizePolicy)
		confirmPasswordLayout = QHBoxLayout()
		widgetConfirmPassword.setLayout(confirmPasswordLayout)
		bodyShadow3 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow3.setBlurRadius(9.0)
		bodyShadow3.setColor(QColor(0, 0, 0, 160))
		bodyShadow3.setOffset(-2)
		widgetConfirmPassword.setGraphicsEffect(bodyShadow3)
	
		self.usernameLineEdit = QtWidgets.QLineEdit()
		
		self.usernameLineEdit.setPlaceholderText("Username")

		self.emailLineEdit = QtWidgets.QLineEdit()
		
		self.emailLineEdit.setPlaceholderText("Email Address") 

		self.passwordLineEdit=QtWidgets.QLineEdit()
		self.passwordLineEdit.setPlaceholderText("Password") 
		self.passwordLineEdit.setEchoMode(2)
	

		self.confirmPasswordLineEdit=QtWidgets.QLineEdit()
		self.confirmPasswordLineEdit.setPlaceholderText("Confirm Password") 
		self.confirmPasswordLineEdit.setEchoMode(2)
		

		usernameLogoLabel = QtWidgets.QLabel()
		usernameLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											border-radius: 19px;
											padding:5px;""")
		usernameLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical
		usernameLogoLabel.setSizePolicy(usernameLogoLabelSizePolicy)
		pixmap = QPixmap("account32px.png")
		usernameLogoLabel.setPixmap(pixmap)
		usernameLogoLabel.setAlignment(Qt.AlignCenter)

		emailLogoLabel = QtWidgets.QLabel()
		emailLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											border-radius: 19px;
											padding:5px;""")
		emailLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		emailLogoLabel.setSizePolicy(emailLogoLabelSizePolicy)
		pixmap = QPixmap("email32px.png")
		emailLogoLabel.setPixmap(pixmap)
		emailLogoLabel.setAlignment(Qt.AlignCenter)


		passwordLogoLabel = QtWidgets.QLabel()
		passwordLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											border-radius: 19px;
											padding:5px;""")
		passwordLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		passwordLogoLabel.setSizePolicy(passwordLogoLabelSizePolicy)
		pixmap = QPixmap("lock32px.png")
		passwordLogoLabel.setPixmap(pixmap)
		passwordLogoLabel.setAlignment(Qt.AlignCenter)

		confirmPasswordLogoLabel = QtWidgets.QLabel()
		confirmPasswordLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											border-radius: 19px;
											padding:5px;""")
		confirmPasswordLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		confirmPasswordLogoLabel.setSizePolicy(confirmPasswordLogoLabelSizePolicy)
		pixmap = QPixmap("lock32px.png")
		confirmPasswordLogoLabel.setPixmap(pixmap)
		confirmPasswordLogoLabel.setAlignment(Qt.AlignCenter)

		usernameLayout.addWidget(usernameLogoLabel)
		usernameLayout.addWidget(self.usernameLineEdit)
		emailLayout.addWidget(emailLogoLabel)
		emailLayout.addWidget(self.emailLineEdit)
		passwordLayout.addWidget(passwordLogoLabel)
		passwordLayout.addWidget(self.passwordLineEdit)
		confirmPasswordLayout.addWidget(confirmPasswordLogoLabel)
		confirmPasswordLayout.addWidget(self.confirmPasswordLineEdit)

		showPasswordCheck=QtWidgets.QCheckBox("Show Password")
		showPasswordCheck.setStyleSheet("""QCheckBox::indicator {
    										border: 3px solid #5A5A5A;
    										background: none;
											}
											
											""")

		resetButton = QtWidgets.QPushButton("Reset Password",objectName="button")
		resetButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		resetButton.setSizePolicy(resetButtonSizePolicy)
		bodyShadow4 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow4.setBlurRadius(9.0)
		bodyShadow4.setColor(QColor(0, 0, 0, 160))
		bodyShadow4.setOffset(-2)
		resetButton.setGraphicsEffect(bodyShadow4)
		resetButton.clicked.connect(self.resetButtonClicked)

		returnButton = QtWidgets.QPushButton("Return to Mainpage",objectName="button")
		returnButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		returnButton.setSizePolicy(returnButtonSizePolicy)
		bodyShadow5 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow5.setBlurRadius(9.0)
		bodyShadow5.setColor(QColor(0, 0, 0, 160))
		bodyShadow5.setOffset(-2)
		returnButton.setGraphicsEffect(bodyShadow5)
		
		returnButton.clicked.connect(self.returnButtonClicked)

		formBlockLayout.addWidget(widgetExplanation,0,0,1,2)
		formBlockLayout.addWidget(widgetUsername,1,0,1,2)

		formBlockLayout.addWidget(widgetEmail,2,0,1,2)

		formBlockLayout.addWidget(widgetPassword,3,0,1,2)

		formBlockLayout.addWidget(widgetConfirmPassword,4,0,1,2)

		formBlockLayout.addWidget(showPasswordCheck,5,0,1,2,Qt.AlignRight)
		formBlockLayout.addWidget(resetButton,6,0,1,1)
		formBlockLayout.addWidget(returnButton,6,1,1,1)
		

		innerFrameLayout.addWidget(logoLabel,Qt.AlignCenter)
		innerFrameLayout.addWidget(formBlock)

		
		frameDoubleVLayout.addWidget(loginLabel,Qt.AlignCenter)
		frameDoubleVLayout.addWidget(innerFrame,Qt.AlignCenter)
		outerFrameLayout.insertStretch(0,1)
		outerFrameLayout.addWidget(frameDouble)
		outerFrameLayout.addStretch(1)
		

		mainGrid = QGridLayout()
		mainGrid.setSpacing(10)
		mainGrid.addWidget(outerFrame)


		outerWidgetBox=QtWidgets.QWidget()
		outerWidgetBox.setLayout(mainGrid)
		self.setMinimumSize(900, 900);
		self.setCentralWidget(outerWidgetBox)		
		self.setWindowTitle("Forgot Password")
		self.showMaximized()


	def resetButtonClicked(self):

		print("regitster")
		inUserName = self.usernameLineEdit.text()
		inUserPassword = self.passwordLineEdit.text()
		inUserEmail = self.emailLineEdit.text()

		if(len(inUserEmail)==0 or len(inUserName)==0):

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Password Reset Failed")
			alertMessage.setText("Please enter a valid username and email address to login.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			return

		if(len(inUserPassword)==0):

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Password Reset Failed")
			alertMessage.setText("Please enter a new password.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			return


		server = SSHTunnelForwarder(
			'146.141.21.92',
			ssh_username='s1533169',
			ssh_password='dingun123',
			remote_bind_address=('127.0.0.1', 3306)
		)
		server.start()

		print("Got here")


		mydb =mysql.connector.connect(host="localhost",user="s1533169",passwd="dingun123" ,port=server.local_bind_port)
		mycursor= mydb.cursor()

		mycursor.execute("USE d1533169")
		print(inUserName)
		print(":::test")
		mycursor.execute("SELECT * FROM ARIMA_USERS WHERE USERNAME=%s",(inUserName.strip(),))
		myresult=mycursor.fetchall()
		print("fetchall result")
		print(myresult)


		if(len(myresult)==0):

			mydb.close()
			server.close()
			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Password Reset Failed")
			alertMessage.setText("The username or email address you entered is incorrect.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			print("The usernme or password is incorrect, Please try again.")

		elif(myresult[0][2] != inUserEmail):

			mydb.close()
			server.close()
			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Password Reset Failed")
			alertMessage.setText("The username or email address you entered is incorrect.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			print("The usernme or password is incorrect, Please try again.")


		else:

			hashedPwd = bcrypt.hashpw(inUserPassword.encode('utf-8'), bcrypt.gensalt())
			sqlInsertCommand ="UPDATE ARIMA_USERS SET PASSWORD = %s WHERE USERNAME = %s"	#(%s,%s,%s)"
			usernamePasswordPair=(hashedPwd,inUserName)
			mycursor.execute(sqlInsertCommand,usernamePasswordPair)

			mydb.commit()

			print("got past create table")
			mydb.close()
			print("got past mydb.close")
			server.close()

			sender_email = "scrapedthroughc2@gmail.com"
			receiver_email = inUserEmail
			password = "arimamodel1!"

			message = MIMEMultipart("alternative")
			message["Subject"] = "STC2 Password Reset"
			message["From"] = sender_email
			message["To"] = receiver_email

			# Create the plain-text and HTML version of your message
			text = """\
			Hi there,
			Thank you for using our product.
			Please click this link to reset your password:
			www.realpython.com"""
			html = """\
			<html>
			  <body>
			    <p>Hi there,<br><br>
			       You have just successfully reset your password! You can now login in with your new password. If this was not you, please send an email to ScrapedThroughC2@gmail.com
			       and we will get back to you as soon as possible to review your account activity.<br><br>
			       We hope that you are enjoying our product. If you should need any assistance, please either email ScrapedThroughC2@gmail.com
			       or call Nic (cell): 0832261920.<br><br>

			       Kind regards,<br><br>
			       The STC2 Team
			    </p>
			  </body>
			</html>
			"""

			# Turn these into plain/html MIMEText objects
			part1 = MIMEText(text, "plain")
			part2 = MIMEText(html, "html")

			# Add HTML/plain-text parts to MIMEMultipart message
			# The email client will try to render the last part first
			message.attach(part1)
			message.attach(part2)

			# Create secure connection with server and send email
			context = ssl.create_default_context()
			with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			    server.login(sender_email, password)
			    server.sendmail(
			        sender_email, receiver_email, message.as_string()
			    )

			print("Email sent to user.")

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Success!")
			alertMessage.setText("Your password has been successfully reset. A confirmation email has been sent to your email address. You can now login using your new password.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()
			print("Password successfully reset.")

			self.next=Login()
			self.next.showMaximized()
			self.close()

	def returnButtonClicked(self):
		self.next=Login()
		self.next.showMaximized()
		self.close()
		print("return")

def window() :
	app=QApplication(sys.argv)#required for all GUIs

	#Style of app and color theme are set below
	app.setStyle("fusion")

	dark_palette = QPalette()
	dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.WindowText, Qt.white)
	dark_palette.setColor(QPalette.Base, QColor(25,25,25))
	dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
	dark_palette.setColor(QPalette.ToolTipText, Qt.white)
	dark_palette.setColor(QPalette.Text, Qt.white)
	dark_palette.setColor(QPalette.Button, QColor(178, 182, 194))
	dark_palette.setColor(QPalette.ButtonText, Qt.white)
	dark_palette.setColor(QPalette.BrightText, Qt.red)
	#dark_palette.setColor(QPalette.Link,QColor(135, 189, 216) )
	dark_palette.setColor(QPalette.Highlight, QColor(135, 189, 216))
	dark_palette.setColor(QPalette.HighlightedText,Qt.black )#Was initially Qt.Black

	app.setPalette(dark_palette)
	#light blue 
	#button color orange QColor(228,107,60)
	#original highlight and link color QColor(42, 130, 218)
	#Style sheet of app is then set. Maybe add this to a new file if it gets too large
	# Original backgroun
	#background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
	#						stop:0 rgba(25,25,25,255), stop:1 rgba(55,55,55,255))

	#QCheckBox{
				#			font-size: 12px
				#		}

	#button max-height:35px;

	"""QCheckBox::indicator {
    										border: 1px solid #5A5A5A;
    										background: none;
											}
						QCheckBox::indicator:checked{
						image: url(dot10x10.png)
						}"""
	app.setStyleSheet('''
						QMainWindow{
						 border-image: url(b161.jpg);
						}
						QFrame#innerFrame{
						background: rgba(90,90,90,100);
						border-width: 1px;
						border-style: outset;
						border-color: rgba(130,130,130,100);
						border-radius: 35px;
						}
						QFrame#innerFrame2{
						background: rgba(90,90,90,50);
						border-width: 1px;
						border-style: outset;
						border-color: rgba(130,130,130,100);
						border-radius: 20px;
						}
						QWidget#groupWidget{
						background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(96,99,108,200), stop:1 rgba(133,131,142,200));
										border-width: 1px;
										border-style: outset;
										min-height:42px;
										border-color: rgba(140,140,140,100);
										border-radius: 29px;

						}
						QWidget#groupWidget:hover{
						background: rgba(60,60,60,255);

						}
						QWidget#groupWidget:focus{
						background: rgba(60,60,60,255);
						}
						
						QPushButton#button{

						min-height:30px;
						
						border-radius:16px;
						font-size: 15px;
						
						color: rgba(60,70,89,225);
						background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
						stop:0 rgba(178, 182, 194,200), stop:1 rgba(215,218,230,225));
						border-width: 1px;	
						border-style: outset;
						border-color: rgba(240,240,240,200);
						
						}
						QPushButton#button:hover {
    									background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(215,218,230,225), stop:1 rgba(178, 182, 194,200));
											}
						QPushButton#button:pressed {
    									background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(175,178,190,225), stop:1 rgba(158, 162, 174,200));  
										border-style: inset;  
											}
										
						QPushButton#button:focus {
							
							
							background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(175,178,190,225), stop:1 rgba(158, 162, 174,200));  
							border-style: inset;  	
							border-color: rgba(255,255,255,255);
							outline: none;

						}
						QPushButton {
							font-size: 15px
						}
						QLineEdit{
						color: rgba(255,255,255,255);
						background:rgba(69, 83, 105,0);
						border-color: rgba(14,14,14,0);
						border-radius: 20px;
						font-size: 15px;
						}
						QLabel{
							font-size: 12px
						}
						
						
						QMessageBox QPushButton{
							background: rgba(55,55,55,255);
						}

							''')

	win=Login()
	win.showMaximized()
	sys.exit(app.exec_())#executes the main loop



#This is the first line of code that is run by the interpreter and will initiate the execution of the program
window()


#Ignore this comment
'''QCheckBox:indicator{

							border-width: 1px;
							border-style: ridge;
							border-color: rgb(42,130,218);
							border-radius: 4px;

}'''

"""QPushButton#button:focus{
    					background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
						stop:0 rgba(205, 202, 210,215), stop:1 rgba(225,228,230,225));
						border-width: 1px;
						border-style: outset;
						border-color: rgba(255,255,255,200);
						}"""