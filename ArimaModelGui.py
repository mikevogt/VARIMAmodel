from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QFrame,QGridLayout,
	QSplitter, QStyleFactory, QApplication,QVBoxLayout,QStyle, QSizePolicy,QSpacerItem,QMessageBox,QAction,QListView,QAbstractItemView)
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
htmlReturnonInvestment="""\
			<html>
    			<body>
        			<p>
            		Return on investment (ROI) is a ratio betweet net profit over a period<br>
            		of time amd the cost of investment. This ratio is used to establish how<br>
            		how efficient the investment is in terms of making a profit or comparing<br>
            		the effficiency to other investments.<br><br>

            		A High ROI is a good indicator of a good investment as the net profit is<br>
            		favourable to the costs that you have invested.

        			</p>
    			</body>
			</html"""

htmlTotalAssetTurnover="""\
			<html>
    			<body>
        			<p>
            		Total Asset Turnover (ATO) is a financial indicator used to measure the efficiency<br>
            		of how well the assets of the company are being used to generate sales revenue for the <br>
            		company. Asset turnover can be further divided into fixed asset turnover as well as working <br>
            		turnover. <br><br>

            		The formula for Total Asset Turnover is:<br>
            		Asset Turnover = Net Sales Revenue / Average Total Assets

        			</p>
    			</body>
			</html>"""

htmlBetatoMarket="""\
			<html>
    			<body>
        			<p>
            		The beta of an investment is a measure of the risk that arises from the exposure <br>
            		to general market movements as opposed to the company specific risk. The market <br>
            		portfolio of all investments has a beta = 1. If a company has a beta > 1, this company <br>
            		would be considered to be more risky than the market as the price movements would <br>
            		fluctuate more than the overall market.

        			</p>
    			</body>
			</html>"""

htmlBetatoUSDZAR="""\
			<html>
    			<body>
        			<p>
            		The beta of an investment is a measure of the risk that arises from the exposure <br>
            		to general market movements as opposed to the company specific risk. This risk is<br>
            		being compared to the USD/ZAR exchange rate. This compares the price movements of <br>
            		the comany to the movements of the exchange. If the beta is > 1, the company would <br>
            		seem to be risky/volatile to the USD.

        			</p>
    			</body>
			</html>"""

htmlNetProfitMargin="""\
			<html>
    			<body>
        			<p>
            		Net Profit Margin (NPM) is a measur of profitability of the company. NPM is used <br>
            		for internal comparison, it is an idicator of the company's pricing strategies<br>
            		and how well the company controls its costs. Differences in competetive strategy<br>
            		will cause the NPM to vary across companies.<br><br>

            		NPM is calculated by finding the net profit as a percentace of revenue.<br>
            		Net Profit Margin = Net Profit / Revenue


        			</p>
    			</body>
			</html>"""

htmlCurrentRatio="""\
			<html>
    			<body>
        			<p>
            		The current ratio is a liquidity ratio that measures whether a firm has enough <br>
            		resources to meet its short-term liabilities, This means that if a company goes <br>
            		insolvent and has to sell all their assets, they will generate enough money to pay<br>
            		off their short-term liabilities.<br><br>

            		The Current Ratio is calculated with the following formula:<br>
            		Current ratio = Current Assets / Current Lieabilities


        			</p>
    			</body>
			</html>"""

htmlVolatility="""\
			<html>
    			<body>
        			<p>
            		Volatility or Company-Specific Risk refers to the risk that a company has that<br>
            		is unique to them and that can be mitigated through diversification. This risk<br>
            		can impact negatively on a company and needs to be monitored carefully. A high<br>
            		volatility can put the company at a disadvantage in the market as other companies<br>
            		do not have to face this risk.

        			</p>
    			</body>
			</html>"""


htmlDebtToEquityR = """\
			<html>
				<body>
			    	<p>
			   		The debt-to-equity (D/E) ratio is calculated by dividing a company’s total<br>
			   		liabilities by its shareholder equity. These numbers are available on the<br>
			   		balance sheet of a company’s financial statements. The ratio is used to<br>
			   		evaluate a company's financial leverage. The D/E ratio is an important metric<br>
			   		used in corporate finance.<br><br>

			   		It is a measure of the degree to which a company is financing its operations<br>
			   		through debt versus wholly-owned funds. More specifically, it reflects the<br>
			   		ability of shareholder equity to cover all outstanding debts in the event<br>
			   		of a business downturn.<br>

			    	</p>
				</body>
			</html>
			"""
htmlDebtToEquityT="""\
			<html>
				<body>
			    	<p>
			   		The debt-to-equity (D/E) ratio is calculated by dividing a company’s total<br>
			   		liabilities by its shareholder equity. These numbers are available on the<br>
			   		balance sheet of a company’s financial statements. The ratio is used to<br>
			   		evaluate a company's financial leverage. The D/E ratio is an important metric<br>
			   		used in corporate finance.<br><br>

			   		It is a measure of the degree to which a company is financing its operations<br>
			   		through debt versus wholly-owned funds. More specifically, it reflects the<br>
			   		ability of shareholder equity to cover all outstanding debts in the event<br>
			   		of a business downturn. This feature provides the trend of the debt<br>
			   		to equity ratio<br>

			    	</p>
				</body>
			</html>
			"""

