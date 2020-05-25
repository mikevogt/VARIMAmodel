from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QFrame,QGridLayout,
	QSplitter, QStyleFactory, QApplication,QVBoxLayout,QStyle, QSizePolicy,QSpacerItem,QMessageBox)
from PyQt5.QtCore import Qt
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

import mysql.connector
from sshtunnel import SSHTunnelForwarder
from numpy.linalg import LinAlgError

import bcrypt

#from sklearn.metrics import mean_squared_error


class MyWindow(QMainWindow):
	#MainWindow constructor. Most of the actual construction takes place in the function initUi(self) when it is called
	def __init__(self):

		super(MyWindow,self).__init__()#This can be written as super().__init__() i think which would make more sense but leave it as is for now
		self.setWindowIcon(QIcon("logo4.ico"))
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
		self.setCentralWidget(widgetBox)
		self.setGeometry(0,0,1500,900)
		self.setWindowTitle("Varima Model")

		#Next, 3 QFrames are built to provide the primary framework of the window

		#############################################################################################################################################
		############################################## The top left frame is built and populated below below ########################################
		#############################################################################################################################################

		topLeft = QFrame(self,objectName="topLeft")#Objectname is only used for stylesheet purposes and hence is not needed for declaring most widgets
		topLeft.setFrameShape(QFrame.Panel)
		topLeft.setFrameShadow(QFrame.Raised)
		#builds layout for top left QFrame.
		gridTopLeft = QGridLayout(topLeft)
		gridTopLeft.setSpacing(10)
		topLeft.setLayout(gridTopLeft)

		#Widgets to be added to top left are made
		#import button made
		buttonImport= QtWidgets.QPushButton("Click herer",objectName="Button1")
		buttonImport.setText("Import Data")
		buttonImport.clicked.connect(self.buttonImportFunction)


		#Shares label is now made
		label1 = QtWidgets.QLabel("Shares")


		#comboBox is now made


		self.comboBox= QtWidgets.QComboBox()

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
		self.featuresListWidget.setAlternatingRowColors(True)

		for column in self.data.columns[3:-2]:#For loop that iterates through all column names in data populating the featuresListWidget
			#Still need to fix this so that it does not add the first 3 column names (namely DateStamps, Shares and Ticker) to the features list
			self.featuresListWidget.addItem(column)



		listWidgetGroupBox=QtWidgets.QGroupBox("Features")#Outer groupBox to house the features list widget
		listWidgetGroupBoxLayout=QtWidgets.QVBoxLayout()
		listWidgetGroupBox.setLayout(listWidgetGroupBoxLayout)
		listWidgetGroupBoxLayout.addWidget(self.featuresListWidget)#featuresListWidget is first added to the groupbox

		#All widgets are then added to the top left grid
		gridTopLeft.addWidget(buttonImport,0,0,1,4)
		gridTopLeft.addWidget(label1,1,0)
		gridTopLeft.addWidget(self.comboBox,1,1,1,3)
		gridTopLeft.addWidget(listWidgetGroupBox,2,0,4,4)# the groupbox (listWidgetGroupBox) is added to the top left grid completing the placement of the features list


		#############################################################################################################################################
		############################################### Bottom left frame is built and populated below ##############################################
		#############################################################################################################################################

		#builds bottom left QFrame and creates a grid layout for it
		bottomLeft = QFrame(self)
		bottomLeft.setFrameShape(QFrame.Panel)
		bottomLeft.setFrameShadow(QFrame.Raised)
		bottomLeftGridLayout= QGridLayout()
		bottomLeft.setLayout(bottomLeftGridLayout)

		#Next, each item in the bottom left frame is created without adding it to the layout just yet

		labelPlotCustomize = QtWidgets.QLabel("Customize Main Plot line:")

		labelPlotColour = QtWidgets.QLabel("Plot line colour:")

		self.radioButtonGreen = QtWidgets.QRadioButton("Green")
		self.radioButtonGreen.setStyle(QStyleFactory.create('windows'))
		self.radioButtonPurple = QtWidgets.QRadioButton("Purple")
		self.radioButtonPurple.setStyle(QStyleFactory.create('windows'))
		self.radioButtonOrange = QtWidgets.QRadioButton("Orange")
		self.radioButtonOrange.setStyle(QStyleFactory.create('windows'))

		buttonPlot = QtWidgets.QPushButton("Plot Data")
		buttonPlot.clicked.connect(self.plotDataClicked)

		labelArimaCustomize = QtWidgets.QLabel("Customize Arima Variables")

		labelPval= QtWidgets.QLabel("P-Value: ")
		lineEditPval = QtWidgets.QLineEdit()
		self.sliderPval = QtWidgets.QSlider(Qt.Horizontal)
		self.sliderPval.setMinimum(0)
		self.sliderPval.setMaximum(5)
		self.sliderPval.setValue(2)
		self.sliderPval.setTickPosition(3)
		self.sliderPval.setTickInterval(1)
		self.sliderPval.valueChanged.connect(self.sliderChangedPvalue)

		self.pValSpinBox = QtWidgets.QSpinBox()
		self.pValSpinBox.setValue(2)
		self.pValSpinBox.setMinimum(0)
		self.pValSpinBox.setMaximum(5)
		self.pValSpinBox.valueChanged.connect(self.spinboxChangedPvalue)

		labelDval= QtWidgets.QLabel("D-Value: ")
		lineEditDval = QtWidgets.QLineEdit()
		self.sliderDval = QtWidgets.QSlider(Qt.Horizontal)
		self.sliderDval.setMinimum(0)
		self.sliderDval.setMaximum(2)
		self.sliderDval.setValue(1)
		self.sliderDval.setTickPosition(3)
		self.sliderDval.setTickInterval(1)
		self.sliderDval.valueChanged.connect(self.sliderChangedDvalue)

		self.dValSpinBox = QtWidgets.QSpinBox()
		self.dValSpinBox.setValue(1)
		self.dValSpinBox.setMinimum(0)
		self.dValSpinBox.setMaximum(2)
		self.dValSpinBox.valueChanged.connect(self.spinboxChangedDvalue)

		labelQval= QtWidgets.QLabel("Q-Value: ")
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
		self.qValSpinBox.setValue(1)
		self.qValSpinBox.setMinimum(0)
		self.qValSpinBox.setMaximum(5)
		self.qValSpinBox.valueChanged.connect(self.spinboxChangedQvalue)

		labelForecastLength = QtWidgets.QLabel("forecastLength: ")
		lineEditForecastLength = QtWidgets.QLineEdit()


		self.dialSpinBox = QtWidgets.QSpinBox()
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

		buttonArima = QtWidgets.QPushButton("Estimate using ARIMA")
		buttonArima.clicked.connect(self.varButtonClicker)

		logoutButton = QtWidgets.QPushButton("Logout")
		logoutButton.clicked.connect(self.logoutButtonClicked)


		#Now each item created above is added to the grid layout for the bottom left frame

		bottomLeftGridLayout.addWidget(labelPlotCustomize,0,0,1,7)

		bottomLeftGridLayout.addWidget(labelPlotColour,1,0,1,1)
		bottomLeftGridLayout.addWidget(self.radioButtonPurple,1,1,1,2)
		bottomLeftGridLayout.addWidget(self.radioButtonGreen,1,3,1,2)
		bottomLeftGridLayout.addWidget(self.radioButtonOrange,1,5,1,2)

		bottomLeftGridLayout.addWidget(buttonPlot,2,0,1,7)

		bottomLeftGridLayout.addWidget(labelArimaCustomize,3,0,1,7)

		bottomLeftGridLayout.addWidget(labelPval,4,0,1,1)
		bottomLeftGridLayout.addWidget(self.pValSpinBox,4,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderPval,4,2,1,5)

		bottomLeftGridLayout.addWidget(labelDval,5,0,1,1)
		bottomLeftGridLayout.addWidget(self.dValSpinBox,5,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderDval,5,2,1,5)

		bottomLeftGridLayout.addWidget(labelQval,6,0,1,1)
		bottomLeftGridLayout.addWidget(self.qValSpinBox,6,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderQval,6,2,1,5)

		bottomLeftGridLayout.addWidget(labelForecastLength,7,0,1,1)
		bottomLeftGridLayout.addWidget(self.dialSpinBox,7,1,1,5)
		bottomLeftGridLayout.addWidget(self.dial,7,6,1,1)

		bottomLeftGridLayout.addWidget(buttonArima,8,0,1,7)
		bottomLeftGridLayout.addWidget(logoutButton,9,0,1,7)



		############################################################################################################################################
		################################################# Right frame is now built and populated ###################################################
		############################################################################################################################################

		#builds right QFrame and sets a grid layout for it
		right = QFrame(self)
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
		ax.patch.set_facecolor('#323232')
		fig.patch.set_facecolor('#191919')

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
		self.rightFrameGridLayout.addWidget(self.plotWidget)

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

		self.plotWidget = FigureCanvas(fig) #FigureCanvas is an matplotlib object that can act as a pyqt5 widget
		self.rightFrameGridLayout.addWidget(self.plotWidget)




	#Currently, this function does not perform a varima model on the selected stock and feature but rather plots the selected stock and feature
	def varButtonClicker(self):

		#self.featuresListWidget.currentItem().text() is the text of the item selected in the featuresList widget
		#self.comboBox.currentText() is the text of the item selected in the drop down list. namely the share

		colourString = "#BF1AED" #Default purple
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
				forecastUpperError = forcasted + rmse
				forecastLowerError = forcasted - rmse

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
				fig.suptitle(self.comboBox.currentText(),fontsize=20,color='white')
				ax.yaxis.label.set_color('white')
				ax.xaxis.label.set_color('white')

				#fig.savefig('temp.png', transparent=True)

				self.plotWidget = FigureCanvas(fig)#FigureCanvas is an matplotlib object that can act as a pyqt5 widget
				self.rightFrameGridLayout.addWidget(self.plotWidget)

			except LinAlgError as err:

				print(err)

				alertMessage=QMessageBox()
				alertMessage.setWindowTitle("Data Invalid")
				alertMessage.setText("The Singular Value Decomposition(SVG) did not converge.\nPlease choose a different model order or data set")
				alertMessage.setIcon(QMessageBox.Warning)
				alertMessage.setWindowIcon(QIcon("logo4.ico"))
				x=alertMessage.exec_()

				self.plotEmptyAxis()

			except ValueError as err:

				alertMessage=QMessageBox()
				alertMessage.setWindowTitle("Data Invalid")
				alertMessage.setText("The Singular Value Decomposition(SVG) did not converge.\nPlease choose a different model order or data set")
				alertMessage.setIcon(QMessageBox.Warning)
				alertMessage.setWindowIcon(QIcon("logo4.ico"))
				x=alertMessage.exec_()

				self.plotEmptyAxis()
				print(err)
			#right.setLayout(self.rightFrameGridLayout)



	def logoutButtonClicked (self):

		self.next=Login()
		self.next.showMaximized()
		self.close()

