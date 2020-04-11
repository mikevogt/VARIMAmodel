from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame,QGridLayout, 
    QSplitter, QStyleFactory, QApplication,QVBoxLayout)
from PyQt5.QtCore import Qt
import sys

from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvas
import datetime


class MyWindow(QMainWindow):
	#MainWindow constructor. Most of the actual construction takes place in the function initUi(self) when it is called
	def __init__(self):
		
		super(MyWindow,self).__init__()#This can be written as super().__init__() i think which would make more sense but leave it as is for now
		self.data =pd.read_csv('ProcessedStandardised.csv',';')#Reads in the standardized data from ProcessedStandardised.csv. This file must be in the same directory as varimaGui.py
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

		for column in self.data.columns:#For loop that iterates through all column names in data populating the featuresListWidget
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
		#P value label and line edit created
		pValLabel=QtWidgets.QLabel("p-val: ")
		pValLineEdit = QtWidgets.QLineEdit()

		#Var button created
		varButton = QtWidgets.QPushButton("Estimate using VAR")
		varButton.clicked.connect(self.varButtonClicker)
		
		#Calculating errors label created
		calculatingErrorsLabel=QtWidgets.QLabel("Calculating Errors")

		#Check box  and line edit for sliding window created. The check box needs to be fixed so that it has a border around it. maybe use stylesheets to fix this
		slidingWindowCheckBox = QtWidgets.QCheckBox("Sliding Window")
		checkBoxLineEdit = QtWidgets.QLineEdit()

		#Start value label and line edit created
		startLabel = QtWidgets.QLabel("Start...")
		startLabelLineEdit = QtWidgets.QLineEdit()

		#no of forecast label and line edit created
		noForecastLabel = QtWidgets.QLabel("No. Forecast P...")
		noForecastLineEdit = QtWidgets.QLineEdit()

		#backTest button created
		backTestButton = QtWidgets.QPushButton("Back test for VARM")
		backTestButton.clicked.connect(self.backTestButtonClicker)

		#Now each item created above is added to the grid layout for the bottom left frame
		
		bottomLeftGridLayout.addWidget(pValLabel,0,0,1,1)
		bottomLeftGridLayout.addWidget(pValLineEdit,0,1,1,3)
		bottomLeftGridLayout.addWidget(varButton,1,0,1,4)
		bottomLeftGridLayout.addWidget(calculatingErrorsLabel,2,0,1,4)
		bottomLeftGridLayout.addWidget(slidingWindowCheckBox,3,0,1,1)
		bottomLeftGridLayout.addWidget(checkBoxLineEdit,3,1,1,3)
		bottomLeftGridLayout.addWidget(startLabel,4,0,1,1)
		bottomLeftGridLayout.addWidget(startLabelLineEdit,4,1,1,3)
		bottomLeftGridLayout.addWidget(noForecastLabel,5,0,1,1)
		bottomLeftGridLayout.addWidget(noForecastLineEdit,5,1,1,3)
		bottomLeftGridLayout.addWidget(backTestButton,6,0,2,4)
		
		
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

		#Now each on-button-click function is created

	def buttonImportFunction(self):
		#So far there is no purpose to this button however we may be able to think of one or replace it etc
		#self.data =pd.read_csv('ProcessedNonStandardised.csv',';')
		print("button import pressed")
		


	#Currently, this function does not perform a varima model on the selected stock and feature but rather plots the selected stock and feature
	def varButtonClicker(self):
		
		#self.featuresListWidget.currentItem().text() is the text of the item selected in the featuresList widget
		#self.comboBox.currentText() is the text of the item selected in the drop down list. namely the share

		if(self.featuresListWidget.currentItem() == None):
			#Makes sure a feature is selected. should maybe have this open an alert box instead of printing to the console
			#If this removed, program will crash if no item is selected
			print("No feature selected, please select one above")
			return
		
		

		if self.rightFrameGridLayout.itemAt(0) == None : #Checks if there is a plot already there
			

			shareData = self.data[self.data.Ticker == self.comboBox.currentText()] #Stores a dataFrame of all shares with the selected ticker
			
			dateColumn = shareData['DateStamps']# takes and stores all the required date stamps
			
			pythonDateList =[] #This will store all the date stamps from dateColumn in python datetime format

			for i in range (0,len(dateColumn)) :

				pythonDateList.append(datetime.datetime.strptime(str(dateColumn.iloc[i]),"%Y%m%d"))


			#Now we convert all the python datetime objects into matplotlib date format
			dates = matplotlib.dates.date2num(pythonDateList)
			#We then access the selected feature column and copy its entire row into y.
			string =self.featuresListWidget.currentItem().text()
			y= shareData[string]			
			
			#Plot of y vs dates is now created below
			fig, ax =plt.subplots()
			#color='#1AB1ED' for blue
			#ax.plot(y,linewidth=3,color='#BF1AED')
			ax.plot_date(dates,y,linewidth = 3,color='#BF1AED',fmt='-')
			
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

			#Now we convert all the python datetime objects into matplotlib date format
			dates = matplotlib.dates.date2num(pythonDateList)

			#We then access the selected feature column and copy its entire row into y.
			string =self.featuresListWidget.currentItem().text()
			y= shareData[string]
			
			#Plot of y vs dates is now created below
			fig, ax =plt.subplots()#Fig must be deleted  later so as not consume memory
			#color='#1AB1ED' for blue
			#ax.plot(y,linewidth=4,color='#BF1AED')
			ax.plot_date(dates,y,linewidth = 3,color='#BF1AED',fmt='-')

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
			#right.setLayout(self.rightFrameGridLayout)

	#This funnctions body was only used for test purposes and has the functionality of reverting back to the login screen
	def backTestButtonClicker (self):

		print("Back test button clicked successfully")
		
		self.next=Login()
		self.close()

