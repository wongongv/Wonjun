import sys

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
# import six
import pdb
# import vert_slider
import glo_var
import lamb_pol
import slider
import rho
# import gc
import jbeta
import jalpha
import phase
import csv
import mawin
import pyqtgraph.widgets.RemoteGraphicsView
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
import pyqtgraph.widgets.RemoteGraphicsView
from PyQt4.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap
from pyqtgraph.dockarea import *

class MyViewBox(pg.ViewBox):
	def __init__(self, parent=None):
		"""
		Constructor of the CustomViewBox
		"""
		super(MyViewBox, self).__init__(parent)



class MyPW(pg.PlotWidget):
	handleBottomRight = 1

	handleSize = +8.0
	handleSpace = -4.0

	handleCursors = {
		handleBottomRight: QtCore.Qt.SizeFDiagCursor,
	}

	def __init__(self):
		"""
		Initialize the shape.
		"""
		super().__init__()
		self.handles = {}
		self.handleSelected = None
		self.__mousePressPos = None
		self.__mousePressRect = None
		self.installEventFilter(self)
		# self.setAcceptHoverEvents(True)
		# self.setFlag(QGraphicsItem.ItemIsMovable, True)
		# self.setFlag(QGraphicsItem.ItemIsSelectable, True)
		# self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
		# self.setFlag(QGraphicsItem.ItemIsFocusable, True)

		self.updateHandlesPos()

	def handleAt(self, point):
		for k, v, in self.handles.items():
			if v.contains(point):
				return k
		return None

	def mousePressEvent(self, event):
		self.__mousePressPos = None
		self.__mouseMovePos = None
		if event.button() == QtCore.Qt.LeftButton:
		# if event.button() == self.mouseDoubleClickEvent:
			self.handleSelected = self.handleAt(event.pos())
			if self.handleSelected :
				self.__mousePressPos = mouseEvent.pos()
				self.mousePressRect = self.boundingRect()
			else :
				self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
				self.__mousePressPos = event.globalPos()
				self.__mouseMovePos = event.globalPos()

		# super(MyPW, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
		# if event.button() == self.mouseDoubleClickEvent:
			# adjust offset from clicked point to origin of widget

			if self.handleSelected:
				self.interactiveResize(event.pos())
			else:
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
			
			self.handleSelected = None
			self.mousePressPos = None
			self.mousePressRect = None
			self.update()

			if moved.manhattanLength() > 3:
				event.ignore()
				return
		# super(MyPW, self).mouseReleaseEvent(event)



	# def paintEvent(self, event):
	# 	option = QtGui.QStyleOptionButton()
	# 	option.initFrom(self.viewport())
	# 	painter = QtGui.QPainter(self.viewport())
	# 	if option.state & QtGui.QStyle.State_MouseOver:
	# 		print(3)
	# 	else:
	# 		pass
	# def eventFilter(self, object, event):
	# 	if event.type() == QtCore.QEvent.HoverMove:
	# 		painter = QtGui.QPainter(self.viewport())
	# 		painter.begin(self.viewport())
	# 		painter.drawRect(QtCore.QRect(0, 0, 100, 48))
	# 		painter.end()
	# 		return True
	# 	return False


	# def hoverMoveEvent(self, event):

	# 	if self.isSelected():
	# 		handle = self.handleAt(event.pos())
	# 		cursor = QtCore.Qt.ArrowCursor if handle is None else self.handleCursors[handle]
	# 		self.setCursor(cursor)
	# 	super().hoverMoveEvent(event)

	# def hoverLeaveEvent(self, event):
	# 	self.setCursor(QtCore.Qt.ArrowCursor)
	# 	super().hoverLeaveEvent(event)

	# def paint(self,  widget=None):
	# 	"""
	# 	Paint the node in the graphic view.
	# 	"""
	# 	Qpainter.setBrush(QBrush(QColor(255, 0, 0, 100)))
	# 	Qpainter.setPen(QPen(QColor(0, 0, 0), 1.0, QtCore.Qt.SolidLine))
	# 	Qpainter.drawRect(self.rect())

	# 	Qpainter.setRenderHint(QPainter.Antialiasing)
	# 	Qpainter.setBrush(QBrush(QColor(255, 0, 0, 255)))
	# 	Qpainter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
	# 	for handle, rect in self.handles.items():
	# 		if self.handleSelected is None or handle == self.handleSelected:
	# 			Qpainter.drawEllipse(rect)



	def boundingRect(self):
		"""
		Returns the bounding rect of the shape (including the resize handles).
		"""
		o = self.handleSize + self.handleSpace
		return self.rect().adjusted(-o, -o, o, o)
	
	def interactiveResize(self, mousePos):
		offset = self.handleSize + self.handleSpace
		boundingRect = self.boundingRect()
		rect = self.rect()
		diff = QPointF(0, 0)


		if self.handleSelected == self.handleBottomRight:

			fromX = self.mousePressRect.right()
			fromY = self.mousePressRect.bottom()
			toX = fromX + mousePos.x() - self.mousePressPos.x()
			toY = fromY + mousePos.y() - self.mousePressPos.y()
			diff.setX(toX - fromX)
			diff.setY(toY - fromY)
			boundingRect.setRight(toX)
			boundingRect.setBottom(toY)
			rect.setRight(boundingRect.right() - offset)
			rect.setBottom(boundingRect.bottom() - offset)
			self.setRect(rect)
		self.updateHandlesPos()

	def updateHandlesPos(self):
		s = self.handleSize
		b = self.boundingRect()
		self.handles[self.handleBottomRight] = QtCore.QRectF(b.right() - s, b.bottom() - s, s, s)