#This is the class for the login page. This is the first page that is created when the app runs and quite obviously it still needs proper designing.
class Register(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowIcon(QIcon("logo4.ico"))
		self.setStyleSheet('''
						QMainWindow{
						 background: qradialgradient(cx: 0.5, cy: 0.5, radius: 2, fx: 0.5, fy: 0.5, stop: 0 rgba(228,107,60,50) , stop: 0.2 rgba(25,25,25,255) , stop: 0.4 rgba(55,55,55,255) );
						 }
						 QLineEdit{
						 font-size: 20px;
						 border-width: 2px;
						 border-style: solid;
						 border-color: None None White None;
						 border-radius: 0px;
						 background: rgba(55,55,55,0);
						 }
						 QLabel:loginLabel{
						 font-size: 80px;
						 }
						 QLabel{
						 font-size: 20px;
						 }
						 QPushButton{
						 background: rgba(55,55,55,255);
						 }''')
		self.initUi()

	def initUi(self):

		outerFrame = QtWidgets.QFrame()
		outerFrame.setFrameShape(QFrame.Panel)
		outerFrame.setFrameShadow(QFrame.Raised)
		outerFrameLayout = QHBoxLayout()
		outerFrameLayout.setSpacing(10)
		outerFrameLayout.setContentsMargins(20,20,20,20)# Left top right then bottom
		#Still need to try set innerframes minimum size to prevent it from being squashed when minimized

		registrationLabel= QtWidgets.QLabel("Registration")
		registrationLabel.setAlignment(Qt.AlignCenter)
		registrationLabel.setStyleSheet("""font-size: 80px;""")
		registrationLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)
		registrationLabel.setSizePolicy(registrationLabelSizePolicy)



		innerFrame = QtWidgets.QFrame(self,objectName="innerFrameRegistration")
		innerFrame.setFrameShape(QFrame.Panel)
		innerFrame.setFrameShadow(QFrame.Raised)
		innerFrame.setStyleSheet("""QFrame{background: rgba(90,90,90,100);}""")


		innerFrameLayout= QGridLayout()
		innerFrameLayout.setSpacing(30)
		innerFrameLayout.setContentsMargins(20,20,20,20)
		innerFrame.setLayout(innerFrameLayout)

		explainLabel = QtWidgets.QLabel("Create an account by filling in the required fields below and \n                    then clicking Create Account button.")
		explainLabel.setStyleSheet("background: rgba(19,18,18,0);")
		explainLabelSP = QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		explainLabel.setSizePolicy(explainLabelSP)


		usernameLabel= QtWidgets.QLabel("Username:")
		usernameLabel.setStyleSheet("backGround: rgba(12,12,12,0);")
		self.usernameLineEdit=QtWidgets.QLineEdit()

		passwordLabel = QtWidgets.QLabel("Password:")
		passwordLabel.setStyleSheet("background: rgba(12,12,12,0)")
		self.passwordLineEdit = QtWidgets.QLineEdit()

		emailAddressLabel=QtWidgets.QLabel("Email Address:")
		emailAddressLabel.setStyleSheet("background: rgba(19,18,18,0);")
		self.emailAddressLineEdit= QtWidgets.QLineEdit()



		registerButton = QtWidgets.QPushButton("Create Account")
		registerButton.clicked.connect(self.registerButtonFunction)

		returnButton= QtWidgets.QPushButton("Return to Mainpage")
		returnButton.clicked.connect(self.returnButtonClicked)

		logo = QtWidgets.QLabel()
		logo.setStyleSheet("""background: rgba(90,90,90,0);""")
		logoSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		logo.setSizePolicy(logoSizePolicy)

		pixmap = QPixmap("logo4.ico")
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		innerFrameLayout.addWidget(logo,0,0,1,5,Qt.AlignCenter)

		innerFrameLayout.addWidget(explainLabel,1,0,1,5)

		innerFrameLayout.addWidget(usernameLabel,2,0,1,1,Qt.AlignCenter)
		innerFrameLayout.addWidget(self.usernameLineEdit,2,1,1,4)

		innerFrameLayout.addWidget(passwordLabel,3,0,1,1,Qt.AlignCenter)
		innerFrameLayout.addWidget(self.passwordLineEdit,3,1,1,4)

		innerFrameLayout.addWidget(emailAddressLabel,4,0,1,1,Qt.AlignCenter)
		innerFrameLayout.addWidget(self.emailAddressLineEdit,4,1,1,4)

		innerFrameLayout.addWidget(registerButton,5,0,1,5)
		innerFrameLayout.addWidget(returnButton,6,0,1,5)

		frameDouble = QtWidgets.QFrame()
		doubleFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		doubleFrameSizePolicy.setHorizontalStretch(1)
		frameDouble.setSizePolicy(doubleFrameSizePolicy)

		frameDoubleVLayout = QVBoxLayout()
		frameDouble.setLayout(frameDoubleVLayout)
		frameDoubleVLayout.addWidget(registrationLabel,Qt.AlignCenter)
		frameDoubleVLayout.addWidget(innerFrame,Qt.AlignCenter)

		outerFrameLayout.insertStretch(0,1)

		outerFrameLayout.addWidget(frameDouble)

		outerFrameLayout.addStretch(1)

		outerFrame.setLayout(outerFrameLayout)

		mainGrid = QGridLayout()
		mainGrid.setSpacing(10)
		mainGrid.addWidget(outerFrame)

		outerWidgetBox=QtWidgets.QWidget()
		outerWidgetBox.setLayout(mainGrid)


		self.setCentralWidget(outerWidgetBox)
		self.setGeometry(0,0,1500,900)
		self.setWindowTitle("Register")
		self.showMaximized()


	def registerButtonFunction(self):

		inUserName= self.usernameLineEdit.text()
		inUserPassword = self.passwordLineEdit.text()
		inUserEmail = self.emailAddressLineEdit.text()
		hashUserPassword = bcrypt.hashpw(inUserPassword.encode('utf-8'), bcrypt.gensalt())

		if(len(inUserPassword)==0 or len(inUserName)==0):

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Registration Failed")
			alertMessage.setText("Please enter a username, password and email address to register.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("logo4.ico"))
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
			alertMessage.setWindowIcon(QIcon("logo4.ico"))
			x=alertMessage.exec_()
			print("UserName already exists, Please try another")
			print("got past create table")


	def returnButtonClicked(self):

		self.next=Login()
		self.next.showMaximized()
		self.close()




class Login(QMainWindow):

	def __init__(self):#Constructor for the login page. All the construction takes place in self.initUi()
		super().__init__()
		self.setWindowIcon(QIcon("logo4.ico"))
		self.setStyleSheet('''
						QMainWindow{
						 background: qradialgradient(cx: 0.5, cy: 0.5, radius: 2, fx: 0.5, fy: 0.5, stop: 0 rgba(228,107,60,50) , stop: 0.2 rgba(25,25,25,255) , stop: 0.4 rgba(55,55,55,255) );
						 }
						 QLineEdit{
						 font-size: 20px;
						 border-width: 2px;
						 border-style: solid;
						 border-color: None None White None;
						 border-radius: 0px;
						 background: rgba(55,55,55,0);
						 }
						 QLabel:loginLabel{
						 font-size: 80px;
						 }
						 QLabel{
						 font-size: 20px;
						 }
						 QPushButton{
						 background: rgba(55,55,55,255);
						 }''')
		self.initUi()

	def initUi(self) :

		outerFrame = QtWidgets.QFrame()
		outerFrame.setFrameShape(QFrame.Panel)
		outerFrame.setFrameShadow(QFrame.Raised)
		outerFrameLayout = QHBoxLayout()
		outerFrameLayout.setSpacing(10)
		outerFrameLayout.setContentsMargins(20,20,20,20)# Left top right then bottom


		loginLabel= QtWidgets.QLabel("Welcome!",objectName="loginLabel")
		loginLabel.setAlignment(Qt.AlignCenter)
		loginLabel.setStyleSheet("""font-size: 100px;""")
		loginLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)
		loginLabel.setSizePolicy(loginLabelSizePolicy)

		innerFrame = QtWidgets.QFrame(self,objectName="innerFrameLogin")
		innerFrame.setFrameShape(QFrame.Panel)
		innerFrame.setFrameShadow(QFrame.Raised)
		innerFrame.setStyleSheet("""QFrame{background: rgba(90,90,90,100);}""")
		#innerFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		#innerFrameSizePolicy.setHorizontalStretch(1)
		#innerFrame.setSizePolicy(innerFrameSizePolicy)
		innerFrameLayout= QGridLayout()
		innerFrameLayout.setSpacing(30)
		innerFrameLayout.setContentsMargins(20,20,20,20)
		innerFrame.setLayout(innerFrameLayout)

		#Makes logo label and places logo image inside it
		logoLabel = QtWidgets.QLabel()
		logoLabel.setStyleSheet("""background: rgba(90,90,90,0);""")
		logoLabelSizePolicy=QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
		logoLabel.setSizePolicy(logoLabelSizePolicy)
		pixmap = QPixmap("logo4.ico")
		logoLabel.setPixmap(pixmap)
		logoLabel.setAlignment(Qt.AlignCenter)


		userNameLabel = QtWidgets.QLabel("Username:")
		userNameLabel.setStyleSheet("""background: rgba(90,90,90,0);""")
		self.usernameLineEditLogin = QtWidgets.QLineEdit()

		passwordLabel = QtWidgets.QLabel("Password:")
		passwordLabel.setStyleSheet("""background: rgba(90,90,90,0);""")
		self.passwordLineEditLogin=QtWidgets.QLineEdit()
		self.passwordLineEditLogin.setEchoMode(2)

		loginButton = QtWidgets.QPushButton("Login")
		loginButton.clicked.connect(self.loginButtonFunction)

		forgotPasswordButton = QtWidgets.QPushButton("Forgot Password?")
		forgotPasswordButton.clicked.connect(self.forgotPasswordClicked)

		goRegisterButton = QtWidgets.QPushButton("Create new Account")
		goRegisterButton.clicked.connect(self.goRegisterButtonFunction)

		quitProgramButton = QtWidgets.QPushButton("Quit Program")
		quitProgramButton.clicked.connect(self.quitButtonClicked)

		formBlock = QtWidgets.QWidget()
		formBlockSizePolicy =QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		formBlock.setSizePolicy(formBlockSizePolicy)
		formBlockLayout = QGridLayout()
		formBlock.setLayout(formBlockLayout)

		formBlockLayout.addWidget(userNameLabel,0,0)
		formBlockLayout.addWidget(self.usernameLineEditLogin,0,1)

		formBlockLayout.addWidget(passwordLabel,1,0)
		formBlockLayout.addWidget(self.passwordLineEditLogin,1,1)


		innerFrameLayout.addWidget(logoLabel,0,0,Qt.AlignCenter)
		innerFrameLayout.addWidget(formBlock,1,0)
		innerFrameLayout.addWidget(loginButton,2,0)
		innerFrameLayout.addWidget(forgotPasswordButton,3,0)
		innerFrameLayout.addWidget(goRegisterButton,4,0)
		innerFrameLayout.addWidget(quitProgramButton,5,0)


		frameDouble = QtWidgets.QFrame()
		doubleFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		doubleFrameSizePolicy.setHorizontalStretch(1)
		frameDouble.setSizePolicy(doubleFrameSizePolicy)

		frameDoubleVLayout = QVBoxLayout()
		frameDouble.setLayout(frameDoubleVLayout)
		frameDoubleVLayout.addWidget(loginLabel,Qt.AlignCenter)
		frameDoubleVLayout.addWidget(innerFrame,Qt.AlignCenter)

		outerFrameLayout.insertStretch(0,1)
		outerFrameLayout.addWidget(frameDouble)
		outerFrameLayout.addStretch(1)

		outerFrame.setLayout(outerFrameLayout)

		mainGrid = QGridLayout()
		mainGrid.setSpacing(10)
		mainGrid.addWidget(outerFrame)


		outerWidgetBox=QtWidgets.QWidget()
		outerWidgetBox.setLayout(mainGrid)

		self.setCentralWidget(outerWidgetBox)
		self.setGeometry(0,0,1500,900)
		self.setWindowTitle("Login")

		self.showMaximized()

	def loginButtonFunction(self):

		inUserName= self.usernameLineEditLogin.text()
		inUserPassword = self.passwordLineEditLogin.text()

		if(len(inUserPassword)==0 or len(inUserName)==0):

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Login Failed")
			alertMessage.setText("Please enter both a username and password to login.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("logo4.ico"))
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
		hashedPwd = myresult[0][1]
		hp = bcrypt.hashpw(inUserPassword.encode('utf8'), hashedPwd.encode('utf8'))

		if(len(myresult)==0):

			mydb.close()
			server.close()
			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("Login Failed")
			alertMessage.setText("The username or password you entered is incorrect.")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("logo4.ico"))
			x=alertMessage.exec_()
			print("The account you entered does not exist, Please try again")




		else:

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
				alertMessage.setWindowIcon(QIcon("logo4.ico"))
				x=alertMessage.exec_()
				print("incorrect password, please try again")





	def goRegisterButtonFunction(self):

		self.next=Register()
		self.next.showMaximized()
		self.close()

	def forgotPasswordClicked(self):
		self.next=ForgotPasswordPage()
		self.next.showMaximized()
		self.close()
		print("Forgot password clicked")

	def quitButtonClicked(self):

		sys.exit()

