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
		gridTopLeft.addWidget(buttonImport,0,0,1,4)

		#Shares label is now made
		label1 = QtWidgets.QLabel("Shares")
		gridTopLeft.addWidget(label1,1,0)

		#comboBox is now made and added to gridTopLeft
		comboBox= QtWidgets.QComboBox()
		comboBox.addItem("MTN")
		comboBox.addItem("Nokia")
		comboBox.addItem("Apple")
		comboBox.addItem("Microsoft")
		comboBox.addItem("Hp")
		comboBox.addItem("foo")
		comboBox.addItem("bar")
		comboBox.addItem("Liverpool")
		comboBox.addItem("JSC")
		comboBox.addItem("LON")
		comboBox.addItem("MTA")
		comboBox.addItem("OLG")
		comboBox.addItem("NHM")
		comboBox.addItem("NPK")
		comboBox.addItem("NTC")
		gridTopLeft.addWidget(comboBox,1,1,1,3)

		#Features scroll area is now made
		#innerGroupBox is made first. This will have a VBoxLayout containing list of hello worlds. 
		#it will then be added to a scrollarea via setWidget
		innerGroupBox=QtWidgets.QGroupBox(objectName="featureBox")
		'''groupBox.setStyleSheet(''QGroupBox {
    							border: 1px solid gray;
   								border-radius: 9px;
   								margin-top: 0.5em;
								}

								QGroupBox::title {
   								subcontrol-origin: margin;
    							left: 10px;
   								padding: 0 3px 0 3px;
								}'')'''
		#VLayout for inner group box created and populated in the for loop below
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
		gridTopLeft.addWidget(groupBoxOuterScroll,2,0,4,4)
		

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
		self.setGeometry(0,0,900,600)
		self.setWindowTitle("Varima Model")
		
	def varButtonClicker(self):
		
		if self.rightFrameGridLayout.itemAt(0) == None :
			print("ENTERED")
			x=np.linspace(0,2*np.pi,100)
			y=np.sin(x)
			fig, ax =plt.subplots()
			#color='#1AB1ED' for blue
			ax.plot(x,y,linewidth=4,color='#BF1AED')

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
			#fig.savefig('temp.png', transparent=True)

			self.plotWidget = FigureCanvas(fig)
			self.rightFrameGridLayout.addWidget(self.plotWidget)
			#right.setLayout(self.rightFrameGridLayout)
			'''
			self.widgetTest = QtWidgets.QPushButton("hello world")
			self.rightFrameGridLayout.replaceWidget(self.plotWidget,self.widgetTest)
			self.plotWidget.deleteLater()
			self.plotWidget=None
			'''
		
		
	def backTestButtonClicker (self):

		print("Back test button clicked successfully")


	def button1Clicker (self):

		self.label1.setText("YOu clicked the button")

		print("button1 clicked")




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

						QLineEdit {

							border-width: 1px;
    						border-style: ridge;
   							border-color: rgb(42,130,218);
   							border-radius: 4px;
							
						}

						

						
						''')
	#border-width: 1px
							#border-style: outset
	#rgb(60,208,228)
	win=MyWindow()
	win.showMaximized()
	sys.exit(app.exec_())#executes the main loop

window()