#This is the class for the login page. This is the first page that is created when the app runs and quite obviously it still needs proper designing.
class Login(QMainWindow):

	def __init__(self):#Constructor for the login page. All the construction takes place in self.initUi()
		super().__init__()
		self.initUi()

	def initUi(self) :

		outerFrame = QtWidgets.QFrame()
		outerFrame.setFrameShape(QFrame.Panel)
		outerFrame.setFrameShadow(QFrame.Raised)
		outerFrameLayout = QVBoxLayout()
		outerFrameLayout.setSpacing(10)
		outerFrameLayout.setContentsMargins(500,20,500,20)# Left top right then bottom
		#Still need to try set innerframes minimum size to prevent it from being squashed when minimized

		innerFrame = QtWidgets.QFrame()
		innerFrame.setFrameShape(QFrame.Panel)
		innerFrame.setFrameShadow(QFrame.Raised)
		innerFrameLayout= QGridLayout(
			)
		innerFrameLayout.setSpacing(1)
		innerFrameLayout.setContentsMargins(10,200,10,200)
		innerFrame.setLayout(innerFrameLayout)

		loginLabel= QtWidgets.QLabel("Login",objectName="loginLabel")
		innerFrameLayout.addWidget(loginLabel,0,0,1,2)

		userNameLabel = QtWidgets.QLabel("Username")
		innerFrameLayout.addWidget(userNameLabel,1,0,1,2)

		usernameLineEdit = QtWidgets.QLineEdit("Please enter your username here")
		innerFrameLayout.addWidget(usernameLineEdit,2,0,1,2)


		passwordLabel = QtWidgets.QLabel("Password")
		innerFrameLayout.addWidget(passwordLabel,3,0,1,2)

		passwordLineEdit=QtWidgets.QLineEdit("Type your Password here")
		innerFrameLayout.addWidget(passwordLineEdit,4,0,1,2)

		loginButton = QtWidgets.QPushButton("Login")
		loginButton.clicked.connect(self.loginButtonFunction)
		innerFrameLayout.addWidget(loginButton,5,0,1,2,Qt.AlignCenter)



		outerFrameLayout.addWidget(innerFrame)
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

		self.next=MyWindow()
		self.next.showMaximized()
		self.close()

def window() :
	app=QApplication(sys.argv)#required for all GUIs
	
	#Style of app and color theme are set below
	app.setStyle("fusion")

	dark_palette = QPalette()
	dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.WindowText, Qt.white)
	dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
	dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
	dark_palette.setColor(QPalette.ToolTipText, Qt.white)
	dark_palette.setColor(QPalette.Text, Qt.white)
	dark_palette.setColor(QPalette.Button, QColor(228,107,60))
	dark_palette.setColor(QPalette.ButtonText, Qt.white)
	dark_palette.setColor(QPalette.BrightText, Qt.red)
	dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.HighlightedText, Qt.black)

	app.setPalette(dark_palette)

	#Style sheet of app is then set. Maybe add this to a new file if it gets too large
	app.setStyleSheet('''QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }
						
						QMainWindow{
						 background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                			stop:0 rgba(25,25,25,255), stop:1 rgba(55,55,55,255))
						
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
						QLabel:loginLabel{

							font-size: 30px
						}

						QLineEdit {

							border-width: 1px;
    						border-style: ridge;
   							border-color: rgb(42,130,218);
   							border-radius: 4px;
							
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