# import sys

# from PyQt4.QtCore import Qt, QRectF, QPointF
# from PyQt4.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap
# from PyQt4.QtGui import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem


# class GraphicsRectItem(QGraphicsRectItem):

# 	handleBottomRight = 8

# 	handleSize = +8.0
# 	handleSpace = -4.0

# 	handleCursors = {
# 		handleBottomRight: QtCore.Qt.SizeFDiagCursor,
# 	}

# 	def __init__(self, *args):
# 		"""
# 		Initialize the shape.
# 		"""
# 		super().__init__(*args)
# 		self.handles = {}
# 		self.handleSelected = None
# 		self.mousePressPos = None
# 		self.mousePressRect = None
# 		self.setAcceptHoverEvents(True)
# 		self.setFlag(QGraphicsItem.ItemIsMovable, True)
# 		self.setFlag(QGraphicsItem.ItemIsSelectable, True)
# 		self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
# 		self.setFlag(QGraphicsItem.ItemIsFocusable, True)
# 		self.updateHandlesPos()

# 	def handleAt(self, point):
# 		"""
# 		Returns the resize handle below the given point.
# 		"""
# 		for k, v, in self.handles.items():
# 			if v.contains(point):
# 				return k
# 		return None

# 	def hoverMoveEvent(self, moveEvent):
# 		"""
# 		Executed when the mouse moves over the shape (NOT PRESSED).
# 		"""
# 		if self.isSelected():
# 			handle = self.handleAt(moveEvent.pos())
# 			cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
# 			self.setCursor(cursor)
# 		super().hoverMoveEvent(moveEvent)

# 	def hoverLeaveEvent(self, moveEvent):
# 		"""
# 		Executed when the mouse leaves the shape (NOT PRESSED).
# 		"""
# 		self.setCursor(Qt.ArrowCursor)
# 		super().hoverLeaveEvent(moveEvent)

# 	def mousePressEvent(self, mouseEvent):
# 		"""
# 		Executed when the mouse is pressed on the item.
# 		"""
# 		self.handleSelected = self.handleAt(mouseEvent.pos())
# 		if self.handleSelected:
# 			self.mousePressPos = mouseEvent.pos()
# 			self.mousePressRect = self.boundingRect()
# 		super().mousePressEvent(mouseEvent)

# 	def mouseMoveEvent(self, mouseEvent):
# 		"""
# 		Executed when the mouse is being moved over the item while being pressed.
# 		"""
# 		if self.handleSelected is not None:
# 			self.interactiveResize(mouseEvent.pos())
# 		else:
# 			super().mouseMoveEvent(mouseEvent)

# 	def mouseReleaseEvent(self, mouseEvent):
# 		"""
# 		Executed when the mouse is released from the item.
# 		"""
# 		super().mouseReleaseEvent(mouseEvent)
# 		self.handleSelected = None
# 		self.mousePressPos = None
# 		self.mousePressRect = None
# 		self.update()

# 	def boundingRect(self):
# 		"""
# 		Returns the bounding rect of the shape (including the resize handles).
# 		"""
# 		o = self.handleSize + self.handleSpace
# 		return self.rect().adjusted(-o, -o, o, o)

# 	def updateHandlesPos(self):
# 		"""
# 		Update current resize handles according to the shape size and position.
# 		"""
# 		s = self.handleSize
# 		b = self.boundingRect()
# 		self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

# 	def interactiveResize(self, mousePos):
# 		"""
# 		Perform shape interactive resize.
# 		"""
# 		offset = self.handleSize + self.handleSpace
# 		boundingRect = self.boundingRect()
# 		rect = self.rect()
# 		diff = QPointF(0, 0)


# 		elif self.handleSelected == self.handleBottomRight:

