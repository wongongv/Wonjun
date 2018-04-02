import sys
from PyQt4 import QtGui, QtCore
import pdb
# app = QtGui.QApplication(sys.argv)

# window = QtGui.QWidget()
# window.setGeometry(0,0,100,100)
# window.setWindowTitle("Hi")

# window.show()

# 1


class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50,50,1000,200)
		self.setWindowTitle("hi")
		self.setWindowIcon(QtGui.QIcon('berkeleylogo.png'))

		ex = QtGui.QAction("&wanna click?",self)
		ex.setShortcut("Ctrl+q")
		ex.setStatusTip('well??')
		ex.triggered.connect(self.close_win)


		self.statusBar()

		mainMenu = self.menuBar()
		file = mainMenu.addMenu('&haha')
		file.addAction(ex)

		self.home()

	def home(self):
		btn = QtGui.QPushButton("click", self)
		btn.clicked.connect(self.close_win)
		btn.resize(btn.sizeHint())
		btn.move(30,30)
		self.show()

	def close_win(self):
		print("www")
		sys.exit()

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())
run()
