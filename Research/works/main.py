import sys

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
import lamb_pol
import slider
import rho
import jbeta
import jalpha
import phase
import csv
import pyqtgraph.widgets.RemoteGraphicsView
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
import pyqtgraph.widgets.RemoteGraphicsView
from pyqtgraph.dockarea import *


# for free movement
	# def __init__(self,parent=None):
	
	# 	QtGui.QMainWindow.__init__(self, parent)
	# 	self.setGeometry(200,100,500,500)
	# 	self.resize(QtGui.QDesktopWidget().availableGeometry(self).size() * 1)
		
	# 	pg.setConfigOption('background', QtGui.QColor(215,214,213,255))
	# 	pg.setConfigOption('foreground', 'k')
	# 	palette = QtGui.QPalette()
	# 	palette.setColor(QtGui.QPalette.Background, QtGui.QColor(215,214,213,255))
	# 	self.setPalette(palette)

	# 	self.widget =  QtGui.QWidget()
	# 	self.layout = QtGui.QGridLayout(self.widget)


	# 	# self.test1 = MyPW()
	# 	# self.i=self.test1.plot([1],[2])
	# 	# self.t1view = self.test1.getPlotItem().getViewBox()
	# 	# self.t1view.setBackgroundColor('w')

	# 	# self.t1widget = self.test1.getViewWidget()


	# 	# self.test2 = pg.PlotWidget()
	# 	# self.f=self.test2.plot([1],[2])
	# 	# self.t2view = self.test2.getPlotItem().getViewBox()
	# 	# self.t2view.setBackgroundColor('w')



	# 	self.setCentralWidget(self.widget)
	# 	# self.layout.addWidget(self.test1,0,0)
	# 	# self.layout.addWidget(self.test2,1,1)

	# 	self.loadaction = QtGui.QAction("&Open",self)
	# 	self.loadaction.setShortcut("Ctrl+O")
	# 	self.loadaction.setStatusTip("Open File")
	# 	self.loadaction.triggered.connect(self.loaddata)


	# 	self.mainMenu = self.menuBar()
	# 	self.fileMenu = self.mainMenu.addMenu("&File")
	# 	self.fileMenu.addAction(self.loadaction)

	# 	self.layout.setColumnStretch(0,5)

	# 	self.layout.setColumnStretch(1,2)

	# 	self.layout.setColumnStretch(2,2)


# fig = plt.figure()
# fig.set_size_inches(18.5, 10.5, forward=True)


# # vert_slider
# vs = vert_slider.make_vs(fig)

# # lambda polynomial
# lambda_poly = lamb_pol.lamb_pol(fig)

# vs.receive(lambda_poly)


# # rho

# rhos = rho.rho(fig)
# # slider
# slider = slide.make_slide(fig, vs.vslides[glo_var.lambdas_degree],vs.vslides[glo_var.lambdas_degree + 1], rhos)



# dependencies
# l -> j
# alpha -> j
# beta -> j
# alphastar ->
# betastar ->
# lambda -> a,b_stars, 

# buttons



# class MainWindow(QtGui.QMainWindow): 

#     def __init__(self, parent=None): 

#         super(MainWindow, self).__init__(parent)

#         self.win_widget = WinWidget(self)
#         widget = QtGui.QWidget()
#         layout = QtGui.QVBoxLayout(widget)
#         layout.addWidget(self.win_widget)

#         self.setCentralWidget(widget)
#         self.statusBar().showMessage('Ready')
#         self.toolbar = self.addToolBar('Exit')

#         exitAction = QtGui.QAction ('Exit', self)
#         exitAction.setShortcut('Ctrl+Q')
#         exitAction.triggered.connect(QtGui.qApp.quit)

#         self.toolbar = self.addToolBar('Exit')
#         self.toolbar.addAction(exitAction)

#         menubar = self.menuBar() 
#         fileMenu = menubar.addMenu('&File')

#         self.setGeometry(300, 300, 450, 250)
#         self.setWindowTitle('Test')  
#         self.setWindowIcon (QtGui.QIcon('logo.png'))
#         self.show()

# class WinWidget (QtGui.QWidget) : 

#     def __init__(self, parent): 
#         super (WinWidget , self).__init__(parent)
#         self.controls()
#         #self.__layout()

#     def controls(self):

#         self.qbtn = QtGui.QPushButton('Quit', self)
#         self.qbtn.setFixedSize (100,25)
#         self.qbtn.setToolTip ("quit")
#         self.qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
#         self.qbtn.move(50, 50)  






#         QWidget.__init__(self, parent)
#         self.scene = QGraphicsScene()
#         self.view = QGraphicsView(self.scene)
#         self.button = QPushButton("Do test")

#         layout = QVBoxLayout()
#         layout.addWidget(self.button)
#         layout.addWidget(self.view)
#         self.setLayout(layout)