htmlInterestCoverTrend="""\
			<html>
				<body>
			    	<p>
			    	The interest coverage ratio is a debt ratio and profitability ratio used to determine<br>
			    	how easily a company can pay interest on its outstanding debt. The interest coverage<br>
			    	ratio may be calculated by dividing a company's earnings before interest and taxes<br>
			    	(EBIT) during a given period by the company's interest payments due within the same<br>
			    	period.<br><br>

					The Interest coverage ratio is also called “times interest earned.” Lenders, investors,<br>
					and creditors often use this formula to determine a company's riskiness relative to its<br>
					current debt or for future borrowing.<br>

			    	</p>
			  	</body>
			</html>
			"""
htmlMarketCapitalization="""\
			<html>
			 	<body>
			    	<p>
			    	Market capitalization refers to the total dollar market value of a company's outstanding<br>
			    	shares of stock. Commonly referred to as "market cap," it is calculated by multiplying the<br>
			    	total number of a company's outstanding shares by the current market price of one share.<br><br>

					As an example, a company with 10 million shares selling for $100 each would have a market<br>
					cap of $1 billion. The investment community uses this figure to determine a company's size<br>
					,as opposed to using sales or total asset figures. In an acquisition, the market cap is<br>
					used to determine whether a takeover candidate represents a good value or not to the <br>
					acquirer.<br>
			    	</p>
			 	</body>
			</html>
			"""
htmlTradingVolume="""\
			<html>
			 	<body>
			    	<p>
			    	Volume of trade is the total quantity of shares or contracts traded for a specified<br>
			    	security. It can be measured on any type of security traded during a trading day.<br>
			    	Volume of trade or trade volume is measured on stocks, bonds, options contracts,<br>
			    	futures contracts and all types of commodities.<br>
			    	</p>
			 	</body>
			</html>
			"""

htmlEarningsYield = """\
			<html>
				<body>
					<p>
					The earnings yield refers to the earnings per share for the most recent 12-month period<br>
					divided by the current market price per share. The earnings yield (which is the inverse<br>
					of the P/E ratio) shows the percentage of how much a company earned per share.<br>
					</p>
				</body>
			</html>"""

htmlEarningsYieldTrend = """\
			<html>
				<body>
					<p>
					The earnings yield refers to the earnings per share for the most recent 12-month period<br>
					divided by the current market price per share. The earnings yield (which is the inverse<br>
					of the P/E ratio) shows the percentage of how much a company earned per share. This<br>
					feature provides the trend of the Earnings Yield<br>
					</p>
				</body>
			</html>"""


htmlBookValuetoPriceRatio = """\
			<html>
				<body>
					<p>
					The P/B ratio reflects the value that market participants attach to a company's equity relative<br>
					to the book value of its equity. A stock's market value is a forward-looking metric that<br>
					reflects a company's future cash flows. The book value of equity is an accounting measure<br>
					based on the historic cost principle and reflects past issuances of equity, augmented by any<br>
					profits or losses, and reduced by dividends and share buybacks.<br>
					</p>
				</body>
			</html>"""

htmlBookValuetoPriceRatioTrend = """\
			<html>
				<body>
					<p>
					The P/B ratio reflects the value that market participants attach to a company's equity relative<br>
					to the book value of its equity. A stock's market value is a forward-looking metric that reflects<br>
					a company's future cash flows.<br><br>
  					The book value of equity is an accounting measure based on the historic cost principle and <br>
  					reflects past issuances of equity, augmented by any profits or losses, and reduced by <br>
  					dividends and share buybacks. This feature provides the trend of the Book Value to Price Ratio<br>
					</p>
				</body>
			</html>"""

htmlSalesToPriceRatio = """\
			<html>
				<body>
					<p>
					The Sales to Price ratio is a ratio representing the sell/buy price of a share. The sell<br>
					price of a share is the amount a share may be sold for, while the buy price of a<br>
					share is the amount a share will cost a buyer. This ratio is used in computing<br>
					profits and losses.<br>
					</p>
				</body>
			</html>"""

htmlSalesToPriceRatioTrend = """\
			<html>
				<body>
					<p>
					The Sales to Price ratio trend is the pattern resulting for the Sales to Price Ratio.<br>
					This is very useful for visualization and strategy planning. Plots and other statistical<br>
					graphical methods may be used for visualizing this trend.  Often used as the "base"<br>
					for decision making in the Stock Exchange.<br>
					</p>
				</body>
			</html>"""