# 			fromX = self.mousePressRect.right()
# 			fromY = self.mousePressRect.bottom()
# 			toX = fromX + mousePos.x() - self.mousePressPos.x()
# 			toY = fromY + mousePos.y() - self.mousePressPos.y()
# 			diff.setX(toX - fromX)
# 			diff.setY(toY - fromY)
# 			boundingRect.setRight(toX)
# 			boundingRect.setBottom(toY)
# 			rect.setRight(boundingRect.right() - offset)
# 			rect.setBottom(boundingRect.bottom() - offset)
# 			self.setRect(rect)

# 		self.updateHandlesPos()

# 	def shape(self):
# 		"""
# 		Returns the shape of this item as a QPainterPath in local coordinates.
# 		"""
# 		path = QPainterPath()
# 		path.addRect(self.rect())
# 		if self.isSelected():
# 			for shape in self.handles.values():
# 				path.addEllipse(shape)
# 		return path

# 	def paint(self, painter, option, widget=None):
# 		"""
# 		Paint the node in the graphic view.
# 		"""
# 		painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
# 		painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
# 		painter.drawRect(self.rect())

# 		painter.setRenderHint(QPainter.Antialiasing)
# 		painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
# 		painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
# 		for handle, rect in self.handles.items():
# 			if self.handleSelected is None or handle == self.handleSelected:
# 				painter.drawEllipse(rect)


class MainWindow(QtGui.QMainWindow):


	def __init__(self,parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.area = DockArea()

		pg.setConfigOption('background', QtGui.QColor(215,214,213,255))
		pg.setConfigOption('foreground', 'k')
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtGui.QColor(215,214,213,255))
		self.setPalette(palette)
		# # self.mainwidget = MainWidget(self)
		self.d3 = Dock("3", size=(500,400))
		self.area.addDock(self.d3, 'bottom')
		self.d2=Dock("1",size=(500,400))
		self.area.addDock(self.d2,'top')
		self.d4=Dock("2")
		self.area.addDock(self.d4,'right')
		self.d5=Dock("2")
		self.area.addDock(self.d5,'right')
		
		self.test1 = pg.PlotWidget()
		self.i=self.test1.plot([1],[2])
		self.t1view = self.test1.getPlotItem().getViewBox()
		self.t1view.setBackgroundColor('w')
		self.test2 = pg.PlotWidget()
		self.f=self.test2.plot([1],[2])
			
		self.test3 = pg.PlotWidget()
		self.g=self.test3.plot([1],[2])

		self.test4 = pg.PlotWidget()
		self.a=self.test4.plot([1],[2])
		self.test5 = pg.PlotWidget()
		self.a=self.test5.plot([1],[2])

		# self.widget =  QtGui.QWidget()
		# self.layout = QtGui.QGridLayout(self.widget)
		self.d2.addWidget(self.test3)
		self.d3.addWidget(self.test1)
		self.d2.addWidget(self.test2)
		self.d4.addWidget(self.test4)
		self.d5.addWidget(self.test5)
		self.setCentralWidget(self.area)

		self.show()



	# def __init__(self,parent=None):




	# 	QtGui.QMainWindow.__init__(self, parent)


	# 	pg.setConfigOption('background', QtGui.QColor(215,214,213,255))
	# 	pg.setConfigOption('foreground', 'k')
	# 	palette = QtGui.QPalette()
	# 	palette.setColor(QtGui.QPalette.Background, QtGui.QColor(215,214,213,255))
	# 	self.setPalette(palette)

	# 	self.widget =  QtGui.QWidget()
	# 	self.layout = QtGui.QGridLayout(self.widget)
		

	# 	self.test1 = MyPW()
	# 	self.t1widget = self.test1.getViewWidget()



	# 	self.i=self.test1.plot([1],[2])
	# 	self.t1view = self.test1.getPlotItem().getViewBox()
	# 	self.t1view.setBackgroundColor('w')

	# 	self.test2 = pg.PlotWidget()
	# 	self.f=self.test2.plot([1],[2])
	# 	self.t2view = self.test2.getPlotItem().getViewBox()
	# 	self.t2view.setBackgroundColor('w')


	# 	self.layout.addWidget(self.test1,0,0)
	# 	self.layout.addWidget(self.test2,1,1)
	# 	self.setCentralWidget(self.widget)

	# 	self.show()
	# 	# self.p = self.view.addPlot()
	# 	# self.p.addItem(self.i)
	# 	# self.pview = self.p.getViewBox()
	# 	# self.pview.setBackgroundColor('w')

	# 	# self.item2 = self.view.getItem(0,0)


	# 	# self.p1 = self.view.addPlot()
	# 	# self.p1.addItem(self.f)
	# 	# self.item3= self.view.getItem(0,1)
	# 	# self.p1view = self.p1.getViewBox()
	# 	# self.p1view.setBackgroundColor('w')

	# 	# self.item2.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
	# 	# self.item2.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

	# 	# self.item3.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
	# 	# self.item3.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)


	# 	# self.widget =  QtGui.QWidget()
	# 	# self.layout = QtGui.QGridLayout(self.widget)
	# 	# self.layout.addWidget(self.test1, 0,0)
	# 	# self.layout.addWidget(self.test2, 1,1)
	# 	# self.layout.addWidget(self.view,1,0)
	# 	# self.layout.addWidget(QtGui.QSizeGrip(self.test1),1,0)
	# 	# pdb.set_trace()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())