class MyPW(pg.PlotWidget):
		
	def mousePressEvent(self, event):
		self.__mousePressPos = None
		self.__mouseMovePos = None
		if event.button() == QtCore.Qt.LeftButton:
			self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
			self.__mousePressPos = event.globalPos()
			self.__mouseMovePos = event.globalPos()

		# super(MyPW, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			# adjust offset from clicked point to origin of widget

			self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
			currPos = self.mapToGlobal(self.pos())
			globalPos = event.globalPos()
			diff = globalPos - self.__mouseMovePos
			newPos = self.mapFromGlobal(currPos + diff)
			self.move(newPos)

			self.__mouseMovePos = globalPos

		# super(MyPW, self).mouseMoveEvent(event)

	def mouseReleaseEvent(self, event):
		if self.__mousePressPos is not None:
			moved = event.globalPos() - self.__mousePressPos 
			if moved.manhattanLength() > 3:
				event.ignore()
				return

		# super(MyPW, self).mouseReleaseEvent(event)
class MyTabWidget(QtGui.QWidget):         
	def __init__(self, parent):   
		super(QtGui.QWidget, self).__init__(parent)
		self.layout = QtGui.QVBoxLayout(self)
 
		# Initialize tab screen
		self.tabs = QtGui.QTabWidget()
		self.tab1 = QtGui.QWidget()
		# self.tabs.resize(300,200) 
 
		# Add tabs
		self.tabs.addTab(self.tab1,"Tab 1")
		# self.tabs.addTab(self.tab2,"Tab 2")
 