htmlProfitMargin = """\
			<html>
				<body>
					<p>
					Profit margin is one of the commonly used profitability ratios to gauge the degree<br>
					to which a company or a business activity makes money. It represents what<br>
					percentage of sales has turned into profits. Simply put, the percentage figure<br>
					indicates how many cents of profit the business has generated for each dollar of<br>
					sale.
					</p>
				</body>
			</html>"""



htmlWorkingCapitalTurnover = """\
			<html>
				<body>
					<p>
					Working capital turnover is a ratio that measures how efficiently a company is<br>
					using its working capital to support a given level of sales. Also referred to as net<br>
					sales to working capital, work capital turnover shows the relationship between the <br>
					funds used to finance a company's operations and the revenues a company<br>
					generates as a result.<br>
					</p>
				</body>
			</html>"""


htmlAssetTurnover = """\
			<html>
				<body>
					<p>
					The asset turnover ratio measures the value of a company's sales or revenues<br>
					relative to the value of its assets. The asset turnover ratio can be used as an<br>
					indicator of the efficiency with which a company is using its assets to generate<br>
					revenue.<br>
					</p>
				</body>
			</html>"""




htmlProfitMargin="""\
			<html>
				<body>
					<p>
					Profit margin is calculated with selling price (or revenue) taken as base times 100. It is<br>
					the percentage of selling price that is turned into profit, whereas "profit percentage" or<br>
					"markup" is the percentage of cost price that one gets as profit on top of cost price.<br>
					While selling something one should know what percentage of profit one will get on a<br>
					particular investment, so companies calculate profit percentage to find the ratio of<br>
					profit to cost.<br><br>
					The profit margin is used mostly for internal comparison.<br><br>
					Individual businesses' operating and financing arrangements vary so much that different<br>
					entities are bound to have different levels of expenditure, so that comparison of one<br>
					with another can have little meaning. A low profit margin indicates a low margin of safety:<br>
					higher risk that a decline in sales will erase profits and result in a net loss, or a negative<br>
					margin.<br><br>

					</p>
				</body>
			</html>
	"""

htmlCapitalTurnover="""\
			<html>
				<body>
					<p>
					Capital turnover compares the annual sales of a business to the total amount of its stockholders'<br>
					equity. The intent is to measure the proportion of revenue that a company can generate with a given<br>
					amount of equity. It is also a general measure of the level of capital investment needed in a<br>
					specific industry in order to generate sales.<br><br>

					</p>
				</body>
			</html>
	"""


htmlCapitalTurnoverTrend="""\
			<html>
				<body>
					<p>
					Capital turnover compares the annual sales of a business to the total amount of its stockholders'<br>
					equity. The intent is to measure the proportion of revenue that a company can generate with a given<br>
					amount of equity. It is also a general measure of the level of capital investment needed in a<br>
					specific industry in order to generate sales.This feature provides the trend of the Capital<br>
					Turnover<br><br>

					</p>
				</body>
			</html>
	"""




htmlReturnOnAssets="""\
			<html>
				<body>
					<p>
					Return on assets (ROA) is a financial ratio that shows the percentage of profit a company earns<br>
					in relation to its overall resources. It is commonly defined as net income divided by total assets.<br>
					Net income is derived from the income statement of the company and is the profit after taxes. The<br>
					assets are read from the balance sheet and include cash and cash-equivalent items such as receivables,<br>
					inventories, land, capital equipment as depreciated, and the value of intellectual property such as<br>
					patents. Companies that have been acquired may also have a category called "good will" representing<br>
					the extra money paid for the company over and above its actual book value at the time of acquisition.<br>
					Because assets will tend to have swings over time, an average of assets over the period to be measured<br>
					should be used. Thus the ROA for a quarter should be based on net income for the quarter divided by average<br>
					assets in that quarter. ROA is a ratio but usually presented as a percentage.<br>


					</p>
				</body>
			</html>
	"""

htmlReturnOnAssetsTrend="""\
			<html>
				<body>
					<p>
					Return on assets (ROA) is a financial ratio that shows the percentage of profit a company earns<br>
					in relation to its overall resources. It is commonly defined as net income divided by total assets.<br>
					Net income is derived from the income statement of the company and is the profit after taxes. The<br>
					assets are read from the balance sheet and include cash and cash-equivalent items such as receivables,<br>
					inventories, land, capital equipment as depreciated, and the value of intellectual property such as<br>
					patents. Companies that have been acquired may also have a category called "good will" representing<br>
					the extra money paid for the company over and above its actual book value at the time of acquisition.<br>
					Because assets will tend to have swings over time, an average of assets over the period to be measured<br>
					should be used. Thus the ROA for a quarter should be based on net income for the quarter divided by average<br>
					assets in that quarter. ROA is a ratio but usually presented as a percentage.This feature provides the<br>
					the trend of the return on assets<br><br>
					</p>
				</body>
			</html>
	"""