# just to store



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

# -----------------------------------------------------------------------------------

# 		QtGui.QMainWindow.__init__(self, parent)

# 		# self.mainwidget = MainWidget(self)
# 		self.test1 = pg.PlotWidget()
# 		self.i=self.test1.plot([1],[2])

# 		self.test2 = pg.PlotWidget()
# 		self.f=self.test2.plot([1],[2])
		

# 		# self.item = self.test2.getPlotItem()
# 		# self.item.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
# 		# self.item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)


# 		# self.win = win
# 		# self.p1 = self.win.addPlot(title = '\u03bb')
# 		# self.viewbox=self.p1.getViewBox()
# 		# self.viewbox.setLimits(xMin = -0.02, yMin = -0.02, xMax = 1.02, yMax = 1.02)
# 		# self.viewbox.setRange(xRange=[-0.02,1.02],yRange=[-0.02,1.02],padding =0)
# 		# self.sp = myscat(size = 10, pen = pg.mkPen(None), brush=pg.mkBrush(100,200,200), symbolPen='w')
# 		# self.lastClicked=[]


# 		self.view = GraphicsLayoutWidget()
# 		self.p = self.view.addPlot()
# 		self.p.addItem(self.i)
# 		self.pview = self.p.getViewBox()
# 		self.pview.setBackgroundColor('w')

# 		self.item2 = self.view.getItem(0,0)


# 		self.p1 = self.view.addPlot()
# 		self.p1.addItem(self.f)
# 		self.item3= self.view.getItem(0,1)
# 		self.p1view = self.p1.getViewBox()
# 		self.p1view.setBackgroundColor('w')

# 		self.item2.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
# 		self.item2.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

# 		self.item3.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
# 		self.item3.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)


# 		# self.widget =  QtGui.QWidget()
# 		# self.layout = QtGui.QGridLayout(self.widget)
# 		# self.layout.addWidget(self.test1, 0,0)
# 		# self.layout.addWidget(self.test2, 1,1)
# 		# self.layout.addWidget(self.view,1,0)
# 		# self.layout.addWidget(QtGui.QSizeGrip(self.test1),1,0)
# 		# pdb.set_trace()
# 		self.setCentralWidget(self.view)

# 		self.show()
# 	# def setup(self):
# 	# 	self.frame = QtGui.QFrame()
# 	# 	self.layout = QtGui.QGridLayout() 
# 	# 	self.frame.setLayout(self.layout)
# 	# 	# self.frame.setLineWidth(0)
# 	# 	# self.frame.setFrameStyle(QtGui.QFrame.Panel)
# 	# 	# self.layout.setContentsMargins(0,0,5,0)
# 	# 	self.test1 = pg.PlotWidget()
# 	# 	self.test1.plot([1],[2])
# 	# 	self.test2 = pg.PlotWidget()
# 	# 	self.layout.addWidget(self.test1,0,0)
# 	# 	# self.layout.addWidget(self.test2,0,1)


# 	# 	self.frame2 = QtGui.QFrame()
# 	# 	self.layout2 = QtGui.QGridLayout() 
# 	# 	self.frame2.setLayout(self.layout2)

# 	# 	self.layout2.addWidget(self.test1,1,0)
# 	# 	# self.layout2.addWidget(self.test1,1,1)

# 	# 	self.mainframe = QtGui.QFrame()
# 	# 	self.layout3 = QtGui.QGridLayout() 
# 	# 	self.mainframe.setLayout(self.layout3)
# 	# 	self.layout3.addWidget(self.frame)
# 	# 	self.layout3.addWidget(self.frame2)

# 	# 	self.setCentralWidget(self.mainframe)
# 	# 	pdb.set_trace()

# 		# self.win = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()

# # 



# 		# pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process! 

# 		# self.win.setWindowIcon(QtGui.QIcon('berkeleylogo1.png'))
# 		# self.win = pg.GraphicsWindow(title = "TASEP")
# 		# self.win.resize(1200,720)
# 		# self.win.setWindowTitle('TASEP')

# 		# self.realinit()



# 		# self.viewmain = pg.GraphicsWindow()
# 		# self.viewmain = GraphicsLayoutWidget()
# 		# self.viewmain.addItem(main_class())
# 		# pg.setConfigOption('background', 'b')
# 		# pg.setConfigOption('foreground', 'k')

# 		# self.setCentralWidget(self.test1)