class MainWindow(QtGui.QMainWindow):
# for dock
	def __init__(self,parent=None):
	

		QtGui.QMainWindow.__init__(self, parent)
	
		# self.setWindowIcon (QtGui.QIcon('sicon.jpg'))
		self.setWindowTitle('TASEP')  

		self.setGeometry(200,100,500,500)
		self.resize(QtGui.QDesktopWidget().availableGeometry(self).size() * 1)
		pg.setConfigOption('background', QtGui.QColor(215,214,213,255))
		pg.setConfigOption('foreground', 'k')
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtGui.QColor(215,214,213,255))
		self.setPalette(palette)

		self.mytab = MyTabWidget(self)
		self.maintab = self.mytab.tabs

		self.mytab.tab1.layout = QtGui.QVBoxLayout(self.mytab)
		self.mytab.tab1.setLayout(self.mytab.tab1.layout)
		# Add tabs to widget        
		self.mytab.layout.addWidget(self.maintab)
		self.mytab.setLayout(self.mytab.layout)


		self.mainframe = QtGui.QFrame()





		# self.test1 = MyPW()
		# self.i=self.test1.plot([1],[2])
		# self.t1view = self.test1.getPlotItem().getViewBox()
		# self.t1view.setBackgroundColor('w')

		# self.t1widget = self.test1.getViewWidget()


		# self.test2 = pg.PlotWidget()
		# self.f=self.test2.plot([1],[2])
		# self.t2view = self.test2.getPlotItem().getViewBox()
		# self.t2view.setBackgroundColor('w')



		# self.layout.addWidget(self.test1,0,0)
		# self.layout.addWidget(self.test2,1,1)

		self.loadaction = QtGui.QAction("&Open",self)
		self.loadaction.setShortcut("Ctrl+O")
		self.loadaction.setStatusTip("Open File")
		self.loadaction.triggered.connect(self.loaddata)


		self.exportaction = QtGui.QAction("&Export",self)
		self.exportaction.setShortcut("Ctrl+E")
		self.exportaction.setStatusTip("Export to latx")
		self.exportaction.triggered.connect(self.exportdata)


		self.mainMenu = self.menuBar()
		self.fileMenu = self.mainMenu.addMenu("&File")
		self.fileMenu.addAction(self.loadaction)
		self.fileMenu.addAction(self.exportaction)


		self.maketoolbar()



		self.area = DockArea()
		
		self.drho = Dock("\u03c1")
		self.dlamb=Dock("\u03bb")
		self.dalpha=Dock("\u03b1")
		self.dbeta=Dock("\u03b2")
		self.dphase=Dock("Phase")
		self.dcontrols=Dock("Controls")


		self.layout = QtGui.QHBoxLayout()
		self.layout.addWidget(self.area)
		self.mainframe.setLayout(self.layout)
		self.mainframe.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
		self.mainframe.setLineWidth(8)

		# for fast revision. Delete it after revision!
		# self.read_file("C:/GUI/data/input1.csv")
		# self.realinit()
	def exportdata(self):
		

		pass


	# def setExportMethods(self, methods):
	#     self.exportMethods = methods
	#     self.export.clear()
	#     for opt, fn in methods.items():
	#         self.export.addAction(opt, self.exportMethod)
		
	# def exportMethod(self):
	#     act = QtGui.QMenu.sender()
	#     self.exportMethods[str(act.text())]()

	def maketoolbar(self):
		self.state = None
		self.titlebarstate = 1
		self.toolbar = self.addToolBar("Toolbar")

		fix = QtGui.QAction(QtGui.QIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_ArrowDown)),'Fix current position',self)
		fix.triggered.connect(self.fixdock)
		self.toolbar.addAction(fix)
		
		save = QtGui.QAction(QtGui.QIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_FileDialogListView)),'Save current position',self)
		save.triggered.connect(self.savedock)
		self.toolbar.addAction(save)

		restore = QtGui.QAction(QtGui.QIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_BrowserReload)),'restore saved position',self)
		restore.triggered.connect(self.restoredock)
		self.toolbar.addAction(restore)

	def fixdock(self):
		if self.titlebarstate == 1:
			self.dlamb.hideTitleBar()
			self.drho.hideTitleBar()
			self.dalpha.hideTitleBar()	
			self.dbeta.hideTitleBar()
			self.dcontrols.hideTitleBar()
			self.dphase.hideTitleBar()
			self.titlebarstate = 0
		else:
			self.dlamb.showTitleBar()
			self.drho.showTitleBar()
			self.dalpha.showTitleBar()	
			self.dbeta.showTitleBar()
			self.dcontrols.showTitleBar()
			self.dphase.showTitleBar()
			self.titlebarstate = 1

	def savedock(self):
		self.state = self.area.saveState()


	def restoredock(self):
		if self.state != None:
			self.area.restoreState(self.state)

	def realinit(self):
		
		self.area = DockArea()
		
		self.drho = Dock("\u03c1")
		self.dlamb=Dock("\u03bb")
		self.dalpha=Dock("\u03b1")
		self.dbeta=Dock("\u03b2")
		self.dphase=Dock("Phase")
		self.dcontrols=Dock("Controls")


		self.layout = QtGui.QHBoxLayout()
		self.layout.addWidget(self.area)
		self.mainframe.setLayout(self.layout)
		self.mainframe.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
		self.mainframe.setLineWidth(8)


		pg.setConfigOptions(antialias=True)

		self.lamb_po = lamb_pol.lamb_pol(self.dlamb)
		self.rh=rho.rho(self.drho)
		self.phas=phase.phase(self.dphase)
		self.jalph = jalpha.jalpha(self.dalpha, self.rh)
		self.jbet = jbeta.jbeta(self.dbeta, self.rh)
		self.slid=slider.Widget(self.dcontrols, self.lamb_po,self.phas, self.rh, self.jbet,self.jalph)
		self.lamb_po.receive(self.slid)


		self.area.addDock(self.drho, 'left')
		self.area.addDock(self.dlamb,'bottom', self.drho)
		self.area.addDock(self.dalpha,'right')
		self.area.addDock(self.dbeta,'right', self.dalpha)
		self.area.addDock(self.dphase,'bottom', self.dalpha)
		self.area.addDock(self.dcontrols,'bottom', self.dbeta)

		self.setCentralWidget(self.area)

	def checkboxes(self):
		self.alphacheck()

	def alphacheck(self):
		self.alphline = QtGui.QCheckBox('\u03B1 line')
		self.alproxy=QtGui.QGraphicsProxyWidget()
		self.alproxy.setWidget(self.alphline)
		self.win.addItem(self.alphline)
		self.alphline.stateChanged.connect(self.alphstate)


	def opengraphs(self):
		self.mn = main.main_class(app)
		self.window.hide()

	def loaddata(self):
		name = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '\home','text (*.txt *.csv)')
		if name == "" :
			pass
		else:
			self.read_file(name)
			self.realinit()

	def read_file(self, input):
		global ison	
		if ison == 0:
			ison = 1
		else:
			self.setCentralWidget(None)
			glo_var.initialize()


		if input[-3:] == 'csv':
			with open(input, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				lis = []
				for j in spamreader:
					lis += j
				glo_var.lambdas_degree = int(len(lis)/2)
				for i in range(glo_var.lambdas_degree):
					glo_var.lambdas += [[eval(lis[i])/100, eval(lis[i + glo_var.lambdas_degree])]]
			glo_var.alpha = 0.1
			glo_var.beta = 0.1
			glo_var.l = 1

		elif input[-3:] == 'txt':
			f = open(input,'r')
			N = int(f.readline().strip())	
			while(N>3):
				T = f.readline().strip()
				glo_var.lambdas +=[[eval(T)[0],eval(T)[1]]]
				glo_var.lambdas_degree+=1
				N-=1
			glo_var.alpha = float(f.readline().strip())
			glo_var.beta = float(f.readline().strip())
			glo_var.l = int(f.readline().strip())
		else:
			err = QtGui.QMessageBox(self.win)
			err.setIcon(QMessageBox().Warning)
			err.setText("Please select txt or csv file Format")
			err.setWindowTitle("File Format Error")
			err.setStandardButtons(QMessageBox.Ok)
			err.buttonClicked.connect()



	def alphstate(self):
		self.alph.alphacheck * (-1)
		self.alph.update()
	def betacheck(self):
		return
	def rhocheck(self):
		return
	def phasecheck(self):
		return





# # #  To Do  : cursor move -> alpha beta switch update. Think about it. 
# if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#     QtGui.QApplication.instance().exec_()
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	ison = 0
	# window = MainWindow()
	# window.show()
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())