class MyWindow(QMainWindow):
	#MainWindow constructor. Most of the actual construction takes place in the function initUi(self) when it is called
	data1 =pd.read_csv('ProcessedStandardisedOG.csv',';')
	def __init__(self):

		super(MyWindow,self).__init__()#This can be written as super().__init__() i think which would make more sense but leave it as is for now
		self.setWindowIcon(QIcon("Logo.ico"))
		self.data =pd.read_csv('ProcessedStandardisedOG.csv',';')#Reads in the standardized data from ProcessedStandardised.csv. This file must be in the same directory as varimaGui.py
		self.pVal=2
		self.dVal=1
		self.qVal=1
		self.forecastLength=27
		self.initUi()
		self.count=0


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

		savePlot = QAction("Save Plot",self)
		savePlot.setShortcut("Ctrl+S")
		file.addAction(savePlot)
		savePlot.triggered.connect(self.savePlotTriggered)


		logout = QAction("Logout",self)
		file.addAction(logout)
		logout.triggered.connect(self.logoutButtonClicked)

		quit = QAction("Quit",self)
		file.addAction(quit)
		quit.triggered.connect(self.quitTriggered)



		view = bar.addMenu("View")

		themes = QAction("Themes",self)
		view.addAction(themes)
		themes.triggered.connect(self.themesTriggered)

		helpMenu = bar.addMenu("Help")


		about=QAction("About",self)
		helpMenu.addAction(about)
		about.triggered.connect(self.aboutTriggered)
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

		self.sharesLabel = QtWidgets.QLabel("Shares")
		self.sharesLabel.setStyleSheet("""font-size: 15px;""")
		sharesLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		self.sharesLabel.setSizePolicy(sharesLabelSizePolicy)

		#comboBox is now made
		"""
		border: 1px solid #32414B;
 										 border-radius: 0;
  										background-color: #19232D;
  										combobox-popup: 0;
		"""
		self.comboBox= QtWidgets.QComboBox()
		self.comboBox.setStyleSheet("""
									QComboBox{
									font-size:13px;


									}


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


		#self.comboBox.setItemData(0, QColor(Qt.black), Qt.ForegroundRole);
		self.comboBox.setMaxVisibleItems(50)
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
'''


		#Next, the features scroll list (called featuresListWidget) is made using a QListWidget() within a QGroupBox()

		self.featuresListWidget = QtWidgets.QListWidget()
		self.featuresListWidget.setStyleSheet("""font-size: 15px;""")
		self.featuresListWidget.setAlternatingRowColors(True)

		for column in self.data.columns[3:-2]:#For loop that iterates through all column names in data populating the featuresListWidget
			#Still need to fix this so that it does not add the first 3 column names (namely DateStamps, Shares and Ticker) to the features list
			self.featuresListWidget.addItem(column)


		self.featuresListWidget.setCurrentRow(0)
		listWidgetGroupBox=QtWidgets.QGroupBox("Features")#Outer groupBox to house the features list widget
		listWidgetGroupBox.setStyleSheet("""font-size:15px;
											""")
		listWidgetGroupBoxLayout=QtWidgets.QVBoxLayout()
		listWidgetGroupBox.setLayout(listWidgetGroupBoxLayout)
		listWidgetGroupBoxLayout.addWidget(self.featuresListWidget)#featuresListWidget is first added to the groupbox

		#All widgets are then added to the top left grid
		#gridTopLeft.addWidget(buttonImport,0,0,1,4)
		gridTopLeft.addWidget(self.sharesLabel,0,0,1,1)
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

		self.labelPlotCustomize = QtWidgets.QLabel("Plot Line Colour")
		self.labelPlotCustomize.setStyleSheet("""font-size: 15px""")

		#customizeLabelWidget = QWidget()
		#layout1=QHBoxLayout()
		#customizeLabelWidget.setLayout(layout1)
		#layout1.addWidget(self.labelPlotCustomize,Qt.AlignCenter)

		self.labelPlotColour = QtWidgets.QLabel("Plot line colour:")

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

		self.labelArimaCustomize = QtWidgets.QLabel("Customize Arima Variables")
		self.labelArimaCustomize.setStyleSheet("""font-size: 15px""")

		self.labelPval= QtWidgets.QLabel("P-Value:")
		self.labelPval.setStyleSheet("""font-size: 13px""")
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

		self.labelDval= QtWidgets.QLabel("D-Value:")
		self.labelDval.setStyleSheet("""font-size: 13px""")
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

		self.labelQval= QtWidgets.QLabel("Q-Value:")
		self.labelQval.setStyleSheet("""font-size: 13px""")
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

		self.labelForecastLength = QtWidgets.QLabel("Forecast Length:")
		self.labelForecastLength.setStyleSheet("""font-size: 13px""")



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
		self.buttonArima = QtWidgets.QPushButton("Estimate using ARIMA",objectName="button")
		self.buttonArima.clicked.connect(self.varButtonClicker)

		self.logoutButton = QtWidgets.QPushButton("Logout",objectName="button")
		self.logoutButton.clicked.connect(self.logoutButtonClicked)


		#Now each item created above is added to the grid layout for the bottom left frame

		bottomLeftGridLayout.addWidget(self.labelPlotCustomize,0,0,1,7,Qt.AlignCenter)

		#bottomLeftGridLayout.addWidget(self.labelPlotColour,1,0,1,1)
		bottomLeftGridLayout.addWidget(self.radioButtonPurple,1,0,1,3,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.radioButtonGreen,1,3,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.radioButtonOrange,1,4,1,3,Qt.AlignCenter)

		#bottomLeftGridLayout.addWidget(buttonPlot,2,0,1,7)

		bottomLeftGridLayout.addWidget(self.labelArimaCustomize,2,0,1,7,Qt.AlignCenter)

		bottomLeftGridLayout.addWidget(self.labelPval,3,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.pValSpinBox,3,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderPval,3,2,1,5)

		bottomLeftGridLayout.addWidget(self.labelDval,4,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.dValSpinBox,4,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderDval,4,2,1,5)

		bottomLeftGridLayout.addWidget(self.labelQval,5,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.qValSpinBox,5,1,1,1)
		bottomLeftGridLayout.addWidget(self.sliderQval,5,2,1,5)

		bottomLeftGridLayout.addWidget(self.labelForecastLength,6,0,1,1,Qt.AlignCenter)
		bottomLeftGridLayout.addWidget(self.dialSpinBox,6,1,1,5)
		bottomLeftGridLayout.addWidget(self.dial,6,6,1,1)

		#bottomLeftGridLayout.addWidget(optimizeButton,,0,1,7)
		bottomLeftGridLayout.addWidget(self.buttonArima,7,0,1,7)

		bottomLeftGridLayout.addWidget(self.logoutButton,8,0,1,7)



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


	def quitTriggered(self):

		print("quit triggered worked")


	def aboutTriggered(self):

		print("aboutTriggered")
		self.current=AboutPage()
		self.current.show()




	def savePlotTriggered(self):

		print("savePlot triggered")

		string="plot"+str(self.count)+".png"
		self.fig.savefig(string,facecolor='#323232')

		self.count=self.count+1
		self.varButtonClicker()

	def themesTriggered(self):

		print("Themes Triggered")


	def plotEmptyAxis(self):

		self.fig, self.ax =plt.subplots()

		self.ax.grid(linestyle="--")
		self.ax.patch.set_facecolor('#282828')
		self.fig.patch.set_facecolor("None")


		self.ax.spines['bottom'].set_color('#ffffff')
		self.ax.spines['top'].set_color('#ffffff')
		self.ax.spines['right'].set_color('#ffffff')
		self.ax.spines['left'].set_color('#ffffff')
		self.ax.tick_params(axis='x', colors='#ffffff')
		self.ax.tick_params(axis='y', colors='#ffffff')
		#ax.set_xlabel("Date",fontsize=15)
		#ax.set_ylabel(self.featuresListWidget.currentItem().text(),fontsize=15)
		self.ax.yaxis.label.set_color('white')
		self.ax.xaxis.label.set_color('white')
		#fig.suptitle(self.comboBox.currentText(),fontsize=20,color='white')

		self.plotWidget = FigureCanvas(self.fig)#FigureCanvas is an matplotlib object that can act as a pyqt5 widget
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

		return (1.01)**(inVal)-1


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

			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("No Feature Selected.")
			alertMessage.setText("You have not selected a feature to plot. Please select a feature from the side bar before plotting")
			alertMessage.setIcon(QMessageBox.Info)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()

			self.plotEmptyAxis()
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
			alertMessage=QMessageBox()
			alertMessage.setWindowTitle("No Feature Selected.")
			alertMessage.setText("You have not selected a feature to plot. Please select a feature from the side bar before plotting")
			alertMessage.setIcon(QMessageBox.Information)
			alertMessage.setWindowIcon(QIcon("Logo.ico"))
			x=alertMessage.exec_()




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


			plt.close(self.fig)
			#plt.clf()
			#plt.cla()
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
			print("pythonForecastDateList")
			print(pythonForecastDateList)
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


					forecastUpperError.append(forcasted[i] + rmse + self.exponentiate(i))
					forecastLowerError.append(forcasted[i] - rmse - self.exponentiate(i))



				print("after")
				print(forecastUpperError)
				#Plot of y vs dates is now created below
				self.fig, self.ax =plt.subplots()#Fig must be deleted  later so as not consume memory
				#color='#1AB1ED' for blue
				#ax.plot(y,linewidth=4,color='#BF1AED')
				self.ax.plot_date(dates,y,linewidth = 3,color=colourString,fmt='-',label="Actual Data")
				self.ax.plot_date(forecastDates,forcasted,linewidth = 3,color='#1AB1ED',fmt='-', label="Forecasted")
				self.ax.plot_date(forecastDates,forecastUpperError,linewidth = 3,color='#ff0066',fmt='--', label="Error")
				self.ax.plot_date(forecastDates,forecastLowerError,linewidth = 3, color='#ff0066', fmt='--')
				plt.legend(loc="upper right")
				self.ax.grid(linestyle="--")
				self.ax.patch.set_facecolor('#282828')
				self.fig.patch.set_facecolor("None")
				#fig.patch.set_alpha(0.0)
				#ax.patch.set_alpha(0.0)
				self.ax.spines['bottom'].set_color('#ffffff')
				self.ax.spines['top'].set_color('#ffffff')
				self.ax.spines['right'].set_color('#ffffff')
				self.ax.spines['left'].set_color('#ffffff')
				self.ax.tick_params(axis='x', colors='#ffffff')
				self.ax.tick_params(axis='y', colors='#ffffff')
				self.ax.set_xlabel("Date",fontsize=15)
				self.ax.set_ylabel(self.featuresListWidget.currentItem().text(),fontsize=15)
				self.fig.suptitle(self.comboBox.currentText(),fontsize=20,color='white')
				self.ax.yaxis.label.set_color('white')
				self.ax.xaxis.label.set_color('white')

				#fig.savefig('temp.png', transparent=True)

				self.plotWidget = FigureCanvas(self.fig)#FigureCanvas is an matplotlib object that can act as a pyqt5 widget
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
		pixmap = QPixmap("registerLogo.png")
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

		self.showPasswordCheck=QtWidgets.QCheckBox("Show Password")
		self.showPasswordCheck.stateChanged.connect(self.showPasswordChecked)


		self.registerButton = QtWidgets.QPushButton("Register")
		registerButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		self.registerButton.setSizePolicy(registerButtonSizePolicy)
		#max-height:35px;
		self.registerButton.setStyleSheet("""	QPushButton{font-size: 15px;
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
										QPushButton:focus {


											background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
											stop:0 rgba(175,178,190,225), stop:1 rgba(158, 162, 174,200));
											border-style: inset;
											border-color: rgba(255,255,255,255);
											outline: none;

										}
										""")
		bodyShadow4 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow4.setBlurRadius(9.0)
		bodyShadow4.setColor(QColor(0, 0, 0, 160))
		bodyShadow4.setOffset(-2)
		self.registerButton.setGraphicsEffect(bodyShadow4)
		self.registerButton.clicked.connect(self.registerButtonClicked)

		self.returnButton = QtWidgets.QPushButton("Return to Mainpage")
		returnButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		self.returnButton.setSizePolicy(returnButtonSizePolicy)
		self.returnButton.setStyleSheet("""	QPushButton{font-size: 15px;
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
										QPushButton:focus {


											background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
											stop:0 rgba(175,178,190,225), stop:1 rgba(158, 162, 174,200));
											border-style: inset;
											border-color: rgba(255,255,255,255);
											outline: none;

										}
										""")
		bodyShadow5 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow5.setBlurRadius(9.0)
		bodyShadow5.setColor(QColor(0, 0, 0, 160))
		bodyShadow5.setOffset(-2)
		self.returnButton.setGraphicsEffect(bodyShadow5)
		self.returnButton.clicked.connect(self.returnButtonClicked)


		formBlockLayout.addWidget(widgetUsername,0,0,1,2)

		formBlockLayout.addWidget(widgetEmail,1,0,1,2)

		formBlockLayout.addWidget(widgetPassword,2,0,1,2)

		formBlockLayout.addWidget(widgetConfirmPassword,3,0,1,2)

		formBlockLayout.addWidget(self.showPasswordCheck,4,0,1,2,Qt.AlignRight)
		formBlockLayout.addWidget(self.registerButton,5,0,1,1)
		formBlockLayout.addWidget(self.returnButton,5,1,1,1)


		innerFrameLayout.addWidget(logoLabel,Qt.AlignCenter)
		innerFrameLayout.addWidget(formBlock)


		#frameDoubleVLayout.addWidget(loginLabel,Qt.AlignCenter)
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

		self.x = 3

	def showPasswordChecked(self):

		if (self.showPasswordCheck.isChecked()):

			self.passwordLineEdit.setEchoMode(0)

		else:

			self.passwordLineEdit.setEchoMode(2)

	def registerButtonClicked(self):
		self.x = 5

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

class AboutPage(QMainWindow):

	def __init__(self):

		super().__init__()
		self.setWindowIcon(QIcon("Logo.ico"))

		self.initUi()

	def initUi(self) :

		mainWidget=QtWidgets.QWidget()
		mainLayout= QHBoxLayout()
		mainWidget.setLayout(mainLayout)


		self.featuresListWidget = QtWidgets.QListWidget()
		self.featuresListWidget.setStyleSheet("""font-size: 15px;""")
		self.featuresListWidget.setAlternatingRowColors(True)

		for column in MyWindow.data1.columns[3:-2]:#For loop that iterates through all column names in data populating the featuresListWidget
			#Still need to fix this so that it does not add the first 3 column names (namely DateStamps, Shares and Ticker) to the features list
			self.featuresListWidget.addItem(column)



		self.featuresListWidget.itemClicked.connect(self.featureClicked)
		listWidgetGroupBox=QtWidgets.QGroupBox("Features")#Outer groupBox to house the features list widget
		listWidgetGroupBox.setStyleSheet("""font-size:15px;""")
		listWidgetGroupBoxLayout=QtWidgets.QVBoxLayout()
		listWidgetGroupBox.setLayout(listWidgetGroupBoxLayout)
		listWidgetGroupBoxLayout.addWidget(self.featuresListWidget)#featuresListWidget is first added to the groupbox


		html = """\
			<html>
			  <body>
			    <p>Hi there,<br><br>
			       You have just successfully reset your password! You can now login in with your new password.<br>
			       If this was not you, please send an email to ScrapedThroughC2@gmail.com and we will get back <br>
			       to you as soon as possible to review your account activity.<br><br>
			       We hope that you are enjoying our product. If you should need any assistance, please either email <br>
			       ScrapedThroughC2@gmail.com or call Nic (cell): 0832261920.<br><br>

			       Kind regards,<br><br>
			       The STC2 Team
			    </p>
			  </body>
			</html>
			"""
		self.label=QtWidgets.QLabel(html)
		self.label.setStyleSheet("""font-size: 15px;""")

		mainLayout.addWidget(listWidgetGroupBox,1)
		mainLayout.addWidget(self.label,2)

		self.setCentralWidget(mainWidget)
		#self.setGeometry(0,0,1500,900)
		self.setMinimumSize(900, 400);
		self.setWindowTitle("About")

		self.show()

	def featureClicked(self):
		featureString = self.featuresListWidget.currentItem().text()

		print(featureString)
		self.label.setText(featureString)
		print("Feature")


		if (featureString=="Return on investment"):

			global htmlReturnonInvestment
			self.label.setText(htmlReturnonInvestment)

		elif (featureString=="Total Asset Turnover"):

			global htmlTotalAssetTurnover
			self.label.setText(htmlTotalAssetTurnover)

		elif (featureString=="Beta to Market"):

			global htmlBetatoMarket
			self.label.setText(htmlBetatoMarket)

		elif (featureString=="Beta to USD/ZAR"):

			global htmlBetatoUSDZAR
			self.label.setText(htmlBetatoUSDZAR)

		elif (featureString=="Net Profit Margin"):

			global htmlNetProfitMargin
			self.label.setText(htmlNetProfitMargin)

		elif (featureString=="Current Ratio"):

			global htmlCurrentRatio
			self.label.setText(htmlCurrentRatio)

		elif (featureString=="Volatility"):

			global htmlVolatility
			self.label.setText(htmlVolatility)

		elif (featureString=="Debt to Equity Ratio"):

			global htmlDebtToEquityR
			self.label.setText(htmlDebtToEquityR)

		elif(featureString=="Debt to Equity Ratio Trend"):

			global htmlDebtToEquityT
			self.label.setText(htmlDebtToEquityT)

		elif (featureString=="Interest Cover Trend"):

			global htmlInterestCoverTrend
			self.label.setText(htmlInterestCoverTrend)

		elif (featureString=="Market Capitalization (Log)"):

			global htmlMarketCapitalization
			self.label.setText(htmlMarketCapitalization)


		elif(featureString=="Trading Volume (Log)"):
			global htmlTradingVolume
			self.label.setText(htmlTradingVolume)

		elif(featureString=="Earnings Yield"):

			global htmlEarningsYield
			self.label.setText(htmlEarningsYield)

		elif(featureString=="Earnings Yield Trend"):

			global htmlEarningsYieldTrend
			self.label.setText(htmlEarningsYieldTrend)

		elif(featureString=="Book Value to Price Ratio"):

			global htmlBookValuetoPriceRatio
			self.label.setText(htmlBookValuetoPriceRatio)

		elif(featureString=="Book Value to Price Ratio Trend"):

			global htmlBookValuetoPriceRatioTrend
			self.label.setText(htmlBookValuetoPriceRatioTrend)

		elif(featureString=="Profit Margin"):

			global htmlProfitMargin
			self.label.setText(htmlProfitMargin)

		elif(featureString=="Capital Turnover"):

			global htmlCapitalTurnover
			self.label.setText(htmlCapitalTurnover)

		elif(featureString=="Capital Turnover Trend"):

			global htmlCapitalTurnoverTrend
			self.label.setText(htmlCapitalTurnoverTrend)

		elif(featureString=="Return on Assets"):

			global htmlReturnOnAssets
			self.label.setText(htmlReturnOnAssets)

		elif(featureString=="Return on Assets Trend"):

			global htmlReturnOnAssetsTrend
			self.label.setText(htmlReturnOnAssetsTrend)


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
		pixmap = QPixmap("stc2.png")
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

		self.loginButton = QtWidgets.QPushButton("Login",objectName="button")
		loginButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical
		self.loginButton.setSizePolicy(loginButtonSizePolicy)
		#min-height:65px;
		#max-height:68px;
		self.loginButton.setStyleSheet("""min-height:45px;

									font-size: 25px;
									border-radius: 20px;""")
		self.loginButton.clicked.connect(self.loginButtonFunction)
		bodyShadow3 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow3.setBlurRadius(9.0)
		bodyShadow3.setColor(QColor(0, 0, 0, 160))
		bodyShadow3.setOffset(-2)
		self.loginButton.setGraphicsEffect(bodyShadow3)

		self.forgotButton = QtWidgets.QPushButton("Forgot Password?",objectName="button")
		forgotButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		self.forgotButton.setSizePolicy(forgotButtonSizePolicy)
		bodyShadow4 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow4.setBlurRadius(9.0)
		bodyShadow4.setColor(QColor(0, 0, 0, 160))
		bodyShadow4.setOffset(-2)
		self.forgotButton.setGraphicsEffect(bodyShadow4)
		self.forgotButton.clicked.connect(self.forgotPasswordClicked)



		self.registerButton = QtWidgets.QPushButton("Register",objectName="button")
		registerButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		self.registerButton.setSizePolicy(registerButtonSizePolicy)
		bodyShadow5 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow5.setBlurRadius(9.0)
		bodyShadow5.setColor(QColor(0, 0, 0, 160))
		bodyShadow5.setOffset(-2)
		self.registerButton.setGraphicsEffect(bodyShadow5)
		self.registerButton.clicked.connect(self.goRegisterButtonFunction)

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
		formBlockLayout.addWidget(self.loginButton,3,0,1,2)
		formBlockLayout.addWidget(self.forgotButton,4,0,1,1)
		formBlockLayout.addWidget(self.registerButton,4,1,1,1)
		formBlockLayout.addWidget(quitButton,5,0,1,2)

		innerFrameLayout.addWidget(logoLabel,Qt.AlignCenter)
		innerFrameLayout.addWidget(formBlock)

		#frameDoubleVLayout.addWidget(loginLabel,Qt.AlignCenter)
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

		self.x = 3
		self.y = 3
		self.z = 3

	def loginButtonFunction(self):

		"""if (True):

			self.next=MyWindow()
			self.next.showMaximized()
			self.close()
			return
		"""
		self.x = 5
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
		self.y = 5
		self.next=Register()
		self.next.showMaximized()
		self.close()

	def forgotPasswordClicked(self):
		self.z = 5
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
		pixmap = QPixmap("forgotLogo.png")
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

		self.showPasswordCheck=QtWidgets.QCheckBox("Show Password")
		self.showPasswordCheck.stateChanged.connect(self.showPasswordChecked)


		self.resetButton = QtWidgets.QPushButton("Reset Password",objectName="button")
		resetButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		self.resetButton.setSizePolicy(resetButtonSizePolicy)
		bodyShadow4 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow4.setBlurRadius(9.0)
		bodyShadow4.setColor(QColor(0, 0, 0, 160))
		bodyShadow4.setOffset(-2)
		self.resetButton.setGraphicsEffect(bodyShadow4)
		self.resetButton.clicked.connect(self.resetButtonClicked)

		self.returnButton = QtWidgets.QPushButton("Return to Mainpage",objectName="button")
		returnButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		self.returnButton.setSizePolicy(returnButtonSizePolicy)
		bodyShadow5 = QtWidgets.QGraphicsDropShadowEffect()
		bodyShadow5.setBlurRadius(9.0)
		bodyShadow5.setColor(QColor(0, 0, 0, 160))
		bodyShadow5.setOffset(-2)
		self.returnButton.setGraphicsEffect(bodyShadow5)

		self.returnButton.clicked.connect(self.returnButtonClicked)

		formBlockLayout.addWidget(widgetExplanation,0,0,1,2)
		formBlockLayout.addWidget(widgetUsername,1,0,1,2)

		formBlockLayout.addWidget(widgetEmail,2,0,1,2)

		formBlockLayout.addWidget(widgetPassword,3,0,1,2)

		formBlockLayout.addWidget(widgetConfirmPassword,4,0,1,2)

		formBlockLayout.addWidget(self.showPasswordCheck,5,0,1,2,Qt.AlignRight)
		formBlockLayout.addWidget(self.resetButton,6,0,1,1)
		formBlockLayout.addWidget(self.returnButton,6,1,1,1)


		innerFrameLayout.addWidget(logoLabel,Qt.AlignCenter)
		innerFrameLayout.addWidget(formBlock)


		#frameDoubleVLayout.addWidget(loginLabel,Qt.AlignCenter)
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


	def showPasswordChecked(self):

		if (self.showPasswordCheck.isChecked()):

			self.passwordLineEdit.setEchoMode(0)

		else:

			self.passwordLineEdit.setEchoMode(2)


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

if __name__ == '__main__':
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
#87bdd8
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
