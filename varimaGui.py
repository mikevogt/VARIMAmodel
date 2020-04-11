from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame,QGridLayout, 
    QSplitter, QStyleFactory, QApplication,QVBoxLayout)
from PyQt5.QtCore import Qt
import sys

from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvas 
#This is a test comment. I have added it whilst in the varButtonBranch
#Now this has been added locally whilst git was closed.

'''QCheckBox:indicator{

							border-width: 1px;
    						border-style: ridge;
   							border-color: rgb(42,130,218);
   							border-radius: 4px;

}'''


class MyWindow(QMainWindow):
	def __init__(self):#Dont understand how this line works
		
		super(MyWindow,self).__init__()# or this one but this can be written as super().__init__() i think
		self.data =pd.read_csv('ProcessedStandardised.csv',';')
		self.initUi()

	def initUi(self):
		#builds top left QFrame. no layout set yet
		
		
		topLeft = QFrame(self,objectName="topLeft")
		topLeft.setFrameShape(QFrame.Panel)
		topLeft.setFrameShadow(QFrame.Raised)
		#builds layout for top left QFrame. 
		gridTopLeft = QGridLayout(topLeft)
		gridTopLeft.setSpacing(10)

		#Widgets to be added to top left are made and added to top left grid\gridTopLeft
		#import button made first
		buttonImport= QtWidgets.QPushButton("Click herer",objectName="Button1")
		buttonImport.setText("Import Data")
		buttonImport.clicked.connect(self.buttonImportFunction)
		gridTopLeft.addWidget(buttonImport,0,0,1,4)

		#Shares label is now made
		label1 = QtWidgets.QLabel("Shares")
		gridTopLeft.addWidget(label1,1,0)

		#comboBox is now made and added to gridTopLeft

		shareNames = {}
		self.comboBox= QtWidgets.QComboBox()
		for share in self.data.Ticker.unique():

			self.comboBox.addItem(share)


		gridTopLeft.addWidget(self.comboBox,1,1,1,3)

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
'''
		self.featuresListWidget = QtWidgets.QListWidget()
		self.featuresListWidget.setAlternatingRowColors(True)

		for column in self.data.columns:
			
			self.featuresListWidget.addItem(column)


		listWidgetGroupBox=QtWidgets.QGroupBox("Features")
		listWidgetGroupBoxLayout=QtWidgets.QVBoxLayout()
		listWidgetGroupBoxLayout.addWidget(self.featuresListWidget)
		listWidgetGroupBox.setLayout(listWidgetGroupBoxLayout)
		gridTopLeft.addWidget(listWidgetGroupBox,2,0,4,4)
		

		#label2 = QtWidgets.QLabel("Features")
		#gridTopLeft.addWidget(label2,2,0,1,4)

		topLeft.setLayout(gridTopLeft)
		
		#builds bottom left QFrame. no layout set
		bottomLeft = QFrame(self)
		bottomLeft.setFrameShape(QFrame.Panel)
		bottomLeft.setFrameShadow(QFrame.Raised)

		#P value label and line edit created
		pValLabel=QtWidgets.QLabel("p-val: ")
		pValLineEdit = QtWidgets.QLineEdit()

		#Var button created
		varButton = QtWidgets.QPushButton("Estimate using VAR")
		varButton.clicked.connect(self.varButtonClicker)
		
		#Calculating errors label created
		calculatingErrorsLabel=QtWidgets.QLabel("Calculating Errors")

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




		bottomLeftGridLayout= QGridLayout()
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
		
		
		bottomLeft.setLayout(bottomLeftGridLayout)



		#builds right QFrame.no layout set yet
		right = QFrame(self)		
		right.setFrameShape(QFrame.Panel)
		right.setFrameShadow(QFrame.Raised)
		self.rightFrameGridLayout=QGridLayout()
		right.setLayout(self.rightFrameGridLayout)

		



		grid = QGridLayout()
		grid.setSpacing(10)
		grid.addWidget(topLeft,0,0,2,1)
		grid.addWidget(bottomLeft,2,0,1,1)
		grid.addWidget(right,0,1,3,3)

		
		widgetBox = QWidget(self)
		widgetBox.setLayout(grid)
		self.setCentralWidget(widgetBox)
		self.setGeometry(0,0,1500,900)
		self.setWindowTitle("Varima Model")

	def buttonImportFunction(self):
		
		#self.data =pd.read_csv('ProcessedNonStandardised.csv',';')
		print("button import pressed")
		
	def varButtonClicker(self):
		

		print(self.comboBox.currentText())
		print(self.featuresListWidget.currentItem().text())

		if self.rightFrameGridLayout.itemAt(0) == None :
			print("ENTERED")
			shareData = self.data[self.data.Ticker == self.comboBox.currentText()]
			y= shareData[shareData.columns[3]]			
			#y= shareData[shareData.columns[4]]

			fig, ax =plt.subplots()
			#color='#1AB1ED' for blue
			ax.plot(y,linewidth=3,color='#BF1AED')

			ax.patch.set_facecolor('#323232')
			ax.grid(linestyle="--")
			fig.patch.set_facecolor('#191919')
			#fig.patch.set_alpha(0.0)
			#ax.patch.set_alpha(0.0)

			ax.spines['bottom'].set_color('#ffffff')
			ax.spines['top'].set_color('#ffffff') 
			ax.spines['right'].set_color('#ffffff')
			ax.spines['left'].set_color('#ffffff')
			ax.tick_params(axis='x', colors='#ffffff')
			ax.tick_params(axis='y', colors='#ffffff')
			ax.set_xlabel("Date")
			ax.set_ylabel("Returns")
			ax.yaxis.label.set_color('white')
			ax.xaxis.label.set_color('white')
			#fig.savefig('temp.png', transparent=True)

			self.plotWidget = FigureCanvas(fig)
			self.rightFrameGridLayout.addWidget(self.plotWidget)
			#right.setLayout(self.rightFrameGridLayout)
			'''
			self.widgetTest = QtWidgets.QPushButton("hello world")
			self.rightFrameGridLayout.replaceWidget(self.plotWidget,self.widgetTest)
			
			self.plotWidget=None
			'''
		else :

			self.plotWidget.deleteLater()
			
			print("ENTERED 2")
			shareData = self.data[self.data.Ticker == self.comboBox.currentText()]
			y= shareData[shareData.columns[3]]#Need to change this so that columns[self.featuresListWidget.currentItem] is taken into account			
			#y= shareData[shareData.columns[4]]

			fig, ax =plt.subplots()
			#color='#1AB1ED' for blue
			ax.plot(y,linewidth=4,color='#BF1AED')

			ax.patch.set_facecolor('#323232')
			ax.grid(linestyle="--")
			fig.patch.set_facecolor('#191919')
			#fig.patch.set_alpha(0.0)
			#ax.patch.set_alpha(0.0)

			ax.spines['bottom'].set_color('#ffffff')
			ax.spines['top'].set_color('#ffffff') 
			ax.spines['right'].set_color('#ffffff')
			ax.spines['left'].set_color('#ffffff')
			ax.tick_params(axis='x', colors='#ffffff')
			ax.tick_params(axis='y', colors='#ffffff')

			ax.set_xlabel("Date")
			ax.set_ylabel("Returns")
			ax.yaxis.label.set_color('white')
			ax.xaxis.label.set_color('white')
			#fig.savefig('temp.png', transparent=True)

			self.plotWidget = FigureCanvas(fig)
			self.rightFrameGridLayout.addWidget(self.plotWidget)
			#right.setLayout(self.rightFrameGridLayout)
	def backTestButtonClicker (self):

		print("Back test button clicked successfully")
		
		self.next=Login()
		self.close()

	def button1Clicker (self):

		self.label1.setText("YOu clicked the button")

		print("button1 clicked")


class Login(QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUi()

	def initUi(self) :

		print("hello login")
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
						QGroupBox {

							font-size: 20px
						}

						

						
						''')
	#border-width: 1px
							#border-style: outset
	#rgb(60,208,228)
	win=Login()#Worked when this was min=MyWindow()
	win.showMaximized()
	sys.exit(app.exec_())#executes the main loop

window()
