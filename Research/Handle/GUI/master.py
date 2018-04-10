# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import main
import sys
import glo_var
import pdb
import csv

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def opengraphs(self):
		self.mn = main.main_class(app)
		self.window.hide()

	def loaddata(self):
		name = QtGui.QFileDialog.getOpenFileName(self.window, 'Open File', '\home','text (*.txt *.csv)')
		self.read_file(name)
		self.mn = main.main_class(app) 	
		self.window.hide()


	def read_file(self, input):
	
		if input[-3:] == 'csv':
			with open(input, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				lis = []
				for j in spamreader:
					lis += j
				glo_var.lambdas_degree = int(len(lis)/2)
				for i in range(glo_var.lambdas_degree):
					glo_var.lambdas[i] = [eval(lis[i])/100, eval(lis[i + glo_var.lambdas_degree])]
			glo_var.alpha = 0.1
			glo_var.beta = 0.1
			glo_var.l = 1

		elif input[-3:] == 'txt':
			f = open(input,'r')
			N = int(f.readline().strip())	
			while(N>3):
				T = f.readline().strip()
				glo_var.lambdas[glo_var.lambdas_degree]=[eval(T)[0],eval(T)[1]]
				glo_var.lambdas_degree+=1
				N-=1
			glo_var.alpha = float(f.readline().strip())
			glo_var.beta = float(f.readline().strip())
			glo_var.l = int(f.readline().strip())
		else:
			err = QtGui.QMessageBox(self.window)
			err.setIcon(QMessageBox().Warning)
			err.setText("Please select txt or csv file Format")
			err.setWindowTitle("File Format Error")
			err.setStandardButtons(QMessageBox.Ok)
			err.buttonClicked.connect()


	def setupUi(self, MainWindow):
		self.window = MainWindow
		MainWindow.setObjectName(_fromUtf8("TASEP"))
		MainWindow.resize(800, 600)
		MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.FrontImage = QtGui.QLabel(self.centralwidget)
		self.FrontImage.setGeometry(QtCore.QRect(290, 70, 225, 225))
		self.FrontImage.setObjectName(_fromUtf8("FrontImage"))
		self.New = QtGui.QPushButton(self.centralwidget)
		self.New.setGeometry(QtCore.QRect(290, 320, 231, 31))
		self.New.setObjectName(_fromUtf8("New"))
		self.New.clicked.connect(self.opengraphs)

		self.Load = QtGui.QPushButton(self.centralwidget)
		self.Load.setGeometry(QtCore.QRect(290, 370, 231, 31))
		self.Load.setObjectName(_fromUtf8("Load"))
		self.Load.clicked.connect(self.loaddata)


		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.toolBar = QtGui.QToolBar(MainWindow)
		self.toolBar.setObjectName(_fromUtf8("toolBar"))
		MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.FrontImage.setPixmap(QtGui.QPixmap("berkeleylogo1.png"))
		# self.FrontImage.setText(_translate("MainWindow", "Hi", None))
		self.New.setText(_translate("MainWindow", "New", None))
		self.Load.setText(_translate("MainWindow", "Load", None))
		self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))



app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())

