from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QFrame,QGridLayout,
	QSplitter, QStyleFactory, QApplication,QVBoxLayout,QStyle, QSizePolicy,QSpacerItem,QMessageBox)
from PyQt5.QtCore import (Qt,QSize)
from PyQt5.QtGui import (QPalette,QColor,QPixmap,QIcon)
import sys

class Login(QMainWindow):

	def __init__(self):#Constructor for the login page. All the construction takes place in self.initUi()
	#background: qradialgradient(cx: 0.5, cy: 0.5, radius: 2, fx: 0.5, fy: 0.5, stop: 0 rgba(228,107,60,50) , stop: 0.2 rgba(25,25,25,255) , stop: 0.4 rgba(55,55,55,255) );
	#background-image: url(b7.jpg);
		super().__init__()
		self.setWindowIcon(QIcon("Logo.ico"))
		self.setStyleSheet('''
						QMainWindow{
						
							border-image: url(b16.jpg);
						

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

		outerFrame.setLayout(outerFrameLayout)
		outerFrameLayout.setSpacing(10)
		outerFrameLayout.setContentsMargins(20,20,20,20)# Left top right then bottom

		frameDouble = QtWidgets.QFrame()
		doubleFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		doubleFrameSizePolicy.setHorizontalStretch(1)
		frameDouble.setSizePolicy(doubleFrameSizePolicy)

		frameDoubleVLayout = QVBoxLayout()
		frameDouble.setLayout(frameDoubleVLayout)

		innerFrame = QtWidgets.QFrame(self,objectName="innerFrameLogin")
		innerFrame.setFrameShape(QFrame.Panel)
		innerFrame.setFrameShadow(QFrame.Raised)
		innerFrame.setStyleSheet("""QFrame{
											background: rgba(90,90,90,100);
											border-width: 1px;
											border-style: outset;
											border-color: rgba(130,130,130,100);
											border-radius: 35px;}""")
		#innerFrameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		#innerFrameSizePolicy.setHorizontalStretch(1)
		#innerFrame.setSizePolicy(innerFrameSizePolicy)
		innerFrameLayout= QVBoxLayout()
		innerFrameLayout.setSpacing(30)
		innerFrameLayout.setContentsMargins(20,20,20,20)
		innerFrame.setLayout(innerFrameLayout)

		
		formBlock = QtWidgets.QWidget()
		formBlockSizePolicy =QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		formBlock.setSizePolicy(formBlockSizePolicy)
		formBlockLayout = QGridLayout()
		formBlock.setLayout(formBlockLayout)



		loginLabel= QtWidgets.QLabel("STC2",objectName="loginLabel")
		loginLabel.setAlignment(Qt.AlignCenter)
		loginLabel.setStyleSheet("""font-size: 100px;""")
		loginLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)
		loginLabel.setSizePolicy(loginLabelSizePolicy)

		

		#Makes logo label and places logo image inside it
		logoLabel = QtWidgets.QLabel()
		logoLabel.setStyleSheet("""background: rgba(90,90,90,0);
									border-color: rgba(140,140,140,0);""")
		logoLabelSizePolicy=QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Maximum)#Horizontal,vertical
		logoLabel.setSizePolicy(logoLabelSizePolicy)
		pixmap = QPixmap("Logo.ico")
		logoLabel.setPixmap(pixmap)
		logoLabel.setAlignment(Qt.AlignCenter)

		widgetUsername = QtWidgets.QWidget()
		widgetUsername.setStyleSheet("""
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(96,99,108,200), stop:1 rgba(133,131,142,200));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(140,140,140,100);
										border-radius: 35px;
										""")
		widgetUsernameSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetUsername.setSizePolicy(widgetUsernameSizePolicy)
		usernameLayout = QHBoxLayout()
		widgetUsername.setLayout(usernameLayout)

		widgetPassword = QtWidgets.QWidget()
		widgetPassword.setStyleSheet("""
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(96,99,108,200), stop:1 rgba(133,131,142,200));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(140,140,140,100);
										border-radius: 35px;
										""")
		widgetPasswordSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical
		widgetPassword.setSizePolicy(widgetPasswordSizePolicy)
		passwordLayout = QHBoxLayout()
		widgetPassword.setLayout(passwordLayout)
	
		self.usernameLineEditLogin = QtWidgets.QLineEdit()
		usernameLineEditSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)#Horizontal,vertical
		self.usernameLineEditLogin.setSizePolicy(logoLabelSizePolicy)
		self.usernameLineEditLogin.setStyleSheet("""color: rgba(255,255,255,255);
													background:rgba(69, 83, 105,0);
													border-color: rgba(14,14,14,0);
													border-radius: 20px;
													font-size: 15px;""")
		self.usernameLineEditLogin.setPlaceholderText("Username") 

		self.passwordLineEditLogin=QtWidgets.QLineEdit()
		self.passwordLineEditLogin.setPlaceholderText("Password") 
		
		self.passwordLineEditLogin.setStyleSheet("""color: rgba(255,255,255,255);
													background:rgba(69, 83, 105,0);
													border-color: rgba(14,14,14,0);
													border-radius: 20px;
													font-size: 15px;""")
		self.passwordLineEditLogin.setEchoMode(2)

		usernameLogoLabel = QtWidgets.QLabel()
		usernameLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											border-radius: 23px;""")
		usernameLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical
		usernameLogoLabel.setSizePolicy(usernameLogoLabelSizePolicy)

		pixmap = QPixmap("48px.png")
		usernameLogoLabel.setPixmap(pixmap)
		usernameLogoLabel.setAlignment(Qt.AlignCenter)

		passwordLogoLabel = QtWidgets.QLabel()
		passwordLogoLabel.setStyleSheet("""background:rgba(156, 165, 179,255);
											border-color: rgba(14,14,14,0);
											border-radius: 23px;""")
		passwordLogoLabelSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		passwordLogoLabel.setSizePolicy(passwordLogoLabelSizePolicy)

		pixmap = QPixmap("lock2_48px.png")
		passwordLogoLabel.setPixmap(pixmap)
		passwordLogoLabel.setAlignment(Qt.AlignCenter)


		usernameLayout.addWidget(usernameLogoLabel)
		usernameLayout.addWidget(self.usernameLineEditLogin)
		passwordLayout.addWidget(passwordLogoLabel)
		passwordLayout.addWidget(self.passwordLineEditLogin)
		showPasswordCheck=QtWidgets.QCheckBox("Show Password")
		showPasswordCheck.setStyleSheet("""QCheckBox::indicator {
    										border: 3px solid #5A5A5A;
    										background: none;
											}
											
											""")

		loginButton = QtWidgets.QPushButton("Login")
		loginButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)#Horizontal,vertical		
		loginButton.setSizePolicy(loginButtonSizePolicy)
		loginButton.setStyleSheet("""	QPushButton{font-size: 25px;
										color: rgba(60,70,89,225);
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(188, 192, 204,200), stop:1 rgba(205,208,220,225));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(240,240,240,200);
										border-radius: 30px;
										min-height:65px;
										max-height:68px;}
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
		loginButton.clicked.connect(self.loginButtonFunction)

		forgotButton = QtWidgets.QPushButton("Forgot Password?")
		forgotButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		forgotButton.setSizePolicy(forgotButtonSizePolicy)
		forgotButton.setStyleSheet("""	QPushButton{font-size: 15px;
										color: rgba(60,70,89,225);
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(188, 192, 204,200), stop:1 rgba(205,208,220,225));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(240,240,240,200);
										border-radius: 16px;
										min-height:30px;
										max-height:35px;}
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
		forgotButton.clicked.connect(self.forgotPasswordClicked)


		registerButton = QtWidgets.QPushButton("Register")
		registerButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		registerButton.setSizePolicy(registerButtonSizePolicy)
		registerButton.setStyleSheet("""	QPushButton{font-size: 15px;
										color: rgba(60,70,89,225);
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(188, 192, 204,200), stop:1 rgba(205,208,220,225));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(240,240,240,200);
										border-radius: 16px;
										min-height:30px;
										max-height:35px;}
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
		registerButton.clicked.connect(self.goRegisterButtonFunction)

		quitButton = QtWidgets.QPushButton("Quit Program")
		quitButtonSizePolicy=QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum)#Horizontal,vertical		
		quitButton.setSizePolicy(quitButtonSizePolicy)
		quitButton.setStyleSheet("""	QPushButton{font-size: 15px;
										color: rgba(60,70,89,225);
										background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
										stop:0 rgba(188, 192, 204,200), stop:1 rgba(205,208,220,225));
										border-width: 1px;
										border-style: outset;
										border-color: rgba(240,240,240,200);
										border-radius: 16px;
										min-height:30px;
										max-height:35px;}
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
		quitButton.clicked.connect(self.quitButtonFunction)


		formBlockLayout.addWidget(widgetUsername,0,0,1,2)

		
		formBlockLayout.addWidget(widgetPassword,1,0,1,2)
		formBlockLayout.addWidget(showPasswordCheck,2,0,1,2,Qt.AlignRight)
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
		self.setWindowTitle("Login")

		self.showMaximized()

	def loginButtonFunction(self):


		print("login clicked")



	def goRegisterButtonFunction(self):

		print("register clicked")
	def forgotPasswordClicked(self):
		print("forgot clicked")

	def quitButtonFunction(self):

		print("quit clicked")


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
						QPushButton {
							font-size: 15px
						}
						QLabel{
							font-size: 12px
						}
						QCheckBox{
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