class ForgotPasswordPage(QMainWindow):

	def __init__(self):#Constructor for the login page. All the construction takes place in self.initUi()
		super().__init__()
		self.setWindowIcon(QIcon("logo4.ico"))
		self.setStyleSheet('''
						QMainWindow{
						 background: qradialgradient(cx: 0.5, cy: 0.5, radius: 2, fx: 0.5, fy: 0.5, stop: 0 rgba(228,107,60,50) , stop: 0.2 rgba(25,25,25,255) , stop: 0.4 rgba(55,55,55,255) );
						 }
						 QLineEdit{
						 font-size: 20px;
						 border-width: 2px;
						 border-style: solid;
						 border-color: None None White None;
						 border-radius: 0px;
						 background: rgba(55,55,55,0);
						 }
						 QLabel:loginLabel{
						 font-size: 80px;
						 }
						 QLabel{
						 font-size: 20px;
						 }
						 QPushButton{
						 background: rgba(55,55,55,255);
						 }''')

		self.initUi()

	def initUi(self) :

		outerFrame = QtWidgets.QFrame()
		outerFrame.setFrameShape(QFrame.Panel)
		outerFrame.setFrameShadow(QFrame.Raised)
		outerFrameLayout = QHBoxLayout()
		outerFrameLayout.setSpacing(10)
		outerFrameLayout.setContentsMargins(20,20,20,20)# Left top right then bottom
		#Still need to try set innerframes minimum size to prevent it from being squashed when minimized

		forgotItLabel= QtWidgets.QLabel("Forgot it Huh?")
		forgotItLabel.setAlignment(Qt.AlignCenter)
		forgotItLabel.setStyleSheet("""font-size: 80px;""")
		forgotItLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)
		forgotItLabel.setSizePolicy(forgotItLabelSizePolicy)

		innerFrame = QtWidgets.QFrame(self,objectName="innerFrameLogin")
		innerFrame.setFrameShape(QFrame.Panel)
		innerFrame.setFrameShadow(QFrame.Raised)
		innerFrame.setStyleSheet("""QFrame{background: rgba(90,90,90,100);}""")


		innerFrameLayout= QGridLayout()
		innerFrameLayout.setSpacing(30)
		innerFrameLayout.setContentsMargins(20,20,20,20)
		innerFrame.setLayout(innerFrameLayout)

		explainLabel = QtWidgets.QLabel("No worries, just type in your username and email Address below and we\n                               will have it sent to you shortly!")
		explainLabel.setStyleSheet("background: rgba(19,18,18,0);")
		explainLabelSP = QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		explainLabel.setSizePolicy(explainLabelSP)


		usernameLabel= QtWidgets.QLabel("Username:")
		usernameLabel.setStyleSheet("backGround: rgba(12,12,12,0);")
		usernameLineEdit=QtWidgets.QLineEdit()

		emailAddressLabel=QtWidgets.QLabel("Email Address:")
		emailAddressLabel.setStyleSheet("background: rgba(19,18,18,0);")
		emailAddressLineEdit= QtWidgets.QLineEdit()

		sendEmailButton = QtWidgets.QPushButton("Send Email")
		returnButton= QtWidgets.QPushButton("Return to Mainpage")
		returnButton.clicked.connect(self.returnButtonClicked)

		logo = QtWidgets.QLabel()
		logo.setStyleSheet("""background: rgba(90,90,90,0);""")
		logoSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		logo.setSizePolicy(logoSizePolicy)

		pixmap = QPixmap("logo4.ico")
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		innerFrameLayout.addWidget(logo,0,0,1,5,Qt.AlignCenter)
		innerFrameLayout.addWidget(explainLabel,1,0,1,5)
		innerFrameLayout.addWidget(usernameLabel,2,0,1,1,Qt.AlignCenter)
		innerFrameLayout.addWidget(usernameLineEdit,2,1,1,4)
		innerFrameLayout.addWidget(emailAddressLabel,3,0,1,1,Qt.AlignCenter)
		innerFrameLayout.addWidget(emailAddressLineEdit,3,1,1,4)
		innerFrameLayout.addWidget(sendEmailButton,4,0,1,5)
		innerFrameLayout.addWidget(returnButton,5,0,1,5)

		frameDouble = QtWidgets.QFrame()
		doubleFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		doubleFrameSizePolicy.setHorizontalStretch(1)
		frameDouble.setSizePolicy(doubleFrameSizePolicy)

		frameDoubleVLayout = QVBoxLayout()
		frameDouble.setLayout(frameDoubleVLayout)
		frameDoubleVLayout.addWidget(forgotItLabel,Qt.AlignCenter)
		frameDoubleVLayout.addWidget(innerFrame,Qt.AlignCenter)

		outerFrameLayout.insertStretch(0,1)
		#outerFrameLayout.addWidget(loginLabel,Qt.AlignCenter)

		outerFrameLayout.addWidget(frameDouble)

		outerFrameLayout.addStretch(1)

		outerFrame.setLayout(outerFrameLayout)

		mainGrid = QGridLayout()
		mainGrid.setSpacing(10)
		mainGrid.addWidget(outerFrame)

		outerWidgetBox=QtWidgets.QWidget()
		outerWidgetBox.setLayout(mainGrid)

		self.setCentralWidget(outerWidgetBox)
		self.setGeometry(0,0,1500,900)
		self.setWindowTitle("Forgot Password")

		self.showMaximized()

	def returnButtonClicked(self):

		self.next=Login()
		self.next.showMaximized()
		self.close()

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
	dark_palette.setColor(QPalette.Button, QColor(228,107,60))
	dark_palette.setColor(QPalette.ButtonText, Qt.white)
	dark_palette.setColor(QPalette.BrightText, Qt.red)
	dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.HighlightedText,Qt.black )#Was initially Qt.Black

	app.setPalette(dark_palette)

	#Style sheet of app is then set. Maybe add this to a new file if it gets too large
	app.setStyleSheet('''QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }
						QMainWindow{
						 background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
							stop:0 rgba(25,25,25,255), stop:1 rgba(55,55,55,255))
						}
						QMainWindow:loginPage{

						background-color: #2a82da
						}
						QPushButton {
							font-size: 15px
						}
						QLabel{
							font-size: 12px
						}
						QCheckBox{
							font-size: 12px
						}
						QLineEdit {
							border-width: 1px;
							border-style: ridge;
							border-color: rgb(42,130,218);
							border-radius: 4px;}
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
